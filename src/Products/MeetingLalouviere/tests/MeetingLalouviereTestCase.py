# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2010 by PloneGov
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
from plone import api

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import (
    MeetingCommunesTestCase,
)
from Products.MeetingLalouviere.adapters import customWfAdaptations
from Products.MeetingLalouviere.testing import MLL_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingLalouviere.tests.helpers import MeetingLalouviereTestingHelpers

# monkey patch the MeetingConfig.wfAdaptations again because it is done in
# adapters.py but overrided by Products.PloneMeeting here in the tests...
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.utils import reviewersFor


from Products.MeetingLalouviere.config import COMMISSION_EDITORS_SUFFIX, COUNCIL_MEETING_COMMISSION_IDS_2020

from collective.contact.plonegroup.utils import get_plone_group_id

MeetingConfig.wfAdaptations = customWfAdaptations


class MeetingLalouviereTestCase(
    MeetingCommunesTestCase, MeetingLalouviereTestingHelpers
):
    """Base class for defining MeetingLalouviere test cases."""

    layer = MLL_TESTING_PROFILE_FUNCTIONAL

    def add_commission_plone_groups(self):
        self.changeUser("admin")
        ag = api.group.create(
            groupname="commission-ag_{}".format(COMMISSION_EDITORS_SUFFIX),
            title='AG Commission Editors',
        )
        self.ag = ag
        api.group.add_user(ag.id, username='commissioneditor')

        pat = api.group.create(
            groupname="commission-patrimoine_{}".format(COMMISSION_EDITORS_SUFFIX),
            title="Commission Patrimoine",
        )
        self.pat = pat
        api.group.add_user(pat.id, username='commissioneditor2')

    def _turnUserIntoPrereviewer(self, member):
        """
          Helper method for adding a given p_member to every '_prereviewers' group
          corresponding to every '_reviewers' group he is in.
        """
        reviewers = reviewersFor(self.meetingConfig.getItemWorkflow())
        groups = [group for group in member.getGroups() if group.endswith('_%s' % reviewers.keys()[1])]
        groups = [group.replace(reviewers.keys()[1], reviewers.keys()[-1]) for group in groups]
        for group in groups:
            self._addPrincipalToGroup(member.getId(), group)

    def _setup_commissions_classifiers(self, commission_version=COUNCIL_MEETING_COMMISSION_IDS_2020):
        # add MEETING_COMMISSION's classifiers
        self.changeUser("admin")

        # wipe all previous classifiers
        ids = self.meetingConfig.classifiers.keys()
        if len(ids) > 0:
            ids = list(ids)
            self.meetingConfig.classifiers.manage_delObjects(ids)

        # flatten commission_version
        commission_classifiers = []
        for i in commission_version:
            if isinstance(i, tuple):
                for j in i:
                    commission_classifiers.append(j)
            else:
                commission_classifiers.append(i)

        # create 1st-supplement for each classifier
        commission_classifiers = commission_classifiers + [
            classifier + "-1er-supplement" for classifier in commission_classifiers
        ]
        commission_classifiers += ["points-conseillers-2eme-supplement", "points-conseillers-3eme-supplement"]

        # add classifiers to the meetingConfig
        for classifier in commission_classifiers:
            self.create("meetingcategory", id=classifier, title="commissionClf", is_classifier=True)

