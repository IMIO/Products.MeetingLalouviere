# -*- coding: utf-8 -*-
#
# File: testAdvices.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testAdvices import testAdvices as mcta
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testAdvices(MeetingLalouviereTestCase, mcta):
    """"""


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testAdvices, prefix="test_"))
    return suite
