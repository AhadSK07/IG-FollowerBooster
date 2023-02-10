import json
from requests import Session
from random import randint, sample


class ChangePassword:
    def __init__(self, username, password, accounts):
        self.session = Session()
        self.username = username
        self.password = password
        self.accounts = accounts
        self.new_password = self.gen_password()
        self.login_url = 'https://www.instagram.com/accounts/login/ajax/'
        self.change_pwd_url = 'https://www.instagram.com/accounts/password/change/'
        self.data_login = {
            'username': self.username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{self.password}'
            }
        self.data_change = {
            'enc_old_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{self.password}',
            'enc_new_password1': f'#PWD_INSTAGRAM_BROWSER:0:&:{self.new_password}',
            'enc_new_password2': f'#PWD_INSTAGRAM_BROWSER:0:&:{self.new_password}'
            }
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        self.login_and_change()

    def gen_password(self):
        keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"+"abcdefghijklmnopqrstuvwxyz"+"1234567890".lower()
        password = "".join(sample(keys, randint(8, 16)))
        return password

    def login_and_change(self):
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
        login = self.session.post(self.login_url, data=self.data_login)
        if 'userId' not in login.json():
            print(f"Login Problem! {login.json()}")
            return
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
            'x-csrftoken': login.cookies['csrftoken'],
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR1TN4gla-aM3DKrODT9HYvDnxFKjeiB-rKi8I1kO9fYvAxs',
            'x-instagram-ajax': '35b547292413',
            'x-requested-with': 'XMLHttpRequest'
            })
        change_response = self.session.post(self.change_pwd_url, data=self.data_change).json()
        if change_response['status'] == 'ok':
            print(f"Password Changed {self.password} to {self.new_password}")
            with open("accounts.json", "w") as file:
                self.accounts[self.username] = self.new_password
                json.dump(self.accounts, file)
        else:
            print(change_response['errors'])
