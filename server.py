from flask import Flask, render_template, render_template_string, redirect, request
from sqlalchemy import create_engine
import os

from model.model import Base, Session

app = Flask(__name__)
courses={}

@app.route('/submitinput',methods=['POST'])
def choose_class():
    coursenumber=request.form.get('coursenumber')
    semester=request.form.get('semester')
    courses[coursenumber]=semester
    return render_template_string(semester)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session.configure(bind = engine)

    app.run(debug=True, port = 3000, host='0.0.0.0')
