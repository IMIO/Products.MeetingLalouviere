# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.MeetingLalouviere.adapters import customWfAdaptations
from Products.MeetingLalouviere.adapters import LLO_WAITING_ADVICES_FROM_STATES
from Products.MeetingLalouviere.testing import MLL_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingLalouviere.tests.helpers import MeetingLalouviereTestingHelpers
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.model import adaptations


# monkey patch the MeetingConfig.wfAdaptations again
MeetingConfig.wfAdaptations = tuple(customWfAdaptations)
adaptations.WAITING_ADVICES_FROM_STATES.update(LLO_WAITING_ADVICES_FROM_STATES)


class MeetingLalouviereTestCase(
    MeetingCommunesTestCase, MeetingLalouviereTestingHelpers
):
    """Base class for defining MeetingLalouviere test cases."""

    layer = MLL_TESTING_PROFILE_FUNCTIONAL

    def switch_reviewer_groups(self):
        self.developers_prereviewers_old = self.developers_prereviewers
        self.developers_prereviewers = self.developers_directors

        self.developers_reviewers_old = self.developers_reviewers
        self.developers_reviewers = self.developers_alderman

        self.vendors_prereviewers_old = self.vendors_prereviewers
        self.vendors_prereviewers = self.vendors_directors

        self.vendors_reviewers_old = self.vendors_reviewers
        self.vendors_reviewers = self.vendors_alderman

    def switch_back_reviewer_groups(self):
        self.developers_prereviewers = self.developers_prereviewers_old
        self.developers_reviewers = self.developers_reviewers_old
        self.vendors_prereviewers = self.vendors_prereviewers_old
        self.vendors_reviewers = self.vendors_prereviewers_old
