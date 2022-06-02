#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from flask import Flask, jsonify, request
from flask_login import LoginManager, login_user, current_user, login_required
from flask_restful import Api, Resource

from D_Delivery.models.user import UserModel
from D_Delivery.resources.history import History
from D_Delivery.resources.meal import Meal
from D_Delivery.resources.meals import Meals
from D_Delivery.resources.order import Order
from D_Delivery.resources.orders import Orders
from D_Delivery.resources.home import Home
from D_Delivery.resources.transporter import Transporter
from D_Delivery.resources.user import User, Login, Logout, Wloggedin
from D_Delivery.core.db import db, creation_script

# sec is a python file contain {key, db_user, db_key}
from D_Delivery.core.sec import sec

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
login_manager = LoginManager(app)
login_manager.init_app(app)


def create_database():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.executescript(creation_script)


def main():
    create_database()
    api.add_resource(Home, '/')
    # Configure flask login

    # ------------- Meal Resource ----------------------
    api.add_resource(Meal, '/meal')

    # ------------- Meals Resource ----------------------
    api.add_resource(Meals, '/meals')

    # ------------- User Resource ----------------------
    api.add_resource(User, '/user')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(Wloggedin, '/wloggedin')

    # ------------- Transporter Resource ----------------------
    api.add_resource(Transporter, '/transporter')

    # ------------- Order Resource ----------------------
    api.add_resource(Order, '/order')
    api.add_resource(Orders, '/orders')

    # ------------- Order Resource ----------------------
    api.add_resource(History, '/history')

    # Configure sqlalchemy
    db.init_app(app)
    app.run()


@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(message="Page not found."), 404
