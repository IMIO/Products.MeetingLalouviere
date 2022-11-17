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

from Products.MeetingCommunes.adapters import (
    CustomMeeting,
    CustomMeetingConfig, CustomToolPloneMeeting, MeetingItemCommunesWorkflowActions,
)
from Products.MeetingCommunes.adapters import CustomMeetingItem
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.interfaces import IMeetingItemCommunesWorkflowActions
from Products.MeetingLalouviere.config import COMMISSION_EDITORS_SUFFIX
from Products.MeetingLalouviere.config import COUNCIL_COMMISSION_IDS
from Products.MeetingLalouviere.config import COUNCIL_MEETING_COMMISSION_IDS_2013
from Products.MeetingLalouviere.config import COUNCIL_MEETING_COMMISSION_IDS_2019
from Products.MeetingLalouviere.config import COUNCIL_MEETING_COMMISSION_IDS_2020
from Products.MeetingLalouviere.config import DG_GROUP_ID
from Products.MeetingLalouviere.config import FINANCE_GROUP_ID
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.model.adaptations import _addIsolatedState
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.adapters import (
    ItemPrettyLinkAdapter,
    CompoundCriterionBaseAdapter,
)
from Products.PloneMeeting.config import NOT_GIVEN_ADVICE_VALUE
from Products.PloneMeeting.interfaces import (
    IMeetingConfigCustom, IToolPloneMeetingCustom,
)
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.PloneMeeting.utils import org_id_to_uid

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from collective.contact.plonegroup.utils import get_all_suffixes
from imio.helpers.content import uuidsToObjects
from plone import api
from plone.memoize import ram
from zope.i18n import translate
from zope.interface import implements


RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {
    "meetingitemcollegelalouviere_workflow":
    # view permissions
    {
        "Access contents information": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "View": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "PloneMeeting: Read budget infos": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "PloneMeeting: Read decision": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "PloneMeeting: Read item observations": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "MeetingLalouviere: Read commission transcript": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "MeetingLalouviere: Read providedFollowUp": ["Manager",],
        "MeetingLalouviere: Read followUp": ["Manager",],
        "MeetingLalouviere: Read neededFollowUp": ["Manager",],
        # edit permissions
        "Modify portal content": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Write budget infos": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
            "MeetingBudgetImpactEditor",
        ],
        "PloneMeeting: Write decision": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "Review portal content": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "Add portal content": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Add annex": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Add annexDecision": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Write decision annex": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        # MeetingManagers edit permissions
        "Delete objects": ["Manager", "MeetingManager",],
        "PloneMeeting: Write item MeetingManager reserved fields": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "MeetingLalouviere: Write commission transcript": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Write marginal notes": ["Manager", "MeetingManager",],
        "MeetingLalouviere: Write providedFollowUp": ["Manager",],
        "MeetingLalouviere: Write followUp": ["Manager",],
        "MeetingLalouviere: Write neededFollowUp": ["Manager",],
    },
    "meetingitemcouncillalouviere_workflow":
    # view permissions
    {
        "Access contents information": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "View": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "PloneMeeting: Read budget infos": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "PloneMeeting: Read decision": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "PloneMeeting: Read item observations": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "MeetingLalouviere: Read commission transcript": [
            "Manager",
            "MeetingManager",
            "MeetingMember",
            "MeetingServiceHead",
            "MeetingOfficeManager",
            "MeetingDivisionHead",
            "MeetingDirector",
            "MeetingObserverLocal",
            "Reader",
        ],
        "MeetingLalouviere: Read providedFollowUp": ["Manager",],
        "MeetingLalouviere: Read followUp": ["Manager",],
        "MeetingLalouviere: Read neededFollowUp": ["Manager",],
        # edit permissions
        "Modify portal content": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Write budget infos": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
            "MeetingBudgetImpactEditor",
        ],
        "PloneMeeting: Write decision": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "Review portal content": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "Add portal content": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Add annex": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Add annexDecision": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Write decision annex": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        # MeetingManagers edit permissions
        "Delete objects": ["Manager", "MeetingManager",],
        "PloneMeeting: Write item MeetingManager reserved fields": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "MeetingLalouviere: Write commission transcript": [
            "Manager",
            "MeetingMember",
            "MeetingOfficeManager",
            "MeetingManager",
        ],
        "PloneMeeting: Write marginal notes": ["Manager", "MeetingManager",],
        "MeetingLalouviere: Write providedFollowUp": ["Manager",],
        "MeetingLalouviere: Write followUp": ["Manager",],
        "MeetingLalouviere: Write neededFollowUp": ["Manager",],
    },
}


