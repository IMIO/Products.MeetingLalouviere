# -*- coding: utf-8 -*-

from Products.MeetingCommunes.tests.testCustomWFAdaptations import testCustomWFAdaptations as mctcwfa
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testCustomWFAdaptations(mctcwfa, MeetingLalouviereTestCase):
    ''' '''


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomWFAdaptations, prefix='test_'))
    return suite
