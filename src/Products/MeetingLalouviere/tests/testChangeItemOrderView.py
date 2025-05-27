# -*- coding: utf-8 -*-
#
# File: testChangeItemOrderView.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testChangeItemOrderView import testChangeItemOrderView as mctciov
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testChangeItemOrderView(MeetingLalouviereTestCase, mctciov):
    """Tests the ChangeItemOrderView class methods."""


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testChangeItemOrderView, prefix="test_"))
    return suite
