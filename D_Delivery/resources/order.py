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
        parser.add_argument('ID', type=int, required=True)

        args = parser.parse_args()
        output = []

        args = parser.parse_args()
        output = []
        query = ""
        query = OrderModel.find_by_id(args['ID'])
        if not query: return not_exists("Order")
        output = query[0].serialize()
        return make_response(jsonify(order=output), 200)

    def post(self):
        msg = "This field can't be empty."
        parser = reqparse.RequestParser()
        parser.add_argument('Status', type=str, required=True, help=msg)
        parser.add_argument('Time', type=str, required=True, help=msg)
        parser.add_argument('Address', type=str, required=True, help=msg)
        parser.add_argument('User', type=int, required=True, help=msg)
        parser.add_argument('Meal', type=int, required=True, help=msg)

        data = parser.parse_args()
        query = MealModel.find_by_id(data['Meal'])
        if not query: return not_exists("Meal")

        query = UserModel.find_by_id(data['User'])
        if not query: return not_exists("User")

        status = OrderModel.statuses.get(data.get("Status"))
        if not status: return not_exists("Status")
        data['Status'] = status

        timestamp = datetime.now()
        data['Time'] = timestamp

        order = OrderModel(**data)
        order.commit()
        return make_response(jsonify(message="Order has been added"), 201)

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ID', type=int, required=True)
        args = parser.parse_args()

        if args.get('ID'):
            query = OrderModel.find_by_id(args['ID'])
            if not query: return not_exists("Order")
            order = query[0]
            order.cancel()
            msg = "Order has been cancelled."
            return make_response(jsonify(message=msg), 200)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ID', type=int, required=True)
        args = parser.parse_args()

        if args.get('ID'):
            query = OrderModel.find_by_id(args['ID'])
            if not query: return not_exists("Order")
            order = query[0]
            order.delete()
            msg = "Order has been deleted."
            return make_response(jsonify(message=msg), 200)
