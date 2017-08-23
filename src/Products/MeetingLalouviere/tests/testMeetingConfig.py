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
import logging
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.PloneMeeting.tests.testMeetingConfig import testMeetingConfig as pmtmc
from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations

class testMeetingConfig(MeetingLalouviereTestCase, pmtmc):
    '''Call testMeetingConfig tests.'''

    def test_pm_SearchItemsToValidateOfEveryReviewerLevelsAndLowerLevels(self):
        '''Test the searchItemsToValidateOfEveryReviewerLevelsAndLowerLevels method.
           This will return items to validate of his highest hierarchic level and every levels
           under, even if user is not in the corresponding Plone reviewer groups.'''
        logger = logging.getLogger('PloneMeeting: testing')
        # by default we use the 'pre_validation_keep_reviewer_permissions' to check
        # this, but if a subplugin has the right workflow behaviour, this can works also
        # so if we have 'pre_validation_keep_reviewer_permissions' apply it, either,
        # check if self.runSearchItemsToValidateOfEveryReviewerLevelsAndLowerLevelsTest() is True
        if not 'pre_validation_keep_reviewer_permissions' and not \
           self.runSearchItemsToValidateOfEveryReviewerLevelsAndLowerLevelsTest():
            logger.info("Could not launch test 'test_pm_SearchItemsToValidateOfEveryReviewerLevelsAndLowerLevels'"
                        "because we need a correctly configured workflow.")
        if 'pre_validation_keep_reviewer_permissions' in self.meetingConfig.listWorkflowAdaptations():
            self.meetingConfig.setWorkflowAdaptations(('pre_validation_keep_reviewer_permissions', ))
            logger = logging.getLogger('PloneMeeting: testing')
            performWorkflowAdaptations(self.portal, self.meetingConfig, logger)
        # create 2 items
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem')
        item2 = self.create('MeetingItem')
        self.do(item1, self.TRANSITIONS_FOR_PROPOSING_ITEM_1[0])
        self.do(item2, self.TRANSITIONS_FOR_PROPOSING_ITEM_1[0])
        self.failIf(self.meetingConfig.searchItemsToValidateOfEveryReviewerLevelsAndLowerLevels('', '', '', ''))
        # as first level user, he will see items
        self.changeUser('pmReviewerLevel1')
        self.failUnless(len(self.meetingConfig.searchItemsToValidateOfEveryReviewerLevelsAndLowerLevels('', '', '', '')) == 2)
        # as second level user, he will also see items because items are from lower reviewer levels
        self.changeUser('pmReviewerLevel2')
        self.failUnless(len(self.meetingConfig.searchItemsToValidateOfEveryReviewerLevelsAndLowerLevels('', '', '', '')) == 0)
        # now propose item1, both items are still viewable to 'pmReviewerLevel2', but 'pmReviewerLevel1'
        # will only see item of 'his' highest hierarchic level
        self.proposeItem(item1)
        self.failUnless(len(self.meetingConfig.searchItemsToValidateOfEveryReviewerLevelsAndLowerLevels('', '', '', '')) == 1)
        self.changeUser('pmReviewerLevel1')
        self.failUnless(len(self.meetingConfig.searchItemsToValidateOfEveryReviewerLevelsAndLowerLevels('', '', '', '')) == 1)
        self.failUnless(self.meetingConfig.searchItemsToValidateOfEveryReviewerLevelsAndLowerLevels('', '', '', '')[0].UID == item2.UID())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingConfig, prefix='test_pm_'))
    return suite
