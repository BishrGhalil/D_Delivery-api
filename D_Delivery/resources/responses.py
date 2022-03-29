#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, make_response


def not_exists(name):
    msg = f"{name} does not exists"
    return make_response(jsonify(message=msg), 404)


def not_authorized(msg):
    return make_response(jsonify(message=msg), 401)


def already_exists(name):
    msg = f"{name} already exists."
    return make_response(jsonify(message=msg), 208)
