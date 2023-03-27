from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
import sqlalchemy
Base = declarative_base()


class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(70))
    Age = Column(Integer)
    Class = Column(String(20))

    def __init__(self, student_name, student_age, student_class):
        self.Name = student_name
        self.Age = student_age
        self.Class = student_class



class Subjects(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50))

    def __init__(self, name):
        self.Name = name


class Marks(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Student_id = Column(Integer, ForeignKey("students.id", ondelete='CASCADE'))
    Subject_id = Column(Integer, ForeignKey("subjects.id", ondelete='CASCADE'))
    Mark = Column(Integer)
    Date = Column(DATETIME)

    def __init__(self, stdent_id, subject_id, mark):
        self.Student_id = stdent_id
        self.Subject_id = subject_id
        self.Mark = mark
        self.Date = datetime.now()
