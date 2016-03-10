#!/usr/bin/env python

"""Helper class for the vk module"""

import configparser
import vk

__author__ = 'Dslt'
__status__ = "Prototype"


class VkHelper:
    TOKEN_FILE = "token"

    def __init__(self):
        self.token = self.get_token_from_file()
        self.session = self.get_session()
        self.api = self.get_api()
        if not self.test_query():
            self.token = self.get_new_token()
            self.save_token_to_file()
            self.session = self.get_session()
            self.api = self.get_api()

    def get_vk_api(self):
        return self.api

    def get_api_configuration(self):
        config = configparser.ConfigParser()
        config.read("vk_helper.ini")
        if 'API Data' in config:
            return config['API Data']
        else:
            return None

    def get_new_token(self):
        global user_password
        config = self.get_api_configuration()
        if config:
            user_password = input("Input pass: ")
        else:
            # TODO: Custom exceptions
            raise NameError('There is no config file!')
        # scope="messages, friends"
        # TODO: exceptions handling!
        session = vk.AuthSession(app_id=config['app_id'], user_login=config['user_login'], user_password=user_password,
                                 scope="friends, groups")
        return session.get_access_token()

    def check_session(self):
        if self.session is None:
            print("Can't do query due to empty session!")

    def get_api(self, session=None):
        if session is None:
            session = self.session
        return vk.API(session)

    def get_session(self, token=None):
        if token is None:
            token = self.token
        return vk.Session(access_token=token)

    def save_token_to_file(self, token=None):
        if token is None:
            token = self.token
        with open(self.TOKEN_FILE, "w+") as file:
            file.write(token)

    def get_token_from_file(self):
        with open(self.TOKEN_FILE, "r") as file:
            token = file.readline()
        return token

    def test_query(self):
        self.check_session()

        try:
            self.api.users.get()
        except vk.exceptions.VkAPIError:
            return False

        return True
