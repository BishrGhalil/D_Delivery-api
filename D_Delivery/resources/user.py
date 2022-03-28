#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE: Returns Status Code
# 404 Fount found, 200 Success, 201 Created (When creating something), 202 Accpeted (When delaying creation), 401 Unauthorized, 403 Forbidden

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_login import login_user, logout_user, login_required, current_user
from D_Delivery.models.user import Usermodel


class User(Resource):

    def get(self, id):
        output = []
        query = UserModel.find_by_id(id)
        not_exists_msg = "User does not exists."
        if not query:
            return make_response(jsonify(message=not_exists_msg), 404)

        else:
            output = query[0].serialize()
            if not output:
                return make_response(jsonify(message=not_exists_msg), 404)

            else:
                return make_response(jsonify(user=output), 200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Username",
                            type=str,
                            required=True,
                            help="This field can't be empty")

        parser.add_argument("Password",
                            type=str,
                            required=True,
                            help="This field can't be empty")

        parser.add_argument('FirstName',
                            type=str,
                            required=True,
                            help="This field can't be empty")

        parser.add_argument('LastName',
                            type=str,
                            required=True,
                            help="This field can't be empty")

        parser.add_argument('Address',
                            type=str,
                            required=False,
                            help="This field can't be empty")

        parser.add_argument('Phone',
                            type=str,
                            required=False,
                            help="This field can't be empty")

        data = User.parser.parse_args()

        if UserModel.find_by_username(data['Username']):
            return make_response(jsonify(message="User already exist."), 404)

        else:
            user = UserModel(data.get('Username'), data.get('Password'),
                             data.get('FirstName'), data.get('LastName'),
                             data.get('Address'), data.get('Phone'))

            user.commit()
            return make_response(jsonify(message="User has been added."), 201)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Username",
                            type=str,
                            required=True,
                            help="This field can't be empty")

        args = User.parser.parse_args()
        if args.get('UserID'):
            query = UserModel.find_by_id(args['UserID'])
            if not query:
                return make_response(jsonify(message=not_exists_msg), 404)

            else:
                user = query[0]
                user.delete()
                msg = "User has been deleted"
                return make_response(jsonify(message=msg), 200)


class Login(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Username',
                            type=str,
                            required=True,
                            help="This field can't be empty.")

        parser.add_argument('Password',
                            type=str,
                            required=True,
                            help="This field can't be empty.")

        data = User.parser.parse_args()
        query = UserModel.find_by_username(data['Username'])
        if not query:
            msg = "Not a valid Username, User does not exists."
            return make_response(jsonify(message=msg), 401)

        else:
            user = query[0]
            if not user.pass_verify(data.get('Password')):
                msg = "Password is not correct."
                return make_response(jsonify(message=msg), 401)

            else:
                login_user(user, remember=True)
                if not current_user.is_authenticated:
                    msg = "Not logged in."
                    make_response(jsonify(message=msg), 401)

                else:
                    msg = f"Logged in as {current_user.Username}."
                    return make_response(jsonify(message=msg), 200)


class Logout(Resource):

    def get(self):
        if not current_user.is_authenticated:
            return make_response(jsonify(message="Not logged in."), 401)
        logout_user()
        return make_response(jsonify(message="Logged out."), 200)


class Wloggedin(Resource):

    def get(self):
        if not current_user.is_authenticated:
            return make_response(jsonify(message="Not logged in."), 401)

        msg = f"username:{current_user.Username}, id:{current_user.UserID}, password:{current_user.Password}"
        return make_response(jsonify(message=msg), 200)
