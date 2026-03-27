from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Parent(Base):
    __tablename__ = "parents"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    students = relationship("Student", back_populates="parent")

class Student(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    dob = Column(DateTime)
    gender = Column(String)
    current_grade = Column(String)
    parent_id = Column(String, ForeignKey("parents.id"))
    parent = relationship("Parent", back_populates="students")
    registrations = relationship("ClassRegistration", back_populates="student")
    subscriptions = relationship("Subscription", back_populates="student")

class ClassModel(Base):
    __tablename__ = "classes"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    subject = Column(String)
    day_of_week = Column(Integer)
    time_slot = Column(String)
    teacher_name = Column(String)
    max_students = Column(Integer)
    registrations = relationship("ClassRegistration", back_populates="class_")

class ClassRegistration(Base):
    __tablename__ = "class_registrations"
    id = Column(String, primary_key=True, index=True)
    class_id = Column(String, ForeignKey("classes.id"))
    student_id = Column(String, ForeignKey("students.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('class_id', 'student_id', name='_class_student_uc'),)
    class_ = relationship("ClassModel", back_populates="registrations")
    student = relationship("Student", back_populates="registrations")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.id"))
    package_name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_sessions = Column(Integer)
    used_sessions = Column(Integer, default=0)
    student = relationship("Student", back_populates="subscriptions")