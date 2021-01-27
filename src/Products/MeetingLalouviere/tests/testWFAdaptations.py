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
from Products.PloneMeeting.model.adaptations import (
    RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS,
)
from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations
from Products.PloneMeeting.tests.PloneMeetingTestCase import pm_logger

from DateTime import DateTime
from Products.CMFCore.permissions import View


class testWFAdaptations(MeetingLalouviereTestCase, mctwfa):
    """Tests various aspects of votes management."""

    def test_pm_WFA_availableWFAdaptations(self):
        """Most of wfAdaptations makes no sense, just make sure most are disabled."""
        self.assertEquals(
            set(self.meetingConfig.listWorkflowAdaptations()),
            set(("removed", "refused", "validate_by_dg_and_alderman", "return_to_proposing_group",)),
        )

    def test_pm_WFA_no_publication(self):
        """No sense..."""
        pass

    def test_pm_WFA_no_proposal(self):
        """No sense..."""
        pass

    def test_pm_WFA_pre_validation(self):
        """No sense..."""
        pass

    def test_pm_WFA_items_come_validated(self):
        """No sense..."""
        pass

    def test_pm_WFA_only_creator_may_delete(self):
        """No sense..."""
        pass

    def test_pm_WFA_no_global_observation(self):
        """No sense..."""
        pass

    def test_pm_WFA_everyone_reads_all(self):
        """No sense..."""
        pass

    def test_pm_WFA_creator_edits_unless_closed(self):
        """No sense..."""
        pass

    def test_subproduct_WFA_add_published_state(self):
        """No sense..."""
        pass

    def _return_to_proposing_group_inactive(self):
        """Tests while 'return_to_proposing_group' wfAdaptation is inactive."""
        # this is active by default in MeetingLalouviere council wf
        return

    def _return_to_proposing_group_active_state_to_clone(self):
        """Helper method to test 'return_to_proposing_group' wfAdaptation regarding the
           RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE defined value.
           In our usecase, this is Nonsense as we use RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS."""
        return

    def _return_to_proposing_group_active_custom_permissions(self):
        """Helper method to test 'return_to_proposing_group' wfAdaptation regarding the
           RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS defined value.
           In our use case, just test that permissions of 'returned_to_proposing_group' state
           are the one defined in RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS."""
        itemWF = self.wfTool.getWorkflowsFor(self.meetingConfig.getItemTypeName())[0]
        returned_to_proposing_group_state_permissions = itemWF.states[
            "returned_to_proposing_group"
        ].permission_roles
        for permission in returned_to_proposing_group_state_permissions:
            self.assertEquals(
                returned_to_proposing_group_state_permissions[permission],
                RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS[
                    self.meetingConfig.getItemWorkflow()
                ][permission],
            )

    def _return_to_proposing_group_active_wf_functionality(self):
        """Tests the workflow functionality of using the 'return_to_proposing_group' wfAdaptation.
           Same as default test until the XXX here under."""
        # while it is active, the creators of the item can edit the item as well as the MeetingManagers
        self.meetingConfig = self.meetingConfig2
        self.meetingConfig.setWorkflowAdaptations("return_to_proposing_group")
        performWorkflowAdaptations(self.meetingConfig, logger=pm_logger)
        self.changeUser("pmCreator1")
        item = self.create("MeetingItem")
        self.proposeItem(item)
        self.changeUser("pmReviewer1")
        self.validateItem(item)
        # create a Meeting and add the item to it
        self.changeUser("pmManager")
        meeting = self.create("Meeting", date=DateTime())
        self.presentItem(item)
        # now that it is presented, the pmCreator1/pmReviewer1 can not edit it anymore
        for userId in ("pmCreator1", "pmReviewer1"):
            self.changeUser(userId)
            self.failIf(self.hasPermission("Modify portal content", item))
        # the item can be send back to the proposing group by the MeetingManagers only
        for userId in ("pmCreator1", "pmReviewer1"):
            self.changeUser(userId)
            self.failIf(self.wfTool.getTransitionsFor(item))
        self.changeUser("pmManager")
        self.failUnless(
            "return_to_proposing_group"
            in [tr["name"] for tr in self.wfTool.getTransitionsFor(item)]
        )
        # send the item back to the proposing group so the proposing group as an edit access to it
        self.do(item, "return_to_proposing_group")
        self.changeUser("pmCreator1")
        self.failUnless(self.hasPermission("Modify portal content", item))
        # MeetingManagers can still edit it also
        self.changeUser("pmManager")
        self.failUnless(self.hasPermission("Modify portal content", item))
        # the creator can send the item back to the meeting managers, as the meeting managers
        for userId in ("pmCreator1", "pmManager"):
            self.changeUser(userId)
            self.failUnless(
                "backTo_presented_from_returned_to_proposing_group"
                in [tr["name"] for tr in self.wfTool.getTransitionsFor(item)]
            )
        # when the creator send the item back to the meeting, it is in the right state depending
        # on the meeting state.  Here, when meeting is 'created', the item is back to 'presented'
        self.do(item, "backTo_presented_from_returned_to_proposing_group")
        self.assertEquals(item.queryState(), "presented")
        # XXX changed by MeetingLalouviere
        # send the item back to proposing group, set the meeting in_committee then send the item back to the meeting
        # the item should be now in the item state corresponding to the meeting frozen state, so 'itemfrozen'
        self.do(item, "return_to_proposing_group")
        self.do(meeting, "setInCommittee")
        self.do(item, "backTo_item_in_committee_from_returned_to_proposing_group")
        self.assertEquals(item.queryState(), "item_in_committee")

    def test_pm_WFA_hide_decisions_when_under_writing(self):
        """Only launch the test for meetingConfig not for meetingConfig2 as no
           'decided' state exists in meetingConfig2 for the 'Meeting'."""
        self.meetingConfig2.setMeetingWorkflow(self.meetingConfig.getMeetingWorkflow())
        mctwfa.test_pm_WFA_hide_decisions_when_under_writing(self)

    def test_pm_Validate_workflowAdaptations_custom(self):
        self.failIf(
            self.meetingConfig.validate_workflowAdaptations(
                ("validate_by_dg_and_alderman",)
            )
        )
        self.meetingConfig.setWorkflowAdaptations("validate_by_dg_and_alderman")
        performWorkflowAdaptations(self.meetingConfig, logger=pm_logger)
        self.failIf(
            self.meetingConfig.validate_workflowAdaptations(
                ("validate_by_dg_and_alderman",)
            )
        )

        self.changeUser("pmManager")
        item = self.create("MeetingItem")
        self.do(item, "proposeToServiceHead")
        self.do(item, "proposeToOfficeManager")
        self.do(item, "proposeToDivisionHead")
        self.do(item, "proposeToDirector")
        self.do(item, "propose_to_dg")

        self.failUnless(self.meetingConfig.validate_workflowAdaptations(()))

        self.do(item, "propose_to_alderman")
        self.failUnless(self.meetingConfig.validate_workflowAdaptations(()))

        self.changeUser("pmAlderman")
        self.do(item, "validate")
        self.failIf(self.meetingConfig.validate_workflowAdaptations(()))

    def test_pm_WFA_ValidateByDgAndAlderman(self):
        self.meetingConfig.setWorkflowAdaptations("validate_by_dg_and_alderman")
        performWorkflowAdaptations(self.meetingConfig, logger=pm_logger)
        self.changeUser("pmManager")
        item = self.create("MeetingItem")
        self.do(item, "proposeToServiceHead")
        self.do(item, "proposeToOfficeManager")
        self.do(item, "proposeToDivisionHead")
        self.do(item, "proposeToDirector")
        self.do(item, "propose_to_dg")
        self.assertEquals(item.queryState(), "proposed_to_dg")

        self.changeUser("pmManager")
        self.failUnless(self.hasPermission("Modify portal content", item))

        for userId in ("pmCreator1", "pmReviewer1", "pmAlderman"):
            self.changeUser(userId)
            self.failIf(self.wfTool.getTransitionsFor(item))

        self.changeUser("pmManager")
        self.do(item, "propose_to_alderman")
        self.assertEquals(item.queryState(), "proposed_to_alderman")

        self.changeUser("pmAlderman")
        self.failUnless(self.hasPermission("Modify portal content", item))

        for userId in ("pmCreator1", "pmDirector1", "pmReviewer1"):
            self.changeUser(userId)
            self.failIf(self.wfTool.getTransitionsFor(item))

        self.changeUser("pmAlderman")
        self.validateItem(item)
        self.assertEquals(item.queryState(), "validated")
        self.failUnless(self.hasPermission(View, item))
        self.failUnless(self.hasPermission("PloneMeeting: Read decision", item))
        self.failUnless(self.hasPermission("PloneMeeting: Read budget infos", item))
        self.failUnless(self.hasPermission("PloneMeeting: Read item observations", item))
        self.failUnless(self.hasPermission("Access contents information", item))

        self.changeUser("pmManager")
        self.failUnless(self.hasPermission("Modify portal content", item))

        for userId in ("pmCreator1", "pmReviewer1", "pmAlderman"):
            self.changeUser(userId)
            self.failIf(self.wfTool.getTransitionsFor(item))

        # test alderman access to presented items and after
        self.changeUser("pmManager")
        meeting = self.create("Meeting", date="2007/12/11 09:00:00")
        self.presentItem(item)
        self.assertEqual(item.queryState(), "presented")
        self.changeUser("pmAlderman")
        self.failUnless(self.hasPermission(View, item))

        self.changeUser("pmManager")
        self.do(meeting, "freeze")
        self.assertEqual(item.queryState(), "itemfrozen")
        self.changeUser("pmAlderman")
        self.failUnless(self.hasPermission(View, item))

        self.changeUser("pmManager")
        self.do(meeting, "decide")
        self.do(item, "accept")
        self.assertEqual(item.queryState(), "accepted")
        self.changeUser("pmAlderman")
        self.failUnless(self.hasPermission(View, item))

        # test back trx
        self.changeUser("pmManager")
        self.do(item, "backToItemFrozen")
        self.do(item, "backToPresented")
        self.do(item, "backToValidated")
        self.do(item, "backToProposedToAlderman")
        self.assertEquals(item.queryState(), "proposed_to_alderman")
        self.changeUser("pmAlderman")
        self.do(item, "backToProposedToDg")
        self.assertEquals(item.queryState(), "proposed_to_dg")
        self.changeUser("pmManager")
        self.do(item, "backToProposedToDirector")
        self.assertEquals(item.queryState(), "proposed_to_director")


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix="test_"))
    return suite
