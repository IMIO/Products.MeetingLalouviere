# -*- coding: utf-8 -*-
#
# File: testViews.py
#
# Copyright (c) 2007-2015 by Imio.be
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

from Products.MeetingCommunes.tests.testViews import testViews as mctv
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)

from plone import api


class testViews(MeetingLalouviereTestCase, mctv):
    """ """
    def _display_user_groups_sub_groups_false(self):
        return [(1, api.user.get('pmCreator1')),
                (1, api.user.get('pmCreator1b')),
                (1, api.user.get('pmManager')),
                (0, api.user.get('pmFollowup1')),
                (0, api.user.get('pmObserver1')),
                (0, api.user.get('pmReviewer1'))]

    def _display_user_groups_sub_groups_true(self):
        return [(1, api.group.get(self.developers_creators)),
                (2, api.user.get('pmCreator1')),
                (2, api.user.get('pmCreator1b')),
                (2, api.user.get('pmManager')),
                (0, api.user.get('pmFollowup1')),
                (0, api.user.get('pmManager')),
                (0, api.user.get('pmObserver1')),
                (0, api.user.get('pmReviewer1'))]

def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testViews, prefix="test_"))
    return suite
