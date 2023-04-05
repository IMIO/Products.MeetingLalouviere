# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
# File: adapters.py
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
# ------------------------------------------------------------------------------
from collections import OrderedDict
from copy import deepcopy

from Products.MeetingCommunes.adapters import (
    CustomMeeting,
    CustomMeetingConfig, CustomToolPloneMeeting, MeetingItemCommunesWorkflowActions,
)
from Products.MeetingCommunes.adapters import CustomMeetingItem
from Products.MeetingCommunes.interfaces import IMeetingItemCommunesWorkflowActions
from Products.MeetingLalouviere.config import DG_GROUP_ID
from Products.MeetingLalouviere.config import FALLBACK_DG_GROUP_ID
from Products.MeetingLalouviere.config import FINANCE_GROUP_ID
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.config import NOT_GIVEN_ADVICE_VALUE
from Products.PloneMeeting.interfaces import (
    IMeetingConfigCustom, IToolPloneMeetingCustom,
)
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.model.adaptations import _addIsolatedState
from Products.PloneMeeting.utils import org_id_to_uid

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from collective.contact.plonegroup.utils import get_all_suffixes
from imio.helpers.content import uuidsToObjects
from plone import api
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implements

customWfAdaptations = list(deepcopy(MeetingConfig.wfAdaptations))
customWfAdaptations.append('apply_council_state_label')
customWfAdaptations.append('propose_to_budget_reviewer')
# disable not compatible waiting advice wfa
customWfAdaptations.remove('waiting_advices_adviser_may_validate')
customWfAdaptations.remove('waiting_advices_from_before_last_val_level')
customWfAdaptations.remove('waiting_advices_from_every_val_levels')
customWfAdaptations.remove('waiting_advices_from_last_val_level')
customWfAdaptations.remove('waiting_advices_given_advices_required_to_validate')
customWfAdaptations.remove('waiting_advices_given_and_signed_advices_required_to_validate')
MeetingConfig.wfAdaptations = tuple(customWfAdaptations)


class LLCustomMeeting(CustomMeeting):
    """Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom."""

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def get_late_state(self):
        if self.getSelf().portal_type == "MeetingCouncil":
            return "decided"
        return super(CustomMeeting, self).get_late_state()
    # helper methods used in templates

    security.declarePublic("getLabelObservations")

    def getLabelObservations(self):
        """Returns the label to use for field Meeting.observations
           The label is different between college and council"""
        if self.portal_type == "MeetingCouncil":
            return self.utranslate(
                "MeetingLalouviere_label_meetingcouncilobservations",
                domain="PloneMeeting",
            )
        else:
            return self.utranslate(
                "PloneMeeting_label_meetingObservations", domain="PloneMeeting"
            )

    Meeting.getLabelObservations = getLabelObservations


