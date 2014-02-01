<<<<<<< HEAD
from flask import Flask, render_template, redirect, jsonify, request
=======
from flask import Flask, render_template, render_template_string, redirect, request
>>>>>>> 531a4131943d8960fdcaf3cf6d6bce25ed14eca2
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
import os

from model.model import sessionContext, Base, Session, User, Department


app = Flask(__name__)

@app.route('/submitinput',methods=['POST'])
def choose_class():
    coursenumber=request.form.get('coursenumber')
    semester=request.form.get('semester')
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule/<userId>')
def schedule(userId):
    with sessionContext() as session:
        try:
            user = session.query(User).filter_by(andrewId = userId).one()
            return jsonify(user.toJSONSerializable())
        except NoResultFound, e:
            return jsonify(error = "No user with andrewId '%s'" % userId)

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
            name = request.args.get('name', '', type = str)
    
            try:
                dept = session.query(Department).filter_by(number = number).one()
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


if __name__ == "__main__":
    engine = create_engine('sqlite:///test.db', echo=True)
    Session.configure(bind = engine)

    Base.metadata.create_all(engine)
        
    app.run(debug=True, port = 3000, host='0.0.0.0')
