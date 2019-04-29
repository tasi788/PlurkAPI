__author__ = '@DingChen_Tsai'
import re
import time
import json

from urllib.parse import urlparse, parse_qs

from dateutil import tz
from datetime import datetime, timedelta

import oauth2 as oauth

import requests
from requests_oauthlib import OAuth1


def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    '''
    plurk id encode
    '''
    if not isinstance(number, (int, float)):
        raise TypeError('number must be an integer')
    base36 = ''
    sign = ''
    if number < 0:
        sign = '-'
        number = -number
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36
    return sign + base36


def base36decode(number):
    '''
    plurk id encode
    '''
    return int(number, 36)


class plurkapi:
    def __init__(self, app_key, app_secret):
        self.base_url = 'https://www.plurk.com'
        self.app_key = app_key
        self.app_secret = app_secret
        self.consumer = oauth.Consumer(self.app_key, self.app_secret)

    def authorize(self):
        try:
            f = open('token.json', 'r').read()
        except FileNotFoundError:
            self.get_request_token()
        except Exception:
            raise
        else:
            api_key = json.loads(f)
            self.oauth_token = api_key['oauth_token']
            self.oauth_token_secret = api_key['oauth_token_access']
            self.oauth = OAuth1(self.app_key,
                                client_secret=self.app_secret,
                                resource_owner_key=self.oauth_token,
                                resource_owner_secret=self.oauth_token_secret)
            api_url = f'{self.base_url}/APP/Users/me'
            r = requests.get(url=api_url, auth=self.oauth)
            if r.status_code == 200:
                print('Login as: ', r.json()['display_name'])
                return oauth
            else:
                raise Exception('Auth Error')

    def get_request_token(self):
        client = oauth.Client(self.consumer)
        response = client.request(
            f'{self.base_url}/OAuth/request_token', method='GET')
        if response[0]['status'] != '200':
            raise Exception(response[0]['status'])
        self.oauth_token = parse_qs(str(response[1])[2:])['oauth_token'][0]
        self.oauth_token_secret = parse_qs(str(response[1])[2:])[
            'oauth_token_secret'][0]
        print(f'{self.base_url}/OAuth/authorize?oauth_token={self.oauth_token}')
        self.verify = input('input code: ')
        self.get_access_token()

    def get_access_token(self):
        token = oauth.Token(self.oauth_token, self.oauth_token_secret)
        token.set_verifier(self.verify)
        client = oauth.Client(self.consumer, token)
        response = client.request(
            f'{self.base_url}/OAuth/access_token', method='GET')
        self.oauth_token = parse_qs(response[1].decode())['oauth_token'][0]
        self.oauth_token_secret = parse_qs(str(response[1])[2:])[
            'oauth_token_secret'][0]

        api_key = {'app_key': self.app_key, 'app_secret': self.app_secret,
                   'oauth_token': self.oauth_token, 'oauth_token_access': self.oauth_token_secret}
        with open('token.json', 'w') as f:
            f.write(json.dumps(api_key))


class user(plurkapi):
    def __init__(self, app_key, app_secret):
        super().__init__(app_key, app_secret)

    def me(self):
        api_url = f'{self.base_url}/APP/Users/me'
        r = requests.get(api_url, auth=self.oauth)
        if r.status_code == 200:
            return r.json()

    def update(self, full_name=None, email=None, display_name=None, privacy=None):
        '''
        full_name: Change full name.
        email: Change email.
        display_name: User's display name, can be empty and full unicode. Must be shorter than 15 characters.
        privacy: User's privacy settings. The option can be world (whole world can view the profile) or only_friends (only friends can view the profile).
        date_of_birth: Should be YYYY-MM-DD, example 1985-05-13.
        '''
        api_url = self.base_url + '/APP/Users/update'
        data = {'full_name': full_name, 'email': email,
                'display_name': display_name, 'privacy': privacy}
        r = requests.post(api_url, auth=self.oauth)
        if r.status_code != 200:
            raise Exception('Request Error')
