# -*- coding: utf-8 -*-
from datetime import datetime

from Products.MeetingCommunes.tests.testCustomViews import testCustomViews as mctcv
from Products.MeetingLalouviere.config import (
    COUNCIL_MEETING_COMMISSION_IDS_2020,
    COUNCIL_MEETING_COMMISSION_IDS_2019,
    COUNCIL_MEETING_COMMISSION_IDS_2013,
    COUNCIL_COMMISSION_IDS,
)
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)

from DateTime import DateTime


class testCustomViews(mctcv, MeetingLalouviereTestCase):
    """
        Tests the custom views
    """


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testCustomViews, prefix="test_"))
    return suite
