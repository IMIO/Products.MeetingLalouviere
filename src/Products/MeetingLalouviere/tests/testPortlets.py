# -*- coding: utf-8 -*-
#
# File: testPortlets.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testPortlets import testPortlets as mctp
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testPortlets(MeetingLalouviereTestCase, mctp):
    """Tests the portlets methods."""


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testPortlets, prefix="test_"))
    return suite
