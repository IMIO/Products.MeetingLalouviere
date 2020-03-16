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


from Products.MeetingLalouviere.config import COMMISSION_EDITORS_SUFFIX

from collective.contact.plonegroup.utils import get_plone_group_id

MeetingConfig.wfAdaptations = customWfAdaptations


class MeetingLalouviereTestCase(
    MeetingCommunesTestCase, MeetingLalouviereTestingHelpers
):
    """Base class for defining MeetingLalouviere test cases."""

    layer = MLL_TESTING_PROFILE_FUNCTIONAL

    def add_commission_orgs(self):
        self.changeUser("admin")
        ag = self.create(
            "organization", id="commission-ag", title="Commission AG", acronym=u"AG"
        )
        self._select_organization(ag.UID())
        self.ag = ag
        self._addPrincipalToGroup('pmCreator1', get_plone_group_id(ag.UID(), 'creators'))
        self._addPrincipalToGroup('pmManager', get_plone_group_id(ag.UID(), 'creators'))

        self._addPrincipalToGroup('pmDirector1', get_plone_group_id(ag.UID(), 'directors'))
        self._addPrincipalToGroup('commissioneditor', get_plone_group_id(ag.UID(), COMMISSION_EDITORS_SUFFIX))

        pat = self.create(
            "organization",
            id="commission-patrimoine",
            title="Commission Patrimoine",
            acronym=u"PAT",
        )
        self._select_organization(pat.UID())
        self.pat = pat

        self._addPrincipalToGroup('pmCreator2', get_plone_group_id(pat.UID(), 'creators'))
        self._addPrincipalToGroup('pmManager', get_plone_group_id(pat.UID(), 'creators'))

        self._addPrincipalToGroup('pmDirector2', get_plone_group_id(pat.UID(), 'directors'))
        self._addPrincipalToGroup('commissioneditor2', get_plone_group_id(pat.UID(), 'commissioneditors'))

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