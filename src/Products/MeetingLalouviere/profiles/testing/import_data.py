# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data

from Products.PloneMeeting.profiles import UserDescriptor, OrgDescriptor

data = deepcopy(mc_import_data.data)

# USERS
pmServiceHead1 = UserDescriptor("pmServiceHead1", [])
pmServiceHead2 = UserDescriptor("pmServiceHead2", [])
pmOfficeManager1 = UserDescriptor("pmOfficeManager1", [])
pmOfficeManager2 = UserDescriptor("pmOfficeManager2", [])
pmDivisionHead1 = UserDescriptor("pmDivisionHead1", [])
pmDivisionHead2 = UserDescriptor("pmDivisionHead2", [])
pmDirector1 = UserDescriptor("pmDirector1", [])
pmDirector2 = UserDescriptor("pmDirector2", [])
pmCreator2 = UserDescriptor("pmCreator2", [])
pmAdviser1 = UserDescriptor("pmAdviser1", [])
pmAdviser2 = UserDescriptor("pmAdviser2", [])
voter1 = UserDescriptor("voter1", [], fullname="M. Voter One")
voter2 = UserDescriptor("voter2", [], fullname="M. Voter Two")

# Commission editors
commissioneditor = UserDescriptor(
    "commissioneditor",
    [],
    email="commissioneditor@plonemeeting.org",
    fullname="M. Commission Editor",
)
commissioneditor2 = UserDescriptor(
    "commissioneditor2",
    [],
    email="commissioneditor2@plonemeeting.org",
    fullname="M. Commission Editor 2",
)

pmAlderman = UserDescriptor(
    "pmAlderman", [], email="pmalderman@plonemeeting.org", fullname="M. PMAlderman One"
)

# Inherited users
pmCreator1 = deepcopy(pm_import_data.pmCreator1)
pmReviewer1 = deepcopy(pm_import_data.pmReviewer1)
pmReviewer2 = deepcopy(pm_import_data.pmReviewer2)
pmReviewerLevel1 = deepcopy(pm_import_data.pmReviewerLevel1)
pmReviewerLevel2 = deepcopy(pm_import_data.pmReviewerLevel2)
pmManager = deepcopy(pm_import_data.pmManager)

# GROUPS
developers = data.orgs[0]
# custom groups
developers.serviceheads.append(pmReviewer1)
developers.serviceheads.append(pmServiceHead1)
developers.serviceheads.append(pmManager)
developers.officemanagers.append(pmOfficeManager1)
developers.officemanagers.append(pmReviewer1)
developers.officemanagers.append(pmManager)
developers.divisionheads.append(pmDivisionHead1)
developers.divisionheads.append(pmReviewer1)
developers.divisionheads.append(pmManager)
developers.directors.append(pmDirector1)
developers.directors.append(pmReviewer1)
developers.directors.append(pmReviewerLevel2)
developers.directors.append(pmManager)
developers.followupwriters.append(pmManager)
developers.budgetimpactreviewers.append(pmManager)
developers.alderman.append(pmManager)
developers.alderman.append(pmAlderman)
developers.commissioneditors.append(commissioneditor)

vendors = data.orgs[1]
vendors.serviceheads.append(pmReviewer2)
vendors.serviceheads.append(pmServiceHead2)
vendors.serviceheads.append(pmManager)
vendors.officemanagers.append(pmOfficeManager2)
vendors.officemanagers.append(pmReviewer2)
vendors.officemanagers.append(pmManager)
vendors.divisionheads.append(pmDivisionHead2)
vendors.divisionheads.append(pmReviewer2)
vendors.divisionheads.append(pmManager)
vendors.directors.append(pmDirector2)
vendors.directors.append(pmReviewer2)
vendors.directors.append(pmReviewerLevel2)
vendors.directors.append(pmManager)
vendors.followupwriters.append(pmManager)
vendors.budgetimpactreviewers.append(pmManager)
vendors.alderman.append(pmManager)
vendors.alderman.append(pmAlderman)
vendors.commissioneditors.append(commissioneditor2)

