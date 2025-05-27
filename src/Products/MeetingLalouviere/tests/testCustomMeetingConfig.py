# -*- coding: utf-8 -*-
#
# File: testCustomMeetingConfig.py
#
# GNU General Public License (GPL)
#

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testCustomMeetingConfig(MeetingLalouviereTestCase):
    """
    Tests the MeetingConfig adapted methods
    """


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testCustomMeetingConfig, prefix="test_"))
    return suite
