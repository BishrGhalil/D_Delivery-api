#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource


class Root(Resource):

    def get(self):
        return "Hello, Qubit!", 200
