import requests
from urllib.parse import urlparse
from time import sleep


class FollowersSender:
    def __init__(self, login_url, username, password, to_send):
        self.session = requests.Session()
        self.login_url = login_url
        self.parsed_url = urlparse(self.login_url)
        self.username = username
        self.password = password
        self.to_send = to_send
        self.session.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

    def login(self, retry=False):
        print(f"Website Domain: {self.parsed_url.netloc}")
        try:
            response = self.session.post(self.login_url, data={'username': self.username, 'password': self.password})
            login = response.json()
            if 'returnUrl' not in login:
                raise Exception(f"Login failed. Error message: {login['error']}")
            print("Logged in successfully")
            return login['returnUrl']
        except Exception as e:
            if retry:
                print(f"Login failed. Error message: {e}")
            else:
                print("Login failed. Error message: Failed to get JSON data. Retrying...")
                return self.login(True)

    def get_credits(self, return_path):
        url = f"{self.parsed_url.scheme}://{self.parsed_url.netloc}{return_path}"
        credits_response = self.session.get(url)
        credits_text = 'takipKrediCount'
        start = credits_response.text.find(f'id="{credits_text}"')
        if start == -1:
            raise Exception(f"Unable to find credits in the response from {url}")
        start = credits_response.text.find('>', start) + 1
        end = credits_response.text.find('<', start)
        return credits_response.text[start:end].strip()

    def send_followers(self, credits, retry=False):
        try:
            followers_response = self.session.post(
                f"{self.credits_response.url}/send-follower?formType=findUserID",
                data={'username': self.to_send}
            )
            user_id = followers_response.url.split("/")[-1]
            send = self.session.post(
                f"{followers_response.url}?formType=send",
                data={'adet': credits, 'userID': user_id, 'userName': self.to_send}
            ).json()
            if send['status'] != 'success':
                raise Exception(send['message'])
            print(f"Followers sent successfully to {self.to_send}. Sleeping for 2 minutes...")
            sleep(120)
        except Exception as error:
            if retry:
                print(f"Failed to send followers. Error message: {error}")
            else:
                print(f"Failed to send followers. Error message: {error}. Retrying after 1 minute...")
                sleep(60)
                self.send_followers(credits, True)

    def run(self):
        return_path = self.login()
        if not return_path:
            return
        credits = self.get_credits(return_path)
        if credits == '0':
            print("No credits left.")
        else:
            print(f"Sending {credits} followers.")
            self.send_followers(credits)
