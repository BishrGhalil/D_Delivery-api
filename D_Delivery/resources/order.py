#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from D_Delivery.models.order import OrderModel
from D_Delivery.models.meal import MealModel
from D_Delivery.models.user import UserModel
from D_Delivery.resources.responses import not_exists
from datetime import datetime


class Order(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('all', type=bool, required=False)
        parser.add_argument('ID', type=int, required=False)
        parser.add_argument('User', type=int, required=False)
        parser.add_argument('Meal', type=int, required=False)

        args = parser.parse_args()
        output = []
        query = ""
        if args.get('all'):
            query = OrderModel.find_all()

        elif args.get('User'):
            query = OrderModel.find_by_user(args['user'])

        elif args.get('Meal'):
            query = OrderModel.find_by_meal(args['meal'])

        elif args.get('ID'):
            query = OrderModel.find_by_id(args['ID'])

        if not query: return not_exists("Order")
        output = [i.serialize() for i in query]
        return make_response(jsonify(orders=output), 200)

    def post(self):
        msg = "This field can't be empty."
        parser = reqparse.RequestParser()
        parser.add_argument('OrderStatus', type=int, required=True, help=msg)
        parser.add_argument('OrderTime', type=str, required=True, help=msg)
        parser.add_argument('OrderAddress', type=str, required=True, help=msg)
        parser.add_argument('UserID', type=int, required=True, help=msg)
        parser.add_argument('MealID', type=int, required=True, help=msg)

        data = parser.parse_args()
        query = MealModel.find_by_id(data['MealID'])
        if not query: return not_exists("Meal")

        query = UserModel.find_by_id(data['UserID'])
        if not query: return not_exists("User")

        data['OrderStatus'] = OrderModel.statuses.get(data.get("OrderStatus"))

        timestamp = datetime.now()
        data['OrderTime'] = timestamp

        order = OrderModel(**data)
        order.commit()
        return make_response(jsonify(message="Order has been added"), 201)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ID', type=int, required=True)
        args = Order.parser.parse_args()

        if args.get('ID'):
            query = OrderModel.find_by_id(args['ID'])
            if not query: return not_exists("Order")
            order = query[0]
            order.delete()
            msg = "Order has been deleted."
            return make_response(jsonify(message=msg), 200)
