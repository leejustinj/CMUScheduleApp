from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from contextlib import contextmanager

Semester = Enum("Fall", "Spring")

Base = declarative_base()
Session = sessionmaker()

@contextmanager
def sessionContext():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    andrewId = Column(String, unique = True, nullable = False)

    def __init__(self, andrewId):
        self.andrewId = andrewId

    def __repr__(self):
        return "<User(andrewId=%s)>" % self.andrewId
    
    def toJSONSerializable(self):
        return {'id' : self.id,
                'user': self.andrewId}

class Department(Base):
    __tablename__ = 'departments'
    number = Column(Integer, primary_key = True)
    name = Column(String)

    def __init__(self, number, name = ""):
        self.number = number
        self.name = name

    def __repr__(self):
        return '<Department(%i, "%s")>' % (self.number, self.name)

    def toJSONSerializable(self):
        return {'number' : self.number, 
                'name' : self.name}
    

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key = True)
    departmentNumber = Column(Integer, ForeignKey('departments.number'), nullable=False)
    department = relationship('Department', backref=backref('classes', order_by=id))

    name = Column(String)

    courseNumber = Column(Integer, nullable= False)
    
    def __init__(self, departmentNumber, courseNumber, name = ""):
        self.departmentNumber = departmentNumber
        self.courseNumber = courseNumber
        self.name = name

    def __repr__(self):
        return '<Course("%d-%d", "%s")>' % (self.departmentNumber, self.courseNumber, self.name)

    def toJSONSerializable(self):
        return {'id' : self.id,
                'department': self.departmentNumber,
                'courseNumber' : self.courseNumber}

class SelectedCourse(Base):
    __tablename__ = 'courseSelections'

    id = Column(Integer, primary_key = True)

    userId = Column(Integer, ForeignKey('users.id'), nullable = False)
    user = relationship('User', backref = backref('selectedClasses'))

    courseId = Column(Integer, ForeignKey('courses.id'), nullable = False)
    course = relationship('Course')

    year = Column(Integer, nullable = False)
    semester = Column(Semester, nullable = False)

    def __init__(self,  user, course, year, semester):
        self.user = user
        self.course = course
        self.year = year
        self.semester = semester

    def __repr__(self):
        return "<SelectedCourse(user=%s, course='%d-%d', year=%d, semester='%s')>" % (
            self.user.andrewId,
            self.course.departmentNumber,
            self.course.courseNumber,
            self.year,
            self.semester)

    def toJSONSerializable(self):
        return { 'id' : self.id,
                 'user' : self.user.toJSONSerializable(),
                 'course' : self.course.toJSONSerializable(),
                 'year' : self.year,
                 'semester' : self.semester}
