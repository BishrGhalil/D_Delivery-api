from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from D_Delivery.models.meal import MealModel
from D_Delivery.models.user import UserModel
from D_Delivery.models.transporter import TransModel
from D_Delivery.models.history import OrdersHistoryModel
from D_Delivery.resources.responses import not_exists, already_exists
from datetime import datetime


class History(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('all', type=bool, required=False)
        parser.add_argument('ID', type=int, required=False)
        parser.add_argument('User', type=int, required=False)
        parser.add_argument('Meal', type=int, required=False)
        parser.add_argument('Transporter', type=int, required=False)

        args = parser.parse_args()
        Output = []
        if args.get('all'):
            query = OrdersHistoryModel.find_all()
            if not query: return not_exists("Order")
            Output = [i.serialize() for i in query]

        else:
            if args.get('User'):
                query = OrdersHistoryModel.find_by_user(args['User'])
                Output.extend([i.serialize() for i in query])

            if args.get('Meal'):
                query = OrdersHistoryModel.find_by_meal(args['Meal'])
                Output.extend([i.serialize() for i in query])

            if args.get('Transporter'):
                query = OrdersHistoryModel.find_by_transporter(
                    args['Transporter'])
                Output.extend([i.serialize() for i in query])

            if args.get('ID'):
                query = OrdersHistoryModel.find_by_id(args['ID'])
                Output = query[0].serialize() if query else None

        if not Output: return not_exists("Order")
        return make_response(jsonify(history=Output), 200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('OrderStatus', type=int, required=True)
        parser.add_argument('OrderTime', type=str, required=True)
        parser.add_argument('TransporterID', type=int, required=True)
        parser.add_argument('UserID', type=int, required=True)
        parser.add_argument('MealID', type=int, required=True)

        data = parser.parse_args()
        query = MealModel.find_by_id(data['MealID'])
        if not query: return not_exists("Meal")

        query = UserModel.find_by_id(data['UserID'])
        if not query: return not_exists("User")

        query = TransModel.find_by_id(data['TransporterID'])
        if not query: return not_exists("Transporter")

        hist = OrdersHistoryModel(**data)
        hist.commit()
        return make_response(
            jsonify(message="Order has been added to the history."), 200)

    def delete(self):
        parser.add_argument('ID', type=int, required=False)
        args = parser.parse_args()

        if args.get('ID'):
            query = OrdersHistoryModel.find_by_id(args['ID'])
            if not query: return not_exists("Order")
            order = query[0]
            order.delete()
            msg = "Order has been deleted."
            return make_response(jsonify(message=msg), 200)