# disable waiting advice
customWfAdaptations = ('item_validation_shortcuts',
                       'item_validation_no_validate_shortcuts',
                       'only_creator_may_delete',
                       # first define meeting workflow state removal
                       'no_freeze',
                       'no_publication',
                       'no_decide',
                       # then define added item decided states
                       'accepted_but_modified',
                       'postpone_next_meeting',
                       'mark_not_applicable',
                       'removed',
                       'removed_and_duplicated',
                       'refused',
                       'delayed',
                       'pre_accepted',
                       # then other adaptations
                       'reviewers_take_back_validated_item',
                       'presented_item_back_to_validation_state',
                       'return_to_proposing_group',
                       'return_to_proposing_group_with_last_validation',
                       'return_to_proposing_group_with_all_validations',
                       'decide_item_when_back_to_meeting_from_returned_to_proposing_group',
                       'hide_decisions_when_under_writing',
                       'waiting_advices',
                       'waiting_advices_adviser_send_back',
                       'waiting_advices_proposing_group_send_back',
                       'accepted_out_of_meeting',
                       'accepted_out_of_meeting_and_duplicated',
                       'accepted_out_of_meeting_emergency',
                       'accepted_out_of_meeting_emergency_and_duplicated',
                       'transfered',
                       'transfered_and_duplicated',
                       'propose_to_budget_reviewer',
                       'apply_council_state_label',
                       'meetingmanager_correct_closed_meeting',
                       )

