# -*- coding: utf-8 -*-
from datetime import datetime

from Products.MeetingCommunes.tests.testCustomViews import testCustomViews as mctcv
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)


class testCustomViews(mctcv, MeetingLalouviereTestCase):
    """
        Tests the custom views
    """


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testCustomViews, prefix="test_"))
    return suite
