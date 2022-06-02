#!/usr/bin/env python
# -*- coding: utf-8 -*-

from D_Delivery.core.db import db
from datetime import datetime as dt


class OrdersHistoryModel(db.Model):
    __tablename__ = 'OrdersHistory'

    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    MealID = db.Column(db.Integer, nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    TransporterID = db.Column(db.Integer, nullable=False)
    OrderTime = db.Column(db.DateTime, nullable=False)
    OrderStatus = db.Column(db.Integer, nullable=False)

    SortKeys = {
        "status": OrderStatus.asc(),
        "default": OrderTime.desc(),
    }

    def __ini__(self, id, meal_id, user_id, trns_id, time, status):
        self.ID = id
        self.MealID = meal_id
        self.UserID = user_id
        self.TransporterID = trns_id
        self.OrderTime = time
        self.OrderStatus = status

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(ID=_id).first()

    @classmethod
    def find_by_user(cls, user_id, sortkey):
        return cls.query.filter_by(UserID=user_id).order_by(
            SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_meal(cls, meal_id, sortkey):
        return cls.query.filter_by(MealID=meal_id).order_by(
            SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_transporter(cls, transporter_id, sortkey):
        return cls.query.filter_by(TransporterID=transporter_id).order_by(
            SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_status(cls, status, sortkey):
        return cls.query.filter_by(OrderStatus=status).order_by(
            SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_time(cls, time, sortkey):
        return cls.query.filter_by(OrderTime=time).order_by(
            SortKeys.get(sortkey)).all()

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "ID": self.ID,
            "MealID": self.MealID,
            "UserID": self.UserID,
            "TransporterID": self.TransporterID,
            "OrderTime": str(self.OrderTime),
            "OrderStatus": self.OrderStatus
        }

    def __repr__(self):
        return f"<ID: {self.ID}, MealID: {self.MealID}, UserID: {self.UserID}, TransporterID: {self.TransporterID}, OrderTime: {self.OrderTime}, OrderStatus: {self.OrderStatus}>"
