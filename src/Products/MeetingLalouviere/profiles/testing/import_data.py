# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data
from Products.MeetingLalouviere.config import LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS, DG_GROUP_ID
from Products.MeetingLalouviere.config import LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS
from Products.PloneMeeting.profiles import UserDescriptor, OrgDescriptor
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data

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
pmDg = UserDescriptor("pmDg", [])
pmCreator2 = UserDescriptor("pmCreator2", [])
pmAdviser1 = UserDescriptor("pmAdviser1", [])
pmAdviser2 = UserDescriptor("pmAdviser2", [])
voter1 = UserDescriptor("voter1", [], fullname="M. Voter One")
voter2 = UserDescriptor("voter2", [], fullname="M. Voter Two")

pmAlderman1 = UserDescriptor(
    "pmAlderman1", [], email="pmalderman1@plonemeeting.org", fullname="M. PMAlderman One"
)

pmAlderman2 = UserDescriptor(
    "pmAlderman2", [], email="pmalderman2@plonemeeting.org", fullname="M. PMAlderman One"
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
developers.serviceheads.append(pmServiceHead1)
developers.serviceheads.append(pmReviewerLevel1)
developers.serviceheads.append(pmManager)
developers.officemanagers.append(pmOfficeManager1)
developers.officemanagers.append(pmManager)
developers.divisionheads.append(pmDivisionHead1)
developers.divisionheads.append(pmManager)
developers.directors.append(pmDirector1)
developers.directors.append(pmReviewerLevel2)
developers.directors.append(pmReviewer1)
developers.directors.append(pmManager)
developers.budgetimpactreviewers.append(pmManager)
developers.budgetimpactreviewers.append(pmBudgetReviewer1)
developers.alderman.append(pmReviewerLevel2)
developers.alderman.append(pmReviewer1)
developers.alderman.append(pmManager)
developers.alderman.append(pmAlderman1)
developers.followupwriters.append(pmFollowup1)
developers.observers.append(pmFollowup1)

vendors = data.orgs[1]
vendors.serviceheads.append(pmServiceHead2)
vendors.officemanagers.append(pmOfficeManager2)
vendors.divisionheads.append(pmDivisionHead2)
vendors.directors.append(pmDirector2)
vendors.directors.append(pmReviewer2)
vendors.directors.append(pmReviewerLevel2)
vendors.budgetimpactreviewers.append(pmBudgetReviewer2)
vendors.alderman.append(pmReviewer2)
vendors.alderman.append(pmAlderman2)
vendors.alderman.append(pmReviewerLevel2)
vendors.followupwriters.append(pmFollowup2)
vendors.observers.append(pmFollowup2)

dg = OrgDescriptor(DG_GROUP_ID, 'Dg', u'Dg')
data.orgs += (dg,)

dg.creators.append(pmDg)
dg.directors.append(pmDg)
dg.directors.append(pmManager)
dg.budgetimpactreviewers.append(pmDg)


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
usedItemAttributes = list(councilMeeting.usedItemAttributes) + [u"committeeTranscript",]
councilMeeting.usedItemAttributes = tuple(usedItemAttributes)
councilMeeting.itemPreferredMeetingStates += ('decided',)

data.meetingConfigs = (collegeMeeting, councilMeeting)
