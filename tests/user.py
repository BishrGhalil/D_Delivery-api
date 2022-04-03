#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import unittest

URL = "http://127.0.0.1:5000/user"

OldUsers = [{
    "Username": "BishrGhalil",
    "Password": "0000",
    "FirstName": "Bishr",
    "LastName": "Gha",
    "Address": "Syria, Latkia",
    "Phone": "099090",
}, {
    "Username": "BishrGhalil2",
    "Password": "0000",
    "FirstName": "Bishr",
    "LastName": "Gha",
    "Address": "Syria, Latkia",
    "Phone": "099090",
}]

NewUsers = [{
    "Username": "Emad12",
    "Password": "0000",
    "FirstName": "Emad",
    "LastName": "Moh",
    "Address": "Syria, Latkia",
    "Phone": "0999999",
}, {
    "Username": "Bemo",
    "Password": "1111",
    "FirstName": "Bayan",
    "LastName": "Ibr",
    "Address": "Syria, Latkia",
    "Phone": "09101010",
}]

OldUsersUsernames = [User.get("Username") for User in OldUsers]
NewUsersUsernames = [User.get("Username") for User in NewUsers]


def get_by_id(id):
    PARAMS = {"ID": id}
    res = requests.get(url=URL, params=PARAMS)
    return res.json(), res.status_code


def get_by_username(username):
    PARAMS = {"Username": username}
    res = requests.get(url=URL, params=PARAMS)
    return res.json(), res.status_code


def get_all():
    PARAMS = {"all": True}
    res = requests.get(url=URL, params=PARAMS)
    return res.json(), res.status_code


def NewUsersIDs():
    return [
        User.get("ID") for User in get_users_by_username(NewUsersUsernames)
    ]


def OldUsersIDs():
    return [
        User.get("ID") for User in get_users_by_username(OldUsersUsernames)
    ]


def post_user(Username, Password, FirstName, LastName, Address, Phone):
    data = {
        "Username": Username,
        "Password": Password,
        "FirstName": FirstName,
        "LastName": LastName,
        "Address": Address,
        "Phone": Phone
    }
    res = requests.post(url=URL, data=data)
    return res.json(), res.status_code


def del_by_username(username):
    PARAMS = {"Username": username}
    res = requests.delete(url=URL, params=PARAMS)
    return res.json(), res.status_code


def post_old_users():
    for User in OldUsers:
        data, code = post_user(**User)


def del_users():
    PARAMS = {"all": True}
    res = requests.delete(url=URL, params=PARAMS)
    return res.json(), res.status_code


class TestGetRequests(unittest.TestCase):

    def setUp(self):
        del_users()
        post_old_users()

    def test_getNotExistsByUsername(self):
        username = NewUsers[0].get('Username')
        user, code = get_by_username(username)
        user = user.get("user")
        self.assertEqual(code, 404)
        self.assertFalse(user)

    def test_getExistsByUsername(self):
        olduser = OldUsers[0]
        username = olduser.get('Username')
        user, code = get_by_username(username)
        user = user.get("user")
        self.assertEqual(code, 200)
        self.assertEqual(olduser.get("Username"), user.get("Username"))

    def test_getExistsById(self):
        olduser = OldUsers[0]
        username = olduser.get('Username')
        user, code = get_by_username(username)
        user = user.get("user")
        self.assertEqual(code, 200)
        user, code = get_by_id(user.get("ID"))
        user = user.get("user")
        self.assertEqual(code, 200)
        self.assertEqual(olduser.get("Username"), user.get("Username"))

    def test_getNotExistsById(self):
        user, code = get_by_id(82390482093)
        user = user.get("user")
        self.assertEqual(code, 404)
        self.assertFalse(user)

    def test_getAll(self):
        users, code = get_all()
        self.assertEqual(code, 200)
        for user in users.get("users"):
            self.assertIn(user.get("Username"),
                          OldUsersUsernames + NewUsersUsernames)


class TestDeleteRequest(unittest.TestCase):

    def setUp(self):
        post_old_users()

    def test_deleteExistsByUsername(self):
        username = OldUsers[1].get("Username")
        data, code = del_by_username(username)
        self.assertEqual(code, 200)

    def test_deleteNotExistsByUsername(self):
        username = NewUsers[1].get("Username")
        data, code = del_by_username(username)
        self.assertEqual(code, 404)


class TestPostRequest(unittest.TestCase):

    def setUp(self):
        del_users()

    def test_postExistsUser(self):
        user = OldUsers[0]
        data, code = post_user(**user)
        self.assertEqual(code, 208)

    def test_postNotExistsUser(self):
        user = NewUsers[0]
        data, code = post_user(**user)
        self.assertEqual(code, 201)


if __name__ == '__main__':
    data, code = del_users()
    post_old_users()
    unittest.main()
