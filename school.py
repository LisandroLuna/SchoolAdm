from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table

Base = declarative_base()

course_times = Table('course_times', Base.metadata,
                     Column('time_id', ForeignKey('time_record.id'), primary_key=True),
                     Column('course_id', ForeignKey('course.id'), primary_key=True)
                     )

teacher_times = Table('teacher_times', Base.metadata,
                      Column('time_id', ForeignKey('time_record.id'), primary_key=True),
                      Column('teacher_id', ForeignKey('teacher.id'), primary_key=True)
                      )


class TimeRecord(Base):
    """Times Record"""
    __tablename__ = 'time_record'
    id = Column(Integer, Sequence('time_id_seq'), primary_key=True)
    course_day = Column(String)
    # Relation many to many
    teachers = relationship(
        "Teacher",
        secondary=teacher_times,
        back_populates="times"
    )
    courses = relationship(
        "Course",
        secondary=course_times,
        back_populates="times"
    )

    def __repr__(self):
        return "{}".format(self.course_day)

class Student(Base):
    """Student model"""
    __tablename__ = 'student'

    id = Column(Integer, Sequence('student_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    lastn = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'))
    # Relation many to one
    courses = relationship(
        'Course',
        back_populates='students'
    )

    def __repr__(self):
        return "{}, {}".format(self.lastn, self.name)


class Teacher(Base):
    """Teacher model"""
    __tablename__ = 'teacher'

    id = Column(Integer, Sequence('teacher_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    lastn = Column(String, nullable=False)

    # Relation many to many
    times = relationship(
        "TimeRecord",
        secondary=teacher_times,
        back_populates="teachers"
    )

    def __repr__(self):
        return "{}, {}".format(self.lastn, self.name)


class Course(Base):
    """Course model"""
    __tablename__ = 'course'

    id = Column(Integer, Sequence('course_id_seq'), primary_key=True)
    stime = Column(Integer, nullable=False)
    etime = Column(Integer, nullable=False)
    # Relation many to one
    students = relationship(
        'Student',
        back_populates='courses',
        cascade='all, delete, delete-orphan'
    )

    # Relation many to many
    times = relationship(
        "TimeRecord",
        secondary=course_times,
        back_populates="courses"
    )

    def __repr__(self):
        return "{}:00/{}:00".format(str(self.stime), str(self.etime))
