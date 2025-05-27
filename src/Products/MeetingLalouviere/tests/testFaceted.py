# -*- coding: utf-8 -*-
#
# File: testFaceted.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testFaceted import testFaceted as mctf
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testFaceted(MeetingLalouviereTestCase, mctf):
    """Tests the faceted navigation."""

    def _orgs_to_exclude_from_filter(self):
        return (self.direction_generale_validation_uid, self.referent_integrite_uid)


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testFaceted, prefix="test_"))
    return suite
