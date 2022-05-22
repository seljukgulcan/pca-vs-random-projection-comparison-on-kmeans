#!/usr/bin/env python
import requests
import json
import urllib
import socket
import sys

def send(chat_id, token, text):

	url = f"https://api.telegram.org/bot{token}/sendMessage?text={text}&chat_id={chat_id}"

	text = urllib.parse.quote_plus(text)
	r = requests.get(url)
	return r


if __name__ == '__main__':
	user_id = sys.argv[1]
	token = sys.argv[2]
	message = sys.argv[3]
	r = send(user_id, token, message)
	print(r)
