#!/usr/bin/env python
# coding: utf-8

# ## SQLAlchemy

# ### Models

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.functions import database_exists, create_database

connectionstring = 'postgresql+psycopg2://postgres:example@postgres/ProjectDatabase'
if not database_exists(connectionstring):  #=> False
    try:
        create_database(connectionstring)
        doCreateAll = True
        print('Database created')
    except Exception as e:
        print('Database does not exists and cannot be created')
        raise
else:
    print('Database already exists')
    
    
BaseModel = declarative_base()
unitedSequence = Sequence('all_id_seq')

#Zkouska_Zkousejici
Examiner_Exam = Table('examiner_groups', BaseModel.metadata,
                      Column('exam_id', ForeignKey('exam.id'), primary_key=True),
                      Column('examiner_id', ForeignKey('user.id'), primary_key=True)
                      )
#Zkouska_Student
Student_Exam = Table('student_groups', BaseModel.metadata,
                     Column('exam_id', ForeignKey('exam.id'), primary_key=True),
                     Column('student_id', ForeignKey('user.id'), primary_key=True)
                     )

#Studijni_skupina_Predmet
StudyGroup_Subject = Table('subject_study_groups', BaseModel.metadata,
                           Column('subject_id', ForeignKey('subject.id'), primary_key=True),
                           Column('study_group_id', ForeignKey('study_group.id'), primary_key=True)
                           )

#Zkouska
class ExamModel(BaseModel):
    __tablename__ = 'exam'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String) #zkouska/zapocet/zapoctovy test..
    id_examiner = Column(BigInteger, ForeignKey('user.id'))
    exam_date = Column(DateTime)
    student_capacity = Column(Integer)
    signed_students = Column(BigInteger, ForeignKey('user.id'))    
    additional_information = Column(String)
    id_subject = Column(BigInteger, ForeignKey('subject.id'))
    
    examiners = relationship('UserModel', secondary=Examiner_Exam, back_populates='exams_examiners')
    students = relationship('UserModel', secondary=Student_Exam, back_populates='exams_students')
    subject = relationship('SubjectModel', back_populates='exams')

#Uzivatel
class UserModel(BaseModel):
    __tablename__ = 'user'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    surname = Column(String)
    title = Column(String)
    email = Column(String)
    phone_number = Column(String)
    id_study_group = Column(BigInteger, ForeignKey('study_group.id'))
    id_authorization = Column(BigInteger, ForeignKey('authorization.id'))
    
    exams_examiners = relationship('ExamModel', secondary=Examiner_Exam, back_populates='examiners')
    exams_students = relationship('ExamModel', secondary=Student_Exam, back_populates='students')
    study_group = relationship('StudyGroupModel', back_populates='users')
    authorization = relationship('AuthorizationModel', back_populates='user') #, uselist='False

#Predmet
class SubjectModel(BaseModel):
    __tablename__ = 'subject'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    study_groups = relationship('StudyGroupModel', secondary=StudyGroup_Subject, back_populates='subjects')
    exams = relationship('ExamModel', back_populates='subject')
    
#Studijni_skupina    
class StudyGroupModel(BaseModel):
    __tablename__ = 'study_group'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    subjects = relationship('SubjectModel', secondary=StudyGroup_Subject, back_populates='study_groups')
    users = relationship('UserModel', back_populates='study_group')

#Opravneni
class AuthorizationModel(BaseModel):
    __tablename__ = 'authorization'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    web_admin = Column(Boolean)
    student = Column(Boolean)
    examiner = Column(Boolean)

    user = relationship('UserModel', back_populates='authorization')
    
from sqlalchemy import create_engine

engine = create_engine(connectionstring) 
BaseModel.metadata.create_all(engine)

# ### CRUD Ops
#taky smazat?       +++
from sqlalchemy.orm import sessionmaker

SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()

# ## GraphQL

import uvicorn
from multiprocessing import Process

servers = {}
_api_process = None

