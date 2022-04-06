#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from D_Delivery.models.meal import MealModel
from D_Delivery.resources.responses import not_exists, already_exists


class Meal(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, required=False)
        parser.add_argument('ID', type=str, required=False)

        output = []
        data = parser.parse_args()
        query = ""

        if data.get("ID"):
            query = MealModel.find_by_id(data.get("ID"))
        elif data.get("Name"):
            query = MealModel.find_by_name(data.get("Name"))

        if not query: return not_exists("Meal")
        output = query.serialize()
        return make_response(jsonify(meal=output), 200)

    def post(self):
        msg = "This field can't be empty."
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, required=True, help=msg)
        parser.add_argument('Price', type=int, required=True, help=msg)
        parser.add_argument('Quantity', type=int, required=True, help=msg)
        parser.add_argument('Category', type=str, required=True, help=msg)
        parser.add_argument('PreparingTime', type=int, required=True, help=msg)
        parser.add_argument('ImgUrl', type=str, required=True, help=msg)
        parser.add_argument('Rating', type=float, required=True, help=msg)

        data = parser.parse_args()
        if MealModel.find_by_name(data['Name']):
            return already_exists("Meal")

        meal = MealModel(**data)
        meal.commit()
        return make_response(jsonify(message="Meal has been added"), 201)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, required=False)
        parser.add_argument('ID', type=int, required=False)

        args = parser.parse_args()
        if args.get("Name"):
            query = MealModel.find_by_name(args.get("Name"))
            if not query: return not_exists("Meal")
            meal = query
            meal.delete()

        elif args.get("ID"):
            query = MealModel.find_by_id(args.get("ID"))
            if not query: return not_exists("Meal")
            meal = query
            meal.delete()

        msg = "Meal has been deleted."
        return make_response(jsonify(message=msg), 200)
