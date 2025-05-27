# -*- coding: utf-8 -*-
#
# File: testMeeting.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testMeeting import testMeetingType as mctm
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testMeetingType(MeetingLalouviereTestCase, mctm):
    """Tests the Meeting class methods."""


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingType, prefix="test_"))
    return suite
