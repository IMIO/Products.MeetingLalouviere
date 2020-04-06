# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.profiles.examples_fr import import_data as mc_import_data

from Products.PloneMeeting.profiles import (
    AnnexTypeDescriptor,
    ItemAnnexTypeDescriptor,
    ItemAnnexSubTypeDescriptor,
    CategoryDescriptor,
    OrgDescriptor)

data = deepcopy(mc_import_data.data)

# Users and groups -------------------------------------------------------------
# no user
data.orgs.append(OrgDescriptor('secretaire-communal', 'Secrétaire Communal', u'Sec'))
data.orgs.append(OrgDescriptor('secretaire-communal-adj', 'Secrétaire Communal Adjoint', u'Sec-Adj'))

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
collegeMeeting.itemWorkflow = "meetingitemcollegelalouviere_workflow"
collegeMeeting.meetingWorkflow = "meetingcollegelalouviere_workflow"
collegeMeeting.itemConditionsInterface = "Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowConditions"
collegeMeeting.itemActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowActions"
)
collegeMeeting.meetingConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowConditions"
)
collegeMeeting.meetingActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowActions"
)
collegeMeeting.itemDecidedStates = [
    "accepted",
    "delayed",
    "accepted_but_modified",
]
collegeMeeting.itemPositiveDecidedStates = ["accepted", "accepted_but_modified"]

collegeMeeting.transitionsForPresentingAnItem = (
    "proposeToServiceHead",
    "proposeToOfficeManager",
    "proposeToDivisionHead",
    "proposeToDirector",
    # applied by WF adaptation
    "propose_to_dg",
    "propose_to_alderman",
    "validate",
    "present",
)
collegeMeeting.itemAdviceViewStates = [
    "proposed_to_servicehead",
    "proposed_to_officemanager",
    "proposed_to_divisionhead",
    "proposed_to_director",
    "proposed_to_dg",
    "proposed_to_alderman",
    "validated",
    "presented",
    "itemfrozen"
]
collegeMeeting.workflowAdaptations = [
    "refused",
    "removed",
    # "return_to_proposing_group",
    "validate_by_dg_and_alderman",
]
collegeMeeting.itemAdviceStates = [
    "proposed_to_director",
]

collegeMeeting.usedItemAttributes = (
    u"budgetInfos",
    u"observations",
    u"toDiscuss",
    u"motivation",
    u"neededFollowUp",
    u"providedFollowUp",
    u"description",
    u"observations",
    u"itemTags",
    u"itemIsSigned",
)


collegeMeeting.itemAdviceEditStates = ["proposed_to_director", "validated"]

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

collegeMeeting.itemBudgetInfosStates = ("proposed_to_budgetimpact_reviewer",)
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

collegeMeeting.useGroupsAsCategories = True

# COUNCIL
councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.transitionsToConfirm = []
councilMeeting.itemWorkflow = "meetingitemcouncillalouviere_workflow"
councilMeeting.meetingWorkflow = "meetingcouncillalouviere_workflow"
councilMeeting.itemConditionsInterface = "Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowConditions"
councilMeeting.itemActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowActions"
)
councilMeeting.meetingConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowConditions"
)
councilMeeting.meetingActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowActions"
)
councilMeeting.itemDecidedStates = [
    "accepted",
    "delayed",
    "accepted_but_modified",
]
councilMeeting.itemPositiveDecidedStates = ["accepted", "accepted_but_modified"]

councilMeeting.transitionsForPresentingAnItem = (
    "proposeToDirector",
    "validate",
    "present",
)
councilMeeting.workflowAdaptations = []
councilMeeting.itemAdviceStates = [
    "proposed_to_director",
]
councilMeeting.itemAdviceEditStates = ["proposed_to_director", "validated"]
councilMeeting.itemCopyGroupsStates = [
    "proposed_to_director",
    "validated",
    "item_in_committee",
    "item_in_council",
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
    {"meeting_transition": "close", "item_action": "accept", "tal_expression": "",},
)

councilMeeting.usedItemAttributes = (
    u"description",
    u"observations",
    u"toDiscuss",
    u"itemTags",
    u"itemIsSigned",
    u"commissionTranscript",
)

categories = [
    CategoryDescriptor(
        "recurrent",
        "Point récurrent",
        categoryId="recurrent",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-travaux", "Commission Travaux", categoryId="commission-travaux",
    ),
    CategoryDescriptor(
        "commission-enseignement",
        "Commission Enseignement",
        categoryId="commission-enseignement",
    ),
    CategoryDescriptor(
        "commission-culture", "Commission Culture", categoryId="commission-culture"
    ),
    CategoryDescriptor(
        "commission-sport", "Commission Sport", categoryId="commission-sport"
    ),
    CategoryDescriptor(
        "commission-sante", "Commission Santé", categoryId="commission-sante"
    ),
    CategoryDescriptor(
        "commission-cadre-de-vie",
        "Commission Cadre de Vie",
        categoryId="commission-cadre-de-vie",
    ),
    CategoryDescriptor("commission-ag", "Commission AG", categoryId="commission-ag"),
    CategoryDescriptor(
        "commission-finances", "Commission Finances", categoryId="commission-finances"
    ),
    CategoryDescriptor(
        "commission-patrimoine",
        "Commission Patrimoine",
        categoryId="commission-patrimoine",
    ),
    CategoryDescriptor(
        "commission-police", "Commission Police", categoryId="commission-police"
    ),
    CategoryDescriptor(
        "commission-speciale",
        "Commission Spéciale",
        categoryId="commission-speciale",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-travaux-1er-supplement",
        "Commission Travaux (1er supplément)",
        categoryId="commission-travaux-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-enseignement-1er-supplement",
        "Commission Enseignement (1er supplément)",
        categoryId="commission-enseignement-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-culture-1er-supplement",
        "Commission Culture (1er supplément)",
        categoryId="commission-culture-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-sport-1er-supplement",
        "Commission Sport (1er supplément)",
        categoryId="commission-travaux-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-sante-1er-supplement",
        "Commission Santé (1er supplément)",
        categoryId="commission-sante-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-cadre-de-vie-1er-supplement",
        "Commission Cadre de Vie (1er supplément)",
        categoryId="commission-cadre-de-vie-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-ag-1er-supplement",
        "Commission AG (1er supplément)",
        categoryId="commission-ag-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-finances-1er-supplement",
        "Commission Finances (1er supplément)",
        categoryId="commission-finances-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-patrimoine-1er-supplement",
        "Commission Patrimoine (1er supplément)",
        categoryId="commission-patrimoine-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-police-1er-supplement",
        "Commission Police (1er supplément)",
        categoryId="commission-police-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "commission-speciale-1er-supplement",
        "Commission Spéciale (1er supplément)",
        categoryId="commission-speciale-1er-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "points-conseillers-2eme-supplement",
        "Points conseillers (2ème supplément)",
        categoryId="points-conseillers-2eme-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
    CategoryDescriptor(
        "points-conseillers-3eme-supplement",
        "Points conseillers (3ème supplément)",
        categoryId="points-conseillers-3eme-supplement",
        usingGroups=(
            "secretaire-communal",
            "secretaire-communal-adj",
            "secretariat",
            "dirgen",
        ),
    ),
]
councilMeeting.categories = categories

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

data.meetingConfigs = (collegeMeeting, councilMeeting)