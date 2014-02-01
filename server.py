from flask import Flask, render_template, render_template_string, redirect, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
import os

from model.model import sessionContext, Base, Session, User, Department, Course, SelectedCourse


app = Flask(__name__)

@app.route('/submitinput',methods=['POST'])
def choose_class():
    coursenumber=request.form.get('coursenumber')
    semester=request.form.get('semester')
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<andrewId>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def user(andrewId):
    with sessionContext() as session:
        if request.method == 'GET':
            try:
                user = session.query(User).filter_by(andrewId = andrewId).one()
                return jsonify(user.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No user with andrewId '%s'" % andrewId)
        elif request.method == 'POST':
            try:
                user = session.query(User).filter_by(andrewId = andrewId).one()
                return jsonify(user.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No user with andrewId '%s'" % andrewId)
           
        elif request.method == 'PUT':
            user = User(andrewId)
            session.add(user)
            return jsonify(user.toJSONSerializable())
        elif request.method == 'DELETE':
            try:
                user = session.query(User).filter_by(andrewId = andrewId).one()
                session.delete(user)
                return jsonify(success = "")
            except NoResultFound, e:
                return jsonify(error = "No user with andrewId '%s'" % andrewId)

@app.route('/department/<int:number>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def department(number):
    with sessionContext() as session:
        if request.method == 'GET':
            try:
                dept = session.query(Department).filter_by(number = number).one()
                return jsonify(dept.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No department with number %d" % number)
        elif request.method == 'POST':
            name = request.args.get('name', type = str)
    
            try:
                dept = session.query(Department).filter_by(number = number).one()
                if name is not None:
                    dept.name = name
                return jsonify(dept.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No department with number %d" % number)
           
        elif request.method == 'PUT':
            name = request.args.get('name', '', type = str)
            dept = Department(number, name)
            session.add(dept)
            return jsonify(dept.toJSONSerializable())
        elif request.method == 'DELETE':
            try:
                dept = session.query(Department).filter_by(number = number).one()
                session.delete(dept)
                return jsonify(success = "")
            except NoResultFound, e:
                return jsonify(error = "No department with number %d" % number)

@app.route('/course/<int:department>/<int:number>', methods = ['GET', 'PUT'])
def courseNumber(department, number):
    with sessionContext() as session:
        if request.method == 'GET':
            try:
                courses = session.query(Course).filter_by(
                    departmentNumber = department,
                    courseNumber = number
                ).all()
                return jsonify(courses = [c.toJSONSerializable() for c in courses])
            except NoResultFound, e:
                return jsonify(error = "No course '%d-%d'" % (department, number))
        elif request.method == 'PUT':
            name = request.args.get('name', '', type = str)
            course = Course(department, number, name)
            session.add(course)
            return jsonify(course.toJSONSerializable())

@app.route('/course', methods = ['GET', 'POST', 'DELETE'])
def course():
    with sessionContext() as session:
        id = int(request.args['id'])
        if request.method == 'GET':
            try:
                course = session.query(Course).filter_by(id = id).one()
                return jsonify(course.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No course with id %d" % id)
        elif request.method == 'POST':
            departmentNumber = request.args.get('departmentNumber', type = int)
            courseNumber = request.args.get('courseNumber', type = int)
            name = request.args.get('name', type = str)
            try:
                course = session.query(Course).filter_by(id = id).one()
                if departmentName is not None:
                    course.departmentNumber = departmentNumber
                if courseNumber is not None:
                    course.courseNumber = courseNumber
                if name is not None:
                    course.name = name
                return jsonify(course.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No course with id %d" % id)
           
        elif request.method == 'DELETE':
            try:
                course = session.query(Course).filter_by(id = id).one()
                session.delete(course)
                return jsonify(success = "")
            except NoResultFound, e:
                return jsonify(error = "No course with id %d" % id)

@app.route('/user/<andrewId>/schedule', methods = ['GET', 'POST', 'DELETE'])
def schedule(andrewId):
    with sessionContext() as session:
        if request.method == 'GET':
            try:
                user = session.query(User).filter_by(andrewId = andrewId).one()
                return jsonify(user = user.toJSONSerializable,
                               schedule = [c.toJSONSerializable for c in user.selectedClasses]
                           )
            except NoResultFound, e:
                return jsonify(error = "No user with andrewId '%s'" % andrewId)
        elif request.method == 'POST':
            courseId = int(request.args['course'])
            year = int(request.args['year'])
            semester = request.args['semester']

            try:                
                user = session.query(User).filter_by(andrewId = andrewId).one()
                try:
                    course = session.query(Course).filter_by(id = courseId).one()
                    selectedCourse = SelectedCourse(user, course, year, semester)
                    session.add(selectedCourse)
                    return jsonify(selectedCourse.toJSONSerializable())
                except NoResultFound, e:
                    return jsonify(error = "No course with id %s" % courseId)
                return jsonify(dept.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No user with andrewId %s" % andrewId)
           
        elif request.method == 'DELETE':
            id = int(request.args['id'])
            selectedCourse = session.query(SelectedCourse).filter_by(id = id).one()
            session.delete(selectedCourse)
            return jsonify(success = "")


if __name__ == "__main__":
    engine = create_engine('sqlite:///test.db', echo=True)
    Session.configure(bind = engine)

    Base.metadata.create_all(engine)
        
    app.run(debug=True, port = 3000, host='0.0.0.0')
