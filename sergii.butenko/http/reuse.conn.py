#!/usr/bin/env python

# Using same TCP connection for all HTTP requests
import time
import logging
import requests

logging.basicConfig(level=logging.DEBUG)

API_URL = "https://example.com/"

def make_get_request():
    for i in range(10):
        requests.get(url=API_URL)

def make_session_get_request():
    session = requests.Session()
    for i in range(10):
        # session.get(url=API_URL)
        session.get(url=API_URL, headers={"Connection": "close"})


def login():
    r = requests.post(url="https://app.cosmosid.com/api/v1/login", headers={"authorization": "Basic c2VyYnV0QHNlci5idXQ6c2VyYnV0QHNlci5idXQ="})
    print(r.text)
if __name__ == "__main__":
    # start_time = time.time()
    # make_get_request()
    # print("--- %s seconds ---" % (time.time() - start_time))

    # start_time = time.time()
    # make_session_get_request()
    # print("--- %s seconds ---" % (time.time() - start_time))
    login()