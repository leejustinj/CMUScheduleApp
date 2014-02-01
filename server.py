from flask import Flask, render_template, render_template_string, redirect, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from itertools import groupby
import os, json

from model.model import sessionContext, Base, Session, User, Department, Course, SelectedCourse


def tryGet(val, key, default):
    if val is None:
        return default
    elif key in val:
        return val[key]
    else:
        return default

def sortIndexSemester(sched):
    if sched.semester == 'Spring':
        return sched.year * 2
    else:
        return 2 * sched.year + 1

def semesterKey(sched):
    return {'semester' : sched.semester, 'year' : sched.year}


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
                session.flush()
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
            existing = session.query(User).filter_by(andrewId = andrewId).all()
            if len(existing) == 0:
                session.add(user)
                session.flush()
                return jsonify(user.toJSONSerializable())
            else:
                return jsonify(existing[0].toJSONSerializable())
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
            data = request.get_json(force = True)
            try:
                dept = session.query(Department).filter_by(number = number).one()
                if 'name' in data:
                    dept.name = data['name']
                return jsonify(dept.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No department with number %d" % number)
           
        elif request.method == 'PUT':
            data = request.get_json(force = True)
            name = tryGet(data, 'name', '')
            dept = Department(number, name)
            session.add(dept)
            session.flush()
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
            data = request.get_json()
            name = tryGet(data, 'name', '')
            course = Course(department, number, name)
            session.add(course)
            session.flush()
            return jsonify(course.toJSONSerializable())

@app.route('/course', methods = ['GET', 'POST', 'DELETE'])
def course():
    with sessionContext() as session:
        data = request.get_json()
        id = data['id']
        if request.method == 'GET':
            try:
                course = session.query(Course).filter_by(id = id).one()
                return jsonify(course.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No course with id %d" % id)
        elif request.method == 'POST':
            try:
                course = session.query(Course).filter_by(id = id).one()
                if 'departmentName' in data:
                    course.departmentNumber = int(data['departmentNumber'])
                if 'courseNumber' in data:
                    course.courseNumber = int(data['courseNumber'])
                if name in data:
                    course.name = data['name']
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
        request.args
        if request.method == 'GET':
            try:
                user = session.query(User).filter_by(andrewId = andrewId).one()
                selectedCourses = sorted(user.selectedClasses, key = sortIndexSemester)
                schedule = [{'semester' : k['semester'], 
                              'year' : k['year'],
                             'courses' : [{'courseId' : c.courseId, 
                                           'course' : c.course.toJSONSerializable()}
                                          for c in courses]}
                            for k, courses in groupby(selectedCourses, semesterKey)]
                return jsonify(user = user.toJSONSerializable(),
                               schedule = schedule)

                # return jsonify(user = user.toJSONSerializable,
                #                schedule = [c.toJSONSerializable for c in user.selectedClasses]
                #            )
            except NoResultFound, e:
                return jsonify(error = "No user with andrewId '%s'" % andrewId)
        elif request.method == 'POST':
            data = request.get_json(force = True)
            courseId = int(data['course'])
            year = int(data['year'])
            semester = data['semester']

            try:                
                user = session.query(User).filter_by(andrewId = andrewId).one()
                try:
                    course = session.query(Course).filter_by(id = courseId).one()
                    selectedCourse = SelectedCourse(user, course, year, semester)
                    session.add(selectedCourse)
                    session.flush()
                    return jsonify(selectedCourse.toJSONSerializable())
                except NoResultFound, e:
                    return jsonify(error = "No course with id %s" % courseId)
                return jsonify(dept.toJSONSerializable())
            except NoResultFound, e:
                return jsonify(error = "No user with andrewId %s" % andrewId)
           
        elif request.method == 'DELETE':
            data = request.get_json(force = True)
            id = int(data['id'])
            selectedCourse = session.query(SelectedCourse).filter_by(id = id).one()
            session.delete(selectedCourse)
            return jsonify(success = "")

if __name__ == "__main__":
    engine = create_engine('sqlite:///test.db', echo=True)
    Session.configure(bind = engine)

    Base.metadata.create_all(engine)
        
    app.run(debug=True, port = 3000, host='0.0.0.0')
