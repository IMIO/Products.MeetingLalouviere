# -*- coding: utf-8 -*-
#
# File: testValidators.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testValidators import testValidators as mctv
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testValidators(MeetingLalouviereTestCase, mctv):
    """
    Tests the validators.
    """


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testValidators, prefix="test_"))
    return suite
