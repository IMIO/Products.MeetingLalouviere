# -*- coding: utf-8 -*-
from copy import deepcopy
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data
from Products.MeetingLalouviere.config import DG_GROUP_ID
from Products.MeetingLalouviere.config import INTREF_GROUP_ID
from Products.MeetingLalouviere.config import LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS
from Products.MeetingLalouviere.config import LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS
from Products.PloneMeeting.profiles import OrgDescriptor
from Products.PloneMeeting.profiles import UserDescriptor
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data


data = deepcopy(mc_import_data.data)

# USERS
pmServiceHead1 = UserDescriptor("pmServiceHead1", [], email="pmservicehead1@plonemeeting.org")
pmServiceHead2 = UserDescriptor("pmServiceHead2", [], email="pmservicehead2@plonemeeting.org")
pmOfficeManager1 = UserDescriptor("pmOfficeManager1", [], email="pmofficemanager1@plonemeeting.org")
pmOfficeManager2 = UserDescriptor("pmOfficeManager2", [], email="pmofficemanager2@plonemeeting.org")
pmDivisionHead1 = UserDescriptor("pmDivisionHead1", [], email="pmdivisionhead1@plonemeeting.org")
pmDivisionHead2 = UserDescriptor("pmDivisionHead2", [], email="pmdivisionhead2@plonemeeting.org")
pmDirector1 = UserDescriptor("pmDirector1", [], email="pmdirector1@plonemeeting.org")
pmDirector2 = UserDescriptor("pmDirector2", [], email="pmdirector2@plonemeeting.org")
pmDg = UserDescriptor("pmDg", [], email="pmdg@plonemeeting.org")
pmCreator2 = UserDescriptor("pmCreator2", [], email="pmcreator2@plonemeeting.org")
pmAdviser1 = UserDescriptor("pmAdviser1", [], email="pmadviser1@plonemeeting.org")
pmAdviser2 = UserDescriptor("pmAdviser2", [], email="pmadviser2@plonemeeting.org")
voter1 = UserDescriptor("voter1", [], email="voter1@plonemeeting.org", fullname="M. Voter One")
voter2 = UserDescriptor("voter2", [], email="voter2@plonemeeting.org", fullname="M. Voter Two")
pmAlderman1 = UserDescriptor("pmAlderman1", [], email="pmalderman1@plonemeeting.org", fullname="M. PMAlderman One")
pmAlderman2 = UserDescriptor("pmAlderman2", [], email="pmalderman2@plonemeeting.org", fullname="M. PMAlderman One")
pmFollowup1 = UserDescriptor("pmFollowup1", [], email="pmfollowup1@plonemeeting.org")
pmFollowup2 = UserDescriptor("pmFollowup2", [], email="pmfollowup2@plonemeeting.org")
pmBudgetReviewer1 = UserDescriptor("pmBudgetReviewer1", [], email="pmbudgetreviewer1@plonemeeting.org")
pmBudgetReviewer2 = UserDescriptor("pmBudgetReviewer2", [], email="pmbudgetreviewer2@plonemeeting.org")

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
dg = OrgDescriptor(DG_GROUP_ID, "Dg", u"Dg")
intref = OrgDescriptor(INTREF_GROUP_ID, "Référent intégrité", u"RI")

data.orgs += (dg, intref, )

dg.creators.append(pmDg)
dg.directors.append(pmDg)
dg.directors.append(pmManager)
dg.budgetimpactreviewers.append(pmDg)
intref.creators.append(pmCreator2)
intref.directors.append(pmDirector2)

# COLLEGE
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)

collegeMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS)
collegeMeeting.itemAdviceStates = [
    "proposed_to_alderman",
]
collegeMeeting.itemAdviceEditStates = ["proposed_to_alderman", "validated"]
usedItemAttributes = list(collegeMeeting.usedItemAttributes) + [
    u"providedFollowUp",
]
collegeMeeting.usedItemAttributes = tuple(usedItemAttributes)

# COUNCIL
councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS)
councilMeeting.itemAdviceStates = [
    "proposed_to_director",
]
councilMeeting.itemAdviceEditStates = ["proposed_to_director", "validated"]
# councilMeeting.workflowAdaptations = deepcopy(LLO_APPLYED_COUNCIL_WFA)
usedItemAttributes = list(councilMeeting.usedItemAttributes) + [
    u"committeeTranscript",
]
councilMeeting.usedItemAttributes = tuple(usedItemAttributes)
councilMeeting.itemPreferredMeetingStates += ("decided",)

data.meetingConfigs = (collegeMeeting, councilMeeting)
