import os

from flask import Flask

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'b2ef5344f4d47cf53fc05361d0fef936'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

from tileapp import routes
