# -*- coding: utf-8 -*-
#
# File: testToolPloneMeeting.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testToolPloneMeeting import testToolPloneMeeting as mctt
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testToolPloneMeeting(MeetingLalouviereTestCase, mctt):
    """Tests the ToolPloneMeeting class methods."""

    def test_pm_Get_selectable_orgs(self):
        """Returns selectable organizations depending on :
        - MeetingConfig.usingGroups;
        - user is creator for if only_selectable=True."""
        cfg = self.meetingConfig
        cfg2 = self.meetingConfig
        self.changeUser("pmCreator1")
        self.assertEqual(self.tool.get_selectable_orgs(cfg), [self.developers])
        self.assertEqual(self.tool.get_selectable_orgs(cfg2), [self.developers])
        self.assertEqual(
            self.tool.get_selectable_orgs(cfg, only_selectable=False),
            [self.developers,
             self.vendors,
             self.direction_generale_validation,
             self.referent_integrite],
        )
        # do not return more than MeetingConfig.usingGroups
        cfg2.setUsingGroups([self.vendors_uid])
        self.assertEqual(self.tool.get_selectable_orgs(cfg2), [])
        self.assertEqual(
            self.tool.get_selectable_orgs(cfg2, only_selectable=False),
            [self.vendors])

    def test_pm_CloneItemKeepProposingGroupWithGroupInCharge(self):
        """Disable "referent-integrite" before testing."""
        self.changeUser('siteadmin')
        self._select_organization(self.referent_integrite_uid, remove=True)
        super(testToolPloneMeeting, self).test_pm_CloneItemKeepProposingGroupWithGroupInCharge()


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testToolPloneMeeting, prefix="test_"))
    return suite
