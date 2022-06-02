#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

creation_script = """
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "Users" (
  ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  Username  TEXT NOT NULL UNIQUE,
  Password TEXT NOT NULL,
  FirstName TEXT NOT NULL,
  LastName TEXT NOT NULL,
  Address TEXT NOT NULL,
  Phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Transporters" (
  ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  Username  TEXT NOT NULL UNIQUE,
  FirstName TEXT NOT NULL,
  LastName TEXT NOT NULL,
  Phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Meals" (
  ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  Quantity TEXT NOT NULL,
  Category TEXT NOT NULL,
  PreparingTime INTEGER NOT NULL,
  Price FLOAT NOT NULL,
  Rating FLOAT NOT NULL,
  ImgUrl TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Orders" (
  ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  OrderStatus INTEGER NOT NULL,
  OrderTime DATETIME NOT NULL,
  OrderAddress TEXT NOT NULL,
  UserID INTEGER NOT NULL,
  MealID INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "OrdersHistory" (
  ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  OrderTime DATETIME NOT NULL,
  OrderStatus INTEGER NOT NULL,
  MealID INTEGER NOT NULL,
  UserID INTEGER NOT NULL,
  TransporterID INTEGER NOT NULL
);

COMMIT;
"""
