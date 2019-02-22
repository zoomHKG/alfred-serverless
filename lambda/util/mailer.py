import os
import requests

def send_mail(emails, title, body):
	url = os.environ.get('MAILER_URL')
	data = {
		'from': 'Alfred',
		'to': ', '.join(emails),
		'subject': title,
		'text': body
	}
	headers = {
		'Origin': 'lambda:Alfred'
	}
	r = requests.post(url, headers=headers, json=data)
	print(r.json())
