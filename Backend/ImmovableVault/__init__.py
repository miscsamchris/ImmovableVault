import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager, UserMixin

from flask_cors import CORS

direc = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    direc, "data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY
db = SQLAlchemy(app)
api = Api(app=app)
CORS(app)


from ImmovableVault.Endpoints.views import endpoints_blueprint

app.register_blueprint(endpoints_blueprint, url_prefix="/backend/")
