import json
from followers import SendFollowers
from pwd_change import ChangePassword

urls = ["https://freefollowerx.com/login",
        "https://instamoda.org/login",
        "https://takipcitime.com/login",
        "https://takipcikrali.com/login",
        "https://takipcimx.net/login",
        "https://takipciking.com/member",
        "https://birtakipci.com/member",
        "https://medyahizmeti.com/member"]

with open("accounts.json", "r") as file:
    accounts = json.load(file)
    for account in accounts.items():
        print(f"Account: {account[0]}")
        for url in urls:
            SendFollowers(url, account[0], account[1], "ah4d1337")
        ChangePassword(account[0], account[1], accounts)
