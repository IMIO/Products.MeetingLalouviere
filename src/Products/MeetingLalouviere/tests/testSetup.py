# -*- coding: utf-8 -*-
#
# File: testSetup.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testSetup import testSetup as mcts
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testSetup(MeetingLalouviereTestCase, mcts):
    """Tests the setup, especially registered profiles."""


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testSetup, prefix="test_"))
    return suite
