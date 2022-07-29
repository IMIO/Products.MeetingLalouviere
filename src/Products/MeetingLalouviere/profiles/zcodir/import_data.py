# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.profiles.zcodir import import_data as mc_import_data
from Products.MeetingLalouviere.config import LLO_ITEM_WF_VALIDATION_LEVELS

data = deepcopy(mc_import_data.data)
meetingConfig = data.meetingConfigs[0]
meetingConfig.itemWFValidationLevels = deepcopy(LLO_ITEM_WF_VALIDATION_LEVELS)
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
