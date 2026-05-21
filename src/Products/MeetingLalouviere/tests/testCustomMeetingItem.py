# -*- coding: utf-8 -*-
#
# File: testCustomMeetingItem.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testCustomMeetingItem import testCustomMeetingItem as mctcm
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from zope.globalrequest import getRequest


class testCustomMeetingItem(mctcm, MeetingLalouviereTestCase):
    """
    Tests the MeetingItem adapted methods
    """

    default_item_ref = (
        "python: 'Ref. ' + (here.hasMeeting() and "
        "here.restrictedTraverse('@@pm_unrestricted_methods').getLinkedMeetingDate()"
        ".strftime('%Y%m%d') or '') + '/' + str(here.getItemNumber(relativeTo='meeting', "
        "for_display=True))"
    )

    llo_item_ref = "python: item.adapted().compute_item_ref()"

    def setUp(self):
        super(testCustomMeetingItem, self).setUp()
        self._activate_wfas(("return_to_proposing_group_with_last_validation", "removed"), keep_existing=True)
        self.meetingConfig.setItemReferenceFormat(self.llo_item_ref)
        self.meetingConfig2.setItemReferenceFormat(self.llo_item_ref)

    def tearDown(self):
        self.meetingConfig.setItemReferenceFormat(self.default_item_ref)
        self.meetingConfig2.setItemReferenceFormat(self.default_item_ref)

    def test_item_ref_college(self):
        self.meetingConfig.setUsedMeetingAttributes(self.meetingConfig.getUsedMeetingAttributes() + ("meeting_number",))
        self.changeUser("pmManager")
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
        self.changeUser("pmManager")
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
