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
from Products.PloneMeeting.config import MEETINGREVIEWERS
from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations
from Products.PloneMeeting.tests.PloneMeetingTestCase import pm_logger

from collective.compoundcriterion.interfaces import ICompoundCriterionFilter
from imio.helpers.cache import cleanRamCacheFor
from zope.component import getAdapter


class testSearches(MeetingLalouviereTestCase, mcts):
    """Test searches."""

    def test_pm_SearchItemsToValidateOfHighestHierarchicLevel(self):
        """Test the searchItemsToValidateOfHighestHierarchicLevel method.
           This should return a list of items a user ***really*** has to validate.
           Items to validate are items for which user is a reviewer and only regarding
           his higher hierarchic level.
           So a reviewer level 1 and level 2 will only see items in level 2, a reviewer in level
           1 (only) will only see items in level 1."""
        self.changeUser("admin")
        cfg = self.meetingConfig
        itemTypeName = cfg.getItemTypeName()

        # first test the generated query
        adapter = getAdapter(
            cfg,
            ICompoundCriterionFilter,
            name="items-to-validate-of-highest-hierarchic-level",
        )
        # if user si not a reviewer, we want the search to return
        # nothing so the query uses an unknown review_state
        self.assertEquals(
            adapter.query, {"review_state": {"query": ["unknown_review_state"]}}
        )
        # for a reviewer, query is correct
        self.changeUser("pmReviewer1")
        cleanRamCacheFor(
            "Products.PloneMeeting.adapters.query_itemstovalidateofhighesthierarchiclevel"
        )
        self.assertEquals(
            adapter.query,
            {
                "getProposingGroup": {"query": [self.developers_uid]},
                "portal_type": {"query": itemTypeName},
                "review_state": {"query": self._stateMappingFor("proposed")},
            },
        )

        # activate 'prevalidation' if necessary
        if (
            "prereviewers" in MEETINGREVIEWERS
            and not "pre_validation" in cfg.getWorkflowAdaptations()
        ):
            cfg.setWorkflowAdaptations("pre_validation")
            performWorkflowAdaptations(cfg, logger=pm_logger)
        # now do the query
        # this adapter is used by the "searchitemstovalidate"
        collection = cfg.searches.searches_items.searchitemstovalidate
        # create an item
        self.changeUser("pmCreator1")
        item = self.create("MeetingItem")
        # jump to first level of validation
        self.do(item, self.TRANSITIONS_FOR_PROPOSING_ITEM_1[0])
        cleanRamCacheFor(
            "Products.PloneMeeting.adapters.query_itemstovalidateofhighesthierarchiclevel"
        )
        self.failIf(collection.getQuery())
        self.changeUser("pmReviewerLevel1")
        cleanRamCacheFor(
            "Products.PloneMeeting.adapters.query_itemstovalidateofhighesthierarchiclevel"
        )
        self.failUnless(collection.getQuery())
        # now as 'pmReviewerLevel2', the item should not be returned
        # as he only see items of his highest hierarchic level
        self.changeUser("pmReviewerLevel2")
        cleanRamCacheFor(
            "Products.PloneMeeting.adapters.query_itemstovalidateofhighesthierarchiclevel"
        )
        self.failIf(collection.getQuery())
        # pass the item to second last level of hierarchy, where 'pmReviewerLevel2' is reviewer for
        self.changeUser("pmReviewerLevel1")
        # jump to last level of validation
        self.proposeItem(item)
        cleanRamCacheFor(
            "Products.PloneMeeting.adapters.query_itemstovalidateofhighesthierarchiclevel"
        )
        self.failIf(collection.getQuery())
        # alderman don't see the item validated to director
        self.changeUser("pmReviewerLevel2")
        cleanRamCacheFor(
            "Products.PloneMeeting.adapters.query_itemstovalidateofhighesthierarchiclevel"
        )
        self.failIf(collection.getQuery())

        self.changeUser("pmDirector1")
        cleanRamCacheFor(
            "Products.PloneMeeting.adapters.query_itemstovalidateofhighesthierarchiclevel"
        )
        self.failUnless(collection.getQuery())

        # now give a view on the item by 'pmReviewer2' and check if, as a reviewer,
        # the search does returns him the item, it should not as he is just a reviewer
        # but not able to really validate the new item
        cfg.setUseCopies(True)
        cfg.setItemCopyGroupsStates("proposed_to_director")
        item.setCopyGroups(("vendors_reviewers",))
        item.at_post_edit_script()
        self.changeUser("pmReviewer2")
        # the user can see the item
        self.failUnless(self.hasPermission("View", item))
        # but the search will not return it
        cleanRamCacheFor(
            "Products.PloneMeeting.adapters.query_itemstovalidateofhighesthierarchiclevel"
        )
        self.failIf(collection.getQuery())
        # if the item is validated, it will not appear for pmReviewer1 anymore
        self.changeUser("pmReviewer1")
        cleanRamCacheFor(
            "Products.PloneMeeting.adapters.query_itemstovalidateofhighesthierarchiclevel"
        )
        self.failUnless(collection.getQuery())
        self.validateItem(item)
        self.failIf(collection.getQuery())


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testSearches, prefix="test_"))
    return suite
