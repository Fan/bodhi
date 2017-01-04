# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""This test suite contains tests for bodhi.server.bugs."""

import unittest

import bunch
import mock

from bodhi.server import bugs


class TestBugzilla(unittest.TestCase):
    """This test class contains tests for the Bugzilla class."""
    def test___init__(self):
        """Assert that the __init__ method sets up the Bugzilla object correctly."""
        bz = bugs.Bugzilla()

        self.assertIsNone(bz._bz)

    @mock.patch('bodhi.server.bugs.bugzilla.Bugzilla.__init__', return_value=None)
    def test__connect_with_creds(self, __init__):
        """Test the _connect() method when the config contains credentials."""
        bz = bugs.Bugzilla()
        patch_config = {'bodhi_email': 'bodhi@example.com', 'bodhi_password': 'bodhi_secret',
                        'bz_server': 'https://example.com/bz'}

        with mock.patch.dict('bodhi.server.bugs.config', patch_config):
            bz._connect()

        __init__.assert_called_once_with(url='https://example.com/bz', user='bodhi@example.com',
                                         password='bodhi_secret', cookiefile=None, tokenfile=None)

    @mock.patch('bodhi.server.bugs.bugzilla.Bugzilla.__init__', return_value=None)
    def test__connect_without_creds(self, __init__):
        """Test the _connect() method when the config does not contain credentials."""
        bz = bugs.Bugzilla()
        patch_config = {'bz_server': 'https://example.com/bz'}

        with mock.patch.dict('bodhi.server.bugs.config', patch_config):
            bz._connect()

        __init__.assert_called_once_with(url='https://example.com/bz',
                                         cookiefile=None, tokenfile=None)


class TestFakeBugTracker(unittest.TestCase):
    """This test class contains tests for the FakeBugTracker class."""
    def test_getbug(self):
        """Ensure correct return value of the getbug() method."""
        bt = bugs.FakeBugTracker()

        b = bt.getbug(1234)

        self.assertTrue(isinstance(b, bunch.Bunch))
        self.assertEqual(b.bug_id, 1234)
