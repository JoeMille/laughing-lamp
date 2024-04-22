from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    registration_form = RegistrationForm(request.form)
    login_form = LoginForm(request.form)
    if request.method == 'POST':
        if registration_form.validate_on_submit():
            hashed_password = generate_password_hash(registration_form.password.data, method='sha256')
            new_user = User(username=registration_form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('User has been successfully registered!', 'success')
            return redirect(url_for('home'))
        elif login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            if user and check_password_hash(user.password, login_form.password.data):
                return redirect(url_for('home'))
            else:
                return 'Invalid username or password'
    return render_template('index.html', login_form=login_form, registration_form=registration_form)
    
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)