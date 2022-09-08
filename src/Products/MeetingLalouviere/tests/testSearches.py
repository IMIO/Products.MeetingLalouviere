# -*- coding: utf-8 -*-
#
# File: testMeetingConfig.py
#
# Copyright (c) 2015 by Imio.be
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

from Products.MeetingCommunes.tests.testSearches import testSearches as mcts
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)
from Products.PloneMeeting.tests.PloneMeetingTestCase import pm_logger

from Products.CMFCore.permissions import ModifyPortalContent
from collective.compoundcriterion.interfaces import ICompoundCriterionFilter
from imio.helpers.cache import cleanRamCacheFor
from zope.component import getAdapter

from Products.PloneMeeting.adapters import _find_nothing_query


class testSearches(MeetingLalouviereTestCase, mcts):
    """Test searches."""

    # def setUp(self):
    #     super(testSearches, self).setUp()
    #     self.switch_reviewer_groups()

    def test_pm_SearchItemsToValidateOfHighestHierarchicLevelReturnsEveryLevels(self):
        pass

    def test_pm_SearchItemsToValidateOfHighestHierarchicLevel(self):
        pass

    def test_pm_SearchItemsToCorrectToValidateOfHighestHierarchicLevel(self):
        pass

    def _test_reviewer_groups(self, developersItem, vendorsItem, collection):
        use_cases = [
            {'transition_user_1': 'pmCreator1',
             'transition_user_2': 'pmCreator2',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_servicehead',
             'check_user_1': 'pmServiceHead1',
             'check_user_2': 'pmServiceHead2'},
            {'transition_user_1': 'pmServiceHead1',
             'transition_user_2': 'pmServiceHead2',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_officemanager',
             'check_user_1': 'pmOfficeManager1',
             'check_user_2': 'pmOfficeManager2'},
            {'transition_user_1': 'pmOfficeManager1',
             'transition_user_2': 'pmOfficeManager2',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_divisionhead',
             'check_user_1': 'pmDivisionHead1',
             'check_user_2': 'pmDivisionHead2'},
            {'transition_user_1': 'pmDivisionHead1',
             'transition_user_2': 'pmDivisionHead2',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_director',
             'check_user_1': 'pmDirector1',
             'check_user_2': 'pmDirector2'},
            {'transition_user_1': 'pmDirector1',
             'transition_user_2': 'pmDirector2',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_dg',
             'check_user_1': 'pmDirector1',
             'check_user_2': 'pmDirector2'},
            {'transition_user_1': 'pmDirector1',
             'transition_user_2': 'pmDirector2',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_alderman',
             'check_user_1': 'pmAlderman1',
             'check_user_2': 'pmAlderman2'},
        ]
        for use_case in use_cases:
            self.changeUser(use_case['transition_user_1'])
            self.do(developersItem, use_case['transition'])
            self.changeUser(use_case['transition_user_2'])
            self.do(vendorsItem, use_case['transition'])

            # pmReviewer 1 may only edit developersItem
            self.changeUser(use_case['check_user_1'])
            self.assertTrue(self.hasPermission(ModifyPortalContent, developersItem))
            cleanRamCacheFor(
                'Products.PloneMeeting.adapters.query_itemstocorrecttovalidateofeveryreviewerlevelsandlowerlevels')
            res = collection.results()
            self.assertEqual(res.length, 1)
            self.assertEqual(res[0].UID, developersItem.UID())

            # pmReviewer 2 may only edit vendorsItem
            self.changeUser(use_case['check_user_2'])
            self.assertTrue(self.hasPermission(ModifyPortalContent, vendorsItem))
            cleanRamCacheFor(
                'Products.PloneMeeting.adapters.query_itemstocorrecttovalidateofeveryreviewerlevelsandlowerlevels')
            res = collection.results()
            self.assertEqual(res.length, 1)
            self.assertEqual(res[0].UID, vendorsItem.UID())


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testSearches, prefix="test_"))
    return suite