class LLCustomMeetingItem(CustomMeetingItem):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom."""

    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    security.declarePublic("getLabelDescription")

    def getLabelDescription(self):
        """Returns the label to use for field MeetingItem.description
          The label is different between college and council"""
        item = self.getSelf()
        if item.portal_type == "MeetingItemCouncil":
            return item.utranslate(
                "MeetingLalouviere_label_councildescription", domain="PloneMeeting"
            )
        else:
            return item.utranslate(
                "PloneMeeting_label_description", domain="PloneMeeting"
            )

    MeetingItem.getLabelDescription = getLabelDescription

    security.declarePublic("activateFollowUp")

    def activateFollowUp(self):
        """Activate follow-up by setting followUp to 'follow_up_yes'."""
        self.setFollowUp("follow_up_yes")
        # initialize the neededFollowUp field with the available content of the 'decision' field
        if not self.getNeededFollowUp():
            self.setNeededFollowUp(self.getDecision())
        self.reindexObject(
            idxs=["getFollowUp",]
        )
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + "#followup")

    MeetingItem.activateFollowUp = activateFollowUp

    security.declarePublic("deactivateFollowUp")

    def deactivateFollowUp(self):
        """Deactivate follow-up by setting followUp to 'follow_up_no'."""
        self.setFollowUp("follow_up_no")
        self.reindexObject(
            idxs=["getFollowUp",]
        )
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + "#followup")

    MeetingItem.deactivateFollowUp = deactivateFollowUp

    security.declarePublic("confirmFollowUp")

    def confirmFollowUp(self):
        """Confirm follow-up by setting followUp to 'follow_up_provided'."""
        self.setFollowUp("follow_up_provided")
        self.reindexObject(
            idxs=["getFollowUp",]
        )
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + "#followup")

    MeetingItem.confirmFollowUp = confirmFollowUp

    security.declarePublic("followUpNotPrinted")

    def followUpNotPrinted(self):
        """While follow-up is confirmed, we may specify that we do not want it printed in the dashboard."""
        self.setFollowUp("follow_up_provided_not_printed")
        self.reindexObject(
            idxs=["getFollowUp",]
        )
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + "#followup")

    MeetingItem.followUpNotPrinted = followUpNotPrinted

    def _getGroupManagingItem(self, review_state, theObject=False):
        '''See doc in interfaces.py.'''
        item = self.getSelf()
        if item.portal_type == 'MeetingItemCollege' and "proposed_to_dg" in review_state:
            dg_group_uid = org_id_to_uid(DG_GROUP_ID) or org_id_to_uid(FALLBACK_DG_GROUP_ID)
            if theObject:
                return uuidsToObjects(dg_group_uid, unrestricted=True)[0]
            else:
                return dg_group_uid
        else:
            return item.getProposingGroup(theObject=theObject)

    def _getAllGroupsManagingItem(self, review_state, theObjects=False):
        '''See doc in interfaces.py.'''
        res = []
        item = self.getSelf()
        if item.portal_type == 'MeetingItemCollege' and "proposed_to_dg" in review_state:
            dg_group_uid = org_id_to_uid(DG_GROUP_ID) or org_id_to_uid(FALLBACK_DG_GROUP_ID)
            if theObjects:
                res += uuidsToObjects(dg_group_uid, unrestricted=True)
            else:
                res.append(dg_group_uid)
        proposingGroup = item.getProposingGroup(theObject=theObjects)
        if proposingGroup:
            res.append(proposingGroup)
        return res


    def mayGenerateFinanceAdvice(self):
        """
          Condition used in the 'Avis DF' PodTemplate.
        """
        finance_group_uid = org_id_to_uid(FINANCE_GROUP_ID)
        if (
            finance_group_uid in self.context.adviceIndex
            and self.context.adviceIndex[finance_group_uid]["delay"]
            and self.context.adviceIndex[finance_group_uid]["type"] != NOT_GIVEN_ADVICE_VALUE
        ):
            return True
        return False

    def getExtraFieldsToCopyWhenCloning(self, cloned_to_same_mc, cloned_from_item_template):
        """
          Keep some new fields when item is cloned (to another mc or from itemtemplate).
        """
        res = []
        if cloned_to_same_mc and not cloned_from_item_template:
            res = ["interventions", "committeeTranscript"]
        return res

    def adviceDelayIsTimedOutWithRowId(self, groupId, rowIds=[]):
        """ Check if advice with delay from a certain p_groupId and with
            a row_id contained in p_rowIds is timed out.
        """
        item = self.getSelf()
        if item.getAdviceDataFor(item) and groupId in item.getAdviceDataFor(item):
            adviceRowId = item.getAdviceDataFor(item, groupId)["row_id"]
        else:
            return False

        if not rowIds or adviceRowId in rowIds:
            return item._adviceDelayIsTimedOut(groupId)
        else:
            return False

    def _get_default_item_ref(self, meeting_date, service, item_number):
        return "{service}/{meetingdate}-{itemnumber}".format(
            meetingdate=meeting_date, service=service, itemnumber=item_number
        )

    def _get_college_item_ref(self, meeting, meeting_date, service, item_number):
        return "{meetingdate}-{meetingnumber}/{service}/{itemnumber}".format(
            meetingdate=meeting_date,
            meetingnumber=meeting.meeting_number,
            service=service,
            itemnumber=item_number,
        )

    def _get_council_item_ref(self, meeting, meeting_date, service, item_number):
        if self.context.getPrivacy() == "secret":
            secretnum = len(meeting.get_items(unrestricted=True)) - len(
                meeting.get_items(
                    unrestricted=True,
                    the_objects=False,
                    additional_catalog_query={"privacy": "public"},
                )
            )

            res = "{date}-HC{secretnum}/{srv}/{itemnum}".format(
                date=meeting_date,
                secretnum=secretnum,
                srv=service,
                itemnum=item_number,
            )
        else:
            res = "{date}/{srv}/{itemnum}".format(
                date=meeting_date, srv=service, itemnum=item_number
            )
        return res

    security.declarePublic("compute_item_ref")

    def compute_item_ref(self):
        if not self.context.hasMeeting():
            return ""

        meeting = self.context.getMeeting()
        if meeting.start_date:
            meeting_date = meeting.start_date
        else:
            meeting_date = meeting.date

        date_str = meeting_date.strftime("%Y%m%d")
        service = (
            self.context.getProposingGroup(theObject=True)
            .acronym.split("/")[0]
            .strip()
            .upper()
        )
        item_number = self.context.getItemNumber(for_display=True)

        if self.context.portal_type == "MeetingItemCollege":
            return self._get_college_item_ref(meeting, date_str, service, item_number)
        elif self.context.portal_type == "MeetingItemCouncil":
            return self._get_council_item_ref(meeting, date_str, service, item_number)
        else:
            return self._get_default_item_ref(date_str, service, item_number)

    security.declarePublic("showFollowUp")

    def showFollowUp(self):
        """
        Final state, every member of the proposing group and the MeetingManager may view.
        presented and itemfrozen, only MeetingManager
        otherwise, only for Manager
        """
        showfollowUp = getRequest().get('Products.MeetingLalouviere.showFollowUp_cachekey', None)
        if showfollowUp is None:
            tool = api.portal.get_tool('portal_plonemeeting')
            if self.getSelf().hasMeeting() and not self.getSelf().query_state().startswith("returned_"):
                cfg = tool.getMeetingConfig(self.getSelf())
                if self.getSelf().query_state() in ('presented', 'itemfrozen'):
                    showfollowUp = tool.isManager(cfg)
                else:
                    org_uid = self.getSelf().getProposingGroup(theObject=False)
                    showfollowUp = tool.isManager(cfg) or tool.user_is_in_org(org_uid=org_uid)
            else:
                showfollowUp = tool.isManager(realManagers=True)

            getRequest().set('Products.MeetingLalouviere.showFollowUp_cachekey', showfollowUp)
        return showfollowUp


class LLMeetingConfig(CustomMeetingConfig):
    """Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom."""

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def _extraSearchesInfo(self, infos):
        """Add some specific searches."""
        super(LLMeetingConfig, self)._extraSearchesInfo(infos)
        cfg = self.getSelf()
        itemType = cfg.getItemTypeName()
        proposed_to_director = (
            "searchproposedtodirector",
            {
                "subFolderId": "searches_items",
                "active": True,
                "query": [
                    {
                        "i": "portal_type",
                        "o": "plone.app.querystring.operation.selection.is",
                        "v": [itemType, ],
                    },
                    {
                        "i": "review_state",
                        "o": "plone.app.querystring.operation.selection.is",
                        "v": ["proposed_to_director"],
                    },
                ],
                "sort_on": u"modified",
                "sort_reversed": True,
                "showNumberOfItems": True,
                "tal_condition": "python:tool.userIsAmong(['directors'])",
                "roles_bypassing_talcondition": ["Manager", ],
            },
        )
        extra_infos = []
        if 'council' in cfg.getId():
            extra_infos = [
                proposed_to_director,
            ]
        elif 'college' in cfg.getId():
            extra_infos = [
                (
                    "searchproposedtobudgetreviewer",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_budget_reviewer"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                (
                    "searchproposedtoservicehead",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_servicehead"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition":
                            "python:tool.userIsAmong(['serviceheads', 'officemanagers', 'divisionheads', 'directors'])",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                (
                    "searchproposedtoofficemanager",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_officemanager"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "python:tool.userIsAmong(['officemanagers', 'divisionheads', 'directors'])",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                (
                    "searchproposedtodivisionhead",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_divisionhead"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "python:tool.userIsAmong(['divisionheads', 'directors'])",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                proposed_to_director,
                # Items in state 'proposed_to_dg'
                (
                    "searchproposedtodg",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_dg"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "python: tool.isManager(cfg)",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                # Items in state 'proposed_to_alderman'
                (
                    "searchproposedtoalderman",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_alderman"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "python:tool.userIsAmong(['alderman'])",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                (
                    "searchItemsTofollow_up_yes",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [
                                    "accepted",
                                    "refused",
                                    "delayed",
                                    "accepted_but_modified",
                                ],
                            },
                            {
                                "i": "getFollowUp",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["follow_up_yes", ],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                # Items to follow provider but not to print in Dashboard'
                (
                    "searchItemsProvidedFollowUpButNotToPrint",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [
                                    "accepted",
                                    "refused",
                                    "delayed",
                                    "accepted_but_modified",
                                ],
                            },
                            {
                                "i": "getFollowUp",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["follow_up_provided_not_printed", ],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                # Items to follow provider and to print
                (
                    "searchItemsProvidedFollowUp",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [
                                    "accepted",
                                    "refused",
                                    "delayed",
                                    "accepted_but_modified",
                                ],
                            },
                            {
                                "i": "getFollowUp",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["follow_up_provided", ],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
            ]
        infos.update(OrderedDict(extra_infos))
        return infos

    def _custom_reviewersFor(self):
        '''Manage reviewersFor Bourgmestre because as some 'creators' suffixes are
           used after reviewers levels, this break the _highestReviewerLevel and other
           related hierarchic level functionalities.'''
        cfg = self.getSelf()

        reviewers = [('directors', ['proposed_to_director', ])]

        if cfg.getId() == 'meeting-config-college':
            reviewers = [
                ('alderman', ['proposed_to_alderman', ]),
                ('directors',
                 ['proposed_to_dg',
                  'proposed_to_director',
                  'proposed_to_divisionhead',
                  'proposed_to_officemanager',
                  'proposed_to_servicehead']),
                ('divisionheads',
                 ['proposed_to_divisionhead',
                  'proposed_to_officemanager',
                  'proposed_to_servicehead']),
                ('officemanagers',
                 ['proposed_to_officemanager',
                  'proposed_to_servicehead']),
                ('serviceheads',
                 ['proposed_to_servicehead']),
            ]
        return OrderedDict(reviewers)

    def get_item_custom_suffix_roles(self, item, item_state):
        '''See doc in interfaces.py.'''
        suffix_roles = {}
        if item_state == 'proposed_to_budget_reviewer':
            for suffix in get_all_suffixes(item.getProposingGroup()):
                suffix_roles[suffix] = ['Reader']
                if suffix == 'budgetimpactreviewers':
                    suffix_roles[suffix] += ['Contributor', 'Editor', 'Reviewer']

        return True, suffix_roles


class MLLCustomToolPloneMeeting(CustomToolPloneMeeting):
    '''Adapter that adapts portal_plonemeeting.'''

    implements(IToolPloneMeetingCustom)
    security = ClassSecurityInfo()

    def performCustomWFAdaptations(
            self, meetingConfig, wfAdaptation, logger, itemWorkflow, meetingWorkflow):
        ''' '''
        if wfAdaptation == 'propose_to_budget_reviewer':
            _addIsolatedState(
                new_state_id='proposed_to_budget_reviewer',
                origin_state_id='itemcreated',
                origin_transition_id='proposeToBudgetImpactReviewer',
                origin_transition_title=translate("proposeToBudgetImpactReviewer", "plone"),
                # origin_transition_icon=None,
                origin_transition_guard_expr_name='mayCorrect()',
                back_transition_guard_expr_name="mayCorrect()",
                back_transition_id='backTo_itemcreated_from_proposed_to_budget_reviewer',
                back_transition_title=translate("validateByBudgetImpactReviewer", "plone"),
                # back_transition_icon=None
                itemWorkflow=itemWorkflow)
            return True
        if wfAdaptation == 'apply_council_state_label':
            meetingWorkflow.states['frozen'].title = translate("in_committee", "plone")
            meetingWorkflow.transitions['freeze'].title = translate("setInCommittee", "plone")
            meetingWorkflow.states['published'].title = translate("in_council", "plone")
            meetingWorkflow.transitions['publish'].title = translate("setInCouncil", "plone")

            itemWorkflow.states['itemfrozen'].title = translate("in_committee", "plone")
            itemWorkflow.transitions['itemfreeze'].title = translate("setItemInCommittee", "plone")
            itemWorkflow.states['itempublished'].title = translate("in_council", "plone")
            itemWorkflow.transitions['itempublish'].title = translate("setItemInCouncil", "plone")
            return True
        return False


class MeetingItemMLLWorkflowActions(MeetingItemCommunesWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCommunesWorkflowActions'''

    implements(IMeetingItemCommunesWorkflowActions)
    security = ClassSecurityInfo()

    def doProposeToBudgetImpactReviewer(self, stateChange):
        pass


# ------------------------------------------------------------------------------
InitializeClass(MLLCustomToolPloneMeeting)
InitializeClass(CustomMeetingItem)
InitializeClass(CustomMeeting)
InitializeClass(LLMeetingConfig)
# ------------------------------------------------------------------------------

LLO_WAITING_ADVICES_FROM_STATES = {
    '*':
    (
        {'from_states': ('itemcreated', ),
         'back_states': ('itemcreated', ),
         'perm_cloned_state': 'itemcreated',
         'use_custom_icon': False,
         # default to "validated", this avoid using the backToValidated title that
         # is translated to "Remove from meeting"
         'use_custom_back_transition_title_for': ("validated", ),
         # we can define some back transition id for some back_to_state
         # if not, a generated transition is used, here we could have for example
         # 'defined_back_transition_ids': {"validated": "validate"}
         'defined_back_transition_ids': {},
         # if () given, a custom transition icon is used for every back transitions
         'only_use_custom_back_transition_icon_for': ("validated", ),
         'use_custom_state_title': False,
         'use_custom_transition_title_for': {},
         'remove_modify_access': True,
         'adviser_may_validate': True,
         # must end with _waiting_advices
         'new_state_id': None,
         },
        {'from_states': ('proposed_to_alderman', ),
         'back_states': ('proposed_to_alderman', ),
         'perm_cloned_state': 'validated',
         'use_custom_icon': False,
         # default to "validated", this avoid using the backToValidated title that
         # is translated to "Remove from meeting"
         'use_custom_back_transition_title_for': ("validated", ),
         # we can define some back transition id for some back_to_state
         # if not, a generated transition is used, here we could have for example
         # 'defined_back_transition_ids': {"validated": "validate"}
         'defined_back_transition_ids': {},
         # if () given, a custom transition icon is used for every back transitions
         'only_use_custom_back_transition_icon_for': ("validated", ),
         'use_custom_state_title': True,
         'use_custom_transition_title_for': {},
         'remove_modify_access': True,
         'adviser_may_validate': False,
         # must end with _waiting_advices
         'new_state_id': None,
         },
    ),
}
adaptations.WAITING_ADVICES_FROM_STATES.update(LLO_WAITING_ADVICES_FROM_STATES)
