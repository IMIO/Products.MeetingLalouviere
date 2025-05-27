# -*- coding: utf-8 -*-
#
# File: testColumns.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testColumns import testColumns as mctc
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testColumns(MeetingLalouviereTestCase, mctc):
    """ """


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testColumns, prefix="test_"))
    return suite
