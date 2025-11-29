from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime
import os

# Import configuration
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Database Models
class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    course = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Admission {self.name}>"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Contact {self.name}>"

# Forms (if needed, e.g., for admin login)
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/academics')
def academics():
    return render_template('academics.html')

@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        data = request.form
        admission_entry = Admission(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            course=data.get('course'),
            message=data.get('message')
        )
        db.session.add(admission_entry)
        db.session.commit()
        flash('Application submitted successfully', 'success')
        return redirect(url_for('admission'))
    return render_template('admission.html')


@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        c = Contact(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            subject=data.get('subject'),
            message=data.get('message')
        )
        db.session.add(c)
        db.session.commit()
        flash('Thank you for contacting us. We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


# Simple admin
@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if u == app.config['ADMIN_USER'] and p == app.config['ADMIN_PASS']:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    admissions = Admission.query.order_by(Admission.created_at.desc()).all()
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin_dashboard.html', admissions=admissions, contacts=contacts)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


# Serve static (images) for convenience if running with DEBUG
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
