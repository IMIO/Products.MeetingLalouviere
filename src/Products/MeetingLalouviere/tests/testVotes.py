# -*- coding: utf-8 -*-
#
# File: testViews.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testVotes import testVotes as mctv
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testVotes(MeetingLalouviereTestCase, mctv):
    """ """


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testVotes, prefix="test_"))
    return suite
