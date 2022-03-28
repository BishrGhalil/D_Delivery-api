#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from models.mealmodel import MealModel


class Meals(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('all', type=bool, required=False)
        parser.add_argument('category', type=str, required=False)
        parser.add_argument('price', type=int, required=False)
        parser.add_argument('ptime', type=int, required=False)
        parser.add_argument('rating', type=float, required=False)
        parser.add_argument('sortkey', type=str, required=False)

        args = Meals.parser.parse_args()
        output = []
        sortkey = args.get('sortkey') if args.get('sortkey') else "default"

        if not MealModel.SortKeys.get(sortkey):
            msg = "Not a valid sortkey."
            return make_response(jsonify(message=msg), 404)

        if args.get('all'):
            query = MealModel.find_all(sortkey)
            output = [i.serialize() for i in query]
            if not output:
                msg = "No Meals"
                return make_response(jsonify(message=msg), 404)
            else:
                return make_response(jsonify(meals=output), 200)

        if args.get('category'):
            query = MealModel.find_by_cat(args['category'], sortkey)
            output.extend([i.serialize() for i in query])

        if args.get('price'):
            query = MealModel.find_by_price(args['price'], sortkey)
            output.extend([i.serialize() for i in query])

        if args.get('rating'):
            query = MealModel.find_by_rating(args['rating'], sortkey)
            output.extend([i.serialize() for i in query])

        if args.get('ptime'):
            query = MealModel.find_by_ptime(args['ptime'], sortkey)
            output.extend([i.serialize() for i in query])

        if not output:
            msg = "No Meals"
            return make_response(jsonify(message=msg), 404)

        else:
            return make_response(jsonify(meals=output), 200)
