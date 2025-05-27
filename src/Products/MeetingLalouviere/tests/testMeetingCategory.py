# -*- coding: utf-8 -*-
#
# File: testMeetingCategory.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testMeetingCategory import testMeetingCategory as mctmc
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testMeetingCategory(MeetingLalouviereTestCase, mctmc):
    """Tests the MeetingCategory class methods."""


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingCategory, prefix="test_"))
    return suite
