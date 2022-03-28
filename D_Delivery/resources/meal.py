#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from models.meal import MealModel


class Meal(Resource):

    def get(self, id):
        output = []
        not_exists_msg = "Meal does not exists."
        query = MealModel.find_by_id(id)

        if not query:
            return make_response(jsonify(message=not_exists_msg), 404)
        else:
            output = query[0].serialize()
            return make_response(jsonify(meal=output), 200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name',
                            type=str,
                            required=True,
                            help="This field can't be empty.")

        parser.add_argument('Price',
                            type=int,
                            required=True,
                            help="This field can't be empty.")

        parser.add_argument('Quantity',
                            type=int,
                            required=True,
                            help="This field can't be empty.")

        parser.add_argument('Category',
                            type=str,
                            required=True,
                            help="This field can't be empty.")

        parser.add_argument('PreparingTime',
                            type=int,
                            required=True,
                            help="This field can't be empty.")

        parser.add_argument('ImgUrl',
                            type=str,
                            required=True,
                            help="This field can't be empty.")

        parser.add_argument('Rating',
                            type=float,
                            required=True,
                            help="This field can't be empty.")

        data = MealAdd.parser.parse_args()
        if MealModel.find_by_name(data['MealName']):
            return make_response(jsonify(message="Meal already exist"), 404)
        else:
            meal = MealModel(**data)
            meal.db_commit()
            return make_response(jsonify(message="Meal has been added"), 201)

    def delete(self, id):
        query = MealModel.find_by_id(id)
        if not query:
            return make_response(jsonify(message=not_exists_msg), 404)
        else:
            meal = query[0]
            meal.db_delete()
            return make_response(jsonify(message="Meal has been deleted."),
                                 200)
