#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from D_Delivery.models.meal import MealModel
from D_Delivery.resources.responses import not_exists


class Meals(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('all', type=bool, required=False)
        parser.add_argument('Category', type=str, required=False)
        parser.add_argument('Price', type=float, required=False)
        parser.add_argument('PreparingTime', type=int, required=False)
        parser.add_argument('Rating', type=float, required=False)
        parser.add_argument('Sortkey', type=str, required=False)

        args = parser.parse_args()
        sortkey = args.get('Sortkey') if args.get('Sortkey') else "default"
        output = []

        if sortkey not in MealModel.SortKeys: return not_exists("Sort key")

        if args.get('all'):
            query = MealModel.find_all(sortkey)
            output = [i.serialize() for i in query]

        else:
            if args.get('Category'):
                query = MealModel.find_by_category(args['Category'], sortkey)
                output.extend([i.serialize() for i in query])

            if args.get('Price'):
                query = MealModel.find_by_price(args['Price'], sortkey)
                output.extend([i.serialize() for i in query])

            if args.get('Rating'):
                query = MealModel.find_by_rating(args['Rating'], sortkey)
                output.extend([i.serialize() for i in query])

            if args.get('PreparingTime'):
                query = MealModel.find_by_time(args['PreparingTime'], sortkey)
                output.extend([i.serialize() for i in query])

        if not output: return not_exists("Meals")
        return make_response(jsonify(meals=output), 200)
