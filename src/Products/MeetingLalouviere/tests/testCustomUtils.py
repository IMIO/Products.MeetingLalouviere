# -*- coding: utf-8 -*-
#
# File: testCustomUtils.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testCustomUtils import testCustomUtils as mctcu
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testCustomUtils(mctcu, MeetingLalouviereTestCase):
    """
    Tests the Extensions/utils methods.
    """

    def test_ExportOrgs(self):
        """Bypass as we have additional groups."""
        pass

    def test_ImportOrgs(self):
        """Bypass as we have additional groups."""
        pass


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testCustomUtils, prefix="test_"))
    return suite
