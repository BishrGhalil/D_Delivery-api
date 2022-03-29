#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from D_Delivery.models.transporter import TransporterModel
from D_Delivery.resources.responses import not_exists, already_exists


class Transporter(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('all', type=bool, required=False)
        parser.add_argument('ID', type=int, required=False)
        parser.add_argument('Username', type=str, required=False)
        args = parser.parse_args()

        output = []
        if args.get('all'):
            query = TransporterModel.find_all()
            if not query: return not_exists("Transporter")
            output = [i.serialize() for i in query]
            return make_response(jsonify(transporter=output), 200)

        elif args.get('ID'):
            query = TransporterModel.find_by_id(args['ID'])
            if not query: return not_exists("Transporter")
            output = query[0].serialize()
            return make_response(jsonify(transporter=output), 200)

    def post(self):
        msg = "This field can't be empty."
        parser = reqparse.RequestParser()
        parser.add_argument('Username', type=str, required=True, help=msg)
        parser.add_argument('FirstName', type=str, required=True, help=msg)
        parser.add_argument('LastName', type=str, required=True, help=msg)
        parser.add_argument('Phone', type=str, required=True, help=msg)

        data = parser.parse_args()
        if TransporterModel.find_by_username(data['Username']):
            return already_exists("Transporter")

        trans = TransporterModel(data.get('Username'), data.get('FirstName'),
                                 data.get('LastName'), data.get('Phone'))
        trans.commit()
        msg = "Transporter has been added."
        return make_response(jsonify(message=msg), 201)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ID', type=int, default=False, required=False)
        args = parser.parse_args()
        if args.get('ID'):
            query = TransporterModel.find_by_id(args['ID'])
            if not query: return not_exists("Transporter")
            trans = query[0]
            trans.delete()
            msg = "Transporter has been deleted."
            return make_response(jsonify(message=msg), 200)
