import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models import db, User
from forms import LoginForm
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route ('/')
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            return redirect(url_for('home'))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
