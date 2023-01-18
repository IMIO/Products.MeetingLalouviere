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
from Products.MeetingLalouviere.testing import MLL_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingLalouviere.tests.helpers import MeetingLalouviereTestingHelpers


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
