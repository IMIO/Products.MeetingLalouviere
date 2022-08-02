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
from datetime import datetime

from Products.MeetingLalouviere.config import COLLEGE_DEFAULT_MOTIVATION
from Products.MeetingLalouviere.config import COUNCIL_DEFAULT_MOTIVATION

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)
from Products.MeetingCommunes.tests.testCustomMeetingItem import (
    testCustomMeetingItem as mctcm,
)
from DateTime import DateTime
from zope.annotation import IAnnotations


class testCustomMeetingItem(mctcm, MeetingLalouviereTestCase):
    """
        Tests the MeetingItem adapted methods
    """

    def test_onDuplicated(self):
        """
          When a college item is duplicated to the council meetingConfig,
          the motivation field for the new item (council item) is populated like this :
          Default value for motivation field of the new item + value of motivation that was
          defined on original item (college item)
        """
        cfg = self.meetingConfig
        cfg.setItemAutoSentToOtherMCStates(("accepted",))
        cfg2 = self.meetingConfig2
        # by default, college items are sendable to council
        destMeetingConfigId = cfg2.getId()
        self.assertTrue(
            destMeetingConfigId
            in [config["meeting_config"] for config in cfg.getMeetingConfigsToCloneTo()]
        )
        # create an item in college, set a motivation, send it to council and check
        self.changeUser("pmManager")
        item = self.create("MeetingItem")
        item.setDecision("<p>A decision</p>")
        item.setOtherMeetingConfigsClonableTo((destMeetingConfigId,))
        self.assertTrue(item.getMotivation() == COLLEGE_DEFAULT_MOTIVATION)
        meeting = self.create("Meeting", date=datetime(2013, 5, 5))
        self.presentItem(item)
        # now close the meeting so the item is automatically accepted and sent to meetingConfig2
        self.closeMeeting(meeting)
        self.assertTrue(item.query_state() in cfg.getItemAutoSentToOtherMCStates())
        self.assertTrue(item._checkAlreadyClonedToOtherMC(destMeetingConfigId))
        # get the item that was sent to meetingConfig2 and check his motivation field
        annotation_key = item._getSentToOtherMCAnnotationKey(destMeetingConfigId)
        newItem = self.portal.uid_catalog(UID=IAnnotations(item)[annotation_key])[
            0
        ].getObject()
        expected_new_item_motivation = "{}<p>&nbsp;</p><p>&nbsp;</p>{}".format(
            COUNCIL_DEFAULT_MOTIVATION, item.getMotivation()
        )
        self.assertEqual(newItem.getMotivation(), expected_new_item_motivation)

    def test_showFollowUp(self):
        self.changeUser("pmManager")
        meeting = self._createMeetingWithItems()
        self.assertGreater(len(meeting.get_items()), 5)

        for item in meeting.get_items():
            self.assertEqual(item.query_state(), 'presented')
            self.assertTrue(item.adapted().showFollowUp())
            self.changeUser("pmFollowup1")
            self.assertFalse(item.adapted().showFollowUp())
            self.changeUser("pmManager")

        self.freezeMeeting(meeting)

        for item in meeting.get_items():
            self.assertEqual(item.query_state(), 'itemfrozen')
            self.assertTrue(item.adapted().showFollowUp())
            self.changeUser("pmFollowup1")
            self.assertFalse(item.adapted().showFollowUp())
            self.changeUser("pmManager")

        self.decideMeeting(meeting)
        item = meeting.get_items()[0]
        self.do(item, 'accept')
        self.assertEqual(item.query_state(), 'accepted')
        self.assertTrue(item.adapted().showFollowUp())
        self.changeUser("pmFollowup1")
        self.assertTrue(item.adapted().showFollowUp())

        self.changeUser("pmManager")
        item = meeting.get_items()[1]
        self.do(item, 'accept_but_modify')
        self.assertEqual(item.query_state(), 'accepted_but_modified')
        self.assertTrue(item.adapted().showFollowUp())
        self.changeUser("pmFollowup1")
        self.assertTrue(item.adapted().showFollowUp())

        self.changeUser("pmManager")
        item = meeting.get_items()[2]
        self.do(item, 'delay')
        self.assertEqual(item.query_state(), 'delayed')
        self.assertTrue(item.adapted().showFollowUp())
        self.changeUser("pmFollowup1")
        self.assertTrue(item.adapted().showFollowUp())

        # returned_to_proposing_group items must not display followp
        self.changeUser("pmManager")
        item = meeting.get_items()[3]
        self.do(item, 'return_to_proposing_group')
        self.assertEqual(item.query_state(), 'returned_to_proposing_group')
        self.assertFalse(item.adapted().showFollowUp())
        self.changeUser("pmFollowup1")
        self.assertFalse(item.adapted().showFollowUp())

        self.changeUser("pmManager")
        item = meeting.get_items()[4]
        self.do(item, 'refuse')
        self.assertEqual(item.query_state(), 'refused')
        self.assertTrue(item.adapted().showFollowUp())
        self.changeUser("pmFollowup1")
        self.assertTrue(item.adapted().showFollowUp())

        self.changeUser("pmManager")
        item = meeting.get_items()[5]
        self.do(item, 'remove')
        self.assertEqual(item.query_state(), 'removed')
        self.assertTrue(item.adapted().showFollowUp())
        self.changeUser("pmFollowup1")
        self.assertTrue(item.adapted().showFollowUp())

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomMeetingItem, prefix="test_"))
    return suite
