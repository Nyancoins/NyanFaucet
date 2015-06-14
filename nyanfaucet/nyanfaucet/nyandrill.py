import mandrill

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

"""
import logging
import django.utils.log
class MandrillLogger(django.utils.log.AdminEmailHandler):
    def __init__(self, *args, **kwargs):
        super(MandrillLogger, self).__init__()
        self.client = mandrill.Mandrill(settings.MANDRILL_SECRET)

    def send_mail(self, subject, message, *args, **kwargs):
        admins = []
        for name, email in settings.ADMINS:
            admins.append({
                'name': name,
                'email': email,
            })
        
        msg = {
            'to': admins,
            'subject': subject,
            'text': message,
        }
        print "sending mail", msg

        self.client.messages.send(msg)
"""

class MandrillBackend(BaseEmailBackend):        
    def __init__(self, fail_silently = False, **kwargs):
        super(MandrillBackend, self).__init__(fail_silently, **kwargs)
        self.client = mandrill.Mandrill(settings.MANDRILL_SECRET)

    def send_messages(self, email_messages):
        if not email_messages:
            return

        for msg in email_messages:
            to = []
            for r in msg.recipients():
                to.append({
                    'email': r,
                })

            mm = {
                'to': to,
                'subject': msg.subject,
                'from_email': msg.from_email,
                'text': msg.message().as_bytes(),
            }
            self.client.messages.send(mm, async=True)

