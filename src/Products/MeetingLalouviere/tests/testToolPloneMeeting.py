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

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.PloneMeeting.tests.testToolPloneMeeting import testToolPloneMeeting as pmtt


class testToolPloneMeeting(MeetingLalouviereTestCase, pmtt):
    '''Tests the ToolPloneMeeting class methods.'''

    def test_pm_UserIsAmong(self):
        """This method will check if a user has a group that ends with a list of given suffixes.
           This will return True if at least one suffixed group corresponds."""
        self.changeUser('pmCreator1')
        self.assertEqual(self.member.getGroups(),
                         ['AuthenticatedUsers', 'developers_creators'])
        # suffixes parameter must be a list of suffixes
        self.assertFalse(self.tool.userIsAmong('creators'))
        self.assertTrue(self.tool.userIsAmong(['creators']))
        self.assertTrue(self.tool.userIsAmong(['creators', 'reviewers']))
        self.assertTrue(self.tool.userIsAmong(['creators', 'powerobservers']))
        self.assertTrue(self.tool.userIsAmong(['creators', 'unknown_suffix']))
        self.changeUser('pmReviewer1')
        self.assertEqual(self.member.getGroups(),
                         ['developers_reviewers', 'developers_observers', 'developers_directors',
                          'AuthenticatedUsers', 'developers_serviceheads'])
        self.assertFalse(self.tool.userIsAmong(['creators']))
        self.assertTrue(self.tool.userIsAmong(['reviewers']))
        self.assertTrue(self.tool.userIsAmong(['observers']))
        self.assertTrue(self.tool.userIsAmong(['reviewers', 'observers']))
        self.changeUser('powerobserver1')
        self.assertEqual(self.member.getGroups(),
                         ['AuthenticatedUsers', '{0}_powerobservers'.format(self.meetingConfig.getId())])
        self.assertFalse(self.tool.userIsAmong(['creators']))
        self.assertFalse(self.tool.userIsAmong(['reviewers']))
        self.assertFalse(self.tool.userIsAmong(['creators', 'reviewers']))
        self.assertTrue(self.tool.userIsAmong(['powerobservers']))
        self.assertTrue(self.tool.userIsAmong(['creators', 'powerobservers']))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testToolPloneMeeting, prefix='test_pm_'))
    return suite
