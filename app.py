from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime
import os

# Import configuration
from config import Config

# Initialize Flask App
# Use os.path.abspath(__file__) to ensure correct pathing for Render
app = Flask(__name__,
            root_path=os.path.dirname(os.path.abspath(__file__)),
            template_folder='templates',
            static_folder='static')
app.config.from_object(Config)

# Initialize SQLAlchemy with the app
# Use 'app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS')' to silence warnings
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

# Forms (for admin login)
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# --- Web Routes ---

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
        # Basic validation check
        if not data.get('name') or not data.get('email') or not data.get('course'):
            flash('Name, Email, and Course are required fields.', 'danger')
            return redirect(url_for('admission'))

        admission_entry = Admission(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            course=data.get('course'),
            message=data.get('message')
        )
        try:
            db.session.add(admission_entry)
            db.session.commit()
            flash('Application submitted successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during submission: {e}', 'danger')

        return redirect(url_for('admission'))
    return render_template('admission.html')


@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        # Basic validation check
        if not data.get('name') or not data.get('email') or not data.get('message'):
            flash('Name, Email, and Message are required fields.', 'danger')
            return redirect(url_for('contact'))
            
        c = Contact(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            subject=data.get('subject'),
            message=data.get('message')
        )
        try:
            db.session.add(c)
            db.session.commit()
            flash('Thank you for contacting us. We will get back to you soon.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during submission: {e}', 'danger')

        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


# --- Admin Routes ---

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        u = form.username.data
        p = form.password.data
        if u == app.config['ADMIN_USER'] and p == app.config['ADMIN_PASS']:
            session['admin'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)


@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('admin_login'))
    
    admissions = Admission.query.order_by(Admission.created_at.desc()).all()
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin_dashboard.html', admissions=admissions, contacts=contacts)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# --- Local Development Startup ---
if __name__ == '__main__':
    with app.app_context():
        # This will create tables if they don't exist.
        # In production, use a migration tool like Flask-Migrate instead.
        db.create_all() 
    app.run(debug=Config.DEBUG)
