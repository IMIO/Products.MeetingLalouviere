# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2011 by CommunesPlone.org
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

__author__ = """Gauthier Bastien <gbastien@commune.sambreville.be>"""
__docformat__ = 'plaintext'

# ------------------------------------------------------------------------------
from Products.MeetingCommunes.interfaces import \
    IMeetingItemCommunesWorkflowConditions, IMeetingItemCommunesWorkflowActions, \
    IMeetingCommunesWorkflowActions, IMeetingCommunesWorkflowConditions


# ------------------------------------------------------------------------------
class IMeetingItemCollegeLalouviereWorkflowActions(IMeetingItemCommunesWorkflowActions):
    '''This interface represents a meeting item as viewed by the specific
       item workflow that is defined in this MeetingLalouviere product.'''
    def doPresent():
        """
          Triggered while doing the 'present' transition
        """
    def doAcceptButModify():
        """
          Triggered while doing the 'accept_but_modify' transition
        """
    def doPreAccept():
        """
          Triggered while doing the 'pre_accept' transition
        """


class IMeetingItemCollegeLalouviereWorkflowConditions(IMeetingItemCommunesWorkflowConditions):
    '''This interface represents a meeting item as viewed by the specific
       item workflow that is defined in this MeetingLalouviere product.'''
    def mayDecide():
        """
          Guard for the 'decide' transition
        """
    def isLateFor():
        """
          is the MeetingItem considered as late
        """
    def mayFreeze():
        """
          Guard for the 'freeze' transition
        """


class IMeetingCollegeLalouviereWorkflowActions(IMeetingCommunesWorkflowActions):
    '''This interface represents a meeting as viewed by the specific meeting
       workflow that is defined in this MeetingLalouviere product.'''
    def doClose():
        """
          Triggered while doing the 'close' transition
        """
    def doDecide():
        """
          Triggered while doing the 'decide' transition
        """
    def doFreeze():
        """
          Triggered while doing the 'freeze' transition
        """
    def doBackToCreated():
        """
          Triggered while doing the 'doBackToCreated' transition
        """


class IMeetingCollegeLalouviereWorkflowConditions(IMeetingCommunesWorkflowConditions):
    '''This interface represents a meeting as viewed by the specific meeting
       workflow that is defined in this MeetingLalouviere product.'''
    def mayFreeze():
        """
          Guard for the 'freeze' transition
        """
    def mayClose():
        """
          Guard for the 'close' transitions
        """
    def mayDecide():
        """
          Guard for the 'decide' transition
        """
    def mayChangeItemsOrder():
        """
          Check if the user may or not changes the order of the items on the meeting
        """


class IMeetingCouncilLalouviereWorkflowActions(IMeetingCommunesWorkflowActions):
    '''This interface represents a meeting as viewed by the specific meeting
       workflow that is defined in this MeetingLalouviere product.'''
    def doClose():
        """
          Triggered while doing the 'close' transition
        """
    def doDecide():
        """
          Triggered while doing the 'decide' transition
        """
    def doFreeze():
        """
          Triggered while doing the 'freeze' transition
        """
    def doBackToCreated():
        """
          Triggered while doing the 'doBackToCreated' transition
        """


class IMeetingCouncilLalouviereWorkflowConditions(IMeetingCommunesWorkflowConditions):
    '''This interface represents a meeting as viewed by the specific meeting
       workflow that is defined in this MeetingLalouviere product.'''
    def mayFreeze():
        """
          Guard for the 'freeze' transition
        """
    def mayClose():
        """
          Guard for the 'close' transitions
        """
    def mayDecide():
        """
          Guard for the 'decide' transition
        """
    def mayChangeItemsOrder():
        """
          Check if the user may or not changes the order of the items on the meeting
        """


class IMeetingItemCouncilLalouviereWorkflowActions(IMeetingItemCommunesWorkflowActions):
    '''This interface represents a meeting item as viewed by the specific
       item workflow that is defined in this MeetingLalouviere product.'''
    def doPresent():
        """
          Triggered while doing the 'present' transition
        """


class IMeetingItemCouncilLalouviereWorkflowConditions(IMeetingItemCommunesWorkflowConditions):
    '''This interface represents a meeting item as viewed by the specific
       item workflow that is defined in this MeetingLalouviere product.'''
    def mayDecide():
        """
          Guard for the 'decide' transition
        """
    def isLateFor():
        """
          is the MeetingItem considered as late
        """
    def mayFreeze():
        """
          Guard for the 'freeze' transition
        """
    def mayRemove():
        """
          Guard for the 'remove' transition (removing an item from the meeting)
        """

# ------------------------------------------------------------------------------
