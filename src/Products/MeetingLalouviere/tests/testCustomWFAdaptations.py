# -*- coding: utf-8 -*-

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.MeetingCommunes.tests.testCustomWFAdaptations import testCustomWFAdaptations as mctcwfa
from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations
from Products.PloneMeeting.tests.PloneMeetingTestCase import pm_logger


class testCustomWFAdaptations(mctcwfa, MeetingLalouviereTestCase):
    ''' '''


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomWFAdaptations, prefix='test_'))
    return suite