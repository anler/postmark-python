import os
import json
import unittest

import postmark


class PostmarkTest(unittest.TestCase):
    pass


class MessageTest(unittest.TestCase):
    def test_sender(self):
        sender = "Sender addr"
        to = "To addr"
        msg = postmark.Message(sender, to)
        self.assertIn(sender, msg.as_string())

    def test_to(self):
        sender = "Sender addr"
        to = "To addr"
        msg = postmark.Message(sender, to)
        self.assertIn(to, msg.as_string())

    def test_to_as_list(self):
        sender = "Sender addr"
        to = ["to1", "to2"]
        msg = postmark.Message(sender, to)
        self.assertIn(",".join(to), msg.as_string())

    def test_cc(self):
        sender = "Sender addr"
        to = "To addr"
        cc = "CC addr"
        msg = postmark.Message(sender, to, cc=cc)
        self.assertIn(cc, msg.as_string())

    def test_cc_as_list(self):
        sender = "Sender addr"
        to = ["to1", "to2"]
        cc = ["cc1", "cc2"]
        msg = postmark.Message(sender, to, cc=cc)
        self.assertIn(",".join(cc), msg.as_string())

    def test_bcc(self):
        sender = "Sender addr"
        to = "To addr"
        bcc = "CC addr"
        msg = postmark.Message(sender, to, bcc=bcc)
        self.assertIn(bcc, msg.as_string())

    def test_bcc_as_list(self):
        sender = "Sender addr"
        to = ["to1", "to2"]
        bcc = ["cc1", "cc2"]
        msg = postmark.Message(sender, to, bcc=bcc)
        self.assertIn(",".join(bcc), msg.as_string())

    def test_subject(self):
        sender = "Sender addr"
        to = "To addr"
        subject = "CC addr"
        msg = postmark.Message(sender, to, subject=subject)
        self.assertIn(subject, msg.as_string())

    def test_tag(self):
        sender = "Sender addr"
        to = "To addr"
        tag = "CC addr"
        msg = postmark.Message(sender, to, tag=tag)
        self.assertIn(tag, msg.as_string())

    def test_html(self):
        sender = "Sender addr"
        to = "To addr"
        html = "CC addr"
        msg = postmark.Message(sender, to, html=html)
        self.assertIn(html, msg.as_string())

    def test_text(self):
        sender = "Sender addr"
        to = "To addr"
        text = "CC addr"
        msg = postmark.Message(sender, to, text=text)
        self.assertIn(text, msg.as_string())

    def test_reply_to(self):
        sender = "Sender addr"
        to = "To addr"
        reply_to = "CC addr"
        msg = postmark.Message(sender, to, reply_to=reply_to)
        self.assertIn(reply_to, msg.as_string())

    def test_add_header(self):
        sender = "Sender addr"
        to = "To addr"
        msg = postmark.Message(sender, to)
        name = "Header"
        value = "My custom header"
        msg.add_header(name, value)
        msg = msg.as_string()
        self.assertIn('"Name": "%s"' % name, msg)
        self.assertIn('"Value": "%s"' % value, msg)

class MessageAttachmentTest(unittest.TestCase):
    def setUp(self):
        self.filename = "attachment.txt"
        with open(self.filename, "w") as f:
            f.write("attachment content")

    def tearDown(self):
        os.unlink(self.filename)

    def test_add_attachment(self):
        sender = "Sender addr"
        to = "To addr"
        msg = postmark.Message(sender, to)
        msg.add_attachment(self.filename)
        msg = msg.as_string()
        self.assertIn('"Name": "%s"' % self.filename, msg)
        self.assertIn('"ContentType": "text/plain"', msg)

