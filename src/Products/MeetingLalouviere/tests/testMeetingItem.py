# -*- coding: utf-8 -*-
#
# File: testMeetingItem.py
#
# Copyright (c) 2007-2012 by CommunesPlone.org
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

from Products.MeetingLalouviere.config import *
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import \
    MeetingLalouviereTestCase
from Products.PloneMeeting.tests.testMeetingItem import testMeetingItem as pmtmi


class testMeetingItem(MeetingLalouviereTestCase, pmtmi):
    """
        Tests the MeetingItem class methods.
    """

    def afterSetUp(self):
        MeetingLalouviereTestCase.afterSetUp(self)

    def afterSetUpPM(self):
        """
            The afterSetUp method from PloneMeeting must be called in each test
            and not in afterSetUp method of this class.
            If not, this test transaction doesn't contain what's done
            in plonemeeting afterSetUp and it is not cleared
        """
        pass
        #pmtmi.afterSetUp(self)

    def test_mll_VerifyTestNumbers(self):
        """
            We verify that there are the same test methods in original product and this sub-product
        """
        tpm = self.getTestMethods(pmtmi, 'test')
        tmc = self.getTestMethods(testMeetingItem, 'test_mll_call_')
        missing = []
        for key in tpm:
            key2 = key.replace('test', 'test_mll_call_')
            if not key2 in tmc:
                missing.append(key)
        if len(missing):
            self.fail("missing test methods %s from PloneMeeting test class '%s'" % (missing, 'testMeetingItem'))

    def test_mll_call_ListProposingGroup(self):
        """
           Run the testListProposingGroup from PloneMeeting
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.testListProposingGroup(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtmi.testListProposingGroup(self)

    def test_mll_call_UsedColorSystemGetColoredLink(self):
        """
           Test the selected system of color while getting a colored link
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.testUsedColorSystemGetColoredLink(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtmi.testUsedColorSystemGetColoredLink(self)

    def test_mll_call_UsedColorSystemShowColors(self):
        """
           Test the selected system of color
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.testUsedColorSystemShowColors(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtmi.testUsedColorSystemShowColors(self)

    def test_mll_call_SendItemToOtherMC(self):
        '''Test the send an item to another meetingConfig functionnality'''
        #we do the test for the college config, to send an item to the council
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        self._adaptCategoriesForTest(self.meetingConfig)
        pmtmi.testSendItemToOtherMC(self)

    def test_mll_call_SelectableCategories(self):
        '''Categories are available if isSelectable returns True.  By default,
           isSelectable will return active categories for wich intersection
           between MeetingCategory.usingGroups and current member
           proposingGroups is not empty.'''
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        self.meetingConfig.useGroupsAsCategories = False
        self._adaptCategoriesForTest(self.meetingConfig)
        pmtmi.testSelectableCategories(self)

    def _getNecessaryMeetingTransitionsToAcceptItem(self):
        '''Returns the necessary transitions to trigger on the Meeting before being
           able to accept an item.'''
        return ['freeze', 'decide', ]

    def test_mll_call_AddAutoCopyGroups(self):
        '''Test the functionnality of automatically adding some copyGroups depending on
           the TAL expression defined on every MeetingGroup.asCopyGroupOn.'''
        pmtmi.testAddAutoCopyGroups(self)

    def test_mll_call_ItemAdvise(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.testItemAdvise(self)

    def test_mll_call_ItemIsSigned(self):
        '''Not used in MeetingLalouviere, already tested in PloneMeeting.'''
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_mll_'))
    return suite
