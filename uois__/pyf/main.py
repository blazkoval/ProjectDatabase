#!/usr/bin/env python
# coding: utf-8

# # SQLAlchemy
 
# ## Models

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.functions import database_exists, create_database

"""
Vytvoření connection stringu k úplnému propojení databáze se serverem
"""
connectionstring = 'postgresql+psycopg2://postgres:example@postgres/data'
if not database_exists(connectionstring): 
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

"""
Tabulky propojující modely, které mají mezi sebou relaci M:N. Vyváří se pomocí funkce Table.
"""
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


class ExamModel(BaseModel):
    """
    Třída reprezentující model zkoušky.
    
    Atributy:
    ---------
    id
        primární klíč
    name
        název: zkouška, zápočet nebo klasifikovaný zápočet
    exam_date
        termín zkoušky ve formátu YYYY-MM-DD hh:mm:ss
    student_capacity
        maximální kapacita studentů
    additional_information
        poznámka
    id_subject
        přiřazení předmětu zkoušce skrz primární klíč SubjectModel
    examiners
        relace mezi zkouškou a zkoušejícím (M:N) - odkazuje na tabulku Examiner_Exam
    students
        relace mezi zkouškou a studentem (M:N) - odkazuje na tabulku Student_Exam
    subjects
        relace mezi zkouškou a předmětem (N:1)
    """
    __tablename__ = 'exam'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String) #zkouska/zapocet/klasifikovany zapocet..
    #id_examiner = Column(BigInteger, ForeignKey('user.id')) #nepouzitelne, kvuli tabulce Examiner_Exam
    exam_date = Column(DateTime)
    student_capacity = Column(Integer)
    signed_students = Column(BigInteger, ForeignKey('user.id'))    
    additional_information = Column(String)
    id_subject = Column(BigInteger, ForeignKey('subject.id'))
    
    examiners = relationship('UserModel', secondary=Examiner_Exam, back_populates='exams_examiners')
    students = relationship('UserModel', secondary=Student_Exam, back_populates='exams_students')
    subject = relationship('SubjectModel', back_populates='exams')


class UserModel(BaseModel):
    """
    Třída reprezentující model uživatele.
    
    Atributy:
    ---------
    id
        primární klíč
    name
        jméno uživatele
    surname
        příjmení uživatele
    title
        titul
    email
        email
    phone_number
        telefoní číslo
    id_study_group
        přiřazení studijní skupiny uživatelovi skrz primární klíč StudyGroupModel
    id_authorization
        přiřazení autorizace uživatelovi skrz primární klíč AuthorizationModel
    exams_examiners
        relace mezi zkouškou a zkoušejícím (M:N) - odkazuje na tabulku Examiner_Exam
    exams_students
        relace mezi zkouškou a studentem (M:N) - odkazuje na tabulku Student_Exam
    study_groups
        relace mezi uživatelem a studijní skupinou (N:1)
    authorization
        relace mezi uživatelem a autorizací (N:1)
    """

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
    authorization = relationship('AuthorizationModel', back_populates='user')

#Predmet
class SubjectModel(BaseModel):
    """
    Třída reprezentující model předmětu.
    
    Atributy:
    ---------
    id
        primární klíč
    name
        název předmětu   
    study_groups
        relace mezi studijní skupinou a předmětem (M:N) - odkazuje na tabulku StudyGroup_Subject
    exams
        relace mezi zkouškou a studijní skupinou (N:1)
    """
    __tablename__ = 'subject'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    study_groups = relationship('StudyGroupModel', secondary=StudyGroup_Subject, back_populates='subjects')
    exams = relationship('ExamModel', back_populates='subject')
    
#Studijni_skupina    
class StudyGroupModel(BaseModel):
    """
    Třída reprezentující model studijní skupiny.
    
    Atributy:
    ---------
    id
        primární klíč
    name
        název studijní skupiny
    subjects
        relace mezi studijní skupinou a předmětem (M:N) - odkazuje na tabulku StudyGroup_Subject
    users
        relace mezi uživatelem a studijní skupinou (N:1)
    """
    __tablename__ = 'study_group'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    subjects = relationship('SubjectModel', secondary=StudyGroup_Subject, back_populates='study_groups')
    users = relationship('UserModel', back_populates='study_group')

#Opravneni
class AuthorizationModel(BaseModel):
    """
    Třída reprezentující model autorizace.
    
    Atributy:
    ---------
    id
        primární klíč
    web_admin
        true pokud je id 1
    student
        true pokud je id 2
    examiner   
        true pokud je id 3
    user
        relace mezi uživatelem a autorizací (N:1)        
    """
    __tablename__ = 'authorization'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    web_admin = Column(Boolean)
    student = Column(Boolean)
    examiner = Column(Boolean)

    user = relationship('UserModel', back_populates='authorization')
    
from sqlalchemy import create_engine

"""
Vytvoření engine a struktury databáze a jejich tabulek
"""
engine = create_engine(connectionstring) 
BaseModel.metadata.create_all(engine)

# # GraphQL

# ## Models

"""
Navázání databázových struktur využívající SQLAlchemy na databázové záznamy.
Modely jsou definovány jako třídy. Atributy tříd jsou nazvány stejne jako v SQLAlchemy.
Díky využití již definovaných modelů v SQLAlchemy není třeba vytvářet mezitabulky ani resolvery.
"""

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
    id_study_group = graphene.ID() 
    id_authorization = graphene.ID()
        
    exams_examiners = graphene.Field(graphene.List(lambda: ExamGQL))
    exams_students = graphene.Field(graphene.List(lambda: ExamGQL))
    study_group = graphene.Field(lambda: StudyGroupGQL)
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
    """
    Třída, která získavá hlavní datové struktury a jsou skrz ni obsluhovány případné dotazy

    Atributy:
    ---------
    user
        dotaz na uživatele
    exam
        dotaz na zkoušku
    subject
        dotaz na předmět
    study_group
        dotaz na studijní skupinu
                
    Metody:
    -------
    resolve_user
        implicitní resolver vrací výsledek dotazu na uživatele
    resolve_exam
        implicitní resolver vrací výsledek dotazu na zkoušku
    resolve_subject
        implicitní resolver vrací výsledek dotazu na předmět
    resolve_study_group
        implicitní resolver vrací výsledek dotazu na studijní skupinu
    """
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
    

"""
Řešení problému nejnovější verze starlette_graphene3
"""    
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


"""
Vytvoření finální aplikace pro čtení z databáze.
"""
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

import graphene
from fastapi import FastAPI
import fastapi

graphql_app = GraphQLApp(
    schema=graphene.Schema(query=QueryGQL), 
    on_get=make_graphiql_handler())

app = FastAPI()#root_path='/api')
app.add_route('/gql/', graphql_app, methods=["POST"])
@app.get('/gql/', response_class=fastapi.responses.HTMLResponse)
def swapiUI():
    return getSwapi()
