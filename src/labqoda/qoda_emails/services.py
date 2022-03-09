import requests


def send_email_to_users_on_course():
    URL = ""
    response = requests.post(URL, {}, headers={})
    print(response)