MeetingConfig.wfAdaptations = customWfAdaptations
CustomMeetingConfig.wfAdaptations = customWfAdaptations


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

    security.declarePublic("get_normal_classifiers")

    def get_normal_classifiers(self):
        """Returns the 'normal' categories"""
        tool = api.portal.get_tool("portal_plonemeeting")
        mc = tool.getMeetingConfig(self.getSelf())
        classifiers = mc.getCategories(catType='classifiers', onlySelectable=False)
        res = []
        for classifier in classifiers:
            classifier_id = classifier.getId()
            if not classifier_id.endswith("supplement"):
                res.append(classifier_id)
        return res

    security.declarePublic("get_first_suppl_classifiers")

    def get_first_suppl_classifiers(self):
        """Returns the '1er-supplement' categories"""
        tool = api.portal.get_tool("portal_plonemeeting")
        mc = tool.getMeetingConfig(self.getSelf())
        classifiers = mc.getCategories(catType='classifiers', onlySelectable=False)
        res = []
        for classifier in classifiers:
            classifier_id = classifier.getId()
            if classifier_id.endswith("1er-supplement"):
                res.append(classifier_id)
        return res

    security.declarePublic("get_second_suppl_classifiers")

    def get_second_suppl_classifiers(self):
        """Returns the '2eme-supplement' categories"""
        tool = api.portal.get_tool("portal_plonemeeting")
        mc = tool.getMeetingConfig(self.getSelf())
        classifiers = mc.getCategories(catType='classifiers', onlySelectable=False)
        res = []
        for classifier in classifiers:
            classifier_id = classifier.getId()
            if classifier_id.endswith("2eme-supplement"):
                res.append(classifier_id)
        return res

    security.declarePublic("get_third_suppl_classifiers")

    def get_third_suppl_classifiers(self):
        """Returns the '3eme-supplement' categories"""
        tool = api.portal.get_tool("portal_plonemeeting")
        mc = tool.getMeetingConfig(self.getSelf())
        classifiers = mc.getCategories(catType='classifiers', onlySelectable=False)
        res = []
        for classifier in classifiers:
            classifier_id = classifier.getId()
            if classifier_id.endswith("3eme-supplement"):
                res.append(classifier_id)
        return res

    def _get_renumbered_items(self, itemUids, privacy, listTypes, base_num_classifiers, item_list_classifiers):
        number = (
                self.getNumberOfItems(
                    itemUids,
                    listTypes=listTypes,
                    privacy=privacy,
                    classifiers=base_num_classifiers
                )
                + 1
        )
        items = self.getSelf().get_items(itemUids,
                                        ordered=True,
                                        listTypes=listTypes,
                                        additional_catalog_query={
                                            'privacy': privacy,
                                            'getRawClassifier': item_list_classifiers
                                        })
        res = []
        for item in items:
            res.append([number, item])
            number += 1
        return res

    security.declarePublic("get_normal_items")

    def get_normal_items(self, itemUids, privacy="public", listTypes=['normal'], renumber=False):
        """Returns the items presented as first supplement"""

        items = self.getSelf().get_items(itemUids,
                                        ordered=True,
                                        listTypes=listTypes,
                                        additional_catalog_query={
                                            'privacy': privacy,
                                            'getRawClassifier': self.get_normal_classifiers()
                                        })
        if renumber:
            number = 1
            res = []
            for item in items:
                res.append([number, item])
                number += 1
            return res

        return items

    security.declarePublic("get_items_first_suppl")

    def get_items_first_suppl(self, itemUids, privacy="public", listTypes=['normal']):
        """Returns the items presented as first supplement"""
        normal_classifiers = self.get_normal_classifiers()
        first_suppl_classifiers = self.get_first_suppl_classifiers()
        return self._get_renumbered_items(itemUids,
                                          privacy,
                                          listTypes,
                                          normal_classifiers,
                                          first_suppl_classifiers)

    security.declarePublic("get_items_second_suppl")

    def get_items_second_suppl(self, itemUids, privacy="public", listTypes=['normal']):
        """Returns the items presented as second supplement"""

        normal_classifiers = self.get_normal_classifiers()
        first_suppl_classifiers = self.get_first_suppl_classifiers()
        second_suppl_classifiers = self.get_second_suppl_classifiers()
        return self._get_renumbered_items(itemUids,
                                          privacy,
                                          listTypes,
                                          normal_classifiers + first_suppl_classifiers,
                                          second_suppl_classifiers)

    security.declarePublic("get_items_third_suppl")

    def get_items_third_suppl(self, itemUids, privacy="public", listTypes=['normal']):
        """Returns the items presented as third supplement"""
        normal_classifiers = self.get_normal_classifiers()
        first_suppl_classifiers = self.get_first_suppl_classifiers()
        second_suppl_classifiers = self.get_second_suppl_classifiers()
        third_suppl_classifiers = self.get_third_suppl_classifiers()
        return self._get_renumbered_items(itemUids,
                                          privacy,
                                          listTypes,
                                          normal_classifiers + first_suppl_classifiers + second_suppl_classifiers,
                                          third_suppl_classifiers)

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

    security.declarePublic("getCommissionTitle")

    def getCommissionTitle(self, commissionNumber=1, roman_prefix=False):
        """
          Given a commissionNumber, return the commission title depending on corresponding classifiers
        """
        meeting = self.getSelf()
        commission_classifiers = meeting.get_commission_classifiers()
        if not len(commission_classifiers) >= commissionNumber:
            return ""
        commission_clf = commission_classifiers[commissionNumber - 1]
        # build title
        if isinstance(commission_clf, tuple):
            res = "Commission " + "/".join(
                [subclf.Title().replace("Commission ", "") for subclf in commission_clf]
            )
        else:
            res = commission_clf.Title()

        if roman_prefix:
            roman_numbers = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}
            res = "{roman}. {res}".format(
                roman=roman_numbers[commissionNumber], res=res
            )

        return res

    security.declarePublic("get_commission_classifiers_ids")

    def get_commission_classifiers_ids(self):
        """Returns the list of classifiers used for Commissions.
           Since june 2013, some commission are aggregating several classifiers, in this case,
           a sublist of classifiers is returned...
           Since 2019, travaux commission is grouped with finance..."""
        meeting = self.getSelf()
        date = meeting.date
        if not date or date.year > 2020 or (date.year == 2020 and date.month > 8):
            # since september 2020 commissions are grouped differently
            # patrimoine is grouped with travaux and finance
            # also police is moved to first place
            commission_classifier_ids = COUNCIL_MEETING_COMMISSION_IDS_2020
        elif date.year >= 2019 and date.month > 8:
            # since september 2019 commissions are grouped differently
            # finance is grouped with travaux
            commission_classifier_ids = COUNCIL_MEETING_COMMISSION_IDS_2019
        # creating a new Meeting or editing an existing meeting with date >= june 2013
        elif date.year >= 2013 and date.month > 5:
            # since 2013 commissions does NOT correspond to commission as MeetingItem.category
            # several MeetingItem.category are taken for one single commission...
            commission_classifier_ids = COUNCIL_MEETING_COMMISSION_IDS_2013
        else:
            commission_classifier_ids = COUNCIL_COMMISSION_IDS

        return commission_classifier_ids

    security.declarePublic("get_commission_classifiers")

    def get_commission_classifiers(self):
        """Returns the list of classifier used for Commissions.
           Since june 2013, some commission are aggregating several classifiers, in this case,
           a sublist of classifiers is returned...
           Since 2019, travaux commission is grouped with finance..."""
        commission_classifier_ids = self.getSelf().adapted().get_commission_classifiers_ids()

        tool = getToolByName(self, "portal_plonemeeting")
        mc = tool.getMeetingConfig(self)
        res = []
        for id in commission_classifier_ids:
            # check if we have sub-classifiers, aka a commission made of several classifiers
            if isinstance(id, tuple):
                res2 = []
                for subcls_id in id:
                    res2.append(getattr(mc.classifiers, subcls_id))
                res.append(tuple(res2))
            else:
                res.append(getattr(mc.classifiers, id))
        return tuple(res)

    Meeting.get_commission_classifiers = get_commission_classifiers


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

    security.declarePublic("getLabelClassifier")

    def getLabelClassifier(self):
        """Returns the label to use for field MeetingItem.category
          The label is different between college and council"""
        item = self.getSelf()
        if item.portal_type == "MeetingItemCouncil":

            return item.utranslate(
                "MeetingLalouviere_label_councilclassifier", domain="PloneMeeting"
            )
        else:
            return item.utranslate("PloneMeeting_label_classifier", domain="PloneMeeting")

    MeetingItem.getLabelClassifier = getLabelClassifier

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
            dg_group_uid = org_id_to_uid(DG_GROUP_ID)
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
            dg_group_uid = org_id_to_uid(DG_GROUP_ID)
            if theObjects:
                res += uuidsToObjects(dg_group_uid, unrestricted=True)
            else:
                res.append(dg_group_uid)
        proposingGroup = item.getProposingGroup(theObject=theObjects)
        if proposingGroup:
            res.append(proposingGroup)
        return res

    # security.declarePublic("getCollegeItem")

    # def getCollegeItem(self):
    #     """Returns the predecessor item that was in the college."""
    #     item = self.getSelf()
    #     predecessor = item.getPredecessor()
    #     collegeItem = None
    #     while predecessor:
    #         if predecessor.portal_type == "MeetingItemCollege":
    #             collegeItem = predecessor
    #             break
    #     return collegeItem

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
            res = ["interventions", "commissionTranscript"]
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
            meetingnumber=meeting.getMeetingNumber(),
            service=service,
            itemnumber=item_number,
        )

    def _get_council_item_ref(self, meeting, meeting_date, service, item_number):
        if self.context.getPrivacy() == "secret":
            secretnum = len(meeting.get_items(unrestricted=True)) - len(
                meeting.get_items(
                    unrestricted=True,
                    theObjects=False,
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
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.getSelf())
        if not self.getSelf().query_state().startswith("returned_") and self.getSelf().hasMeeting():
            if self.getSelf().query_state() in ('presented', 'itemfrozen'):
                return tool.isManager(cfg)
            else:
                return not tool.isPowerObserverForCfg(cfg)
        else:
            return tool.isManager(realManagers=True)


class LLMeetingConfig(CustomMeetingConfig):
    """Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom."""

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def _extraSearchesInfo(self, infos):
        """Add some specific searches."""
        super(CustomMeetingConfig, self)._extraSearchesInfo(infos)
        cfg = self.getSelf()
        itemType = cfg.getItemTypeName()
        extra_infos = OrderedDict(
            [
                # Items in state 'proposed'
                # Items in state 'proposed'
                (
                    "searchproposeditems",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType,],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed"],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "python: tool.userIsAmong(['creators']) "
                        "and not tool.userIsAmong(['reviewers'])",
                        "roles_bypassing_talcondition": ["Manager",],
                    },
                ),
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
                                "v": [itemType,],
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
                        "tal_condition": "tool.isManager(here) and 'validate_by_dg_and_alderman' in "
                        "cfg.getWorkflowAdaptations()",
                        "roles_bypassing_talcondition": ["Manager",],
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
                                "v": [itemType,],
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
                        "tal_condition": "python:tool.userIsAmong(['alderman']) and 'validate_by_dg_and_alderman' "
                        "in cfg.getWorkflowAdaptations()",
                        "roles_bypassing_talcondition": ["Manager",],
                    },
                ),
                # Items in state 'validated'
                (
                    "searchvalidateditems",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType,],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["validated"],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager",],
                    },
                ),
                # Items to follow up'
                (
                    "searchItemsTofollow_up_yes",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType,],
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
                                "v": ["follow_up_yes",],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager",],
                    },
                ),
                # Items to follow provider but not to print in Dashboard'
                (
                    "searchItemsToProviderNotToPrint",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType,],
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
                                "v": ["follow_up_provided_not_printed",],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager",],
                    },
                ),
                # Items to follow provider and to print'
                (
                    "searchItemsForDashboard",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType,],
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
                                "v": ["follow_up_provided",],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager",],
                    },
                ),
                (
                    "searchitemsofmycommissions",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType,],
                            },
                            {
                                "i": "CompoundCriterion",
                                "o": "plone.app.querystring.operation.compound.is",
                                "v": "items-of-my-commissions",
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": False,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager",],
                    },
                ),
                (
                    "searchitemsofmycommissionstoedit",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType,],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["itemfrozen"],
                            },
                            {
                                "i": "CompoundCriterion",
                                "o": "plone.app.querystring.operation.compound.is",
                                "v": "items-of-my-commissions",
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": False,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager",],
                    },
                ),
                (
                    FINANCE_ADVICES_COLLECTION_ID,
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType,],
                            },
                            {
                                "i": "indexAdvisers",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [
                                    "delay_row_id__unique_id_002",
                                    "delay_row_id__unique_id_003",
                                    "delay_row_id__unique_id_004",
                                ],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "python: 'tool.userIsAmong(['budgetimpactreviewers']) or tool.isManager(here)",
                        "roles_bypassing_talcondition": ["Manager",],
                    },
                ),
            ]
        )
        infos.update(extra_infos)
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

    # def get_item_corresponding_state_to_assign_local_roles(self, item_state):
    #     '''See doc in interfaces.py.'''
    #     cfg = self.getSelf()
    #     corresponding_item_state = None
    #     item_val_levels_states = cfg.getItemWFValidationLevels(data='state', only_enabled=True)
    #     # return_to_proposing_group WFAdaptation
    #     if item_state.startswith('returned_to_proposing_group'):
    #         if item_state == 'returned_to_proposing_group':
    #             corresponding_item_state = item_val_levels_states[0] if item_val_levels_states else 'itemcreated'
    #         else:
    #             corresponding_item_state = item_state.split('returned_to_proposing_group_')[1]
    #     # waiting_advices WFAdaptation
    #     elif item_state.endswith('_waiting_advices'):
    #         corresponding_item_state = item_state.split('_waiting_advices')[0]
    #     return corresponding_item_state


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
                origin_transition_title=translate("proposeToBudgetImpactReviewer", "imio.actionspanel"),
                # origin_transition_icon=None,
                origin_transition_guard_expr_name='mayCorrect()',
                back_transition_guard_expr_name="mayCorrect()",
                back_transition_id='backTo_itemcreated_from_proposed_to_budget_reviewer',
                back_transition_title=translate("validateByBudgetImpactReviewer_done_descr", "imio.actionspanel"),
                # back_transition_icon=None
                itemWorkflow=itemWorkflow)
            return True
        if wfAdaptation == 'apply_council_state_label':
            meetingWorkflow.states['frozen'].title = translate("in_committee", "plone")
            meetingWorkflow.states['decided'].title = translate("in_council", "plone")
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


