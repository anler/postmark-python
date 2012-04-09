import os
import json
import urllib2
import unittest

from pyDoubles.framework import spy, assert_that_method

import postmark


class PostmarkTest(unittest.TestCase):

    api_key = "dummy"

    def test_sendmail(self):
        def request_factory(*args, **kwargs):
            return spy(urllib2.Request(*args, **kwargs))
        class dummyopener(object):
            def open(self, request):
                pass
        opener = spy(dummyopener())
        p = postmark.Postmark(self.api_key, request_factory, opener)
        m = spy(postmark.Message("from", "to"))
        p._send_request(m)

        assert_that_method(m.as_string).was_called()
        assert_that_method(p.request.add_data).was_called()
        assert_that_method(opener.open).was_called().with_args(p.request)


class MessageTest(unittest.TestCase):
    def test_sender(self):
        sender = "Sender addr"
        to = "To addr"
        msg = postmark.Message(sender, to)
        self.assertEqual(sender, msg.sender)
        self.assertIn(sender, msg.as_string())

    def test_to(self):
        sender = "Sender addr"
        to = "To addr"
        msg = postmark.Message(sender, to)
        self.assertEqual(to, msg.to)
        self.assertIn(to, msg.as_string())

    def test_to_as_list(self):
        sender = "Sender addr"
        to = ["to1", "to2"]
        msg = postmark.Message(sender, to)
        self.assertEqual(to, msg.to)
        self.assertIn(",".join(to), msg.as_string())

    def test_cc(self):
        sender = "Sender addr"
        to = "To addr"
        cc = "CC addr"
        msg = postmark.Message(sender, to, cc=cc)
        self.assertEqual(cc, msg.cc)
        self.assertIn(cc, msg.as_string())

    def test_cc_as_list(self):
        sender = "Sender addr"
        to = ["to1", "to2"]
        cc = ["cc1", "cc2"]
        msg = postmark.Message(sender, to, cc=cc)
        self.assertEqual(cc, msg.cc)
        self.assertIn(",".join(cc), msg.as_string())

    def test_bcc(self):
        sender = "Sender addr"
        to = "To addr"
        bcc = "Bcc addr"
        msg = postmark.Message(sender, to, bcc=bcc)
        self.assertEqual(bcc, msg.bcc)
        self.assertIn(bcc, msg.as_string())

    def test_bcc_as_list(self):
        sender = "Sender addr"
        to = ["to1", "to2"]
        bcc = ["bcc1", "bcc2"]
        msg = postmark.Message(sender, to, bcc=bcc)
        self.assertEqual(bcc, msg.bcc)
        self.assertIn(",".join(bcc), msg.as_string())

    def test_subject(self):
        sender = "Sender addr"
        to = "To addr"
        subject = "Subject"
        msg = postmark.Message(sender, to, subject=subject)
        self.assertEqual(subject, msg.subject)
        self.assertIn(subject, msg.as_string())

    def test_tag(self):
        sender = "Sender addr"
        to = "To addr"
        tag = "Tag"
        msg = postmark.Message(sender, to, tag=tag)
        self.assertEqual(tag, msg.tag)
        self.assertIn(tag, msg.as_string())

    def test_html(self):
        sender = "Sender addr"
        to = "To addr"
        html = "<p>Html</p>"
        msg = postmark.Message(sender, to, html=html)
        self.assertEqual(html, msg.html)
        self.assertIn(html, msg.as_string())

    def test_text(self):
        sender = "Sender addr"
        to = "To addr"
        text = "Text"
        msg = postmark.Message(sender, to, text=text)
        self.assertEqual(text, msg.text)
        self.assertIn(text, msg.as_string())

    def test_reply_to(self):
        sender = "Sender addr"
        to = "To addr"
        reply_to = "Reply to"
        msg = postmark.Message(sender, to, reply_to=reply_to)
        self.assertEqual(reply_to, msg.reply_to)
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

