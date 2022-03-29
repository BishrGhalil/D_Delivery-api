#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE: Returns Status Code
# 404 Fount found, 200 Success, 201 Created (When creating something), 202 Accpeted (When delaying creation), 401 Unauthorized, 403 Forbidden

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_login import login_user, logout_user, login_required, current_user
from D_Delivery.models.user import Usermodel
from D_Delivery.resources.responses import not_exists, not_authorized, already_exists


class User(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Username", type=str, required=False, help=msg)
        parser.add_argument("ID", type=int, required=False, help=msg)
        data = parser.parse_args()

        if data.get("Username"):
            query = UserModel.find_by_username(data.get("Username"))
        elif data.get("ID"):
            query = UserModel.find_by_id(data.get("ID"))

        if not query: return not_exists("User")

        output = query[0].serialize()
        if not output: return not_exists("User")
        return make_response(jsonify(user=output), 200)

    def post(self):
        parser = reqparse.RequestParser()
        msg = "This field can't be empty."
        parser.add_argument("Username", type=str, required=True, help=msg)
        parser.add_argument("Password", type=str, required=True, help=msg)
        parser.add_argument('FirstName', type=str, required=True, help=msg)
        parser.add_argument('LastName', type=str, required=True, help=msg)
        parser.add_argument('Address', type=str, required=False, help=msg)
        parser.add_argument('Phone', type=str, required=False, help=msg)

        data = User.parser.parse_args()

        if UserModel.find_by_username(data['Username']):
            return already_exists("User")

        else:
            user = UserModel(data.get('Username'), data.get('Password'),
                             data.get('FirstName'), data.get('LastName'),
                             data.get('Address'), data.get('Phone'))

            user.commit()
            return make_response(jsonify(message="User has been added."), 201)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("ID", type=int, required=True, help=msg)
        msg = "This field can't be empty."

        args = User.parser.parse_args()
        query = UserModel.find_by_id(args['ID'])
        if not query: return not_exists("User")
        user = query[0]
        user.delete()
        msg = "User has been deleted"
        return make_response(jsonify(message=msg), 200)


class Login(Resource):

    def post(self):
        msg = "This field can't be empty."
        parser = reqparse.RequestParser()
        parser.add_argument('Username', type=str, required=True, help=msg)
        parser.add_argument('Password', type=str, required=True, help=msg)

        data = User.parser.parse_args()
        username = data.get("Username")
        password = data.get("Password")
        query = UserModel.find_by_username(username)
        if not query: return not_authorized("Not a valid Username")

        user = query[0]
        if not user.pass_verify(password):
            return not_authorized("Not a valid password")

        login_user(user, remember=True)
        if not current_user.is_authenticated:
            return not_authorized("Not logged in")

        msg = f"Logged in as {current_user.Username}."
        return make_response(jsonify(message=msg), 200)


class Logout(Resource):

    def get(self):
        if not current_user.is_authenticated:
            return not_authorized("Not logged in.")

        logout_user()
        return make_response(jsonify(message="Logged out."), 200)


class Wloggedin(Resource):

    def get(self):
        if not current_user.is_authenticated:
            return not_authorized("Not logged in.")

        msg = f"username:{current_user.Username}, id:{current_user.UserID}, password:{current_user.Password}"
        return make_response(jsonify(message=msg), 200)
