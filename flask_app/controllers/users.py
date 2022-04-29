from flask import render_template, request, redirect, session, flash
from flask_app import app, Bcrypt
from flask_app.models.user import User
from flask_app.models.solve import Solve
import re

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    scram = Solve.scramble()
    return render_template('index.html', scram=scram)

@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    if User.get_by_email(request.form):
        flash('Email already registered')
        return redirect('/register_page')
    if not User.validate_user(request.form):
        return redirect('/register_page')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['user_name'] = data['first_name']
    return redirect('/dash')

@app.route('/register_page')
def reg_page():
    return render_template('register.html')

@app.route('/login_page')
def log_page():
    return render_template('login.html')

@app.route('/dash')                      
def dash():
    if 'user_id' not in session:
        return redirect('/logout')
    scram = Solve.scramble()
    print(scram)
    return render_template('dash.html', users=User.get_all(), scram=scram)

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    print(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/login_page")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login_page')
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.first_name
    return redirect("/dash")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/save_time', methods=['POST'])
def save_time():
    print(request.form)
    id = Solve.save(request.form)
    return redirect('/dash')

@app.route('/profile/<int:id>')
def profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id":id}
    print(User.get_user_with_solves(data))
    return render_template('profile.html', users=User.get_user_with_solves(data))

@app.route('/delete/<int:sid>')
def delete(sid):
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = session['user_id']
    data = {"id":sid}
    Solve.destroy(data)
    return redirect(f"/profile/{user_id}")