class MLItemPrettyLinkAdapter(ItemPrettyLinkAdapter):
    """
      Override to take into account MeetingLiege use cases...
    """

    def _leadingIcons(self):
        """
          Manage icons to display before the icons managed by PrettyLink._icons.
        """
        # Default PM item icons
        icons = super(MLItemPrettyLinkAdapter, self)._leadingIcons()

        item = self.context

        if item.isDefinedInTool():
            return icons

        itemState = item.query_state()
        tool = api.portal.get_tool("portal_plonemeeting")
        cfg = tool.getMeetingConfig(item)

        # add some icons specific for dashboard if we are actually on the dashboard...
        if (
            itemState in cfg.getItemDecidedStates()
            and item.REQUEST.form.get("topicId", "") == "searchitemsfollowupdashboard"
        ):
            itemFollowUp = item.getFollowUp()
            if itemFollowUp == "follow_up_yes":
                icons.append(("follow_up_yes.png", "icon_help_follow_up_needed"))
            elif itemFollowUp == "follow_up_provided":
                icons.append(("follow_up_provided.png", "icon_help_follow_up_provided"))

        # Add our icons for wf states
        if itemState == "proposed_to_director":
            icons.append(
                (
                    "proposeToDirector.png",
                    translate(
                        "icon_help_proposed_to_director",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "proposed_to_divisionhead":
            icons.append(
                (
                    "proposeToDivisionHead.png",
                    translate(
                        "icon_help_proposed_to_divisionhead",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "proposed_to_officemanager":
            icons.append(
                (
                    "proposeToOfficeManager.png",
                    translate(
                        "icon_help_proposed_to_officemanager",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "itempublished":
            icons.append(
                (
                    "itempublished.png",
                    translate(
                        "icon_help_itempublished",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "proposed_to_servicehead":
            icons.append(
                (
                    "proposeToServiceHead.png",
                    translate(
                        "icon_help_proposed_to_servicehead",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "itemfrozen":
            icons.append(
                (
                    "itemfrozen.png",
                    translate(
                        "icon_help_itemfrozen",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "proposed_to_budgetimpact_reviewer":
            icons.append(
                (
                    "proposed_to_budgetimpact_reviewer.png",
                    translate(
                        "icon_help_proposed_to_budgetimpact_reviewer",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "proposed_to_dg":
            icons.append(
                (
                    "proposeToDg.png",
                    translate(
                        "icon_help_proposed_to_dg",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "proposed_to_alderman":
            icons.append(
                (
                    "proposeToAlderman.png",
                    translate(
                        "icon_help_proposed_to_alderman",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )

        return icons


class SearchItemsOfMyCommissionsAdapter(CompoundCriterionBaseAdapter):
    def itemsofmycommissions_cachekey(method, self):
        """cachekey method for every CompoundCriterion adapters."""
        return str(self.request._debug)

    @property
    @ram.cache(itemsofmycommissions_cachekey)
    def query_itemsofmycommissions(self):
        """Queries all items of commissions of the current user, no matter wich suffix
           of the group the user is in."""
        if not self.cfg:
            return {}
        # retrieve the commissions which the current user is editor for.
        # a commission groupId match a category but with an additional suffix (COMMISSION_EDITORS_SUFFIX)
        # so we remove that suffix
        groups = self.tool.get_plone_groups_for_user()
        clasifiers = []
        for group in groups:
            if group.endswith(COMMISSION_EDITORS_SUFFIX):
                clasifier_id = group.split("_")[0]
                clasifiers.append(clasifier_id)
                clasifiers.append("{}-1er-supplement".format(clasifier_id))

        return {
            "portal_type": {"query": self.cfg.getItemTypeName()},
            "getRawClassifier": {"query": sorted(clasifiers)},
        }

    # we may not ram.cache methods in same file with same name...
    query = query_itemsofmycommissions
