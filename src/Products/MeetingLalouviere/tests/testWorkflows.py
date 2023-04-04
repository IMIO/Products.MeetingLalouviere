# -*- coding: utf-8 -*-
from datetime import datetime

from Products.MeetingCommunes.tests.testWorkflows import testWorkflows as mctw
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)
from Products.PloneMeeting.config import AddAnnex

from AccessControl import Unauthorized
from Products.CMFCore.permissions import ModifyPortalContent


class testWorkflows(MeetingLalouviereTestCase, mctw):
    """Tests the default workflows implemented in MeetingLalouviere.

       WARNING:
       The Plone test system seems to be bugged: it does not seem to take into
       account the write_permission and read_permission tags that are defined
       on some attributes of the Archetypes model. So when we need to check
       that a user is not authorized to set the value of a field protected
       in this way, we do not try to use the accessor to trigger an exception
       (self.assertRaise). Instead, we check that the user has the permission
       to do so (getSecurityManager().checkPermission)."""

    def _check_users_can_modify(self, item, users, annex):
        for user_id in users:
            self.changeUser(user_id)
            self.assertTrue(item.mayQuickEdit("observations"))
            self.failUnless(self.hasPermission(ModifyPortalContent, (item, annex)))

    def _testWholeDecisionProcessCollege(self):
        """This test covers the whole decision workflow. It begins with the
           creation of some items, and ends by closing a meeting."""
        # pmCreator1 creates an item with 1 annex and proposes it
        self._enableField("observations")
        self._activate_wfas(('waiting_advices',
                             # 'waiting_advices_adviser_send_back',
                             'waiting_advices_proposing_group_send_back',
                             'propose_to_budget_reviewer'),
                            keep_existing=True)
        self.meetingConfig.setItemAdviceStates(("itemcreated_waiting_advices", ))
        self.changeUser("pmCreator1")
        item1 = self.create("MeetingItem", title="The first item", optionalAdvisers=(self.vendors_uid, ))
        self.assertTrue(item1.mayQuickEdit("observations"))
        annex1 = self.addAnnex(item1)
        self.addAnnex(item1, relatedTo="item_decision")
        item1.setOptionalAdvisers((self.vendors_uid, ))
        self.do(item1, "wait_advices_from_itemcreated")
        self.assertEqual("itemcreated_waiting_advices", item1.query_state())
        self.do(item1, "backTo_itemcreated_from_waiting_advices")
        self.do(item1, "proposeToBudgetImpactReviewer")
        self.assertEqual("proposed_to_budget_reviewer", item1.query_state())
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission("PloneMeeting: Add annex", item1))
        self.changeUser("pmBudgetReviewer1")
        self.assertTrue(item1.mayQuickEdit("observations"))
        self.do(item1, "backTo_itemcreated_from_proposed_to_budget_reviewer")
        self.assertEqual("itemcreated", item1.query_state())
        self.changeUser("pmCreator1")
        self.do(item1, "proposeToServiceHead")
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission(AddAnnex, item1))
        self.failIf(self.hasPermission(ModifyPortalContent, (item1, annex1)))
        # the ServiceHead validation level
        self._check_users_can_modify(item1,
                                     ['pmServiceHead1',
                                      'pmOfficeManager1',
                                      'pmDivisionHead1',
                                      'pmDirector1',
                                      ],
                                     annex1)
        self.changeUser("pmServiceHead1")
        self.do(item1, "proposeToOfficeManager")
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission(AddAnnex, item1))
        self.failIf(self.hasPermission(ModifyPortalContent, (item1, annex1)))
        # the OfficeManager validation level
        self._check_users_can_modify(item1,
                                     ['pmOfficeManager1',
                                      'pmDivisionHead1',
                                      'pmDirector1',
                                      ],
                                     annex1)
        self.changeUser("pmOfficeManager1")
        self.do(item1, "proposeToDivisionHead")
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission(AddAnnex, item1))
        self.failIf(self.hasPermission(ModifyPortalContent, (item1, annex1)))
        # the DivisionHead validation level
        self._check_users_can_modify(item1,
                                     ['pmDivisionHead1',
                                      'pmDirector1',
                                      ],
                                     annex1)
        self.changeUser("pmDivisionHead1")
        self.do(item1, "proposeToDirector")
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission(AddAnnex, item1))
        self.failIf(self.hasPermission(ModifyPortalContent, (item1, annex1)))
        # the Director validation level
        self._check_users_can_modify(item1,
                                     ['pmDirector1'],
                                     annex1)
        self.changeUser("pmDirector1")
        self.do(item1, 'proposeToDg')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission(AddAnnex, item1))
        self.failIf(self.hasPermission(ModifyPortalContent, (item1, annex1)))
        self._check_users_can_modify(item1,
                                     ['pmDg'],
                                     annex1)
        self.do(item1, 'proposeToAlderman')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission(AddAnnex, item1))
        self.failIf(self.hasPermission(ModifyPortalContent, (item1, annex1)))
        self._check_users_can_modify(item1,
                                     ['pmAlderman1'],
                                     annex1)
        self.do(item1, "validate")
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo="item_decision")
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission("PloneMeeting: Add annex", item1))
        # pmManager creates a meeting
        self.changeUser("pmManager")
        self.assertTrue(item1.mayQuickEdit("observations"))
        meeting = self.create("Meeting", date=datetime(2007, 12, 11, 9))
        self.addAnnex(item1, relatedTo="item_decision")
        # pmCreator2 creates and proposes an item
        self.changeUser("pmCreator2")
        item2 = self.create(
            "MeetingItem", title="The second item", preferredMeeting=meeting.UID()
        )
        self.do(item2, "proposeToServiceHead")
        # pmReviewer1 can not validate the item has not in the same proposing group
        self.changeUser("pmReviewer1")
        self.failIf(self.hasPermission(ModifyPortalContent, item2))
        # but pmReviwer2 can because its his own group
        self.changeUser("pmReviewer2")
        self.failUnless(self.hasPermission(ModifyPortalContent, item2))
        # do the complete validation

        self.proposeItem(item2)
        # pmManager inserts item1 into the meeting and publishes it
        self.changeUser("pmManager")
        managerAnnex = self.addAnnex(item1)
        self.portal.restrictedTraverse("@@delete_givenuid")(managerAnnex.UID())
        self.do(item1, "present")
        # Now reviewers can't add annexes anymore
        self.changeUser("pmReviewer2")
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        # freeze the meeting
        self.changeUser("pmManager")
        self.do(meeting, "freeze")
        # validate item2 after meeting freeze
        self.changeUser("pmReviewer2")
        self.do(item2, "validate")
        self.changeUser("pmManager")
        self.do(item2, "present")
        self.addAnnex(item2)
        # So now we should have 3 normal item (no recurring items) and one late item in the meeting
        self.assertEqual(len(meeting.get_items(list_types=["normal"])), 3)
        self.assertEqual(len(meeting.get_items(list_types=["late"])), 1)
        self.assertEqual(meeting.get_items(list_types=["late"])[0], item2)
        self.do(meeting, "decide")
        item1.activateFollowUp()
        self.assertEqual(item1.getDecision(), item1.getNeededFollowUp())
        item2.activateFollowUp()
        self.assertEqual(item2.getDecision(), item2.getNeededFollowUp())
        # followup writer cannot edit follow up on frozen items
        self.changeUser("pmFollowup1")
        self.assertFalse(item1.mayQuickEdit("neededFollowUp"))
        self.assertFalse(item1.mayQuickEdit("providedFollowUp"))
        # manager can edit neededfollowup for frozen and decided items
        self.changeUser("pmManager")
        self.assertTrue(item1.mayQuickEdit("neededFollowUp"))
        self.assertTrue(item1.mayQuickEdit("providedFollowUp"))

        self.assertEquals(item2.query_state(), "itemfrozen")
        self.assertTrue(item2.mayQuickEdit("neededFollowUp"))
        self.assertTrue(item2.mayQuickEdit("providedFollowUp"))

        self.do(item1, "accept")
        self.assertEquals(item1.query_state(), "accepted")
        self.assertTrue(item1.mayQuickEdit("neededFollowUp"))
        self.assertTrue(item1.mayQuickEdit("providedFollowUp"))
        self.changeUser("pmFollowup1")
        self.assertFalse(item1.mayQuickEdit("neededFollowUp"))
        self.assertTrue(item1.mayQuickEdit("providedFollowUp"))
        item1.setProvidedFollowUp("<p>Followed</p>")
        self.changeUser("pmManager")
        item1.confirmFollowUp()
        item1.deactivateFollowUp()
        self.do(meeting, "close")
        # every items without a decision are automatically accepted
        self.assertEquals(item2.query_state(), "accepted")
        self.assertFalse(item2.mayQuickEdit("neededFollowUp"))
        self.assertFalse(item2.mayQuickEdit("providedFollowUp"))
        self.changeUser("pmFollowup2")
        self.assertFalse(item2.mayQuickEdit("neededFollowUp"))
        self.assertFalse(item2.mayQuickEdit("providedFollowUp"))

    def _testWholeDecisionProcessCouncil(self):
        """
            This test covers the whole decision workflow. It begins with the
            creation of some items, and ends by closing a meeting.
        """
        self.changeUser("admin")
        self.setMeetingConfig(self.meetingConfig2.getId())
        self._enableField("observations")
        self._enableField("committees", related_to='Meeting')
        self._enableField("committeeTranscript")
        self._activate_wfas(('waiting_advices',
                             # 'waiting_advices_adviser_send_back',
                             'waiting_advices_proposing_group_send_back',
                             'propose_to_budget_reviewer',
                             'apply_council_state_label',
                             'return_to_proposing_group',
                             'accepted_but_modified'),
                            keep_existing=True)
        # add a recurring item that is inserted when the meeting is 'setInCouncil'
        self.create(
            "MeetingItemRecurring",
            title="Rec item 1",
            proposingGroup=self.developers_uid,
            category="deployment",
            meetingTransitionInsertingMe="setInCouncil",
        )
        # pmCreator1 creates an item with 1 annex and proposes it
        self.changeUser("pmCreator1")
        item1 = self.create(
            "MeetingItem",
            title="The first item",
            autoAddCategory=False,
            category="deployment",
            committees_index=("commission-ag",),
            decision="<p>test</p>"
        )
        annex1 = self.addAnnex(item1)
        self._check_users_can_modify(item1,
                                     ['pmCreator1',
                                      'pmServiceHead1',
                                      'pmOfficeManager1',
                                      'pmDivisionHead1',
                                      'pmDirector1',
                                      ],
                                     annex1)
        self.changeUser("pmCreator1")
        # The creator can add a decision annex on created item
        self.addAnnex(item1, relatedTo="item_decision")
        self.do(item1, "proposeToDirector")
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission(AddAnnex, item1))
        self.failIf(self.hasPermission(ModifyPortalContent, (item1, annex1)))
        # the Director validation level
        self._check_users_can_modify(item1,
                                     ['pmDirector1'],
                                     annex1)
        self.addAnnex(item1, relatedTo="item_decision")
        self.do(item1, "validate")
        self.failIf(self.hasPermission(ModifyPortalContent, item1))
        # The reviewer cannot add a decision annex on validated item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo="item_decision")
        # pmManager creates a meeting
        self.changeUser("pmManager")
        self.assertTrue(item1.mayQuickEdit("observations"))
        meeting = self.create("Meeting", date=datetime(2007, 12, 11, 9, 0, 0))
        # The meetingManager can add a decision annex
        self.addAnnex(item1, relatedTo="item_decision")
        # pmCreator2 creates and proposes an item
        self.changeUser("pmCreator2")
        item2 = self.create(
            "MeetingItem",
            title="The second item",
            preferredMeeting=meeting.UID(),
            category="deployment",
            committees_index=("commission-patrimoine",),
            decision="<p>test</p>"
        )
        self.do(item2, "proposeToDirector")
        # pmManager inserts item1 into the meeting and freezes it
        self.changeUser("pmManager")
        managerAnnex = self.addAnnex(item1)
        self.portal.restrictedTraverse("@@delete_givenuid")(managerAnnex.UID())
        self.presentItem(item1)
        self.changeUser("pmCreator1")
        # The creator cannot add any kind of annex on presented item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo="item_decision")
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.changeUser("pmManager")
        self.do(meeting, "freeze")
        self.assertEqual(item1.query_state(), "itemfrozen")
        # pmReviewer2 validates item2
        self.changeUser("pmDirector2")
        item2.setPreferredMeeting(meeting.UID())

        self.do(item2, "validate")
        # pmManager inserts item2 into the meeting, as late item, and adds an
        # annex to it
        self.changeUser("pmManager")
        self.presentItem(item2)
        self.addAnnex(item2)
        # An item is freely addable to a meeting if the meeting is 'open'
        # so in states 'created', 'in_committee' and 'in_council'
        # the 'late items' functionnality is not used
        self.failIf(len(meeting.get_items()) != 2)
        self.failIf(len(meeting.get_items(list_types=["late"])) != 0)
        # remove the item, set the meeting in council and add it again
        self.backToState(item2, "validated")
        self.failIf(len(meeting.get_items()) != 1)
        self.do(meeting, "publish")
        self.setCurrentMeeting(None)

        item1_addition = self.create(
            "MeetingItem",
            title="Addition to the first item",
            autoAddCategory=False,
            category="deployment",
            committees_index=("commission-ag__suppl_1",)
        )
        self.do(item1_addition, "proposeToDirector")
        item1_addition.setPreferredMeeting(meeting.UID())
        self.do(item1_addition, "validate")
        self.do(item1_addition, "present")
        self.assertEqual(len(meeting.get_items()), 2)
        self.failIf(item1_addition.isLate())
        # an item can be sent back to the service so MeetingMembers
        # can edit it and send it back to the meeting
        self.changeUser("pmCreator1")
        self.failIf(self.hasPermission(ModifyPortalContent, item1))
        self.changeUser("pmManager")
        # send the item back to the service
        self.do(item1, "return_to_proposing_group")
        self.changeUser("pmCreator1")
        self.failUnless(self.hasPermission(ModifyPortalContent, item1))
        self.do(item1, "backTo_itempublished_from_returned_to_proposing_group")
        self.failIf(self.hasPermission(ModifyPortalContent, item1))
        # item state follow meeting state
        self.changeUser("pmManager")
        self.assertEquals(item1.query_state(), "itempublished")
        # while closing a meeting, every no decided items are accepted
        self.do(meeting, "decide")
        self.do(item2, "present")
        self.assertEqual(len(meeting.get_items()), 3)
        self.failUnless(item2.isLate())
        self.do(item1, "accept_but_modify")
        self.do(meeting, "close")
        self.assertEquals(item1.query_state(), "accepted_but_modified")
        self.assertEquals(item2.query_state(), "accepted")

    # TODO use in test custom WF or delete
    # def _checkCustomRecurringItemsCouncil(self):
    #     """Tests the recurring items system.
    #        Recurring items are added when the meeting is setInCouncil."""
    #     # First, define a recurring item in the meeting config
    #     # that will be added when the meeting is set to 'in_council'
    #     self.changeUser("admin")
    #     self.create(
    #         "MeetingItemRecurring",
    #         title="Rec item 1",
    #         proposingGroup=self.developers_uid,
    #         category="deployment",
    #         meetingTransitionInsertingMe="setInCouncil",
    #     )
    #     setRoles(self.portal, "pmManager", ["MeetingManager", "Manager"])
    #     self.changeUser("pmManager")
    #     meeting = self.create("Meeting", date=datetime(2007, 12, 11, 9, 0))
    #     self.failUnless(len(meeting.get_items()) == 0)
    #     self.do(meeting, "setInCommittee")
    #     self.failUnless(len(meeting.get_items()) == 0)
    #     self.do(meeting, "setInCouncil")
    #     self.failUnless(len(meeting.get_items()) == 1)
    #     self.do(meeting, "close")
    #     self.failUnless(len(meeting.get_items()) == 1)

    # def test_pm_RecurringItemsBypassSecurity(self):
    #     """Tests that recurring items are addable by a MeetingManager even if by default,
    #        one of the transition to trigger for the item to be presented should not be triggerable
    #        by the MeetingManager inserting the recurring item.
    #        For example here, we will add a recurring item for group 'developers' and
    #        we create a 'pmManagerRestricted' that will not be able to propose the item."""
    #     self.changeUser("pmManager")
    #     self._removeConfigObjectsFor(self.meetingConfig)
    #     # just one recurring item added for 'developers'
    #     self.changeUser("admin")
    #     self.create(
    #         "MeetingItemRecurring",
    #         title="Rec item developers",
    #         proposingGroup=self.developers_uid,
    #         meetingTransitionInsertingMe="_init_",
    #     )
    #     self.createUser("pmManagerRestricted", ("MeetingManager",))
    #     developers_creators = '{}_creators'.format(self.developers_uid)
    #     self.portal.portal_groups.addPrincipalToGroup(
    #         "pmManagerRestricted", developers_creators
    #     )
    #     self.changeUser("pmManagerRestricted")
    #     # first check that current 'pmManager' may not 'propose'
    #     # an item created with proposing group 'vendors'
    #     item = self.create("MeetingItem")
    #     # 'pmManager' may propose the item and he will be able to validate it
    #     self.proposeItem(item)
    #     self.assertTrue(
    #         item.query_state() == self.WF_ITEM_STATE_NAME_MAPPINGS_1["proposed"]
    #     )
    #     # we have no avaialble transition, or just two
    #     availableTransitions = self.wfTool.getTransitionsFor(item)
    #     if availableTransitions:
    #         self.assertTrue(len(availableTransitions) == 2)
    #     # now, create a meeting, the item is correctly
    #     meeting = self.create("Meeting")
    #     self.assertTrue(len(meeting.get_items()) == 1)
    #     self.assertTrue(meeting.get_items()[0].getProposingGroup() == self.developers_uid)


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflows, prefix="test_"))
    return suite
