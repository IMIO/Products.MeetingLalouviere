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
        cfg2.setDefaultMeetingItemMotivation("<p>test</p>")
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
        self.assertTrue(item.getMotivation() == cfg.getDefaultMeetingItemMotivation())
        meeting = self.create("Meeting", date=DateTime("2013/05/05"))
        self.presentItem(item)
        # now close the meeting so the item is automatically accepted and sent to meetingConfig2
        self.closeMeeting(meeting)
        self.assertTrue(item.queryState() in cfg.getItemAutoSentToOtherMCStates())
        self.assertTrue(item._checkAlreadyClonedToOtherMC(destMeetingConfigId))
        # get the item that was sent to meetingConfig2 and check his motivation field
        annotation_key = item._getSentToOtherMCAnnotationKey(destMeetingConfigId)
        newItem = self.portal.uid_catalog(UID=IAnnotations(item)[annotation_key])[
            0
        ].getObject()
        expected_new_item_motivation = "{}<p>&nbsp;</p><p>&nbsp;</p>{}".format(
            cfg2.getDefaultMeetingItemMotivation(), item.getMotivation()
        )
        self.assertEqual(newItem.getMotivation(), expected_new_item_motivation)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomMeetingItem, prefix="test_"))
    return suite
