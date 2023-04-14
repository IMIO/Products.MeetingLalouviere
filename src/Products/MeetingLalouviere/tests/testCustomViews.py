# -*- coding: utf-8 -*-
from datetime import datetime

from Products.MeetingCommunes.tests.testCustomViews import testCustomViews as mctcv
from Products.MeetingLalouviere.browser.overrides import MLLItemDocumentGenerationHelperView
from Products.MeetingLalouviere.browser.overrides import MLLMeetingDocumentGenerationHelperView
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)


class testCustomViews(mctcv, MeetingLalouviereTestCase):
    """
        Tests the custom views
    """
    def test_MLLMeetingDocumentGenerationHelperView(self):
        """Test if the browser layer is correctly applied"""
        self.changeUser('pmManager')
        meeting = self.create('Meeting')
        view = meeting.restrictedTraverse("@@document-generation")
        helper = view.get_generation_context_helper()
        self.assertTrue(isinstance(helper, MLLMeetingDocumentGenerationHelperView))

    def test_MLLItemDocumentGenerationHelperView(self):
        """Test if the browser layer is correctly applied"""
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        view = item.restrictedTraverse("@@document-generation")
        helper = view.get_generation_context_helper()
        self.assertTrue(isinstance(helper, MLLItemDocumentGenerationHelperView))


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testCustomViews, prefix="test_"))
    return suite
