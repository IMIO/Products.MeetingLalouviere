# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.config import PORTAL_CATEGORIES
from Products.MeetingLalouviere.config import LLO_ITEM_CPAS_WF_VALIDATION_LEVELS, \
    LLO_APPLYED_CPAS_WFA
from Products.MeetingCommunes.profiles.zcpas import import_data as mc_import_data
from Products.PloneMeeting.profiles import (
    AnnexTypeDescriptor,
    ItemAnnexTypeDescriptor,
    ItemAnnexSubTypeDescriptor,
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
bpMeeting = deepcopy(mc_import_data.bpMeeting)
bpMeeting.transitionsToConfirm = []
bpMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_CPAS_WF_VALIDATION_LEVELS)
bpMeeting.workflowAdaptations = deepcopy(LLO_APPLYED_CPAS_WFA)

bpMeeting.itemPositiveDecidedStates = ["accepted", "accepted_but_modified"]

bpMeeting.itemAdviceViewStates = [
    "proposed_to_president",
    "proposed_to_secretaire",
    "proposed_to_n2",
    "proposed_to_n1",
    "validated",
    "presented",
    "itemfrozen",
]

bpMeeting.itemAdviceStates = [
    "proposed_to_president",
    "proposed_to_secretaire",
    "proposed_to_n2",
    "proposed_to_n1",
]

bpMeeting.usedItemAttributes = (
    u"description",
    u"budgetInfos",
    u"proposingGroupWithGroupInCharge",
    u"motivation",
    u"decisionSuite",
    u"internalNotes",
    u"observations",
    u"manuallyLinkedItems",
    u"textCheckList",
    u"providedFollowUp",
)

bpMeeting.usedMeetingAttributes = (
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

bpMeeting.itemAdviceEditStates = [
    "proposed_to_president",
    "proposed_to_secretaire",
    "proposed_to_n2",
    "proposed_to_n1",
    "validated"
]
bpMeeting.itemAdvicesStates = ["proposed_to_president"]

bpMeeting.annexTypes = [
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

bpMeeting.itemBudgetInfosStates = ()
bpMeeting.meetingAppDefaultView = "searchallitems"

bpMeeting.onMeetingTransitionItemActionToExecute = (
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
bpMeeting.itemColumns = [
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
bpMeeting.dashboardItemsListingsFilters = (
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
bpMeeting.availableItemsListVisibleColumns = [
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
bpMeeting.dashboardMeetingAvailableItemsFilters = (
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
bpMeeting.itemsListVisibleColumns = [
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
bpMeeting.dashboardMeetingLinkedItemsFilters = (
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
casMeeting = deepcopy(mc_import_data.casMeeting)
casMeeting.transitionsToConfirm = []
casMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_CPAS_WF_VALIDATION_LEVELS)
casMeeting.itemPositiveDecidedStates = ["accepted", "accepted_but_modified"]

casMeeting.workflowAdaptations = deepcopy(LLO_APPLYED_CPAS_WFA)
casMeeting.itemAdviceStates = ["proposed_to_president",]
casMeeting.itemAdviceEditStates = ["proposed_to_president", "validated"]
casMeeting.itemCopyGroupsStates = [
    "validated",
    "itemfrozen",
]

casMeeting.usedItemAttributes = (
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
)

casMeeting.usedMeetingAttributes = (
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

casMeeting.categories = PORTAL_CATEGORIES

for recurringItem in casMeeting.recurringItems:
    recurringItem.category = "recurrent"

casMeeting.annexTypes = [
    financialAnalysis,
    legalAnalysis,
    budgetAnalysisCfg2,
    itemAnnex,
    decisionAnnex,
    adviceAnnex,
    adviceLegalAnalysis,
    meetingAnnex,
]

casMeeting.itemBudgetInfosStates = ()
casMeeting.meetingAppDefaultView = "searchallitems"
casMeeting.itemAdviceViewStates = []
casMeeting.itemColumns = [
    "static_labels",
    "static_item_reference",
    "Creator",
    "CreationDate",
    "ModificationDate",
    "review_state_title",
    "getCategory",
    "getProposingGroup",
    "getGroupsInCharge",
    "advices",
    "meeting_date",
    "async_actions",
]
casMeeting.dashboardItemsListingsFilters = (
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
casMeeting.availableItemsListVisibleColumns = [
    "static_labels",
    "Creator",
    "getCategory",
    "getProposingGroup",
    "getGroupsInCharge",
    "advices",
    "preferred_meeting_date",
    "async_actions",
]
casMeeting.dashboardMeetingAvailableItemsFilters = (
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
casMeeting.itemsListVisibleColumns = [
    "static_labels",
    "static_item_reference",
    "CreationDate",
    "ModificationDate",
    "review_state_title",
    "getCategory",
    "getProposingGroup",
    "getGroupsInCharge",
    "advices",
    "async_actions",
]
casMeeting.dashboardMeetingLinkedItemsFilters = (
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


data.meetingConfigs = (bpMeeting, casMeeting)

