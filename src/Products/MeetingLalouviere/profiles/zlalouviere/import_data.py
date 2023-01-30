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
    u"budgetInfos",
    u"motivation",
    u"toDiscuss",
    u"observations",
    u"manuallyLinkedItems",
    u"itemTags",
    u"neededFollowUp",
    u"providedFollowUp",
)

collegeMeeting.usedMeetingAttributes = (
    u"start_date",
    u"end_date",
    u"signatures",
    u"assembly",
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
    u"budgetInfos",
    u"motivation",
    u"oralQuestion",
    u"itemInitiator",
    u"observations",
    u"manuallyLinkedItems",
    u"privacy",
    u"itemTags",
    u"interventions",
    u"committeeTranscript",
)

councilMeeting.usedMeetingAttributes = (
    u"start_date",
    u"end_date",
    u"signatures",
    u"assembly",
    u"place",
    u"observations",
)

classifiers = [
    CategoryDescriptor(
        "administration",
        "Administration générale",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-travaux", "Commission Travaux"),
    CategoryDescriptor(
        "commission-enseignement",
        "Commission Enseignement"),
    CategoryDescriptor(
        "commission-culture", "Commission Culture"),
    CategoryDescriptor(
        "commission-sport", "Commission Sport"),
    CategoryDescriptor(
        "commission-sante", "Commission Santé"),
    CategoryDescriptor(
        "commission-cadre-de-vie",
        "Commission Cadre de Vie"),
    CategoryDescriptor("commission-ag", "Commission AG"),
    CategoryDescriptor(
        "commission-finances", "Commission Finances"),
    CategoryDescriptor(
        "commission-patrimoine",
        "Commission Patrimoine"),
    CategoryDescriptor(
        "commission-police", "Commission Police"),
    CategoryDescriptor(
        "commission-speciale",
        "Commission Spéciale",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-travaux-1er-supplement",
        "Commission Travaux (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-enseignement-1er-supplement",
        "Commission Enseignement (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-culture-1er-supplement",
        "Commission Culture (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-sport-1er-supplement",
        "Commission Sport (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-sante-1er-supplement",
        "Commission Santé (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-cadre-de-vie-1er-supplement",
        "Commission Cadre de Vie (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-ag-1er-supplement",
        "Commission AG (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-finances-1er-supplement",
        "Commission Finances (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-patrimoine-1er-supplement",
        "Commission Patrimoine (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-police-1er-supplement",
        "Commission Police (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-speciale-1er-supplement",
        "Commission Spéciale (1er supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "points-conseillers-2eme-supplement",
        "Points conseillers (2ème supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "points-conseillers-3eme-supplement",
        "Points conseillers (3ème supplément)",
        using_groups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
]
councilMeeting.classifiers = classifiers
councilMeeting.categories = PORTAL_CATEGORIES
councilMeeting.useGroupsAsCategories = False

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
councilMeeting.availableItemsListVisibleColumns = [
    "Creator",
    "CreationDate",
    "getProposingGroup",
    "getCategory",
    "actions",
]
councilMeeting.itemsListVisibleColumns = [
    "Creator",
    "CreationDate",
    "review_state",
    "getProposingGroup",
    "getCategory",
    "actions",
]
# columns shown on items listings.  Order is important!
councilMeeting.itemColumns = [
    "Creator",
    "CreationDate",
    "review_state",
    "getProposingGroup",
    "getCategory",
    "actions",
]

data.meetingConfigs = (collegeMeeting, councilMeeting)
