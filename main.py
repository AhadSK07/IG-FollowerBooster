import json

from utils.send_followers import FollowersSender
from utils.change_password import PasswordChanger

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

def process_account(urls, account_name, account_password, accounts, target_username):
    for url in urls:
        try:
            FollowersSender(url, account_name, account_password, target_username).run()
        except Exception as e:
            print(f"Failed to send followers with error: {str(e)}")

    try:
        PasswordChanger(account_name, account_password, accounts).run()
    except Exception as e:
        print(f"Failed to change password with error: {str(e)}")


def get_accounts(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return {}
    except json.JSONDecodeError:
        print(f"Failed to parse the JSON data from {file_path}.")
        return {}

def main():
    accounts = get_accounts("config.json")
    for account_name, account_password in accounts.items():
        print(f"Processing account: {account_name}")
        process_account(URLS, account_name, account_password, accounts, "ahad.rex")

main()
