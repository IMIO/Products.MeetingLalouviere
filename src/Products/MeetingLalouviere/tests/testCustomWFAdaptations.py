# -*- coding: utf-8 -*-

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.MeetingCommunes.tests.testCustomWFAdaptations import testCustomWFAdaptations as mctcwfa


class testCustomWFAdaptations(mctcwfa, MeetingLalouviereTestCase):
    ''' '''


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomWFAdaptations, prefix='test_'))
    return suite