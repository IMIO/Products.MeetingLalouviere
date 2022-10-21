# -*- coding: utf-8 -*-
#
# File: testMeetingConfig.py
#
# Copyright (c) 2007-2013 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
from Products.MeetingCommunes.tests.testMeetingConfig import testMeetingConfig as mctmc
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)

from AccessControl import Unauthorized
from DateTime import DateTime
from collective.contact.plonegroup.utils import select_org_for_function
from ftw.labels.interfaces import ILabeling


class testMeetingConfig(MeetingLalouviereTestCase, mctmc):
    """Call testMeetingConfig tests."""

    def _usersToRemoveFromGroupsForUpdatePersonalLabels(self):
        return ['pmBudgetReviewer1', 'pmFollowup1']

    def test_pm_UpdatePersonalLabels(self):
        """Test the 'updatePersonalLabels' method that will activate a personal label
           on every existing items that were not modified for a given number of days."""
        cfg = self.meetingConfig
        # custom cleanup for profiles having extra roles
        self._removeUsersFromEveryGroups(self._usersToRemoveFromGroupsForUpdatePersonalLabels())
        # do not consider observers group as it changes too often from one WF to another...
        self._removePrincipalFromGroups('pmReviewer1', [self.developers_observers])
        self._removePrincipalFromGroups('pmObserver1', [self.developers_observers])
        self.changeUser('pmManager')
        item1 = self.create('MeetingItem')
        item2 = self.create('MeetingItem')
        # only for Managers
        self.assertRaises(Unauthorized, cfg.updatePersonalLabels)
        self.changeUser('siteadmin')
        # by default, it only updates items not modified for 30 days
        # so calling it will change nothing
        cfg.updatePersonalLabels(personal_labels=['personal-label'])
        item1_labeling = ILabeling(item1)
        item2_labeling = ILabeling(item2)
        self.assertEqual(item1_labeling.storage, {})
        self.assertEqual(item2_labeling.storage, {})
        cfg.updatePersonalLabels(personal_labels=['personal-label'], modified_since_days=0)
        self.assertEqual(
            sorted(item1_labeling.storage['personal-label']),
            ['budgetimpacteditor',
             'pmCreator1',
             'pmCreator1b',
             'pmDirector1',
             'pmDivisionHead1',
             'pmManager',
             'pmOfficeManager1',
             'pmReviewer1',
             'pmReviewerLevel1',
             'pmReviewerLevel2',
             'pmServiceHead1',
             'powerobserver1'])
        self.assertEqual(
            sorted(item2_labeling.storage['personal-label']),
            ['budgetimpacteditor',
             'pmCreator1',
             'pmCreator1b',
             'pmDirector1',
             'pmDivisionHead1',
             'pmManager',
             'pmOfficeManager1',
             'pmReviewer1',
             'pmReviewerLevel1',
             'pmReviewerLevel2',
             'pmServiceHead1',
             'powerobserver1'])
        # method takes into account users able to see the items
        # when item is proposed, powerobserver1 may not see it...
        self.proposeItem(item1)
        cfg.updatePersonalLabels(personal_labels=['personal-label'], modified_since_days=0)
        self.assertEqual(
            sorted(item1_labeling.storage['personal-label']),
            ['pmAlderman1',
             'pmCreator1',
             'pmCreator1b',
             'pmDirector1',
             'pmDivisionHead1',
             'pmManager',
             'pmOfficeManager1',
             'pmReviewer1',
             'pmReviewerLevel1',
             'pmReviewerLevel2',
             'pmServiceHead1'])
        self.assertEqual(
            sorted(item2_labeling.storage['personal-label']),
            ['budgetimpacteditor',
             'pmCreator1',
             'pmCreator1b',
             'pmDirector1',
             'pmDivisionHead1',
             'pmManager',
             'pmOfficeManager1',
             'pmReviewer1',
             'pmReviewerLevel1',
             'pmReviewerLevel2',
             'pmServiceHead1',
             'powerobserver1'])

        # test that only items older than given days are updated
        self.proposeItem(item2)
        item2.setModificationDate(DateTime() - 50)
        item2.reindexObject()
        cfg.updatePersonalLabels(personal_labels=['personal-label'], modified_since_days=30)
        # still old value for item2
        self.assertEqual(
            sorted(item2_labeling.storage['personal-label']),
            ['budgetimpacteditor',
             'pmCreator1',
             'pmCreator1b',
             'pmDirector1',
             'pmDivisionHead1',
             'pmManager',
             'pmOfficeManager1',
             'pmReviewer1',
             'pmReviewerLevel1',
             'pmReviewerLevel2',
             'pmServiceHead1',
             'powerobserver1'])

    def test_pm_ListSelectableAdvisers(self):
        """Vocabulary used for MeetingConfig.selectableAdvisers
           and Meetingconfig.selectableAdviserUsers fields."""
        cfg = self.meetingConfig
        self.changeUser("siteadmin")
        self._select_organization(self.endUsers_uid)
        self.assertListEqual(
            cfg.listSelectableAdvisers().keys(),
            [self.developers_uid, self.direction_generale_uid, self.endUsers_uid, self.vendors_uid])
        # restrict _advisers to developers and vendors
        select_org_for_function(self.developers_uid, "advisers")
        select_org_for_function(self.vendors_uid, "advisers")
        # endUsers no more in selectable advisers
        self.assertListEqual(
            cfg.listSelectableAdvisers().keys(),
            [self.developers_uid, self.vendors_uid])


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingConfig, prefix="test_"))
    return suite
