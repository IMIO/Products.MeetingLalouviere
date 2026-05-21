# -*- coding: utf-8 -*-
#
# File: testAnnexes.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testAnnexes import testAnnexes as mcta
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testAnnexes(MeetingLalouviereTestCase, mcta):
    """ """


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testAnnexes, prefix="test_"))
    return suite
