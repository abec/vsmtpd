#
# vsmtpd/tests/test_transaction.py
#
# Copyright (C) 2011 Damien Churchill <damoxc@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.    If not, write to:
#   The Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor
#   Boston, MA    02110-1301, USA.
#

from vsmtpd.address import Address
from vsmtpd.transaction import Transaction
from vsmtpd.tests.common import TestCase

class TransactionTestCase(TestCase):

    def setUp(self):
        self.tnx = Transaction(None)

    def test_add_recipient_as_string(self):
        address = Address('test@example.com')
        self.tnx.add_recipient('test@example.com')
        self.assertEqual(address, self.tnx.recipients[0])

    def test_add_recipient_as_address(self):
        address = Address('test@example.com')
        self.tnx.add_recipient(address)
        self.assertEqual(address, self.tnx.recipients[0])

    def test_remove_recipient_as_string(self):
        address = Address('test@example.com')
        self.tnx.add_recipient(address)

        self.tnx.remove_recipient('test@example.com')
        self.assertEqual(self.tnx.recipients, [])

    def test_remove_recipient_as_address(self):
        address = Address('test@example.com')
        self.tnx.add_recipient(address)

        self.tnx.remove_recipient(address)
        self.assertEqual(self.tnx.recipients, [])

    def test_setting_sender_as_string(self):
        address = Address('test@example.com')
        self.tnx.sender = 'test@example.com'
        self.assertEqual(self.tnx.sender, address)

    def test_setting_sender_as_address(self):
        address = Address('test@example.com')
        self.tnx.sender = address
        self.assertEqual(self.tnx.sender, address)

    def test_body_flush(self):
        self.tnx.body.write('Subject: blah blah\r\n')
        self.tnx.body.write('From: John Smith <john@example.com>\r\n')
        self.tnx.body.write('To: Joe Bloggs <joe@example.com>\r\n')
        self.tnx.body.write('Date: Fri, 25 Mar 2011 13:35:33 -0000\r\n')
        self.tnx.body.write('\r\n')
        self.tnx.body.write('This is testing writing an email\r\n')
        old_tell = self.tnx.body.tell()

        self.tnx.flush()
        self.assertNotEqual(self.tnx.body_filename, None)
        self.assertEqual(old_tell, self.tnx.body.tell())

    def test_body_flush_twice(self):
        self.tnx.body.write('Subject: blah blah\r\n')
        self.tnx.body.write('From: John Smith <john@example.com>\r\n')
        self.tnx.body.write('To: Joe Bloggs <joe@example.com>\r\n')
        self.tnx.body.write('Date: Fri, 25 Mar 2011 13:35:33 -0000\r\n')
        self.tnx.body.write('\r\n')
        self.tnx.body.write('This is testing writing an email\r\n')
        self.tnx.flush()
        self.assertNotEqual(self.tnx.body_filename, None)

        filename = self.tnx.body_filename
        self.tnx.flush()
        self.assertEqual(self.tnx.body_filename, filename)

    def test_body_write(self):
        msg = """Subject: blah blah
From: John Smith <john@example.com>
To: Joe Bloggs <joe@example.com>
Date: Fri, 25 Mar 2011 13:35:33 -0000

This is testing writing an email"""
        self.tnx.body.write(msg)
        self.assertEqual(self.tnx.body.name, None)
        self.assertEqual(self.tnx.body.getvalue(), msg)

    def test_body_write_flush(self):
        self.assertEqual(self.tnx.body.name, None)
        self.tnx.body.write(' ' * (1024 * 512))
        self.assertNotEqual(self.tnx.body.name, None)

    def test_end_headers(self):
        self.tnx.body.write('Subject: blah blah\r\n')
        self.tnx.body.write('From: John Smith <john@example.com>\r\n')
        self.tnx.body.write('To: Joe Bloggs <joe@example.com>\r\n')
        self.tnx.body.write('Date: Fri, 25 Mar 2011 13:35:33 -0000\r\n')
        self.tnx.body.write('\r\n')
        self.tnx.end_headers()
        self.assertTrue(self.tnx.body.body_start > 0)
        self.assertEqual(self.tnx.body.body_start, 132)

    def test_body_property(self):
        self.assertNotEqual(self.tnx.body, None)

    def test_body_filename_flush(self):
        self.assertNotEqual(self.tnx.body_filename, None)

    def test_connection_property(self):
        self.assertEqual(self.tnx.connection, self.tnx._connection)

    def test_body_insert_header(self):
        self.tnx.body.write('Subject: blah blah\r\n')
        self.tnx.body.write('From: John Smith <john@example.com>\r\n')
        self.tnx.body.write('To: Joe Bloggs <joe@example.com>\r\n')
        self.tnx.body.write('Date: Fri, 25 Mar 2011 13:35:33 -0000\r\n')
        self.tnx.body.write('\r\n')
        self.tnx.end_headers()

        self.tnx.headers.insert_header(0, 'Received', 'By me')
        self.assertTrue(self.tnx.headers.has_key('Received'))
        self.assertEqual(self.tnx.headers.keys()[0], 'Received')

        self.tnx.headers.insert_header(5, 'X-Test', 'vsmtpd')
        self.assertTrue(self.tnx.headers.has_key('X-Test'))
        self.assertEqual(self.tnx.headers.keys()[5], 'X-Test')

    def tearDown(self):
        self.tnx.close()
