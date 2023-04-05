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
from Products.PloneMeeting.config import WriteBudgetInfos, WriteInternalNotes
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
                          # Custom
                          'apply_council_state_label',
                          # End of custom
                          'decide_item_when_back_to_meeting_from_returned_to_proposing_group',
                          'delayed',
                          'hide_decisions_when_under_writing',
                          'hide_decisions_when_under_writing_check_returned_to_proposing_group',
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
                          'propose_to_budget_reviewer',
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
                          'waiting_advices_adviser_send_back',
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

    def test_pm_WFA_pre_validation(self):
        pass

    def _waiting_advices_active(self):
        '''Tests while 'waiting_advices' wfAdaptation is active.'''
        cfg = self.meetingConfig
        # by default it is linked to the 'proposed' state
        itemWF = cfg.getItemWorkflow(True)
        waiting_state_name = '{0}_waiting_advices'.format(self._stateMappingFor('proposed_first_level'))
        waiting_transition_name = 'wait_advices_from_{0}'.format(self._stateMappingFor('proposed_first_level'))
        self.assertIn(waiting_state_name, itemWF.states.keys())

        # the budget impact editors functionnality still works even if 'remove_modify_access': True
        cfg.setItemBudgetInfosStates((waiting_state_name, ))
        # check that the internalNotes functionnality works as well
        # enable field internalNotes
        self._enableField('internalNotes', reload=True)
        # make internal notes editable by copyGroups
        self._activate_config('itemInternalNotesEditableBy',
                              'reader_copy_groups')
        cfg.setItemCopyGroupsStates((waiting_state_name, ))

        # right, create an item and set it to 'waiting_advices'
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem', copyGroups=[self.vendors_reviewers])
        self.proposeItem(item, first_level=True)
        # 'pmCreator1' is not able to set item to 'waiting_advices'
        self.assertFalse(self.transitions(item))
        # 'pmReviewer1' may do it but by default is not able to edit it
        self.changeUser('pmManager')
        # no advice asked so a No() instance is returned for now
        self.assertNotIn(waiting_transition_name, self.transitions(item))
        advice_required_to_ask_advices = translate('advice_required_to_ask_advices',
                                                   domain='PloneMeeting',
                                                   context=self.request)
        proposed_state = self._stateMappingFor('proposed_first_level')
        self.assertEqual(
            translate(item.wfConditions().mayWait_advices(
                proposed_state, waiting_state_name).msg, context=self.request),
            advice_required_to_ask_advices)
        # ask an advice so transition is available
        item.setOptionalAdvisers((self.vendors_uid, ))
        item._update_after_edit()
        # still not available because no advice may be asked in state waiting_state_name
        self.assertNotIn(waiting_state_name, self.vendors.item_advice_states)
        self.assertNotIn(waiting_transition_name, self.transitions(item))

        # do things work
        self.vendors.item_advice_states = ("{0}__state__{1}".format(
            cfg.getId(), waiting_state_name), )
        # clean MeetingConfig.getItemAdviceStatesForOrg
        notify(ObjectModifiedEvent(self.vendors))

        self.assertIn(waiting_transition_name, self.transitions(item))
        self._setItemToWaitingAdvices(item, waiting_transition_name)
        self.assertEqual(item.query_state(), waiting_state_name)
        self.assertFalse(self.hasPermission(ModifyPortalContent, item))
        self.assertFalse(self.hasPermission(DeleteObjects, item))

        # pmCreator1 may view but not edit
        self.changeUser('pmCreator1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertFalse(self.hasPermission(ModifyPortalContent, item))
        self.assertFalse(self.hasPermission(DeleteObjects, item))
        self.assertFalse(self.transitions(item))

        # budget impact editors access are correct even when 'remove_modify_access': True
        self.changeUser('budgetimpacteditor')
        self.assertTrue(self.hasPermission(WriteBudgetInfos, item))

        # check internalNotes editable by copyGroups
        self.changeUser('pmReviewer2')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(WriteInternalNotes, item))
        # change text and add image
        text = '<p>Internal note with image <img src="%s"/>.</p>' % self.external_image1
        item.setInternalNotes(text)
        item.at_post_edit_script()

        # right come back to 'proposed'
        self.changeUser('pmReviewerLevel1')
        self.do(item, 'backTo_%s_from_waiting_advices' % self._stateMappingFor('proposed_first_level'))
        self.assertEqual(item.query_state(), self._stateMappingFor('proposed_first_level'))

    def test_pm_Validate_workflowAdaptations_dependencies(self):
        """Test MeetingConfig.validate_workflowAdaptations that manage dependencies
           between wfAdaptations, a base WFA must be selected and other will complete it."""
        wa_dependencies = translate('wa_dependencies', domain='PloneMeeting', context=self.request)
        cfg = self.meetingConfig

        # item_validation_shortcuts alone is ok
        self.failIf(cfg.validate_workflowAdaptations(('item_validation_shortcuts', )))
        # but item_validation_no_validate_shortcuts depends on it
        self.assertEqual(
            cfg.validate_workflowAdaptations(
                ('item_validation_no_validate_shortcuts', )),
            wa_dependencies)


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix="test_"))
    return suite
