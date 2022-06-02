#!/usr/bin/env python
# -*- coding: utf-8 -*-

from D_Delivery.core.db import db


class OrderModel(db.Model):
    __tablename__ = 'Orders'

    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Status = db.Column(db.Integer, nullable=False)
    Time = db.Column(db.DateTime, nullable=False)
    Address = db.Column(db.String, nullable=False)
    User = db.Column(db.Integer, nullable=False)
    Meal = db.Column(db.Integer, nullable=False)

    STATUS_WAITING = 1
    STATUS_DONE = 2
    STATUS_CANCELLED = 3

    statuses = {
        "waiting": STATUS_WAITING,
        "done": STATUS_DONE,
        "cancelled": STATUS_CANCELLED
    }

    SortKeys = {
        "status": Status.asc(),
        "time": Time.asc(),
        "default": Time.asc(),
    }

    def __ini__(self, id, status, time, address, user_id, meal_id):
        self.ID = id
        self.Status = status
        self.Time = time
        self.Address = address
        self.User = user_id
        self.Meal = meal_id

    @classmethod
    def find_all(cls, sortkey):
        return cls.query.order_by(cls.SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(ID=id).all()

    @classmethod
    def find_by_user(cls, id, sortkey):
        return cls.query.filter_by(User=id).order_by(
            cls.SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_meal(cls, id, sortkey):
        return cls.query.filter_by(Meal=id).order_by(
            cls.SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_destination(cls, dest_id, sortkey):
        return cls.query.filter_by(Address=dest_id).order_by(
            cls.SortKeys.get(sortkey)).all()

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def cancel(self):
        self.Status = self.STATUS_CANCELLED
        self.commit()

    def done(self):
        self.Status = self.STATUS_DONE
        self.commit()

    def get_status_string(self, status):
        for key, value in self.statuses.items():
            if value == status: return key

    def serialize(self):
        return {
            "ID": self.ID,
            "Status": self.get_status_string(self.Status),
            "Time": self.Time,
            "Address": self.Address,
            "User": self.User,
            "Meal": self.Meal
        }

    def __repr__(self):
        return f"<ID: {self.ID}, Status: {self.Status}, Time: {self.Time}, Address: {self.Address}, User: {self.User}, Meal: {self.Meal}>"
