from requests import Session
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from time import sleep


class SendFollowers:
    def __init__(self, login_url, username, password, to_send):
        self.session = Session()
        self.login_url = login_url
        self.parsed_url = urlparse(self.login_url)
        self.username = username
        self.password = password
        self.to_send = to_send
        self.crd_response = None
        self.folo_response = None
        self.session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        self.main()
        
    def login(self, retry=False):
        print(f"Website Domain: {self.parsed_url.netloc}")
        try:
            login = self.session.post(self.login_url, data={'username': self.username, 'password': self.password}).json()
            if 'returnUrl' in login:
                print("Logged Successfully")
                return login['returnUrl']
            else:
                print(f"Login Failed\nError Message: {login['error']}")
        except:
            if retry != True:
                print("Login Failed\nError Message: Failed to Get Json Data\nRetrying... Login")
                return self.login(True)
            else:
                print("Login Failed\nError Message: Failed to Get Json Data")

    def get_credits(self, return_path):
        self.crd_response = self.session.get(f"{self.parsed_url.scheme}://{self.parsed_url.netloc}{return_path}")
        soup = BeautifulSoup(self.crd_response.text, 'html.parser')
        return soup.find(id='takipKrediCount').text

    def send_followers(self, credits, retry=False):
        self.folo_response = self.session.post(f"{self.crd_response.url}/send-follower?formType=findUserID", data={'username': self.to_send})
        send_data = {'adet': credits, 'userID': self.folo_response.url.split("/")[-1], 'userName': self.to_send}
        send = self.session.post(f"{self.folo_response.url}?formType=send", data=send_data).json()
        if send['status'] != 'success':
            if retry != True:
                print(f"Failed to Send Followers\nError Message: {send['message']}\nRetrying... after 1Min")
                sleep(60)
                return self.send_followers(credits, True)
            else:
                print(f"Failed to Send Followers\nError Message: {send['message']}") 
        else:
            print(f"Send Followers Done to {self.to_send}\nSleeping... for 2Min")
            sleep(120)

    def main(self):
        return_path = self.login()
        if return_path == None:
            return
        credits = self.get_credits(return_path)
        if credits != '0':
            print(credits)
            self.send_followers(credits)
        else:
            print("No Credits Left")
