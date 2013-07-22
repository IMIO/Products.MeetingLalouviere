# -*- coding: utf-8 -*-
#
# File: testWFAdaptations.py
#
# Copyright (c) 2013 by Imio.be
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
from Products.MeetingCommunes.tests.testWFAdaptations import testWFAdaptations as mctwfa


class testWFAdaptations(MeetingLalouviereTestCase, mctwfa):
    '''Tests various aspects of votes management.'''

    def test_subproduct_call_WFA_availableWFAdaptations(self):
        '''Most of wfAdaptations makes no sense, just make sure most are disabled.'''
        self.assertEquals(set(self.meetingConfig.listWorkflowAdaptations()),
                          set(('archiving', 'local_meeting_managers', )))

    def test_subproduct_call_WFA_no_publication(self):
        '''No sense...'''
        pass

    def test_subproduct_call_WFA_no_proposal(self):
        '''No sense...'''
        pass

    def test_subproduct_call_WFA_pre_validation(self):
        '''No sense...'''
        pass

    def test_subproduct_call_WFA_items_come_validated(self):
        '''No sense...'''
        pass

    def test_subproduct_call_WFA_only_creator_may_delete(self):
        '''No sense...'''
        pass

    def test_subproduct_call_WFA_no_global_observation(self):
        '''No sense...'''
        pass

    def test_subproduct_call_WFA_everyone_reads_all(self):
        '''No sense...'''
        pass

    def test_subproduct_call_WFA_creator_edits_unless_closed(self):
        '''No sense...'''
        pass

    def test_subproduct_WFA_add_published_state(self):
        '''No sense...'''
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix='test_subproduct_'))
    return suite