ag = OrgDescriptor('commission-ag', 'Commission AG', u'AG')
ag.creators.append(pmCreator1)
ag.creators.append(pmManager)
ag.prereviewers.append(pmReviewerLevel1)
ag.reviewers.append(pmReviewer1)
ag.reviewers.append(pmReviewerLevel2)
ag.reviewers.append(pmManager)
ag.observers.append(pmReviewer1)
ag.observers.append(pmManager)
ag.advisers.append(pmAdviser1)
ag.advisers.append(pmManager)
ag.commissioneditors.append(commissioneditor)
ag.serviceheads.append(pmReviewer1)
ag.serviceheads.append(pmServiceHead1)
ag.serviceheads.append(pmManager)
ag.officemanagers.append(pmOfficeManager1)
ag.officemanagers.append(pmReviewer1)
ag.officemanagers.append(pmManager)
ag.divisionheads.append(pmDivisionHead1)
ag.divisionheads.append(pmReviewer1)
ag.divisionheads.append(pmManager)
ag.directors.append(pmDirector1)
ag.directors.append(pmReviewer1)
ag.directors.append(pmReviewerLevel2)
ag.directors.append(pmManager)
ag.followupwriters.append(pmManager)
ag.budgetimpactreviewers.append(pmManager)
ag.alderman.append(pmManager)
ag.alderman.append(pmAlderman)
ag.commissioneditors.append(commissioneditor)

patrimoine = OrgDescriptor('commission-patrimoine', 'Commission Patrimoine', u'PAT')
patrimoine.creators.append(pmCreator2)
patrimoine.creators.append(pmManager)
patrimoine.prereviewers.append(pmReviewerLevel2)
patrimoine.reviewers.append(pmReviewer2)
patrimoine.reviewers.append(pmReviewerLevel2)
patrimoine.reviewers.append(pmManager)
patrimoine.observers.append(pmReviewer2)
patrimoine.observers.append(pmManager)
patrimoine.advisers.append(pmAdviser2)
patrimoine.advisers.append(pmManager)
patrimoine.commissioneditors.append(commissioneditor)
patrimoine.serviceheads.append(pmReviewer2)
patrimoine.serviceheads.append(pmServiceHead2)
patrimoine.serviceheads.append(pmManager)
patrimoine.officemanagers.append(pmOfficeManager2)
patrimoine.officemanagers.append(pmReviewer2)
patrimoine.officemanagers.append(pmManager)
patrimoine.divisionheads.append(pmDivisionHead2)
patrimoine.divisionheads.append(pmReviewer2)
patrimoine.divisionheads.append(pmManager)
patrimoine.directors.append(pmDirector2)
patrimoine.directors.append(pmReviewer2)
patrimoine.directors.append(pmReviewerLevel2)
patrimoine.directors.append(pmManager)
patrimoine.followupwriters.append(pmManager)
patrimoine.budgetimpactreviewers.append(pmManager)
patrimoine.alderman.append(pmManager)
patrimoine.alderman.append(pmAlderman)
patrimoine.commissioneditors.append(commissioneditor2)

endUsers = data.orgs[2]
data.orgs = (developers, vendors, endUsers, ag, patrimoine)

# COLLEGE
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)
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
    "validate",
    "present",
)
collegeMeeting.workflowAdaptations = []
collegeMeeting.itemAdviceStates = [
    "proposed_to_director",
]

collegeMeeting.usedItemAttributes = (
    u"description",
    u"observations",
    u"toDiscuss",
    u"itemTags",
    u"itemIsSigned",
)


collegeMeeting.itemAdviceEditStates = ["proposed_to_director", "validated"]

# COUNCIL
councilMeeting = deepcopy(mc_import_data.councilMeeting)
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
    {
        "meeting_transition": "close",
        "item_action": "accept",
        "tal_expression": "",
    },
)

councilMeeting.usedItemAttributes = (
    u"description",
    u"observations",
    u"toDiscuss",
    u"itemTags",
    u"itemIsSigned",
    u"commissionTranscript",
)

data.meetingConfigs = (collegeMeeting, councilMeeting)
