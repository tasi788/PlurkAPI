import json
from urllib.parse import urlparse, parse_qs

import oauth2 as oauth


class plurkapi:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.consumer = oauth.Consumer(self.app_key, self.app_secret)
        self.request_token = 'https://www.plurk.com/OAuth/request_token'
        self.access_token = 'https://www.plurk.com/OAuth/access_token'
        self.base_url = 'https://www.plurk.com'
        self.authorization_url = '/OAuth/authorize'

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
            token = oauth.Token(self.oauth_token, self.oauth_token_secret)
            client = oauth.Client(self.consumer, token)
            return client

    def get_request_token(self):
        client = oauth.Client(self.consumer)
        response = client.request(self.request_token, method='GET')
        if response[0]['status'] != '200':
            raise Exception(response[0]['status'])
        self.oauth_token = parse_qs(str(response[1])[2:])['oauth_token'][0]
        self.oauth_token_secret = parse_qs(str(response[1])[2:])[
            'oauth_token_secret'][0]
        print(f'{self.base_url}{self.authorization_url}?oauth_token={self.oauth_token}')
        self.verify = input('input code: ')
        self.get_access_token()

    def get_access_token(self):
        token = oauth.Token(self.oauth_token, self.oauth_token_secret)
        token.set_verifier(self.verify)
        client = oauth.Client(self.consumer, token)
        response = client.request(self.access_token, method='GET')
        self.oauth_token = parse_qs(response[1].decode())['oauth_token'][0]
        self.oauth_token_secret = parse_qs(str(response[1])[2:])[
            'oauth_token_secret'][0]

        api_key = {'app_key': self.app_key, 'app_secret': self.app_secret,
                   'oauth_token': self.oauth_token, 'oauth_token_access': self.oauth_token_secret}
        with open('token.json', 'w') as f:
            f.write(json.dumps(api_key))
        self.getOwnProfile()

    def getOwnProfile(self):
        apiUrl = 'https://www.plurk.com/APP/Users/me'
        token = oauth.Token(self.oauth_token, self.oauth_token_secret)
        client = oauth.Client(self.consumer, token)
        # response = client.request(apiUrl, method='GET')
        # pp(json.loads(response[1]))
