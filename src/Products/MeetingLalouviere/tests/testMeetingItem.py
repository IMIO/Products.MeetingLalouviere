# -*- coding: utf-8 -*-
#
# File: testMeetingItem.py
#
# Copyright (c) 2007-2012 by CommunesPlone.org
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

from Products.MeetingCommunes.tests.testMeetingItem import testMeetingItem as mctmi
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)


class testMeetingItem(MeetingLalouviereTestCase, mctmi):
    """
        Tests the MeetingItem class methods.
    """

    def _extraNeutralFields(self):
        """This method is made to be overrided by subplugins that added
           neutral fields to the MeetingItem schema."""
        return ["followUp", "neededFollowUp", "providedFollowUp"]

    def test_pm_SendItemToOtherMCUsingEmergencyInitializePreferredMeeting(self):
        # by pass because council meeting are never late
        pass

    def test_pm_SendItemToOtherMCUsingEmergency(self):
        # by pass because council meeting are never late
        pass

    def test_pm_OnTransitionFieldTransforms(self):
        # by pass because nobody can refuse or delay an item
        pass

    def test_pm_OnTransitionFieldTransformsUseLastCommentFromHistory(self):
        # by pass because nobody can refuse or delay an item
        pass




def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from mctmi
    suite.addTest(makeSuite(testMeetingItem, prefix="test_"))
    return suite
