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

    def setUp(self):
        super(testSearches, self).setUp()
        self._removePrincipalFromGroups('pmManager', [self.direction_generale_directors])

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
             'check_user_1': 'pmDg',
             'check_user_2': 'pmDg'},
            {'transition_user_1': 'pmDg',
             'transition_user_2': 'pmDg',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_alderman',
             'check_user_1': 'pmAlderman1',
             'check_user_2': 'pmAlderman2'},
        ]
        for use_case in use_cases:
            self.changeUser(use_case['transition_user_1'])
            self.do(developersItem, use_case['transition'])
            # pmReviewer 1 may only edit developersItem
            self.changeUser(use_case['check_user_1'])
            self.assertTrue(self.hasPermission(ModifyPortalContent, developersItem))
            cleanRamCacheFor(
                'Products.PloneMeeting.adapters.query_itemstocorrecttovalidateofeveryreviewerlevelsandlowerlevels')
            res = collection.results()
            self.assertEqual(res.length, 1)
            self.assertEqual(res[0].UID, developersItem.UID())

            self.changeUser(use_case['transition_user_2'])
            self.do(vendorsItem, use_case['transition'])
            # pmReviewer 2 may only edit vendorsItem
            self.changeUser(use_case['check_user_2'])
            self.assertTrue(self.hasPermission(ModifyPortalContent, vendorsItem))
            cleanRamCacheFor(
                'Products.PloneMeeting.adapters.query_itemstocorrecttovalidateofeveryreviewerlevelsandlowerlevels')
            res = collection.results()
            if use_case['check_user_2'] == 'pmDg':
                self.assertEqual(res.length, 2)
            else:
                self.assertEqual(res.length, 1)
            self.assertEqual(res[0].UID, vendorsItem.UID())

    def test_pm_SearchItemsToValidateOfMyReviewerGroups(self):
        '''Test the 'items-to-validate-of-my-reviewer-groups' adapter.
           This should return a list of items a user could validate at any level,
           so not only his highest hierarchic level.  This will return finally every items
           corresponding to Plone reviewer groups the user is in.'''
        cfg = self.meetingConfig
        self.changeUser('admin')

        # activate the 'pre_validation' wfAdaptation if it exists in current profile...
        # if not, then reviewers must be at least 2 elements long
        reviewers = cfg.reviewersFor()
        if not len(reviewers) > 1:
            self._enablePrevalidation(cfg)
        if not len(reviewers) > 1:
            pm_logger.info("Could not launch test 'test_pm_SearchItemsToValidateOfMyReviewerGroups' "
                           "because we need at least 2 levels of item validation.")

        # first test the generated query
        adapter = getAdapter(cfg,
                             ICompoundCriterionFilter,
                             name='items-to-validate-of-my-reviewer-groups')
        # if user si not a reviewer, we want the search to return
        # nothing so the query uses an unknown review_state
        itemTypeName = cfg.getItemTypeName()
        self.assertEqual(adapter.query, _find_nothing_query(itemTypeName))
        # for a reviewer, query is correct
        self.changeUser('pmReviewer1')
        # only reviewer for highest level
        reviewers = cfg.reviewersFor()
        self._removeUsersFromEveryGroups(['pmReviewer1'])
        self._addPrincipalToGroup('pmReviewer1',
                                  "{0}_{1}".format(self.developers_uid, reviewers.keys()[0]))
        cleanRamCacheFor('Products.PloneMeeting.adapters.query_itemstovalidateofmyreviewergroups')
        query = adapter.query
        query['reviewProcessInfo']['query'].sort()
        states = reviewers.values()[0]
        self.assertEqual({'portal_type': {'query': itemTypeName},
                          'reviewProcessInfo': {
                              'query': sorted(['{0}__reviewprocess__{1}'.format(self.developers_uid, state)
                                               for state in states])}},
                         adapter.query)

        # now do the query
        # this adapter is not used by default, but is intended to be used with
        # the "searchitemstovalidate" collection so use it with it
        collection = cfg.searches.searches_items.searchitemstovalidate
        patchedQuery = list(collection.query)
        patchedQuery[0]['v'] = 'items-to-validate-of-my-reviewer-groups'
        collection.query = patchedQuery

        # create 2 items
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem')
        item2 = self.create('MeetingItem')
        self.do(item1, self.TRANSITIONS_FOR_PROPOSING_ITEM_1[0])
        self.do(item2, self.TRANSITIONS_FOR_PROPOSING_ITEM_1[0])
        cleanRamCacheFor('Products.PloneMeeting.adapters.query_itemstovalidateofmyreviewergroups')
        self.failIf(collection.results())
        # as first level user, he will see items
        self.changeUser('pmReviewerLevel1')
        cleanRamCacheFor('Products.PloneMeeting.adapters.query_itemstovalidateofmyreviewergroups')
        self.assertEqual(collection.results().length, 2)
        # as second level user, he will not see items of first level also
        self.changeUser('pmDirector1')
        cleanRamCacheFor('Products.PloneMeeting.adapters.query_itemstovalidateofmyreviewergroups')
        self.assertEqual(collection.results().length, 2)

        # he can access first validation level items
        cleanRamCacheFor('Products.PloneMeeting.adapters.query_itemstovalidateofmyreviewergroups')
        self.assertEqual(collection.results().length, 2)
        # move item1 to last validation level
        self.proposeItem(item1)
        # both items still returned by the search for 'pmReviewerLevel2'
        cleanRamCacheFor('Products.PloneMeeting.adapters.query_itemstovalidateofmyreviewergroups')
        self.assertEqual(collection.results().length, 1)
        self.changeUser('pmAlderman1')
        self.assertEqual(collection.results().length, 1)
        # but now, the search only returns item2 to 'pmReviewerLevel1'
        self.changeUser('pmReviewerLevel1')
        cleanRamCacheFor('Products.PloneMeeting.adapters.query_itemstovalidateofmyreviewergroups')
        self.assertEqual(collection.results().length, 1)
        self.failUnless(collection.results()[0].UID == item2.UID())


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testSearches, prefix="test_"))
    return suite
