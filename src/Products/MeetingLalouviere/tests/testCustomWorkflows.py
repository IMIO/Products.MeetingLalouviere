# -*- coding: utf-8 -*-
#
# File: testWorkflows.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testCustomWorkflows import testCustomWorkflows as mctcw
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testCustomWorkflows(mctcw, MeetingLalouviereTestCase):
    """Tests the default workflows implemented in PloneMeeting."""


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testCustomWorkflows, prefix="test_"))
    return suite
