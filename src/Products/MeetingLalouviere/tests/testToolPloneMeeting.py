# -*- coding: utf-8 -*-
#
# File: testToolPloneMeeting.py
#
# Copyright (c) 2007-2012 by PloneGov
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

from Products.MeetingCommunes.tests.testToolPloneMeeting import testToolPloneMeeting as mctt
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testToolPloneMeeting(MeetingLalouviereTestCase, mctt):
    """Tests the ToolPloneMeeting class methods."""

    def test_pm_Get_selectable_orgs(self):
        """Returns selectable organizations depending on :
        - MeetingConfig.usingGroups;
        - user is creator for if only_selectable=True."""
        cfg = self.meetingConfig
        cfg2 = self.meetingConfig
        self.changeUser("pmCreator1")
        self.assertEqual(self.tool.get_selectable_orgs(cfg), [self.developers])
        self.assertEqual(self.tool.get_selectable_orgs(cfg2), [self.developers])
        self.assertEqual(
            self.tool.get_selectable_orgs(cfg, only_selectable=False),
            [self.developers, self.vendors, self.direction_generale],
        )
        # do not return more than MeetingConfig.usingGroups
        cfg2.setUsingGroups([self.vendors_uid])
        self.assertEqual(self.tool.get_selectable_orgs(cfg2), [])
        self.assertEqual(self.tool.get_selectable_orgs(cfg2, only_selectable=False), [self.vendors])


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testToolPloneMeeting, prefix="test_"))
    return suite
