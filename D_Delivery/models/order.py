#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db


class OrderModel(db.Model):
    __tablename__ = 'Orders'

    ID = db.Column(db.Integer, primary_key=True)
    OrderStatus = db.Column(db.Integer, nullable=False)
    OrderTime = db.Column(db.DateTime, nullable=False)
    DestinationAddress = db.Column(db.String, nullable=False)
    UserID = db.Column(db.Integer, foreign_key=True, nullable=False)
    MealID = db.Column(db.Integer, foreign_key=True, nullable=False)

    STATUS_WAITING = 0
    STATUS_DONE = 1
    STATUS_CANCELLED = 2

    DefaultSortKey = OrderTime.desc()

    def __ini__(self, id, status, time, address, user_id, meal_id):
        self.ID = id
        self.OrderStatus = status
        self.OrderTime = time
        self.DestinationAddress = address
        self.UserID = user_id
        self.MealID = meal_id

    @classmethod
    def find_all(cls, sortkey=OrderModel.DefaultSortKey):
        return cls.query.order_by(sortkey).all()

    @classmethod
    def find_by_id(cls, id, sortkey=OrderModel.DefaultSortKey):
        return cls.query.filter_by(OrderID=_id).order_by(sortkey).all()

    @classmethod
    def find_by_user(cls, id, sortkey=OrderModel.DefaultSortKey):
        return cls.query.filter_by(UserID=_id).order_by(sortkey).all()

    @classmethod
    def find_by_meal(cls, id, sortkey=OrderModel.DefaultSortKey):
        return cls.query.filter_by(MealID=_id).order_by(sortkey).all()

    @classmethod
    def find_by_destination(cls, dest_id, sortkey=OrderModel.DefaultSortKey):
        return cls.query.filter_by(
            DestinationAddress=dest_id).order_by(sortkey).all()

    def db_commit(self):
        db.session.add(self)
        db.session.commit()

    def db_delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "ID": self.ID,
            "OrderStatus": self.OrderStatus,
            "OrderTime": self.OrderTime,
            "DestinationAddress": self.DestinationAddress,
            "UserID": self.UserID,
            "MealID": self.MealID
        }

    def __repr__(self):
        return f"<ID: {self.ID}, OrderStatus: {self.OrderStatus}, OrderTime: {self.OrderTime}, DestinationAddress: {self.DestinationAddress}, UserID: {self.UserID}, MealID: {self.MealID}>"
