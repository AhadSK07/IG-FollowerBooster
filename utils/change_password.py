import json
import random
import string

import requests


class PasswordChanger:
    def __init__(self, username, password, accounts):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.accounts = accounts
        self.new_password = self.generate_password()
        self.login_url = 'https://www.instagram.com/accounts/login/ajax/'
        self.change_pwd_url = 'https://www.instagram.com/accounts/password/change/'
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'

    def generate_password(self):
        password_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(password_characters) for _ in range(16))

    def setup_session(self):
        self.session.cookies.update({
            'sessionid': '', 'mid': '', 'ig_pr': '1',
            'ig_vw': '1920', 'ig_cb': '1', 'csrftoken': '',
            's_network': '', 'ds_user_id': ''})
        self.session.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })
        self.session.get(self.login_url)
        self.session.headers['X-CSRFToken'] = self.session.cookies.get_dict()['csrftoken']

    def update_session_headers(self, login_cookies):
        self.session.headers.update({
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-length': '658',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'pragma': 'no-cache',
            'referer': 'https://www.instagram.com/accounts/password/change/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-csrftoken': login_cookies['csrftoken'],
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR1TN4gla-aM3DKrODT9HYvDnxFKjeiB-rKi8I1kO9fYvAxs',
            'x-instagram-ajax': '35b547292413',
            'x-requested-with': 'XMLHttpRequest'
        })

    def login(self):
        login_data = {'username': self.username, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{self.password}'}
        response = self.session.post(self.login_url, data=login_data)
        response_json = response.json()
        if 'userId' not in response_json:
            print(f"Login Failed! {response_json}")
            return False
        else:
            print("Instagram login successful")
            return response.cookies

    def change_password(self):
        change_data = {
            'enc_old_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{self.password}',
            'enc_new_password1': f'#PWD_INSTAGRAM_BROWSER:0:&:{self.new_password}',
            'enc_new_password2': f'#PWD_INSTAGRAM_BROWSER:0:&:{self.new_password}'
        }
        response = self.session.post(self.change_pwd_url, data=change_data).json()
        if response['status'] == 'ok':
            print(f"Password Changed from {self.password} to {self.new_password}")
            with open("config.json", "w") as file:
                self.accounts[self.username] = self.new_password
                json.dump(self.accounts, file)
        else:
            print(f"Password Change Failed: {response['errors']}")

    def run(self):
        self.setup_session()
        login_cookies = self.login()
        if not login_cookies:
            return
        self.update_session_headers(login_cookies)
        self.change_password()
