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
from zope.globalrequest import getRequest


class testCustomMeetingItem(mctcm, MeetingLalouviereTestCase):
    """
        Tests the MeetingItem adapted methods
    """
    default_item_ref = "python: 'Ref. ' + (here.hasMeeting() and " \
                       "here.restrictedTraverse('@@pm_unrestricted_methods').getLinkedMeetingDate()" \
                       ".strftime('%Y%m%d') or '') + '/' + str(here.getItemNumber(relativeTo='meeting', " \
                       "for_display=True))"

    llo_item_ref = "python: item.adapted().compute_item_ref()"

    def setUp(self):
        super(testCustomMeetingItem, self).setUp()
        self._activate_wfas(('return_to_proposing_group_with_last_validation', 'removed'), keep_existing=True)
        self.meetingConfig.setItemReferenceFormat(self.llo_item_ref)
        self.meetingConfig2.setItemReferenceFormat(self.llo_item_ref)

    def tearDown(self):
        self.meetingConfig.setItemReferenceFormat(self.default_item_ref)
        self.meetingConfig2.setItemReferenceFormat(self.default_item_ref)

    def test_showFollowUp(self):
        self.changeUser("pmManager")
        meeting = self._createMeetingWithItems()
        ordered_items = meeting.get_items(ordered=True)
        self.assertGreater(len(ordered_items), 5)

        def get_showFollowUp_and_purge_cache(item):
            showFollowUp = item.adapted().showFollowUp()
            getRequest().set('Products.MeetingLalouviere.showFollowUp_cachekey', None)
            return showFollowUp

        for item in ordered_items:
            self.assertEqual(item.query_state(), 'presented')
            self.assertTrue(get_showFollowUp_and_purge_cache(item))
            self.changeUser("pmFollowup1")
            self.assertFalse(get_showFollowUp_and_purge_cache(item))
            self.changeUser("pmFollowup2")
            self.assertFalse(get_showFollowUp_and_purge_cache(item))
            self.changeUser("pmManager")

        self.freezeMeeting(meeting)

        for item in ordered_items:
            self.assertEqual(item.query_state(), 'itemfrozen')
            self.assertTrue(get_showFollowUp_and_purge_cache(item))
            self.changeUser("pmFollowup1")
            self.assertFalse(get_showFollowUp_and_purge_cache(item))
            self.changeUser("pmFollowup2")
            self.assertFalse(get_showFollowUp_and_purge_cache(item))
            self.changeUser("pmManager")

        self.decideMeeting(meeting)
        item = ordered_items[0]
        self.do(item, 'accept')
        self.assertEqual(item.query_state(), 'accepted')
        self.assertTrue(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup1")
        self.assertTrue(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup2")
        self.assertFalse(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmManager")
        item = ordered_items[1]
        self.do(item, 'accept_but_modify')
        self.assertEqual(item.query_state(), 'accepted_but_modified')
        self.assertTrue(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup1")
        self.assertTrue(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup2")
        self.assertFalse(get_showFollowUp_and_purge_cache(item))

        self.changeUser("pmManager")
        item = ordered_items[2]
        self.do(item, 'delay')
        self.assertEqual(item.query_state(), 'delayed')
        self.assertTrue(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup1")
        self.assertTrue(get_showFollowUp_and_purge_cache(item))

        # returned_to_proposing_group items must not display followp
        self.changeUser("pmManager")
        item = ordered_items[3]
        self.do(item, 'return_to_proposing_group')
        self.assertEqual(item.query_state(), 'returned_to_proposing_group')
        self.assertFalse(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup1")
        self.assertFalse(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup2")
        self.assertFalse(get_showFollowUp_and_purge_cache(item))

        self.changeUser("pmManager")
        item = ordered_items[4]
        self.do(item, 'refuse')
        self.assertEqual(item.query_state(), 'refused')
        self.assertTrue(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup1")
        self.assertFalse(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup2")
        self.assertTrue(get_showFollowUp_and_purge_cache(item))

        self.changeUser("pmManager")
        item = ordered_items[5]
        self.do(item, 'remove')
        self.assertEqual(item.query_state(), 'removed')
        self.assertTrue(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup1")
        self.assertFalse(get_showFollowUp_and_purge_cache(item))
        self.changeUser("pmFollowup2")
        self.assertTrue(get_showFollowUp_and_purge_cache(item))

    def test_item_ref_college(self):
        self.meetingConfig.setUsedMeetingAttributes(self.meetingConfig.getUsedMeetingAttributes() + ("meeting_number",))
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems()
        ordered_items = meeting.get_items(ordered=True)
        self.freezeMeeting(meeting)
        date_formatted = meeting.date.strftime("%Y%m%d")
        expected = [
            date_formatted + "-1/DEVEL/1",
            date_formatted + "-1/DEVEL/2",
            date_formatted + "-1/DEVEL/3",
            date_formatted + "-1/DEVEL/4",
            date_formatted + "-1/DEVIL/5",
            date_formatted + "-1/DEVIL/6",
            date_formatted + "-1/DEVIL/7",
        ]
        self.assertListEqual(expected, [item.getItemReference() for item in ordered_items])

    def test_item_ref_council(self):
        self.setMeetingConfig(self.meetingConfig2.getId())
        self.meetingConfig.setUsedMeetingAttributes(self.meetingConfig.getUsedMeetingAttributes() + ("meeting_number",))
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems()
        ordered_items = meeting.get_items(ordered=True)
        self.freezeMeeting(meeting)
        date_formatted = meeting.date.strftime("%Y%m%d")
        expected = [
            date_formatted + "/DEVEL/1",
            date_formatted + "-HC2/DEVIL/2",
            date_formatted + "-HC2/DEVEL/3",
            date_formatted + "/DEVIL/4",
            date_formatted + "/DEVIL/5",
        ]
        self.assertListEqual(expected, [item.getItemReference() for item in ordered_items])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomMeetingItem, prefix="test_"))
    return suite
