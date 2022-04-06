#!/usr/bin/env python
# -*- coding: utf-8 -*-

from D_Delivery.core.db import db
from datetime import datetime as dt


class MealModel(db.Model):
    __tablename__ = "Meals"

    ID = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,
                   nullable=False)
    Name = db.Column(db.String(45), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    PreparingTime = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Float, nullable=False)
    Category = db.Column(db.String(45), nullable=False)
    Rating = db.Column(db.Float, nullable=False)
    ImgUrl = db.Column(db.String(300), nullable=False)

    SortKeys = {
        "name": Name.asc(),
        "category": Category.asc(),
        "price": Price.asc(),
        "rating": Rating.desc(),
        "preparetime": PreparingTime.asc(),
        "default": Rating.desc()
    }

    def __ini__(self, id, name, quantity, preparing_time, price, category,
                img_url, rating):
        self.ID = id
        self.Name = name
        self.Quantity = quantity
        self.PreparingTime = preparing_time
        self.Price = price
        self.Category = category
        self.Rating = rating
        self.ImgUrl = img_url

    @classmethod
    def fetch_all(cls, sortkey):
        return cls.query.order_by(SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(Name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(ID=id).first()

    @classmethod
    def find_by_category(cls, category, sortkey):
        return cls.query.filter_by(Category=category).order_by(
            SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_price(cls, price, sortkey):
        return cls.query.filter_by(Price=price).order_by(
            SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_rating(cls, rating, sortkey):
        return cls.query.filter_by(Rating=rating).order_by(
            SortKeys.get(sortkey)).all()

    @classmethod
    def find_by_time(cls, preparing_time, sortkey):
        return cls.query.filter_by(PreparingTime=preparing_time).order_by(
            SortKeys.get(sortkey)).all()

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            'ID': self.ID,
            'Name': self.Name,
            'Quantity': self.Quantity,
            'PreparingTime': self.PreparingTime,
            'Price': self.Price,
            'Category': self.Category,
            'Rating': self.Rating,
            'ImgUrl': self.ImgUrl
        }

    def __repr__(self):
        return f"<ID: {self.ID}, Name: {self.Name}, Quantity: {self.Quantity}, PreparingTime: {self.PreparingTime}, Price: {self.Price}, Category: {self.Category}, Rating: {self.Rating}, ImgUrl: {self.ImgUrl}>"
