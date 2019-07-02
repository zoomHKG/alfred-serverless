import os
import requests

def send_mail(emails, title, body):
	url = os.environ.get('MAILER_URL')
	for email in emails:
		print('Sending email to: {}'.format(email))
		data = {
			'from': 'Alfred',
			'to': email,
			'subject': title,
			'text': body
		}
		headers = {
			'Origin': 'lambda:Alfred'
		}
		r = requests.post(url, headers=headers, json=data)
		res = r.json()
		print(res)
		if 'error' in res:
			raise Exception(res['error']['details'][0]['message'])
