#!/usr/bin/env python
# -*- coding: utf-8 -*-

from D_Delivery.core.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class UserModel(UserMixin, db.Model):
    __tablename__ = "Users"

    ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(45), unique=True, nullable=False)
    Password = db.Column(db.String(256), nullable=False)
    FirstName = db.Column(db.String(45), nullable=False)
    LastName = db.Column(db.String(45), nullable=False)
    Address = db.Column(db.String(45), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)

    def __init__(self, id, username, password, firstname, lastname, address,
                 phone):
        self.ID = id
        self.Username = username
        self.Password = generate_password_hash(password)
        self.FirstName = firstname
        self.LastName = lastname
        self.Address = address
        self.Phone = phone

    def get_id(self):
        return self.ID

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def fetch_by_username(cls, username):
        return cls.query.filter_by(Username=username).all()

    @classmethod
    def fetch_by_id(cls, id):
        return cls.query.filter_by(ID=id).all()

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def pass_verify(self, password):
        return check_password_hash(self.Password, password)

    def serialize(self):
        return {
            "ID": self.ID,
            "Username": self.Username,
            "Password": self.Password,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Address": self.Address,
            "Phone": self.Phone
        }
