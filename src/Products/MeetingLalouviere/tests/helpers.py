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

    TRANSITIONS_FOR_PROPOSING_ITEM_1 = ('propose_to_director', )
    TRANSITIONS_FOR_PROPOSING_ITEM_2 = ('propose_to_director', )
    TRANSITIONS_FOR_VALIDATING_ITEM_1 = ('propose_to_director', 'validate', )
    TRANSITIONS_FOR_VALIDATING_ITEM_2 = ('propose_to_director', 'validate', )
    TRANSITIONS_FOR_PRESENTING_ITEM_1 = ('propose_to_director', 'validate', 'present', )
    TRANSITIONS_FOR_PRESENTING_ITEM_2 = ('propose_to_director', 'validate', 'present', )
