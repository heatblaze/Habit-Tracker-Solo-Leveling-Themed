from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Add this code to reset your database
# with app.app_context():
    #db.drop_all()
    #db.create_all()
    #print("Database has been reset successfully!")

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=200)
    hp = db.Column(db.Integer, default=1000)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50))
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    max_points = db.Column(db.Integer, default=500)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    frequency = db.Column(db.String(20))
    completions = db.Column(db.Integer, default=0)

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        # Add default skills
        for skill_name in ['Creativity', 'Health', 'Focus', 'Learning', 'Wisdom']:
            skill = Skill(user_id=user.id, name=skill_name)
            db.session.add(skill)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    skills = Skill.query.filter_by(user_id=user.id).all()
    habits = Habit.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, skills=skills, habits=habits)

@app.route('/stats')
def stats():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    skills = Skill.query.filter_by(user_id=user.id).all()
    return render_template('stats.html', user=user, skills=skills)

@app.route('/habits', methods=['GET', 'POST'])
def habits():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        frequency = request.form['frequency']
        habit = Habit(user_id=user.id, name=name, description=description, frequency=frequency)
        db.session.add(habit)
        db.session.commit()
        flash('Habit added!', 'success')
    habits = Habit.query.filter_by(user_id=user.id).all()
    return render_template('habits.html', habits=habits)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database created successfully!")
    app.run(debug=True)
