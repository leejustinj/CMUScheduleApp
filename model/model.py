from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///:memory:')
Base = declarative_base()


Semester = Enum("Fall", "Spring")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    andrewID = Column(String, unique = True, nullable = False)

    def __init__(self, andrewId):
        self.andrewId = andrewId

    def __repr__(self):
        return "<User(andrewId=%s)>" % self.andrewId
    

class Department(Base):
    __tablename__ = 'departments'
    number = Column(Integer, primary_key = True)
    name = Column(String)

    def __init__(self, number, name = ""):
        self.number = number
        self.name = name

    def __repr__(self):
        return '<Department(%i, "%s")>' % (self.number, self.name)
    

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

Base.metadata.create_all(engine)
