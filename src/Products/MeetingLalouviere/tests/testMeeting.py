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
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.MeetingCommunes.tests.testMeeting import testMeeting as mctm
from Products.PloneMeeting.config import MEETING_STATES_ACCEPTING_ITEMS

class testMeeting(MeetingLalouviereTestCase, mctm):
    """Tests the Meeting class methods."""

    def test_subproduct_call_AvailableItems(self):
        """
          By default, available items should be :
          - validated items
          - with no preferred meeting
          - items for wich the preferredMeeting is not a future meeting
        """
        self.changeUser('pmManager')
        for meetingConfig in (self.meetingConfig.getId(), self.meetingConfig2.getId()):
            self.setMeetingConfig(meetingConfig)
            self._checkAvailableItems()

    def _checkAvailableItems(self):
        """Helper method for test_pm_AvailableItems."""
        #create 3 meetings
        #we can do every steps as a MeetingManager
        self.changeUser('pmManager')
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
        i1.setTitle('i1')
        i1.setDecision('<p>Decision item 1</p>')
        i2 = self.create('MeetingItem')
        i2.setPreferredMeeting(m2.UID())
        i2.setTitle('i2')
        i2.setDecision('<p>Decision item 2</p>')
        i3 = self.create('MeetingItem')
        i3.setPreferredMeeting(m3.UID())
        i3.setTitle('i3')
        i3.setDecision('<p>Decision item 3</p>')
        # set a category if the meetingConfig use it
        if not self.meetingConfig.getUseGroupsAsCategories():
            i1.setCategory('development')
            i2.setCategory('research')
            i3.setCategory('events')
        i1.reindexObject()
        i2.reindexObject()
        i3.reindexObject()
        # for now, no items are presentable...
        # except if items are already 'validated', this could be the case when using
        # 'items_come_validated' wfAdaptation or if item initial_state is 'validated'
        if not self.wfTool[i1.getWorkflowName()].initial_state == 'validated':
            self.assertEquals(len(m1.adapted().getAvailableItems()), 0)
            self.assertEquals(len(m2.adapted().getAvailableItems()), 0)
            self.assertEquals(len(m3.adapted().getAvailableItems()), 0)
        # validate the items
        for item in (i1, i2, i3):
            self.validateItem(item)
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

        # if a meeting is frozen, it will only accept late items
        # to be able to freeze a meeting, it must contains at least one item...
        self.setCurrentMeeting(m1)
        self.presentItem(i1)
        self.freezeMeeting(m1)
        self.assertTrue(not m1.adapted().getAvailableItems())
        # turn i2 into a late item
        proposedState = self.WF_STATE_NAME_MAPPINGS['proposed']
        # if current workflow does not use late items, we pass this test...
        i2Wf = self.wfTool.getWorkflowsFor(i2)[0]
        if proposedState in i2Wf.states.keys():
            self.backToState(i2, proposedState)
            i2.setPreferredMeeting(m1.UID())
            i2.reindexObject()
            self.validateItem(i2)
            # i1 is a late item
            if self.meetingConfig.getId() != 'meeting-config-council':
                self.assertTrue(i2.wfConditions().isLateFor(m1))
                self.assertTrue([item.UID for item in m1.adapted().getAvailableItems()] == [i2.UID()])

        # if a meeting is not in a MEETING_STATES_ACCEPTING_ITEMS state
        # it can not accept any kind of items, getAvailableItems returns []
        self.closeMeeting(m1)
        self.assertTrue(not m1.queryState() in MEETING_STATES_ACCEPTING_ITEMS)
        self.assertTrue(not m1.adapted().getAvailableItems())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeeting, prefix='test_subproduct_'))
    return suite
