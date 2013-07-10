# -*- coding: utf-8 -*-
#
# File: testCustomMeetingItem.py
#
# Copyright (c) 2007-2012 by CommunesPlone.org
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

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import \
    MeetingLalouviereTestCase
from Products.PloneMeeting.tests.testMeetingItem import testMeetingItem as pmtmi
from DateTime import DateTime


class testCustomMeetingItem(MeetingLalouviereTestCase, pmtmi):
    """
        Tests the MeetingItem adapted methods
    """

    def afterSetUp(self):
        MeetingLalouviereTestCase.afterSetUp(self)

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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mll_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testCustomMeetingItem, prefix='test_mll_'))
    return suite
