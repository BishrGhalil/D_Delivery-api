#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import unittest

URL = "http://127.0.0.1:5000/meal"

OldMeals = [{
    "Name": "Tacko Wite Souce",
    "Price": 10,
    "Quantity": 9,
    "Category": "meat",
    "PreparingTime": 8,
    "ImgUrl": "https://SomePhotoUrl.com",
    "Rating": 9.3,
}, {
    "Name": "French Rice",
    "Price": 29,
    "Quantity": 30,
    "Category": "rice",
    "PreparingTime": 10,
    "ImgUrl": "https://SomePhotoUrl.com",
    "Rating": 7.0,
}]

NewMeals = [{
    "Name": "Pasta White Souce",
    "Price": 10,
    "Quantity": 100,
    "Category": "pasta",
    "PreparingTime": 8,
    "ImgUrl": "https://SomePhotoUrl.com",
    "Rating": 9.8,
}, {
    "Name": "Pasta Italiano",
    "Price": 10,
    "Quantity": 20,
    "Category": "pasta",
    "PreparingTime": 9,
    "ImgUrl": "https://SomePhotoUrl.com",
    "Rating": 9.8,
}]

OldMealsNames = [Meal.get("Name") for Meal in OldMeals]
NewMealsNames = [Meal.get("Name") for Meal in NewMeals]


def get_by_id(id):
    PARAMS = {"ID": id}
    res = requests.get(url=URL, params=PARAMS)
    return res.json(), res.status_code


def get_by_name(mealname):
    PARAMS = {"Name": mealname}
    res = requests.get(url=URL, params=PARAMS)
    return res.json(), res.status_code


def post_meal(Name, Price, Quantity, Category, PreparingTime, ImgUrl, Rating):
    data = {
        "Name": Name,
        "Price": Price,
        "Quantity": Quantity,
        "Category": Category,
        "PreparingTime": PreparingTime,
        "ImgUrl": ImgUrl,
        "Rating": Rating
    }
    res = requests.post(url=URL, data=data)
    return res.json(), res.status_code


def del_by_name(mealname):
    PARAMS = {"Name": mealname}
    res = requests.delete(url=URL, params=PARAMS)
    return res.json(), res.status_code


def post_old_meals():
    for Meal in OldMeals:
        data, code = post_meal(**Meal)


class TestGetRequests(unittest.TestCase):

    def setUp(self):
        post_old_meals()

    def test_getNotExistsByName(self):
        mealname = NewMeals[0].get('Name')
        meal, code = get_by_name(mealname)
        meal = meal.get("meal")
        self.assertEqual(code, 404)
        self.assertFalse(meal)

    def test_getExistsByName(self):
        oldmeal = OldMeals[0]
        mealname = oldmeal.get('Name')
        meal, code = get_by_name(mealname)
        meal = meal.get("meal")
        self.assertEqual(code, 200)
        self.assertEqual(oldmeal.get("Name"), meal.get("Name"))

    def test_getExistsById(self):
        oldmeal = OldMeals[0]
        mealname = oldmeal.get('Name')
        meal, code = get_by_name(mealname)
        meal = meal.get("meal")
        self.assertEqual(code, 200)
        meal, code = get_by_id(meal.get("ID"))
        meal = meal.get("meal")
        self.assertEqual(code, 200)
        self.assertEqual(oldmeal.get("Name"), meal.get("Name"))

    def test_getNotExistsById(self):
        meal, code = get_by_id(82390482093)
        meal = meal.get("meal")
        self.assertEqual(code, 404)
        self.assertFalse(meal)


class TestDeleteRequest(unittest.TestCase):

    def setUp(self):
        post_old_meals()

    def test_deleteExistsByName(self):
        mealname = OldMeals[1].get("Name")
        data, code = del_by_name(mealname)
        self.assertEqual(code, 200)

    def test_deleteNotExistsByName(self):
        mealname = NewMeals[0].get("Name")
        data, code = del_by_name(mealname)
        self.assertEqual(code, 404)


class TestPostRequest(unittest.TestCase):

    def setUp(self):
        pass

    def test_postExistsMeal(self):
        meal = OldMeals[0]
        data, code = post_meal(**meal)
        self.assertEqual(code, 208)

    def test_postNotExistsMeal(self):
        meal = NewMeals[1]
        data, code = post_meal(**meal)
        self.assertEqual(code, 201)


if __name__ == '__main__':
    post_old_meals()
    unittest.main()
