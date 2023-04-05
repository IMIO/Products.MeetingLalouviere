# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.config import PORTAL_CATEGORIES
from Products.MeetingLalouviere.config import LLO_APPLYED_COLLEGE_WFA
from Products.MeetingLalouviere.config import LLO_APPLYED_COUNCIL_WFA
from Products.MeetingLalouviere.config import LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS
from Products.MeetingLalouviere.config import LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS
from Products.MeetingCommunes.profiles.examples_fr import import_data as mc_import_data
from Products.PloneMeeting.profiles import (
    AnnexTypeDescriptor,
    ItemAnnexTypeDescriptor,
    ItemAnnexSubTypeDescriptor,
    CategoryDescriptor,
    OrgDescriptor,
)

data = deepcopy(mc_import_data.data)

# Users and groups -------------------------------------------------------------
# no user
data.orgs.append(OrgDescriptor("secretaire-communal", "Secrétaire Communal", u"Sec"))
data.orgs.append(
    OrgDescriptor("secretaire-communal-adj", "Secrétaire Communal Adjoint", u"Sec-Adj")
)

# <editor-fold desc="Annex types">
overheadAnalysisSubtype = ItemAnnexSubTypeDescriptor(
    "overhead-analysis-sub-annex",
    "Overhead analysis sub annex",
    other_mc_correspondences=("cfg2_-_annexes_types_-_item_annexes_-_budget-analysis",),
)

overheadAnalysis = ItemAnnexTypeDescriptor(
    "overhead-analysis",
    "Administrative overhead analysis",
    u"overheadAnalysis.png",
    subTypes=[overheadAnalysisSubtype],
    other_mc_correspondences=(
        "cfg2_-_annexes_types_-_item_annexes_-_budget-analysis_-_budget-analysis-sub-annex",
    ),
)

financialAnalysisSubAnnex = ItemAnnexSubTypeDescriptor(
    "financial-analysis-sub-annex", "Financial analysis sub annex"
)

financialAnalysis = ItemAnnexTypeDescriptor(
    "financial-analysis",
    "Financial analysis",
    u"financialAnalysis.png",
    u"Predefined title for financial analysis",
    subTypes=[financialAnalysisSubAnnex],
)

legalAnalysis = ItemAnnexTypeDescriptor(
    "legal-analysis", "Legal analysis", u"legalAnalysis.png"
)

budgetAnalysisCfg2Subtype = ItemAnnexSubTypeDescriptor(
    "budget-analysis-sub-annex", "Budget analysis sub annex"
)

budgetAnalysisCfg2 = ItemAnnexTypeDescriptor(
    "budget-analysis",
    "Budget analysis",
    u"budgetAnalysis.png",
    subTypes=[budgetAnalysisCfg2Subtype],
)

budgetAnalysisCfg1Subtype = ItemAnnexSubTypeDescriptor(
    "budget-analysis-sub-annex",
    "Budget analysis sub annex",
    other_mc_correspondences=(
        "cfg2_-_annexes_types_-_item_annexes_-_budget-analysis_-_budget-analysis-sub-annex",
    ),
)

budgetAnalysisCfg1 = ItemAnnexTypeDescriptor(
    "budget-analysis",
    "Budget analysis",
    u"budgetAnalysis.png",
    subTypes=[budgetAnalysisCfg1Subtype],
    other_mc_correspondences=("cfg2_-_annexes_types_-_item_annexes_-_budget-analysis",),
)

itemAnnex = ItemAnnexTypeDescriptor("item-annex", "Other annex(es)", u"itemAnnex.png")
# Could be used once we
# will digitally sign decisions ? Indeed, once signed, we will need to
# store them (together with the signature) as separate files.
decision = ItemAnnexTypeDescriptor(
    "decision", "Decision", u"decision.png", relatedTo="item_decision"
)
decisionAnnex = ItemAnnexTypeDescriptor(
    "decision-annex",
    "Decision annex(es)",
    u"decisionAnnex.png",
    relatedTo="item_decision",
)
# A vintage annex type
marketingAnalysis = ItemAnnexTypeDescriptor(
    "marketing-annex",
    "Marketing annex(es)",
    u"legalAnalysis.png",
    relatedTo="item_decision",
    enabled=False,
)
# Advice annex types
adviceAnnex = AnnexTypeDescriptor(
    "advice-annex", "Advice annex(es)", u"itemAnnex.png", relatedTo="advice"
)
adviceLegalAnalysis = AnnexTypeDescriptor(
    "advice-legal-analysis",
    "Advice legal analysis",
    u"legalAnalysis.png",
    relatedTo="advice",
)
# Meeting annex types
meetingAnnex = AnnexTypeDescriptor(
    "meeting-annex", "Meeting annex(es)", u"itemAnnex.png", relatedTo="meeting"
)
# </editor-fold>