def start_api(app=None, port=9992, runNew=True):
    """Stop the API if running; Start the API; Wait until API (port) is available (reachable)"""
    assert port in [9991, 9992, 9993, 9994], f'port has unexpected value {port}'
    def run():
        uvicorn.run(app, port=port, host='0.0.0.0', root_path='')    
        
    _api_process = servers.get(port, None)
    if _api_process:
        _api_process.terminate()
        _api_process.join()
        del servers[port]
    
    if runNew:
        assert (not app is None), 'app is None'
        _api_process = Process(target=run, daemon=True)
        _api_process.start()
        servers[port] = _api_process


# ### Models

import graphene

class ExamGQL(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    exam_date = graphene.String()
    student_capacity = graphene.Int() 
    signed_students = graphene.List(lambda: UserGQL) #ForeignKey
    additional_information = graphene.String()
    id_subject = graphene.ID() #ForeignKey ID/Int?
    
    examiners = graphene.Field(graphene.List(lambda: UserGQL))
    students = graphene.Field(graphene.List(lambda: UserGQL))
    subject = graphene.Field(lambda: SubjectGQL)
                            
class UserGQL(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    surname = graphene.String()
    title = graphene.String()
    email = graphene.String()
    phone_number = graphene.String()
    id_study_group = graphene.ID() #ForeignKey
    id_authorization = graphene.ID() #ForeignKey
        
    exams_examiners = graphene.Field(graphene.List(lambda: ExamGQL))
    exams_students = graphene.Field(graphene.List(lambda: ExamGQL))
    study_group = graphene.Field(lambda: StudyGroupGQL) #jedna skupina, ne mnozina skupin
    authorization = graphene.Field(lambda: AuthorizationGQL)

class SubjectGQL(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    
    study_groups = graphene.Field(graphene.List(lambda: StudyGroupGQL))

class StudyGroupGQL(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    
    subjects = graphene.Field(graphene.List(lambda: SubjectGQL))
    users = graphene.Field(graphene.List(lambda: UserGQL))
    
class AuthorizationGQL(graphene.ObjectType):
    id = graphene.ID()
    web_admin = graphene.Boolean()
    student = graphene.Boolean()
    examiner = graphene.Boolean()
    
    user = graphene.Field(graphene.List(lambda: UserGQL))


# ### Query Root
class QueryGQL(graphene.ObjectType):
    user = graphene.Field(UserGQL, id = graphene.ID(required = True)) #pta se pouze na uzivatele
    exam = graphene.Field(ExamGQL, id = graphene.ID(required = True))
    subject = graphene.Field(SubjectGQL, id = graphene.ID(required = True))
    study_group = graphene.Field(StudyGroupGQL, id = graphene.ID(required = True))    
    
    def resolve_user(parent, info, id):
        result = session.query(UserModel).filter(UserModel.id == id).first()
        return result
    
    def resolve_exam(parent, info, id):
        result = session.query(ExamModel).filter(ExamModel.id == id).first()
        return result
    
    def resolve_subject(parent, info, id):
        result = session.query(SubjectModel).filter(SubjectModel.id == id).first()
        return result
    
    def resolve_study_group(parent, info, id):
        result = session.query(StudyGroupModel).filter(StudyGroupModel.id == id).first()
        return result
    
import requests

def singleCache(f):
    cache = None
    def decorated():
        nonlocal cache
        if cache is None:
            fResult = f()
            cache = fResult.replace('https://swapi-graphql.netlify.app/.netlify/functions/index', '/gql')
        else:
            #print('cached')
            pass
        return cache
    return decorated

@singleCache
def getSwapi():
    source = "https://raw.githubusercontent.com/graphql/swapi-graphql/master/public/index.html"
    import requests
    r = requests.get(source)
    return r.text

#from starlette.graphql import GraphQLApp
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

import graphene
from fastapi import FastAPI
import fastapi

graphql_app = GraphQLApp(
    schema=graphene.Schema(query=QueryGQL), 
    on_get=make_graphiql_handler())

app = FastAPI()#root_path='/api')

#defineStartupAndShutdown(app, SessionMaker)

app.add_route('/gql/', graphql_app, methods=["POST"])

@app.get('/gql/', response_class=fastapi.responses.HTMLResponse)
def swapiUI():
    return getSwapi()
