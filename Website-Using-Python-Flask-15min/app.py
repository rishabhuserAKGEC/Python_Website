from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'supersecretkey'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Database model for storing messages from the contact form
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Message({self.name}, {self.email})'

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact route with form submission handling
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save the submitted message to the database
        msg = Message(name=name, email=email, message=message)
        db.session.add(msg)
        db.session.commit()

        # Flash message to notify the user of successful submission
        flash(f'Thank you, {name}! We have received your message.')
        return redirect(url_for('contact'))

    return render_template('contact.html')

# Dynamic user profile route
@app.route('/user/<username>')
def profile(username):
    return f'<h1>Welcome to {username}\'s profile</h1>'

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Example check for static credentials
        if username == 'admin' and password == 'adminpass':
            session['user'] = username
            flash('You were successfully logged in')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username or password.')

    return render_template('login.html')

# User logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You were successfully logged out')
    return redirect(url_for('home'))

# Error handler for 404 pages
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Uncomment the following lines to create the database tables
    # from app import db
    # db.create_all()

    app.run(debug=True)
