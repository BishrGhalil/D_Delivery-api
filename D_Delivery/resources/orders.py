#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from D_Delivery.models.order import OrderModel
from D_Delivery.models.meal import MealModel
from D_Delivery.models.user import UserModel
from D_Delivery.resources.responses import not_exists
from datetime import datetime


class Orders(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('all', type=bool, required=False)
        parser.add_argument('User', type=int, required=False)
        parser.add_argument('Meal', type=int, required=False)
        parser.add_argument('Sortkey', type=str, required=False)

        args = parser.parse_args()
        sortkey = args.get('Sortkey') if args.get('Sortkey') else "default"
        if sortkey not in OrderModel.SortKeys: return not_exists("Sort key")
        output = []

        args = parser.parse_args()
        output = []
        query = ""
        if args.get('all'):
            query = OrderModel.find_all(sortkey)

        elif args.get('User'):
            query = OrderModel.find_by_user(args['User'], sortkey)

        elif args.get('Meal'):
            query = OrderModel.find_by_meal(args['Meal'], sortkey)

        if not query: return not_exists("Orders")
        output = [i.serialize() for i in query]
        return make_response(jsonify(orders=output), 200)
