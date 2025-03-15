# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from flask import jsonify

from pprint import pprint
import json
import random

db = database()

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x     = random.choice(['I like to surf.','I DJ on the side','Graduating 1 year early.'])
	return render_template('home.html', fun_fact = x)

@app.route('/projects')
def projects():
	return render_template('projects.html')

@app.route('/piano')
def piano():
	return render_template('piano.html')

@app.route('/resume', methods=['GET'])
def resume():
    resume_data = db.getResumeData()
    return render_template('resume.html', resume_data=resume_data)

@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    name = request.form['name']
    email = request.form['email']
    comment = request.form['comment']

    db.insert_feedback(name, email, comment)

    feedback_data = db.get_all_feedback()

    return render_template('processfeedback.html', feedback_data=feedback_data)