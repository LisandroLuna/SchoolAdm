from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table

Base = declarative_base()


# TimeRecord nos va a servir para asociar un Profesor con un Curso
class TimeRecord(Base):
    """Times Record"""
    __tablename__ = 'time_record'
    id = Column(Integer, Sequence('time_id_seq'), primary_key=True)
    course_day = Column(String)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    # Relation many to one
    teachers = relationship(
        'Teacher',
        back_populates='times'
    )
    courses = relationship(
        'Course',
        back_populates='times'
    )

    def gett(self):
        return self.teachers

    def getc(self):
        return self.courses

    def __repr__(self):
        return "{}".format(self.course_day)


# Creamos el modelo de Alumno
class Student(Base):
    """Student model"""
    __tablename__ = 'student'

    id = Column(Integer, Sequence('student_id_seq'), primary_key=True)
    # Code seria el equivalente a un numero de inscripcion
    code = Column(String)
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
    code = Column(String)
    name = Column(String, nullable=False)
    lastn = Column(String, nullable=False)
    # Relation many to one
    times = relationship(
        'TimeRecord',
        back_populates='teachers',
        cascade='all, delete, delete-orphan'
    )

    def showc(self):
        days = self.getcour()
        print('Profesor: ' + str(self))
        for d in days:
            print('- ' + str(d))
        input("\nPresiona Enter para continuar...")

    def getcour(self):
        timesc = []
        for atime, acour in session.query(TimeRecord, Course). \
                filter(TimeRecord.teacher_id == self.id). \
                filter(TimeRecord.course_id == Course.id). \
                all():
            timesc.append(str(atime) + ': ' + str(acour))
        return timesc

    def __repr__(self):
        return "{}, {}".format(self.lastn, self.name)


class Course(Base):
    """Course model"""
    __tablename__ = 'course'

    id = Column(Integer, Sequence('course_id_seq'), primary_key=True)
    code = Column(String)
    # El horario va en formato HH:MM
    stime = Column(String, nullable=False)
    etime = Column(String, nullable=False)
    # Relation many to one
    students = relationship(
        'Student',
        back_populates='courses',
        cascade='all, delete, delete-orphan'
    )
    times = relationship(
        'TimeRecord',
        back_populates='courses',
        cascade='all, delete, delete-orphan'
    )

    def getstu(self):
        data = session.query(Student).join(Course, Student.course_id == self.id).all()
        return data

    def getcout(self):
        timest = []
        for atime, ateach in session.query(TimeRecord, Teacher). \
                filter(TimeRecord.course_id == self.id). \
                filter(TimeRecord.teacher_id == Teacher.id). \
                all():
            timest.append(str(atime) + ': ' + str(ateach))
        return timest

    def getfull(self):
        code = str(self.code)
        times = self.getcout()
        students = self.getstu()
        print('Informacion del curso ' + code)
        print('Horario: ' + self.stime + '/' + self.etime)
        print('Profesores: ')
        for t in times:
            print('- ' + str(t))
        print('Alumnos: ')
        for s in students:
            print('- ' + str(s))
        input("\nPresiona Enter para continuar...")

    def __repr__(self):
        return "{} - {}/{}".format(self.code,
                                   datetime.strptime(self.stime, '%H:%M').time(),
                                   datetime.strptime(self.etime, '%H:%M').time()
                                   )


# Configuro la sesion
engine = create_engine('sqlite:///:memory:')
#engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Creo Cursos
cur1 = Course(code='C2525', stime='08:15', etime='12:15')
cur2 = Course(code='C2543', stime='14:10', etime='18:10')

# Creo Alumnos
stu1 = Student(code='S0001', name='Jose', lastn='Perez')
stu2 = Student(code='S0002', name='Sofia', lastn='Rodriguez')
stu3 = Student(code='S0003', name='Matias', lastn='Bilardo')
stu4 = Student(code='S0004', name='Josefina', lastn='Luna')
stu5 = Student(code='S0005', name='Marta', lastn='Propato')
stu6 = Student(code='S0005', name='Lucas', lastn='Ortigoza')

# Creo Profesores
prof1 = Teacher(code='T0001', name='Pedro', lastn='Lopez')
prof2 = Teacher(code='T0002', name='Susana', lastn='Avalos')
prof3 = Teacher(code='T0003', name='Martin', lastn='Gomez')
prof4 = Teacher(code='T0004', name='Estefania', lastn='Perez')
prof5 = Teacher(code='T0005', name='Lucas', lastn='Albertengo')
prof6 = Teacher(code='T0006', name='Estela', lastn='Yosida')
prof7 = Teacher(code='T0007', name='Fernando', lastn='Suarez')

# Creo Horarios Para asociar curso y Profesor con el dia que les toca
time1 = TimeRecord(course_day='Lunes Mañana')
time2 = TimeRecord(course_day='Martes Mañana')
time3 = TimeRecord(course_day='Mircoles Mañana')
time4 = TimeRecord(course_day='Jueves Mañana')
time5 = TimeRecord(course_day='Viernes Mañana')
time6 = TimeRecord(course_day='Lunes Tarde')
time7 = TimeRecord(course_day='Martes Tarde')
time8 = TimeRecord(course_day='Mircoles Tarde')
time9 = TimeRecord(course_day='Jueves Tarde')
time10 = TimeRecord(course_day='Viernes Tarde')

# Agrego Cursos y Profesores para generarles un ID
session.add(cur1)
session.add(cur2)
session.add(prof1)
session.add(prof2)
session.add(prof3)
session.add(prof4)
session.add(prof5)
session.add(prof6)
session.add(prof7)
session.add(time1)
session.add(time2)
session.add(time3)
session.add(time4)
session.add(time5)
session.add(time6)
session.add(time7)
session.add(time8)
session.add(time9)
session.add(time10)

# Recupero sus valores con ID
cur1 = session.query(Course).filter_by(code='C2525').one()
cur2 = session.query(Course).filter_by(code='C2543').one()
prof1 = session.query(Teacher).filter_by(code='T0001').one()
prof2 = session.query(Teacher).filter_by(code='T0002').one()
prof3 = session.query(Teacher).filter_by(code='T0003').one()
prof4 = session.query(Teacher).filter_by(code='T0004').one()
prof5 = session.query(Teacher).filter_by(code='T0005').one()
prof6 = session.query(Teacher).filter_by(code='T0006').one()
prof7 = session.query(Teacher).filter_by(code='T0007').one()

# Agrego Alumnos a un Curso
cur1.students.append(stu1)
cur1.students.append(stu2)
cur1.students.append(stu3)
cur2.students.append(stu4)
cur2.students.append(stu5)
cur2.students.append(stu6)

# Agrego Profesores y Curso a un horario en comun
prof1.times.append(time1)
prof2.times.append(time2)
prof3.times.append(time3)
prof4.times.append(time4)
prof5.times.append(time5)
cur1.times.append(time1)
cur1.times.append(time2)
cur1.times.append(time3)
cur1.times.append(time4)
cur1.times.append(time5)
prof6.times.append(time6)
prof7.times.append(time7)
prof1.times.append(time8)
prof2.times.append(time9)
prof3.times.append(time10)
cur2.times.append(time6)
cur2.times.append(time7)
cur2.times.append(time8)
cur2.times.append(time9)
cur2.times.append(time10)

print('Informacion de Cursos:')
cur1.getfull()
cur2.getfull()
print('Informacion de Profesores:')
prof1.showc()
prof2.showc()

session.commit()


