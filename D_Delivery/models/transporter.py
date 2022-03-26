#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db


class TransporterModel(db.Model):
    __tablename__ = 'Transporters'

    ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), unique=True, nullable=False)
    FirstName = db.Column(db.String(45), nullable=False)
    LastName = db.Column(db.String(45), nullable=False)
    Phone = db.Column(db.String(10), nullable=False)

    DefaultSortKey = Username

    def __init__(self, id, username, firstname, lastname, phone):
        self.ID = id
        self.Username = username
        self.FirstName = firstname
        self.LastName = lastname
        self.Phone = phone

    @classmethod
    def find_all(cls, sortkey=TransporterModel.DefaultSortKey):
        return cls.query.order_by(sortkey).all()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(Username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(ID=id).first()

    def db_commit(self):
        db.session.add(self)
        db.session.commit()

    def db_delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            'ID': self.ID,
            'Username': self.Username,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Phone': self.Phone,
        }

    def __repr__(self):
        return f"<ID: {self.ID}, Username: {self.Username}, FirstName: {self.FirstName}, LastName: {self.LastName}, Phone: {self.Phone}>"
