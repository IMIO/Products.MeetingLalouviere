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
from copy import deepcopy

from Products.MeetingCommunes.tests.testWFAdaptations import testWFAdaptations as mctwfa
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)

from Products.CMFCore.permissions import ModifyPortalContent, DeleteObjects, View
from zope.event import notify
from zope.i18n import translate
from zope.lifecycleevent import ObjectModifiedEvent


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
                          'waiting_advices_proposing_group_send_back'
                          ])

    def _process_transition_for_correcting_item(self, item, all):
        if all:
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

    def _get_developers_reviewers_groups(self):
        return [self.developers_serviceheads,
                self.developers_officemanagers,
                self.developers_divisionheads,
                self.developers_directors,
                self.developers_alderman,
                self.developers_reviewers]

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
        self._activate_wfas(('return_to_proposing_group_with_last_validation',))

        meeting = self.create('Meeting')
        item = self.create('MeetingItem')
        self.presentItem(item)
        self.freezeMeeting(meeting)
        self.do(item, 'return_to_proposing_group')
        self.assertEqual(item.query_state(), 'returned_to_proposing_group')
        self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group_with_last_validation',)))
        if 'return_to_proposing_group' in cfg.listWorkflowAdaptations():
            self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group',)))
        if 'return_to_proposing_group_with_all_validations' in cfg.listWorkflowAdaptations():
            self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group_with_all_validations',)))
        self.do(item, 'goTo_returned_to_proposing_group_proposed_to_alderman')
        self.assertEqual(item.query_state(), 'returned_to_proposing_group_proposed_to_alderman')
        self.assertEqual(
            cfg.validate_workflowAdaptations(()),
            return_to_proposing_group_removed_error)
        if 'return_to_proposing_group' in cfg.listWorkflowAdaptations():
            self.assertEqual(
                cfg.validate_workflowAdaptations(('return_to_proposing_group',)),
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
        self._activate_wfas(('return_to_proposing_group_with_all_validations',))

        meeting = self.create('Meeting')
        item = self.create('MeetingItem')
        self.presentItem(item)
        self.freezeMeeting(meeting)
        self.do(item, 'return_to_proposing_group')
        self.assertEqual(item.query_state(), 'returned_to_proposing_group')
        self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group_with_all_validations',)))
        if 'return_to_proposing_group' in cfg.listWorkflowAdaptations():
            self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group',)))

        if 'return_to_proposing_group_with_last_validation' in cfg.listWorkflowAdaptations():
            self.failIf(cfg.validate_workflowAdaptations(('return_to_proposing_group_with_last_validation',)))
        self._process_transition_for_correcting_item(item, True)
        self.assertEqual(item.query_state(), 'returned_to_proposing_group_proposed_to_alderman')
        self.assertEqual(
            cfg.validate_workflowAdaptations(()),
            return_to_proposing_group_removed_error)
        if 'return_to_proposing_group' in cfg.listWorkflowAdaptations():
            self.assertEqual(
                cfg.validate_workflowAdaptations(('return_to_proposing_group',)),
                return_to_proposing_group_removed_error)
        if 'return_to_proposing_group_with_last_validation' in cfg.listWorkflowAdaptations():
            self.assertEqual(
                cfg.validate_workflowAdaptations(('return_to_proposing_group_with_last_validation',)),
                return_to_proposing_group_removed_error)
        # make wfAdaptation unselectable
        self.do(item, 'backTo_itemfrozen_from_returned_to_proposing_group')
        self.failIf(cfg.validate_workflowAdaptations(()))

    def test_pm_WFA_waiting_advices_unknown_state(self):
        '''Does not fail to be activated if a from/back state does not exist.'''
        cfg = self.meetingConfig
        # ease override by subproducts
        if not self._check_wfa_available(['waiting_advices']):
            return

        from Products.PloneMeeting.model import adaptations
        original_WAITING_ADVICES_FROM_STATES = deepcopy(adaptations.WAITING_ADVICES_FROM_STATES)
        adaptations.WAITING_ADVICES_FROM_STATES['*'] = adaptations.WAITING_ADVICES_FROM_STATES['*'] + (
            {'from_states': ('unknown',),
             'back_states': ('unknown',), },)
        self._activate_wfas(('waiting_advices', 'waiting_advices_proposing_group_send_back'))
        itemWF = cfg.getItemWorkflow(True)
        # does not fail and existing states are taken into account
        self.assertListEqual(
            sorted([st for st in itemWF.states if 'waiting_advices' in st]),
            ['itemcreated_waiting_advices', 'proposed_to_alderman_waiting_advices'])

        # back to original configuration
        adaptations.WAITING_ADVICES_FROM_STATES = original_WAITING_ADVICES_FROM_STATES

    def _item_validation_shortcuts_inactive(self):
        self._enable_mc_Prevalidation(self.meetingConfig)
        super(testWFAdaptations, self)._item_validation_shortcuts_inactive()


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix="test_"))
    return suite
