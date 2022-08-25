# -*- coding: utf-8 -*-
#
# File: testWFAdaptations.py
#
# Copyright (c) 2013 by Imio.be
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

from Products.MeetingCommunes.tests.testWFAdaptations import testWFAdaptations as mctwfa
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)

from Products.CMFCore.permissions import ModifyPortalContent, DeleteObjects
from zope.i18n import translate


class testWFAdaptations(MeetingLalouviereTestCase, mctwfa):
    """Tests various aspects of votes management."""

    def test_pm_WFA_availableWFAdaptations(self):
        self.assertEqual(sorted(self.meetingConfig.listWorkflowAdaptations().keys()),
                         ['accepted_but_modified',
                          'accepted_out_of_meeting',
                          'accepted_out_of_meeting_and_duplicated',
                          'accepted_out_of_meeting_emergency',
                          'accepted_out_of_meeting_emergency_and_duplicated',
                          'decide_item_when_back_to_meeting_from_returned_to_proposing_group',
                          'delayed',
                          'hide_decisions_when_under_writing',
                          'item_validation_no_validate_shortcuts',
                          'item_validation_shortcuts',
                          'mark_not_applicable',
                          'meetingmanager_correct_closed_meeting',
                          'no_decide',
                          'no_freeze',
                          'no_publication',
                          'only_creator_may_delete',
                          'postpone_next_meeting',
                          'pre_accepted',
                          'presented_item_back_to_itemcreated',
                          # Do no exist (like spaghetti a la bolognese)
                          # 'presented_item_back_to_proposed',
                          # NEW
                          'presented_item_back_to_proposed_to_alderman',
                          'presented_item_back_to_proposed_to_dg',
                          'presented_item_back_to_proposed_to_director',
                          'presented_item_back_to_proposed_to_divisionhead',
                          'presented_item_back_to_proposed_to_officemanager',
                          'presented_item_back_to_proposed_to_servicehead',
                          # End of custom
                          'refused',
                          'removed',
                          'removed_and_duplicated',
                          'return_to_proposing_group',
                          'return_to_proposing_group_with_all_validations',
                          'return_to_proposing_group_with_last_validation',
                          'reviewers_take_back_validated_item',
                          'transfered',
                          'transfered_and_duplicated',
                          'waiting_advices',
                          'waiting_advices_adviser_may_validate',
                          'waiting_advices_adviser_send_back',
                          'waiting_advices_from_before_last_val_level',
                          'waiting_advices_from_every_val_levels',
                          'waiting_advices_from_last_val_level',
                          'waiting_advices_given_advices_required_to_validate',
                          'waiting_advices_given_and_signed_advices_required_to_validate',
                          'waiting_advices_proposing_group_send_back'])

    def _process_transition_for_correcting_item(self, item):
        self.changeUser('pmCreator1')
        self.do(item, 'goTo_returned_to_proposing_group_proposed_to_servicehead')
        self.failIf(self.hasPermission(ModifyPortalContent, item))
        self.changeUser('pmServiceHead1')
        self.do(item, 'goTo_returned_to_proposing_group_proposed_to_officemanager')
        self.failIf(self.hasPermission(ModifyPortalContent, item))
        self.changeUser('pmOfficeManager1')
        self.do(item, 'goTo_returned_to_proposing_group_proposed_to_divisionhead')
        self.failIf(self.hasPermission(ModifyPortalContent, item))
        self.changeUser('pmDivisionHead1')
        self.do(item, 'goTo_returned_to_proposing_group_proposed_to_director')
        self.failIf(self.hasPermission(ModifyPortalContent, item))
        self.changeUser('pmDirector1')
        self.do(item, 'goTo_returned_to_proposing_group_proposed_to_dg')
        self.failIf(self.hasPermission(ModifyPortalContent, item))
        self.changeUser('pmManager')
        self.do(item, 'goTo_returned_to_proposing_group_proposed_to_alderman')

    def _return_to_proposing_group_with_validation_active_wf_functionality(self):
        '''Tests the workflow functionality of using the
           'return_to_proposing_group_with_last_validation' wfAdaptation.'''
        # while it is active, the creators of the item can edit the item as well as the MeetingManagers
        # after, he must be sent to reviewer the item
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        self.proposeItem(item)
        self.changeUser('pmReviewer1')
        self.validateItem(item)
        # create a Meeting and add the item to it
        self.changeUser('pmManager')
        meeting = self.create('Meeting')
        self.presentItem(item)
        # now that it is presented, the pmCreator1/pmReviewer1 can not edit it anymore
        for userId in ('pmCreator1', 'pmReviewer1'):
            self.changeUser(userId)
            self.failIf(self.hasPermission(ModifyPortalContent, item))
        # the item can be send back to the proposing group by the MeetingManagers only
        for userId in ('pmCreator1', 'pmReviewer1'):
            self.changeUser(userId)
            self.failIf(self.transitions(item))
        self.changeUser('pmManager')
        self.failUnless('return_to_proposing_group' in self.transitions(item))
        # send the item back to the proposing group so the proposing group as an edit access to it
        self.do(item, 'return_to_proposing_group')
        self.changeUser('pmCreator1')
        self.failUnless(self.hasPermission(ModifyPortalContent, item))
        # the item creator may not be able to delete the item
        self.failIf(self.hasPermission(DeleteObjects, item))
        # MeetingManagers can still edit it also
        self.changeUser('pmManager')
        self.failUnless(self.hasPermission(ModifyPortalContent, item))
        # Now send item to the reviewer
        self._process_transition_for_correcting_item(item)
        # MeetingManagers can still edit it also
        self.changeUser('pmManager')
        self.failUnless(self.hasPermission(ModifyPortalContent, item))
        # the reviewer can send the item back to the meeting managers, as the meeting managers
        for userId in ('pmAlderman', 'pmManager'):
            self.changeUser(userId)
            self.failUnless('backTo_presented_from_returned_to_proposing_group' in self.transitions(item))
        # when the creator send the item back to the meeting, it is in the right state depending
        # on the meeting state.  Here, when meeting is 'created', the item is back to 'presented'
        self.do(item, 'backTo_presented_from_returned_to_proposing_group')
        self.assertEqual(item.query_state(), 'presented')
        # send the item back to proposing group, freeze the meeting then send the item back to the meeting
        # the item should be now in the item state corresponding to the meeting frozen state, so 'itemfrozen'
        self.do(item, 'return_to_proposing_group')
        self._process_transition_for_correcting_item(item)
        self.freezeMeeting(meeting)
        self.do(item, 'backTo_itemfrozen_from_returned_to_proposing_group')
        self.assertEqual(item.query_state(), 'itemfrozen')

        # test when there is reviewers so item may be returned directly to meeting by the creator
        self._remove_all_members_from_groups([self.developers_serviceheads,
                                              self.developers_officemanagers,
                                              self.developers_divisionheads,
                                              self.developers_directors,
                                              self.developers_alderman,
                                              self.developers_reviewers])
        self.changeUser('pmManager')
        self.do(item, 'return_to_proposing_group')
        self.changeUser('pmCreator1')
        # item may be directly returned to the meeting as itemcreated is the last validation level
        self.assertEqual(self.transitions(item), ['backTo_itemfrozen_from_returned_to_proposing_group'])
        self.failUnless(self.hasPermission(ModifyPortalContent, item))
        self.do(item, 'backTo_itemfrozen_from_returned_to_proposing_group')
        self.assertEqual(item.query_state(), 'itemfrozen')

    def test_pm_Validate_workflowAdaptations_removed_return_to_proposing_group_with_last_validation(self):
        """Test MeetingConfig.validate_workflowAdaptations that manage removal
           of wfAdaptations 'return_to_proposing_group with last validation' that is not possible if
           some items are 'returned_to_proposing_group xxx'."""
        # ease override by subproducts
        cfg = self.meetingConfig
        if not self._check_wfa_available(['return_to_proposing_group_with_last_validation']):
            return

        return_to_proposing_group_removed_error = translate(
            'wa_removed_return_to_proposing_group_with_last_validation_error',
            domain='PloneMeeting',
            context=self.request)
        self.changeUser('pmManager')
        self._activate_wfas(('return_to_proposing_group_with_last_validation', ))

        meeting = self.create('Meeting')
        item = self.create('MeetingItem')
        self.presentItem(item)
        self.freezeMeeting(meeting)
        self.do(item, 'return_to_proposing_group')
        self.assertEqual(item.query_state(), 'returned_to_proposing_group')
        self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group_with_last_validation',)))
        if 'return_to_proposing_group' in cfg.listWorkflowAdaptations():
            self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group', )))
        if 'return_to_proposing_group_with_all_validations' in cfg.listWorkflowAdaptations():
            self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group_with_all_validations',)))
        self.do(item, 'goTo_returned_to_proposing_group_proposed_to_alderman')
        self.assertEqual(item.query_state(), 'returned_to_proposing_group_proposed_to_alderman')
        self.assertEqual(
            cfg.validate_workflowAdaptations(()),
            return_to_proposing_group_removed_error)
        if 'return_to_proposing_group' in cfg.listWorkflowAdaptations():
            self.assertEqual(
                cfg.validate_workflowAdaptations(('return_to_proposing_group', )),
                return_to_proposing_group_removed_error)
        if 'return_to_proposing_group_with_all_validations' in cfg.listWorkflowAdaptations():
            self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group_with_all_validations',)))
        # make wfAdaptation unselectable
        self.do(item, 'backTo_itemfrozen_from_returned_to_proposing_group')
        self.failIf(cfg.validate_workflowAdaptations(()))

    def test_pm_Validate_workflowAdaptations_removed_return_to_proposing_group_with_all_validations(self):
        """Test MeetingConfig.validate_workflowAdaptations that manage removal
           of wfAdaptations 'return_to_proposing_group with all validations' that is not possible if
           some items are 'returned_to_proposing_group xxx'."""
        # ease override by subproducts
        cfg = self.meetingConfig
        if not self._check_wfa_available(['return_to_proposing_group_with_all_validations']):
            return

        return_to_proposing_group_removed_error = translate(
            'wa_removed_return_to_proposing_group_with_all_validations_error',
            domain='PloneMeeting',
            context=self.request)
        self.changeUser('pmManager')
        self._activate_wfas(('return_to_proposing_group_with_all_validations', ))

        meeting = self.create('Meeting')
        item = self.create('MeetingItem')
        self.presentItem(item)
        self.freezeMeeting(meeting)
        self.do(item, 'return_to_proposing_group')
        self.assertEqual(item.query_state(), 'returned_to_proposing_group')
        self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group_with_all_validations',)))
        if 'return_to_proposing_group' in cfg.listWorkflowAdaptations():
            self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group', )))

        if 'return_to_proposing_group_with_last_validation' in cfg.listWorkflowAdaptations():
            self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group_with_last_validation',)))
        self._process_transition_for_correcting_item(item)
        self.assertEqual(item.query_state(), 'returned_to_proposing_group_proposed_to_alderman')
        self.assertEqual(
            cfg.validate_workflowAdaptations(()),
            return_to_proposing_group_removed_error)
        if 'return_to_proposing_group' in cfg.listWorkflowAdaptations():
            self.assertEqual(
                cfg.validate_workflowAdaptations(('return_to_proposing_group', )),
                return_to_proposing_group_removed_error)
        if 'return_to_proposing_group_with_last_validation' in cfg.listWorkflowAdaptations():
            self.assertEqual(
                cfg.validate_workflowAdaptations(('return_to_proposing_group_with_last_validation',)),
                return_to_proposing_group_removed_error)
        # make wfAdaptation unselectable
        self.do(item, 'backTo_itemfrozen_from_returned_to_proposing_group')
        self.failIf(cfg.validate_workflowAdaptations(()))

def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix="test_"))
    return suite
