# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data

from Products.PloneMeeting.profiles import UserDescriptor, PloneGroupDescriptor

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
developers.commissioneditors.append(commissioneditor2)

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

# COLLEGE
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)
collegeMeeting.itemWorkflow = "meetingitemcollegelalouviere_workflow"
collegeMeeting.meetingWorkflow = "meetingcollegelalouviere_workflow"
collegeMeeting.itemConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowConditions"
)
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
collegeMeeting.itemAdviceEditStates = ["proposed_to_director", "validated"]

# COUNCIL
councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.itemWorkflow = "meetingitemcouncillalouviere_workflow"
councilMeeting.meetingWorkflow = "meetingcouncillalouviere_workflow"
councilMeeting.itemConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowConditions"
)
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
    {'meeting_transition': 'setInCommittee',
     'item_action': 'setItemInCommittee',
     'tal_expression': ''},
    {'meeting_transition': 'setInCouncil',
     'item_action': 'setItemInCouncil',
     'tal_expression': ''},
    {'meeting_transition': 'backToCreated',
     'item_action': 'backToPresented',
     'tal_expression': ''},
    {'meeting_transition': 'backToInCommittee',
     'item_action': 'backToItemInCouncil',
     'tal_expression': ''},
    {'meeting_transition': 'backToInCommittee',
     'item_action': 'backToItemInCommittee',
     'tal_expression': ''},
)

data.meetingConfigs = (collegeMeeting, councilMeeting)
