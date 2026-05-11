from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# ================= USER MODEL =================

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(300), nullable=False)

    tasks = db.relationship('Task', backref='owner', lazy=True)


# ================= TASK MODEL =================

class Task(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.String(500))

    priority = db.Column(db.String(50))

    status = db.Column(db.String(50), default='Pending')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


# ================= LOGIN LOADER =================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# ================= HOME =================

@app.route('/')
@login_required
def home():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    total_tasks = len(tasks)

    completed_tasks = len([t for t in tasks if t.status == 'Completed'])

    pending_tasks = len([t for t in tasks if t.status == 'Pending'])

    completion_percentage = 0

    if total_tasks > 0:
        completion_percentage = round((completed_tasks / total_tasks) * 100, 2)

    return render_template(
        'index.html',
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_percentage=completion_percentage
    )


# ================= REGISTER =================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']

        email = request.form['email']

        password = generate_password_hash(request.form['password'])

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:

            flash('Email already exists!', 'danger')

            return redirect(url_for('register'))

        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        flash('Registration Successful!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')


# ================= LOGIN =================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            flash('Login Successful!', 'success')

            return redirect(url_for('home'))

        else:

            flash('Invalid Email or Password!', 'danger')

    return render_template('login.html')


# ================= LOGOUT =================

@app.route('/logout')
@login_required
def logout():

    logout_user()

    flash('Logged Out Successfully!', 'info')

    return redirect(url_for('login'))


# ================= ADD TASK =================

@app.route('/add-task', methods=['POST'])
@login_required
def add_task():

    title = request.form['title']

    description = request.form['description']

    priority = request.form['priority']

    status = request.form['status']

    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        status=status,
        user_id=current_user.id
    )

    db.session.add(new_task)

    db.session.commit()

    flash('Task Added Successfully!', 'success')

    return redirect(url_for('home'))


# ================= UPDATE TASK =================

@app.route('/update-task/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):

    task = Task.query.get_or_404(id)

    if request.method == 'POST':

        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.status = request.form['status']

        db.session.commit()

        return redirect(url_for('home'))

    return render_template('update_task.html', task=task)

# ================= DELETE TASK =================

@app.route('/delete-task/<int:id>')
@login_required
def delete_task(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)

    db.session.commit()

    flash('Task Deleted Successfully!', 'danger')

    return redirect(url_for('home'))


# ================= MAIN =================

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)