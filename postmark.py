import os
import urllib2
import json
import base64
import logging

POSTMARK_URL = "%(scheme)s://api.postmarkapp.com/email"

logger = logging.getLogger("postmark")

class Postmark(object):
    def __init__(self, api_key, use_ssl=True):
        if use_ssl:
            scheme = "https"
        else:
            scheme = "http"
        api_key = api_key
        url = POSTMARK_URL % {"scheme": scheme}
        default_headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "X-Postmark-Server-Token": api_key
        }
        self.request = urllib2.Request(url, headers=default_headers)

    def sendmail(self, msg):
        self.request.add_data(msg.as_string())
        try:
            response = urllib2.urlopen(self.request).read()
        except urllib2.URLError, e:
            response = e.read()

        return json.loads(response)


class Message(object):

    _fields = {"sender": "From", "to": "To", "cc": "Cc", "bcc": "Bcc",
               "reply_to": "ReplyTo", "subject": "Subject",
               "html": "HtmlBody", "text": "TextBody", "tag": "Tag"}

    def __init__(self, sender, to, subject=None, html=None, text=None,
                 cc=None, bcc=None, reply_to=None, tag=None):
        self._message = {}
        self._message.setdefault("Headers", [])
        self._message.setdefault("Attachments", [])
        self.sender = sender
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.reply_to = reply_to
        self.subject = subject
        self.html = html
        self.text = text
        self.tag = tag
        self.reply_to = reply_to

    def __getattr__(self, name):
        if name in self._fields:
            value = self._message.get(self._fields[name])
        else:
            value = super(Message, self).__getattr__(name)

        return value

    def __setattr__(self, name, value):
        if name in self._fields:
            self._message[self._fields[name]] = value
        else:
            return super(Message, self).__setattr__(name, value)

    def as_string(self):
        message = {}
        for key, value in self._message.items():
            if value is None:
                continue
            elif key in ("To", "Cc", "Bcc"):
                if isinstance(value, list):
                    value = ",".join(value)
            message[key] = value

        return json.dumps(message)

    def add_header(self, name, value):
        self._message["Headers"].append({"Name": name, "Value": value})

    def add_attachment(self, filename):
        mimetype, encoding = mimetypes.guess_type(filename)
        self._message["Attachments"].append({
            "Name": os.path.basename(filename),
            "Value": base64.encodestring(open(filename).read()),
            "ContentType": mimetype
        })

