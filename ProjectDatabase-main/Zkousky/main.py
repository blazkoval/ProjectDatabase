from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

unitedSequence = Sequence('all_id_seq')

#mezitabulky
StudyGroup_Subject = Table('subject_study_groups', BaseModel.metadata,
                           Column('subject_id', ForeignKey('subject.id'), primary_key=True),
                           Column('study_group_id', ForeignKey('study_group.id'), primary_key=True)
                           )

Student_Exam = Table('student_groups', BaseModel.metadata,
                     Column('exam_id', ForeignKey('exam.id'), primary_key=True),
                     Column('student_id', ForeignKey('user.id'), primary_key=True)
                     )

Examiner_Exam = Table('examiner_groups', BaseModel.metadata,
                      Column('exam_id', ForeignKey('exam.id'), primary_key=True),
                      Column('examiner_id', ForeignKey('user.id'), primary_key=True)
                      )


class ExamModel(BaseModel):
    __table_name__ = 'exam'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    id_subject = Column(BigInteger, ForeignKey('subject.id'))
    name = Column(String)
    id_examiner = Column(BigInteger, ForeignKey('user.id'))
    exam_date = Column(DateTime)
    student_capacity = Column(Integer)
    signed_students = Column(BigInteger, ForeignKey('user.id'))
    additional_information = Column(String)

    subjects = relationship('SubjectModel', secondary=StudyGroup_Subject, back_populates='exams')
    students = relationship('UserModel', secondary=Student_Exam, back_populates='exams')
    examiners = relationship('UserModel', secondary=Examiner_Exam, back_populates='exams')


class UserModel(BaseModel):
    __table_name__ = 'user'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    id_authorization = Column(BigInteger, ForeignKey('authorization.id'))
    id_study_group = Column(BigInteger, ForeignKey('study_group.id'))
    name = Column(String)
    surname = Column(String)
    title = Column(String)
    email = Column(String)
    phone_number = Column(String)

    authorization = relationship('AuthorizationModel', back_populates='user', uselist='False')
    study_group = relationship('StudyGroupModel', back_populates='users')
    exams_student = relationship('ExamModel', secondary=Student_Exam, back_populates='students')
    exams_examiners = relationship('ExamModel', secondary=Examiner_Exam, back_populates='examiners')


class AuthorizationModel(BaseModel):
    __table_name__ = 'authorization'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    web_admin = Column(bool)
    student = Column(bool)
    examiner = Column(bool)

    users = relationship('UserModel', back_populates='authorization')


class StudyGroupModel(BaseModel):
    __table_name__ = 'study_group'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    users = relationship('UserModel', back_populates='study_group')


class SubjectModel(BaseModel):
    __table_name__ = 'subject'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    id_study_group = Column(BigInteger, ForeignKey('study_group.id'))
    name = Column(String)

    exams = relationship('ExamModel', secondary=StudyGroup_Subject, back_populates='subject')
