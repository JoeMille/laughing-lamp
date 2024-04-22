import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route ('/')
def index():
    return render_template('index.html')

