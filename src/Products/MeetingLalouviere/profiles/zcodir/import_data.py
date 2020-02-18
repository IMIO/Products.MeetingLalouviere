# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.profiles.zcodir import import_data as mc_import_data

data = deepcopy(mc_import_data.data)
meetingConfig = data.meetingConfigs[0]
meetingConfig.itemWorkflow = "meetingitemcollegelalouviere_workflow"
meetingConfig.meetingWorkflow = "meetingcollegelalouviere_workflow"
meetingConfig.itemConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowConditions"
)
meetingConfig.itemActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowActions"
)
meetingConfig.meetingConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowConditions"
)
meetingConfig.meetingActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowActions"
)
meetingConfig.workflowAdaptations = ['refused']

meetingConfig.itemDecidedStates = [
    "accepted",
    "delayed",
    "accepted_but_modified",
]
meetingConfig.transitionsForPresentingAnItem = (
    "proposeToServiceHead",
    "proposeToOfficeManager",
    "proposeToDivisionHead",
    "proposeToDirector",
    "validate",
    "present",
)

meetingConfig.itemAdviceViewStates = (
    "validated",
    "presented",
    "itemfrozen",
    "accepted",
    "refused",
    "accepted_but_modified",
    "delayed",
)