# COLLEGE
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)
collegeMeeting.transitionsToConfirm = []
collegeMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS)
collegeMeeting.workflowAdaptations = deepcopy(LLO_APPLYED_COLLEGE_WFA)

collegeMeeting.itemPositiveDecidedStates = ["accepted", "accepted_but_modified"]

collegeMeeting.itemAdviceViewStates = [
    "proposed_to_director",
    "proposed_to_dg",
    "proposed_to_alderman",
    "validated",
    "presented",
    "itemfrozen",
]

collegeMeeting.itemAdviceStates = [
    "proposed_to_director",
    "proposed_to_dg",
    "proposed_to_alderman",
]

collegeMeeting.usedItemAttributes = (
    u"description",
    u"budgetInfos",
    u"proposingGroupWithGroupInCharge",
    u"motivation",
    u"decisionSuite",
    u"internalNotes",
    u"observations",
    u"manuallyLinkedItems",
    u"textCheckList",
    u"neededFollowUp",
    u"providedFollowUp",
)

collegeMeeting.usedMeetingAttributes = (
    u"start_date",
    u"end_date",
    u"assembly_guests",
    u"attendees",
    u"excused",
    u"absents",
    u"non_attendees",
    u"signatories",
    u"place",
    u"observations",
)

collegeMeeting.itemAdviceEditStates = ["proposed_to_director", "proposed_to_dg", "proposed_to_alderman", "validated"]
collegeMeeting.itemAdvicesStates = ["proposed_to_director"]

collegeMeeting.annexTypes = [
    financialAnalysis,
    budgetAnalysisCfg1,
    overheadAnalysis,
    itemAnnex,
    decisionAnnex,
    marketingAnalysis,
    adviceAnnex,
    adviceLegalAnalysis,
    meetingAnnex,
]

collegeMeeting.itemBudgetInfosStates = ()  # TODO '("proposed_to_budget_reviewer",)
collegeMeeting.meetingAppDefaultView = "searchallitems"

collegeMeeting.onMeetingTransitionItemActionToExecute = (
    {
        "meeting_transition": "freeze",
        "item_action": "itemfreeze",
        "tal_expression": "",
    },
    {
        "meeting_transition": "decide",
        "item_action": "itemfreeze",
        "tal_expression": "",
    },
    {"meeting_transition": "close", "item_action": "itemfreeze", "tal_expression": ""},
    {"meeting_transition": "close", "item_action": "accept", "tal_expression": ""},
)
collegeMeeting.itemColumns = [
    "static_labels",
    "static_item_reference",
    "Creator",
    "CreationDate",
    "ModificationDate",
    "review_state",
    "getProposingGroup",
    "getGroupsInCharge",
    "advices",
    "meeting_date",
    "async_actions",
]
collegeMeeting.dashboardItemsListingsFilters = (
    "c4",
    "c6",
    "c7",
    "c8",
    "c9",
    "c10",
    "c11",
    "c13",
    "c14",
    "c15",
    "c16",
    "c19",
    "c20",
    "c26",
)
collegeMeeting.availableItemsListVisibleColumns = [
    "static_labels",
    "Creator",
    "CreationDate",
    "ModificationDate",
    "getProposingGroup",
    "getGroupsInCharge",
    "advices",
    "preferred_meeting_date",
    "async_actions",
]
collegeMeeting.dashboardMeetingAvailableItemsFilters = (
    "c4",
    "c7",
    "c8",
    "c10",
    "c11",
    "c13",
    "c14",
    "c16",
    "c20",
    "c26",
)
collegeMeeting.itemsListVisibleColumns = [
    "static_labels",
    "static_item_reference",
    "Creator",
    "review_state",
    "getCategory",
    "getProposingGroup",
    "getGroupsInCharge",
    "advices",
    "async_actions",
]
collegeMeeting.dashboardMeetingLinkedItemsFilters = (
    "c4",
    "c6",
    "c7",
    "c8",
    "c11",
    "c13",
    "c14",
    "c16",
    "c19",
    "c20",
    "c26",
)

