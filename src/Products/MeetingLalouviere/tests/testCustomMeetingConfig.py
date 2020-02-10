# -*- coding: utf-8 -*-
#
# File: testCustomMeetingConfig.py
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

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)
from DateTime import DateTime
from imio.helpers.cache import cleanRamCacheFor


class testCustomMeetingConfig(MeetingLalouviereTestCase):
    """
        Tests the MeetingConfig adapted methods
    """

    def test_getMeetingsAcceptingItems(self):
        """
          For 'meeting-config-council', meetings in state 'in_committee',
          'in_council' are also accepting items.
        """
        cfg2 = self.meetingConfig2
        self.changeUser("pmManager")
        self.setMeetingConfig(cfg2.getId())
        meeting = self.create("Meeting", date=DateTime("2016/10/04"))

        # created, available for everyone
        self.assertEqual(meeting.queryState(), "created")
        self.assertEqual(
            [brain.UID for brain in cfg2.getMeetingsAcceptingItems()], [meeting.UID()]
        )
        self.changeUser("pmCreator1")
        self.assertEqual(
            [brain.UID for brain in cfg2.getMeetingsAcceptingItems()], [meeting.UID()]
        )
        # in_committee
        self.changeUser("pmManager")
        self.do(meeting, "setInCommittee")
        self.assertEqual(meeting.queryState(), "in_committee")
        self.assertEqual(
            [brain.UID for brain in cfg2.getMeetingsAcceptingItems()], [meeting.UID()]
        )
        cleanRamCacheFor(
            "Products.PloneMeeting.MeetingConfig.getMeetingsAcceptingItems"
        )
        self.changeUser("pmCreator1")
        self.assertEqual([brain.UID for brain in cfg2.getMeetingsAcceptingItems()], [])
        # in_council
        self.changeUser("pmManager")
        self.do(meeting, "setInCouncil")
        self.assertEqual(meeting.queryState(), "in_council")
        cleanRamCacheFor(
            "Products.PloneMeeting.MeetingConfig.getMeetingsAcceptingItems"
        )
        self.assertEqual(
            [brain.UID for brain in cfg2.getMeetingsAcceptingItems()], [meeting.UID()]
        )
        cleanRamCacheFor(
            "Products.PloneMeeting.MeetingConfig.getMeetingsAcceptingItems"
        )
        self.changeUser("pmCreator1")
        self.assertEqual([brain.UID for brain in cfg2.getMeetingsAcceptingItems()], [])
        cleanRamCacheFor(
            "Products.PloneMeeting.MeetingConfig.getMeetingsAcceptingItems"
        )
        # closed
        self.changeUser("pmManager")
        self.do(meeting, "close")
        self.assertEqual(meeting.queryState(), "closed")
        self.assertEqual([brain.UID for brain in cfg2.getMeetingsAcceptingItems()], [])
        cleanRamCacheFor(
            "Products.PloneMeeting.MeetingConfig.getMeetingsAcceptingItems"
        )
        self.changeUser("pmCreator1")
        self.assertEqual([brain.UID for brain in cfg2.getMeetingsAcceptingItems()], [])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomMeetingConfig, prefix='test_'))
    return suite
