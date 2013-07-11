# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2010 by PloneGov
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from DateTime import DateTime

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.MeetingLalouviere.testing import MLL_TEST_PROFILE_FUNCTIONAL


class MeetingLalouviereTestCase(MeetingCommunesTestCase):
    """Base class for defining MeetingLalouviere test cases."""

    layer = MLL_TEST_PROFILE_FUNCTIONAL

    def _createMeetingWithItems(self):
        '''Create a meeting with a bunch of items.'''
        meetingDate = DateTime().strftime('%y/%m/%d %H:%M:%S')
        meeting = self.create('Meeting', date=meetingDate)
        item1 = self.create('MeetingItem')
        item1.setProposingGroup('developers')
        item2 = self.create('MeetingItem')
        item2.setProposingGroup('vendors')
        for item in (item1, item2):
            self.do(item, 'propose')
            self.do(item, 'validate')
            self.do(item, 'present')
        return meeting


# this is necessary to execute base test
# test_tescasesubproduct_VerifyTestFiles from PloneMeeting
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(MeetingCommunesTestCase, prefix='test_testcasesubproduct_'))
    return suite