# COUNCIL
councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.transitionsToConfirm = []
councilMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS)
councilMeeting.itemPositiveDecidedStates = ["accepted", "accepted_but_modified"]

councilMeeting.workflowAdaptations = deepcopy(LLO_APPLYED_COUNCIL_WFA)
councilMeeting.itemAdviceStates = ["proposed_to_director",]
councilMeeting.itemAdviceEditStates = ["proposed_to_director", "validated"]
councilMeeting.itemCopyGroupsStates = [
    "validated",
    "itemfrozen",
    "itempublished",
]

councilMeeting.onMeetingTransitionItemActionToExecute = (
    {
        "meeting_transition": "setInCommittee",
        "item_action": "setItemInCommittee",
        "tal_expression": "",
    },
    {
        "meeting_transition": "setInCouncil",
        "item_action": "setItemInCouncil",
        "tal_expression": "",
    },
    {
        "meeting_transition": "backToCreated",
        "item_action": "backToPresented",
        "tal_expression": "",
    },
    {
        "meeting_transition": "backToInCommittee",
        "item_action": "backToItemInCouncil",
        "tal_expression": "",
    },
    {
        "meeting_transition": "backToInCommittee",
        "item_action": "backToItemInCommittee",
        "tal_expression": "",
    },
    {"meeting_transition": "close", "item_action": "accept", "tal_expression": "", },
)

councilMeeting.usedItemAttributes = (
    u"category",
    u"description",
    u"budgetInfos",
    u"proposingGroupWithGroupInCharge",
    u"motivation",
    u"decisionSuite",
    u"oralQuestion",
    u"itemInitiator",
    u"internalNotes",
    u"observations",
    u"manuallyLinkedItems",
    u"privacy",
    u"textCheckList",
    u"interventions",
    u"committeeTranscript",
)

councilMeeting.usedMeetingAttributes = (
    u"start_date",
    u"end_date",
    u"assembly_guests",
    u"attendees",
    u"excused",
    u"absents",
    u"non_attendees",
    u"signatories",
    u"place",
    u"observations",
    u"committees",
    u"committees_place",
    u"committees_assembly",
)

councilMeeting.categories = PORTAL_CATEGORIES

for recurringItem in councilMeeting.recurringItems:
    recurringItem.category = "recurrent"

councilMeeting.annexTypes = [
    financialAnalysis,
    legalAnalysis,
    budgetAnalysisCfg2,
    itemAnnex,
    decisionAnnex,
    adviceAnnex,
    adviceLegalAnalysis,
    meetingAnnex,
]

councilMeeting.itemBudgetInfosStates = ()
councilMeeting.meetingAppDefaultView = "searchallitems"
councilMeeting.itemAdviceViewStates = []
councilMeeting.itemColumns = [
    "static_labels",
    "static_item_reference",
    "Creator",
    "CreationDate",
    "ModificationDate",
    "review_state_title",
    "getCategory",
    "getProposingGroup",
    "getGroupsInCharge",
    "committees_index",
    "advices",
    "meeting_date",
    "async_actions",
]
councilMeeting.dashboardItemsListingsFilters = (
    "c4",
    "c5",
    "c6",
    "c7",
    "c8",
    "c9",
    "c10",
    "c11",
    "c13",
    "c14",
    "c15",
    "c16",
    "c19",
    "c20",
    "c26",
    "c31",
)
councilMeeting.availableItemsListVisibleColumns = [
    "static_labels",
    "Creator",
    "getCategory",
    "getProposingGroup",
    "getGroupsInCharge",
    "committees_index",
    "advices",
    "preferred_meeting_date",
    "async_actions",
]
councilMeeting.dashboardMeetingAvailableItemsFilters = (
    "c4",
    "c5",
    "c7",
    "c8",
    "c10",
    "c11",
    "c13",
    "c14",
    "c16",
    "c20",
    "c26",
    "c31",
)
councilMeeting.itemsListVisibleColumns = [
    "static_labels",
    "static_item_reference",
    "CreationDate",
    "ModificationDate",
    "review_state_title",
    "getCategory",
    "getProposingGroup",
    "getGroupsInCharge",
    "committees_index",
    "advices",
    "async_actions",
]
councilMeeting.dashboardMeetingLinkedItemsFilters = (
    "c4",
    "c5",
    "c6",
    "c7",
    "c8",
    "c11",
    "c13",
    "c14",
    "c16",
    "c19",
    "c20",
    "c26",
    "c31",
)

data.meetingConfigs = (collegeMeeting, councilMeeting)
