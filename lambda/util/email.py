#!/usr/bin/env python3
"""Email related stuffs"""
import re
import smtplib

class Email():
    """Email class to send notifications"""

    email_text = 'From: {}\nTo: {}\nSubject: {}\n{}'
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd
        self.server = None


    def send_mail(self, emails, title, body):
        """Send email"""
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.email, self.passwd)
        self.server.sendmail(self.email, emails, self.email_text.format(
            'Alfred', ', '.join(emails), title, re.sub(r'\W', ' ', body)))
        self.server.quit()
