# -*- coding: utf-8 -*-
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

from Products.PloneMeeting.tests.helpers import PloneMeetingTestingHelpers


class MeetingLalouviereTestingHelpers(PloneMeetingTestingHelpers):
    '''Override some values of PloneMeetingTestingHelpers.'''

    TRANSITIONS_FOR_PROPOSING_ITEM_1 = ('proposeToDirector', )
    TRANSITIONS_FOR_PROPOSING_ITEM_2 = ('proposeToDirector', )
    TRANSITIONS_FOR_VALIDATING_ITEM_1 = ('proposeToDirector', 'validate', )
    TRANSITIONS_FOR_VALIDATING_ITEM_2 = ('proposeToDirector', 'validate', )
    TRANSITIONS_FOR_PRESENTING_ITEM_1 = ('proposeToDirector', 'validate', 'present', )
    TRANSITIONS_FOR_PRESENTING_ITEM_2 = ('proposeToDirector', 'validate', 'present', )
    BACK_TO_WF_PATH = {'proposed': ('backToItemFrozen', 'backToPresented', 'backToValidated', 'backToProposedToDirector', ),
                       'validated': ('backToItemFrozen', 'backToPresented', 'backToValidated', )}
    WF_STATE_NAME_MAPPINGS = {'proposed': 'proposed_to_director',
                              'validated': 'validated'}

    def _doTransitionsFor(self, itemOrMeeting, transitions):
        """Overrided from PloneMeetingTestingHelpers, check XXX here under."""
        currentUser = self.portal.portal_membership.getAuthenticatedMember().getId()
        # do things as admin to avoid permission issues
        self.changeUser('admin')
        # XXX begin changes for MeetingLalouviere
        if itemOrMeeting.portal_type == 'MeetingItemCouncil':
            # a category is mandatory for 'MeetingItemCouncil'
            if not itemOrMeeting.getCategory():
                itemOrMeeting.setCategory(itemOrMeeting.listCategories()[1])
        # XXX end changes
        for tr in transitions:
            if tr in self.transitions(itemOrMeeting):
                self.do(itemOrMeeting, tr)
        self.changeUser(currentUser)
