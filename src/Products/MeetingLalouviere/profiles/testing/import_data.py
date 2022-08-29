# -*- coding: utf-8 -*-
import copy
from copy import deepcopy

from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data

from Products.MeetingLalouviere.config import LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS
from Products.MeetingLalouviere.config import LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data

from Products.PloneMeeting.profiles import UserDescriptor

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
data.usersOutsideGroups.append(commissioneditor)
data.usersOutsideGroups.append(commissioneditor2)

pmAlderman = UserDescriptor(
    "pmAlderman", [], email="pmalderman@plonemeeting.org", fullname="M. PMAlderman One"
)

pmFollowup1 = UserDescriptor("pmFollowup1", [])
pmFollowup2 = UserDescriptor("pmFollowup2", [])
pmBudgetReviewer1 = UserDescriptor("pmBudgetReviewer1", [])
pmBudgetReviewer2 = UserDescriptor("pmBudgetReviewer2", [])

# Inherited users
pmReviewer1 = pm_import_data.pmReviewer1
pmReviewer2 = pm_import_data.pmReviewer2
pmReviewerLevel1 = pm_import_data.pmReviewerLevel1
pmReviewerLevel2 = pm_import_data.pmReviewerLevel2
pmManager = pm_import_data.pmManager

# GROUPS
developers = data.orgs[0]
# custom groups
developers.serviceheads.append(pmReviewer1)
developers.serviceheads.append(pmServiceHead1)
developers.serviceheads.append(pmReviewerLevel1)
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
developers.budgetimpactreviewers.append(pmManager)
developers.budgetimpactreviewers.append(pmBudgetReviewer1)
developers.alderman.append(pmReviewer1)
developers.alderman.append(pmManager)
developers.alderman.append(pmAlderman)
developers.followupwriters.append(pmFollowup1)
developers.observers.append(pmFollowup1)

vendors = data.orgs[1]
vendors.serviceheads.append(pmReviewer2)
vendors.serviceheads.append(pmServiceHead2)
vendors.officemanagers.append(pmOfficeManager2)
vendors.officemanagers.append(pmReviewer2)
vendors.divisionheads.append(pmDivisionHead2)
vendors.divisionheads.append(pmReviewer2)
vendors.directors.append(pmDirector2)
vendors.directors.append(pmReviewer2)
vendors.directors.append(pmReviewerLevel2)
vendors.directors.append(pmManager)
vendors.budgetimpactreviewers.append(pmManager)
vendors.budgetimpactreviewers.append(pmBudgetReviewer2)
vendors.alderman.append(pmReviewer2)
vendors.alderman.append(pmManager)
vendors.alderman.append(pmAlderman)
vendors.followupwriters.append(pmFollowup1)
vendors.followupwriters.append(pmFollowup2)
vendors.observers.append(pmFollowup1)
vendors.observers.append(pmFollowup2)

# COLLEGE
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)

collegeMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS)
collegeMeeting.itemAdviceStates = [
    "proposed_to_alderman",
]
collegeMeeting.itemAdviceEditStates = [
    "proposed_to_alderman",
    "validated"
]
usedItemAttributes = list(collegeMeeting.usedItemAttributes) + [u"neededFollowUp", u"providedFollowUp",]
collegeMeeting.usedItemAttributes = tuple(usedItemAttributes)
# collegeMeeting.workflowAdaptations = deepcopy(LLO_APPLYED_COLLEGE_WFA)

# COUNCIL
councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS)
councilMeeting.itemAdviceStates = [
    "proposed_to_director",
]
councilMeeting.itemAdviceEditStates = [
    "proposed_to_director",
    "validated"
]
# councilMeeting.workflowAdaptations = deepcopy(LLO_APPLYED_COUNCIL_WFA)
usedItemAttributes = list(councilMeeting.usedItemAttributes) + [u"commissionTranscript",]
councilMeeting.usedItemAttributes = tuple(usedItemAttributes)

data.meetingConfigs = (collegeMeeting, councilMeeting)
