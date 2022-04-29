from flask import render_template, request, redirect, session, flash
from flask_app import app, Bcrypt
from flask_app.models.user import User
import re

bcrypt = Bcrypt(app)

@app.route('/save_time', methods=['POST'])
def save_time():
    id = Solve.save(request.form)
    return redirect('/dash')