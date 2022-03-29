#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, jsonify, request
from flask_login import LoginManager, login_user, current_user, login_required
from flask_restful import Api, Resource

from D_Delivery.models.user import UserModel
from D_Delivery.resources.history import History
from D_Delivery.resources.meal import Meal
from D_Delivery.resources.meals import Meals
from D_Delivery.resources.orders import Orders
from D_Delivery.resources.home import Home
from D_Delivery.resources.transporter import Transporter
from D_Delivery.resources.user import User, Login, Logout

# sec is a python file contain {key, db_user, db_key}
from sec import sec

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DB_NAME = "D_Delivery.db"
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = sec.key

# SqlAlchemy Database Configuration With SQLite3
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_NAME'] = "D_Delivery_token"

# Configure restful api
api = Api(app)
api.add_resource(Home, '/')

# Configure flask login
login_manager = LoginManager(app)
login_manager.init_app(app)

# ------------- Meal Resource ----------------------
api.add_resource(Meal, '/meal')

# ------------- Meals Resource ----------------------
api.add_resource(Meals, '/meals')

# ------------- User Resource ----------------------
api.add_resource(User, '/user')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Wloggedin, '/wloggedin')


@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


# ------------- Transporter Resource ----------------------
api.add_resource(Trans, '/transporter')

# ------------- Order Resource ----------------------
api.add_resource(Order, '/order')

# ------------- Order Resource ----------------------
api.add_resource(Hist, '/history')


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(message="Page not found."), 404


if __name__ == "__main__":
    # Configure sqlalchemy
    from db import db
    db.init_app(app)
    app.run()
