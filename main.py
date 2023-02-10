import json
from followers import FollowersSender
from pwd_change import ChangePassword

URLS = [
    "https://freefollowerx.com/login",
    "https://instamoda.org/login",
    "https://takipcitime.com/login",
    "https://takipcikrali.com/login",
    "https://takipcimx.net/login",
    "https://takipciking.com/member",
    "https://birtakipci.com/member",
    "https://medyahizmeti.com/member",
]

with open("accounts.json", "r") as file:
    accounts = json.load(file)
    for account_name, account_password in accounts.items():
        print(f"Account: {account_name}")
        for url in URLS:
            FollowersSender(url, account_name, account_password, "ah4d1337").run()
        ChangePassword(account_name, account_password, accounts)
