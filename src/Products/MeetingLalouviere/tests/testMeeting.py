# -*- coding: utf-8 -*-
#
# File: testMeeting.py
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

from DateTime import DateTime
from Products.MeetingLalouviere.config import *
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import \
    MeetingLalouviereTestCase
from Products.PloneMeeting.tests.testMeeting import testMeeting as pmtm


class testMeeting(MeetingLalouviereTestCase, pmtm):
    """
        Tests the Meeting class methods.
        For insertion methods, the 'MeetingManager' here can not trigger every transitions
        so the 'Manager' (admin) creates the meetings
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
        #pmtm.afterSetUp(self)

    def _createMeetingWithItems(self):
        '''Create a meeting with a bunch of items.'''
        meetingDate = DateTime().strftime('%y/%m/%d %H:%M:00')
        meeting = self.create('Meeting', date=meetingDate)
        item1 = self.create('MeetingItem')  # id=o2
        item1.setProposingGroup('vendors')
        item1.setAssociatedGroups(('developers',))
        item1.setPrivacy('public')
        item1.setCategory('commission-travaux')
        item2 = self.create('MeetingItem')  # id=o3
        item2.setProposingGroup('developers')
        item2.setPrivacy('public')
        item2.setCategory('commission-enseignement')
        item3 = self.create('MeetingItem')  # id=o4
        item3.setProposingGroup('vendors')
        item3.setPrivacy('secret')
        item3.setCategory('commission-ag')
        item4 = self.create('MeetingItem')  # id=o5
        item4.setProposingGroup('developers')
        item4.setPrivacy('secret')
        item4.setCategory('commission-enseignement')
        item5 = self.create('MeetingItem')  # id=o6
        item5.setProposingGroup('vendors')
        item5.setPrivacy('public')
        item5.setCategory('commission-travaux')
        for item in (item1, item2, item3, item4, item5):
            for tr in item.wfConditions().transitionsForPresentingAnItem:
                self.do(item, tr)
        return meeting

    def test_mll_VerifyTestNumbers(self):
        """
            We verify that there are the same test methods in original product and this sub-product
        """
        tpm = self.getTestMethods(pmtm, 'test')
        tmc = self.getTestMethods(testMeeting, 'test_mll_call_')
        missing = []
        for key in tpm:
            key2 = key.replace('test', 'test_mll_call_')
            if not key2 in tmc:
                missing.append(key)
        if len(missing):
            self.fail("missing test methods %s from PloneMeeting test class '%s'" % (missing, 'testMeeting'))

    def test_mll_call_InsertItem(self):
        """
          Run the testInsertItem from PloneMeeting
          No recurring items added, just the order is different
          meeting-config-college use "on_proposing_group"
          meeting-config-council use "on_privacy_then_categories"
        """
        #between college and council
        self.login('pmManager')
        for meetingConfig in self.tool.getActiveConfigs():
            meetingConfigId = meetingConfig.getId()
            self.setMeetingConfig(meetingConfigId)
            meeting = self._createMeetingWithItems()
            if meetingConfigId == 'meeting-config-council':
                #here, we do not have recurring items
                expected = ['o2', 'o6', 'o3', 'o5', 'o4']
            if meetingConfigId == 'meeting-config-college':
                #here, we do not have recurring items
                expected = ['o3', 'o5', 'o2', 'o4', 'o6']
            self.assertEquals([item.id for item in meeting.getItemsInOrder()],
                              expected)

    def test_mll_call_AvailableItems(self):
        """
           Run the testAvailableItems from PloneMeeting
           Call default PloneMeeting test for meeting-config-college
           Redefines the test here for meeting-config-council because we need a category
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        self.login('pmManager')
        member = self.portal.portal_membership.getAuthenticatedMember()
        member.addRole('Manager')
        pmtm.testAvailableItems(self)
        #we do the test for the council config
        #the method Meeting.getAvailableItems is adapted
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        #create 3 meetings
        #we can do every steps as a MeetingManager
        meetingDate = DateTime('2008/06/12 08:00:00')
        m1 = self.create('Meeting', date=meetingDate)
        meetingDate = DateTime('2008/06/19 08:00:00')
        m2 = self.create('Meeting', date=meetingDate)
        meetingDate = DateTime('2008/06/26 08:00:00')
        m3 = self.create('Meeting', date=meetingDate)
        #create 3 items
        #one with no preferredMeeting
        #one with m2 preferredMeeting
        #one with m3 as preferredMeeting
        i1 = self.create('MeetingItem')
        i1.setCategory('commission-travaux')
        i1.setTitle('i1')
        i1.reindexObject()
        i2 = self.create('MeetingItem')
        i2.setPreferredMeeting(m2.UID())
        i2.setCategory('commission-travaux')
        i2.setTitle('i2')
        i2.reindexObject()
        i3 = self.create('MeetingItem')
        i3.setPreferredMeeting(m3.UID())
        i3.setCategory('commission-travaux')
        i3.setTitle('i3')
        i3.reindexObject()
        #for now, no items are presentable...
        self.assertEquals(len(m1.adapted().getAvailableItems()), 0)
        self.assertEquals(len(m2.adapted().getAvailableItems()), 0)
        self.assertEquals(len(m3.adapted().getAvailableItems()), 0)
        ##propose and validate the items
        #use transitionsForPresentingAnItem but do not do the last transition
        #that is supposed to be 'present'
        for item in (i1, i2, i3):
            for tr in item.wfConditions().transitionsForPresentingAnItem[:-1]:
                self.do(item, tr)
        #now, check that available items have some respect
        #the first meeting has only one item, the one with no preferred meeting selected
        itemTitles = []
        for brain in m1.adapted().getAvailableItems():
            itemTitles.append(brain.Title)
        self.assertEquals(itemTitles, ['i1', ])
        #the second meeting has 2 items, the no preferred meeting one and the i2
        #for wich we selected this meeting as preferred
        itemTitles = []
        for brain in m2.adapted().getAvailableItems():
            itemTitles.append(brain.Title)
        self.assertEquals(itemTitles, ['i1', 'i2', ])
        #the third has 3 items
        #--> no preferred meeting item
        #--> the second item because the meeting date is in the future
        #--> the i3 where we selected m3 as preferred meeting
        itemTitles = []
        for brain in m3.adapted().getAvailableItems():
            itemTitles.append(brain.Title)
        self.assertEquals(itemTitles, ['i1', 'i2', 'i3', ])
        #Now, specific behaviour : an item is still presentable if the Meeting
        #is 'in_committee' and 'in_council' if the preferredMeeting is selected
        #we in_committee or in_council, a meeting for wich no item is the preferred meeting
        #will not have any available items to present
        self.do(m1, 'setInCommittee')
        self.assertEquals(len(m1.adapted().getAvailableItems()), 0)
        self.do(m1, 'setInCouncil')
        self.assertEquals(len(m1.adapted().getAvailableItems()), 0)
        #if a meeting is the preferred meeting of an item, then is item is still
        #available even if the meeting is 'in_committee' or 'in_council'
        #items are available for preferred meeting but not before the date of the preferred meeting
        self.do(m2, 'setInCommittee')
        self.assertEquals(len(m2.adapted().getAvailableItems()), 1)
        self.do(m2, 'setInCouncil')
        self.assertEquals(len(m2.adapted().getAvailableItems()), 1)
        self.do(m3, 'setInCommittee')
        #items are available for preferred meeting and meeting after the date of the preferred meeting
        self.assertEquals(len(m3.adapted().getAvailableItems()), 2)
        self.do(m3, 'setInCouncil')
        self.assertEquals(len(m3.adapted().getAvailableItems()), 2)

    def test_mll_call_InsertItemCategories(self):
        '''Do not need to test this.  Already tested in MeetingCommunes.
           We only use test_mll_call_InsertItem here above.'''
        pass

    def test_mll_call_InsertItemAllGroups(self):
        '''Do not need to test this.  Already tested in MeetingCommunes.
           We only use test_mll_call_InsertItem here above.'''
        pass

    def test_mll_call_InsertItemPrivacyThenProposingGroups(self):
        '''Do not need to test this.  Already tested in MeetingCommunes.
           We only use test_mll_call_InsertItem here above.'''
        pass

    def test_mll_call_InsertItemPrivacyThenCategories(self):
        '''Do not need to test this.  Already tested in MeetingCommunes.
           We only use test_mll_call_InsertItem here above.'''
        pass

    def test_mll_call_RemoveOrDeleteLinkedItem(self):
        '''Do not need to test this.  Already tested in PloneMeeting.'''
        pass

    def test_mll_call_MeetingNumbers(self):
        '''Do not need to test this.  Already tested in PloneMeeting.'''
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mll_' to avoid launching the tests coming from pmtm
    suite.addTest(makeSuite(testMeeting, prefix='test_mll_'))
    return suite
