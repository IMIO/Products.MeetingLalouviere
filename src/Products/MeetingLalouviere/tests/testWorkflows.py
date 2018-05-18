# -*- coding: utf-8 -*-
#
# File: testWorkflows.py
#
# Copyright (c) 2007-2010 by PloneGov
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

from AccessControl import Unauthorized
from DateTime import DateTime
from plone.app.testing.helpers import setRoles
from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations
from Products.PloneMeeting.tests.PloneMeetingTestCase import pm_logger

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.PloneMeeting.tests.testWorkflows import testWorkflows as pmtw


class testWorkflows(MeetingLalouviereTestCase, pmtw):
    """Tests the default workflows implemented in MeetingLalouviere.

       WARNING:
       The Plone test system seems to be bugged: it does not seem to take into
       account the write_permission and read_permission tags that are defined
       on some attributes of the Archetypes model. So when we need to check
       that a user is not authorized to set the value of a field protected
       in this way, we do not try to use the accessor to trigger an exception
       (self.assertRaise). Instead, we check that the user has the permission
       to do so (getSecurityManager().checkPermission)."""

    def test_pm_WholeDecisionProcess(self):
        """
            This test covers the whole decision workflow. It begins with the
            creation of some items, and ends by closing a meeting.
            This call 2 sub tests for each process : college and council
        """
        # remove recurring items
        self.changeUser('admin')
        self._removeConfigObjectsFor(self.meetingConfig, folders=['recurringitems'])
        self._testWholeDecisionProcessCollege()
        self.setMeetingConfig(self.meetingConfig2.getId())
        # remove recurring items
        self.changeUser('admin')
        self._removeConfigObjectsFor(self.meetingConfig2, folders=['recurringitems'])
        self._testWholeDecisionProcessCouncil()

    def _testWholeDecisionProcessCollege(self):
        '''This test covers the whole decision workflow. It begins with the
           creation of some items, and ends by closing a meeting.'''
        # pmCreator1 creates an item with 1 annex and proposes it
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem', title='The first item')
        self.assertTrue(item1.mayQuickEdit('observations'))
        annex1 = self.addAnnex(item1)
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'proposeToServiceHead')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # the ServiceHead validation level
        self.changeUser('pmServiceHead1')
        self.assertTrue(item1.mayQuickEdit('observations'))
        self.failUnless(self.hasPermission('Modify portal content', (item1, annex1)))
        self.do(item1, 'proposeToOfficeManager')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # the OfficeManager validation level
        self.changeUser('pmOfficeManager1')
        self.assertTrue(item1.mayQuickEdit('observations'))
        self.failUnless(self.hasPermission('Modify portal content', (item1, annex1)))
        self.do(item1, 'proposeToDivisionHead')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # the DivisionHead validation level
        self.changeUser('pmDivisionHead1')
        self.assertTrue(item1.mayQuickEdit('observations'))
        self.failUnless(self.hasPermission('Modify portal content', (item1, annex1)))
        self.do(item1, 'proposeToDirector')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # the Director validation level
        self.changeUser('pmDirector1')
        self.assertTrue(item1.mayQuickEdit('observations'))
        self.failUnless(self.hasPermission('Modify portal content', (item1, annex1)))
        self.do(item1, 'validate')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # pmManager creates a meeting
        self.changeUser('pmManager')
        self.assertTrue(item1.mayQuickEdit('observations'))
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        self.addAnnex(item1, relatedTo='item_decision')
        # pmCreator2 creates and proposes an item
        self.changeUser('pmCreator2')
        item2 = self.create('MeetingItem', title='The second item',
                            preferredMeeting=meeting.UID())
        self.do(item2, 'proposeToServiceHead')
        # pmReviewer1 can not validate the item has not in the same proposing group
        self.changeUser('pmReviewer1')
        self.failIf(self.hasPermission('Modify portal content', item2))
        # even pmManagercan not see/validate an item in the validation queue
        self.changeUser('pmManager')
        self.failIf(self.hasPermission('Modify portal content', item2))
        # do the complete validation
        self.changeUser('admin')
        self.do(item2, 'proposeToOfficeManager')
        self.do(item2, 'proposeToDivisionHead')
        self.do(item2, 'proposeToDirector')
        # pmManager inserts item1 into the meeting and publishes it
        self.changeUser('pmManager')
        managerAnnex = self.addAnnex(item1)
        self.portal.restrictedTraverse('@@delete_givenuid')(managerAnnex.UID())
        self.do(item1, 'present')
        # Now reviewers can't add annexes anymore
        self.changeUser('pmReviewer2')
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        # freeze the meeting
        self.changeUser('pmManager')
        self.do(meeting, 'freeze')
        # validate item2 after meeting freeze
        self.changeUser('pmReviewer2')
        self.do(item2, 'validate')
        self.changeUser('pmManager')
        self.do(item2, 'present')
        self.addAnnex(item2)
        # So now we should have 1 normal item (no recurring items) and one late item in the meeting
        self.failUnless(len(meeting.getItems(listTypes=['normal'])) == 1)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 1)
        self.do(meeting, 'decide')
        self.do(item1, 'accept')
        self.assertEquals(item1.queryState(), 'accepted')
        self.assertEquals(item2.queryState(), 'itemfrozen')
        self.do(meeting, 'close')
        self.assertEquals(item1.queryState(), 'accepted')
        # every items without a decision are automatically accepted
        self.assertEquals(item2.queryState(), 'accepted')

    def _testWholeDecisionProcessCouncil(self):
        """
            This test covers the whole decision workflow. It begins with the
            creation of some items, and ends by closing a meeting.
        """
        # add a recurring item that is inserted when the meeting is 'setInCouncil'
        self.changeUser('admin')
        self.meetingConfig = self.meetingConfig2
        self.meetingConfig.setWorkflowAdaptations('return_to_proposing_group')
        performWorkflowAdaptations(self.meetingConfig, logger=pm_logger)
        self.create('MeetingItemRecurring', title='Rec item 1',
                    proposingGroup='developers',
                    category='deployment',
                    meetingTransitionInsertingMe='setInCouncil')
        # pmCreator1 creates an item with 1 annex and proposes it
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem', title='The first item', autoAddCategory=False)
        self.assertTrue(item1.mayQuickEdit('observations'))
        self.addAnnex(item1)
        # The creator can add a decision annex on created item
        self.addAnnex(item1, relatedTo='item_decision')
        # the item is not proposable until it has a category
        self.failIf(self.transitions(item1))  # He may trigger no more action
        item1.setCategory('deployment')
        self.do(item1, 'proposeToDirector')
        self.failIf(self.hasPermission('Modify portal content', item1))
        # The creator cannot add a decision annex on proposed item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.changeUser('pmDirector1')
        self.assertTrue(item1.mayQuickEdit('observations'))
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'validate')
        self.failIf(self.hasPermission('Modify portal content', item1))
        # The reviewer cannot add a decision annex on validated item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        # pmManager creates a meeting
        self.changeUser('pmManager')
        self.assertTrue(item1.mayQuickEdit('observations'))
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        # The meetingManager can add a decision annex
        self.addAnnex(item1, relatedTo='item_decision')
        # pmCreator2 creates and proposes an item
        self.changeUser('pmCreator2')
        item2 = self.create('MeetingItem', title='The second item',
                            preferredMeeting=meeting.UID())
        item2.setCategory('events')
        self.do(item2, 'proposeToDirector')
        # pmManager inserts item1 into the meeting and freezes it
        self.changeUser('pmManager')
        managerAnnex = self.addAnnex(item1)
        self.portal.restrictedTraverse('@@delete_givenuid')(managerAnnex.UID())
        self.do(item1, 'present')
        self.changeUser('pmCreator1')
        # The creator cannot add any kind of annex on presented item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.changeUser('pmManager')
        self.do(meeting, 'setInCommittee')
        # pmReviewer2 validates item2
        self.changeUser('pmDirector2')
        self.do(item2, 'validate')
        # pmManager inserts item2 into the meeting, as late item, and adds an
        # annex to it
        self.changeUser('pmManager')
        self.do(item2, 'present')
        self.addAnnex(item2)
        # An item is freely addable to a meeting if the meeting is 'open'
        # so in states 'created', 'in_committee' and 'in_council'
        # the 'late items' functionnality is not used
        self.failIf(len(meeting.getItems()) != 2)
        self.failIf(len(meeting.getItems(listTypes=['late'])) != 0)
        # remove the item, set the meeting in council and add it again
        self.backToState(item2, 'validated')
        self.failIf(len(meeting.getItems()) != 1)
        self.do(meeting, 'setInCouncil')
        # remove published meeting to check that item is correctly presented in this cas as well
        self.setCurrentMeeting(None)
        self.do(item2, 'present')
        # setting the meeting in council (setInCouncil) add 1 recurring item...
        self.failIf(len(meeting.getItems()) != 3)
        self.failIf(len(meeting.getItems(listTypes=['late'])) != 0)
        # an item can be send back to the service so MeetingMembers
        # can edit it and send it back to the meeting
        self.changeUser('pmCreator1')
        self.failIf(self.hasPermission('Modify portal content', item1))
        self.changeUser('pmManager')
        # send the item back to the service
        self.do(item1, 'return_to_proposing_group')
        self.changeUser('pmCreator1')
        self.failUnless(self.hasPermission('Modify portal content', item1))
        self.do(item1, 'backTo_item_in_council_from_returned_to_proposing_group')
        self.failIf(self.hasPermission('Modify portal content', item1))
        # item state follow meeting state
        self.changeUser('pmManager')
        self.assertEquals(item1.queryState(), 'item_in_council')
        self.assertEquals(item2.queryState(), 'item_in_council')
        self.do(meeting, 'backToInCommittee')
        self.assertEquals(item1.queryState(), 'item_in_committee')
        self.assertEquals(item2.queryState(), 'item_in_committee')
        self.do(meeting, 'setInCouncil')
        self.assertEquals(item1.queryState(), 'item_in_council')
        self.assertEquals(item2.queryState(), 'item_in_council')
        # while closing a meeting, every no decided items are accepted
        self.do(item1, 'accept_but_modify')
        self.do(meeting, 'close')
        self.assertEquals(item1.queryState(), 'accepted_but_modified')
        self.assertEquals(item2.queryState(), 'accepted')

    def test_pm_RecurringItems(self):
        """
            Tests the recurring items system.
        """
        # we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        # super(testWorkflows, self).test_pm_RecurringItems() workflow is different
        self._checkRecurringItemsCollege()
        # we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        self._testRecurringItemsCouncil()

    def _checkRecurringItemsCollege(self):
        '''Tests the recurring items system.'''
        # First, define recurring items in the meeting config
        self.changeUser('admin')
        # 2 recurring items already exist in the college config, add one supplementary for _init_
        self.create('MeetingItemRecurring', title='Rec item 1',
                    proposingGroup='developers',
                    meetingTransitionInsertingMe='_init_')
        # add 3 other recurring items that will be inserted at other moments in the WF
        # backToCreated is not in MeetingItem.meetingTransitionsAcceptingRecurringItems
        # so it will not be added...
        self.create('MeetingItemRecurring', title='Rec item 2',
                    proposingGroup='developers',
                    meetingTransitionInsertingMe='backToCreated')
        self.create('MeetingItemRecurring', title='Rec item 3',
                    proposingGroup='developers',
                    meetingTransitionInsertingMe='freeze')
        self.create('MeetingItemRecurring', title='Rec item 4',
                    proposingGroup='developers',
                    meetingTransitionInsertingMe='decide')
        self.changeUser('pmManager')
        # create a meeting without supplementary items, only the recurring items
        meeting = self._createMeetingWithItems(withItems=False)
        # The recurring items must have as owner the meeting creator
        for item in meeting.getItems():
            self.assertEquals(item.getOwner().getId(), 'pmManager')
        # The meeting must contain recurring items : 2 defined and one added here above
        self.failUnless(len(meeting.getItems()) == 3)
        self.failIf(meeting.getItems(listTypes=['late']))
        # After freeze, the meeting must have one recurring item more
        self.freezeMeeting(meeting)
        self.failUnless(len(meeting.getItems()) == 4)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 1)
        # Back to created: rec item 2 is not inserted because
        # only some transitions can add a recurring item (see MeetingItem).
        self.backToState(meeting, 'created')
        self.failUnless(len(meeting.getItems()) == 4)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 1)
        # Recurring items can be added twice...
        self.freezeMeeting(meeting)
        self.failUnless(len(meeting.getItems()) == 5)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 2)
        # Decide the meeting, a third late item is added
        self.decideMeeting(meeting)
        self.failUnless(len(meeting.getItems()) == 6)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 3)

    def _testRecurringItemsCouncil(self):
        '''Tests the recurring items system.
           Recurring items are added when the meeting is setInCouncil.'''
        # First, define a recurring item in the meeting config
        # that will be added when the meeting is set to 'in_council'
        self.changeUser('admin')
        self.create('MeetingItemRecurring', title='Rec item 1',
                    proposingGroup='developers',
                    category='deployment',
                    meetingTransitionInsertingMe='setInCouncil')
        setRoles(self.portal, 'pmManager', ['MeetingManager', 'Manager', ])
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        self.failUnless(len(meeting.getItems()) == 0)
        self.do(meeting, 'setInCommittee')
        self.failUnless(len(meeting.getItems()) == 0)
        self.do(meeting, 'setInCouncil')
        self.failUnless(len(meeting.getItems()) == 1)
        self.do(meeting, 'close')
        self.failUnless(len(meeting.getItems()) == 1)

    def test_pm_RecurringItemsBypassSecutiry(self):
        '''Tests that recurring items are addable by a MeetingManager even if by default,
           one of the transition to trigger for the item to be presented should not be triggerable
           by the MeetingManager inserting the recurring item.
           For example here, we will add a recurring item for group 'developers' and
           we create a 'pmManagerRestricted' that will not be able to propose the item.'''
        self.changeUser('pmManager')
        self._removeConfigObjectsFor(self.meetingConfig)
        # just one recurring item added for 'developers'
        self.changeUser('admin')
        self.create('MeetingItemRecurring', title='Rec item developers',
                    proposingGroup='developers',
                    meetingTransitionInsertingMe='_init_')
        self.createUser('pmManagerRestricted', ('MeetingManager', ))
        self.portal.portal_groups.addPrincipalToGroup('pmManagerRestricted', 'developers_creators')
        self.changeUser('pmManagerRestricted')
        # first check that current 'pmManager' may not 'propose'
        # an item created with proposing group 'vendors'
        item = self.create('MeetingItem')
        # 'pmManager' may propose the item and he will be able to validate it
        self.proposeItem(item)
        self.assertTrue(item.queryState() == self.WF_ITEM_STATE_NAME_MAPPINGS_1['proposed'])
        # we have no avaialble transition, or just two
        availableTransitions = self.wfTool.getTransitionsFor(item)
        if availableTransitions:
            self.assertTrue(len(availableTransitions) == 2)
        # now, create a meeting, the item is correctly
        meeting = self.create('Meeting', date=DateTime('2013/01/01'))
        self.assertTrue(len(meeting.getItems()) == 1)
        self.assertTrue(meeting.getItems()[0].getProposingGroup() == 'developers')

    def test_pm_WorkflowPermissions(self):
        """Bypass this test..."""
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflows, prefix='test_pm_'))
    return suite
