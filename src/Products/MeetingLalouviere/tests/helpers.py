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

from Products.MeetingCommunes.tests.helpers import MeetingCommunesTestingHelpers


class MeetingLalouviereTestingHelpers(MeetingCommunesTestingHelpers):
    """Override some values of PloneMeetingTestingHelpers."""

    TRANSITIONS_FOR_PROPOSING_ITEM_1 = (
        "proposeToServiceHead",
        "proposeToOfficeManager",
        "proposeToDivisionHead",
        "proposeToDirector",
    )
    TRANSITIONS_FOR_PROPOSING_ITEM_2 = ("proposeToDirector",)
    TRANSITIONS_FOR_VALIDATING_ITEM_1 = (
        "proposeToServiceHead",
        "proposeToOfficeManager",
        "proposeToDivisionHead",
        "proposeToDirector",
        "validate",
    )
    TRANSITIONS_FOR_VALIDATING_ITEM_2 = (
        "proposeToDirector",
        "validate",
    )
    TRANSITIONS_FOR_PRESENTING_ITEM_1 = (
        "proposeToServiceHead",
        "proposeToOfficeManager",
        "proposeToDivisionHead",
        "proposeToDirector",
        "validate",
        "present",
    )
    TRANSITIONS_FOR_PRESENTING_ITEM_2 = (
        "proposeToDirector",
        "validate",
        "present",
    )
    TRANSITIONS_FOR_ACCEPTING_ITEMS_1 = (
        "freeze",
        "decide",
    )
    TRANSITIONS_FOR_ACCEPTING_ITEMS_2 = (
        "setItemInCommittee",
        "setItemInCouncil",
    )

    TRANSITIONS_FOR_DECIDING_MEETING_1 = (
        "freeze",
        "decide",
    )
    TRANSITIONS_FOR_DECIDING_MEETING_2 = (
        "setInCommittee",
        "setInCouncil",
    )
    TRANSITIONS_FOR_CLOSING_MEETING_1 = (
        "freeze",
        "decide",
        "close",
    )
    TRANSITIONS_FOR_CLOSING_MEETING_2 = (
        "setInCommittee",
        "setInCouncil",
        "close",
    )
    BACK_TO_WF_PATH_1 = {
        # Meeting
        "created": ("backToDecided", "backToPublished", "backToFrozen", "backToCreated",),
        # MeetingItem
        "itemcreated": (
            "backToItemFrozen",
            "backToPresented",
            "backToValidated",
            "backToProposedToDirector",
            "backToProposedToDivisionHead",
            "backToProposedToOfficeManager",
            "backToProposedToServiceHead",
            "backToItemCreated",
        ),
        "proposed_to_director": (
            "backToItemFrozen",
            "backToPresented",
            "backToValidated",
            "backToProposedToDirector",
        ),
        "validated": ("backToItemFrozen", "backToPresented", "backToValidated",),
    }
    BACK_TO_WF_PATH_2 = {
        "itemcreated": (
            "backToItemFrozen",
            "backToPresented",
            "backToValidated",
            "backToProposedToDirector",
            "backToItemCreated",
        ),
        "proposed_to_director": (
            "backToItemFrozen",
            "backToPresented",
            "backToValidated",
            "backToProposedToDirector",
        ),
        "validated": ("backToItemFrozen", "backToPresented", "backToValidated",),
    }

    WF_ITEM_STATE_NAME_MAPPINGS_1 = {
        "itemcreated": "itemcreated",
        "proposed": "proposed_to_director",
        "validated": "validated",
        "presented": "presented",
        "itemfrozen": "itemfrozen",
    }

    WF_ITEM_STATE_NAME_MAPPINGS_2 = {
        "itemcreated": "itemcreated",
        "proposed": "proposed_to_director",
        "validated": "validated",
        "presented": "presented",
        "itemfrozen": "item_in_committee",
    }

    WF_MEETING_TRANSITION_NAME_MAPPINGS_2 = {"frozen": "in_committee"}

    # in which state an item must be after an particular meeting transition?
    ITEM_WF_STATE_AFTER_MEETING_TRANSITION = {
        "publish_decisions": "accepted",
        "close": "accepted",
    }

    TRANSITIONS_FOR_FREEZING_MEETING_1 = TRANSITIONS_FOR_PUBLISHING_MEETING_1 = (
        "freeze",
    )
    TRANSITIONS_FOR_FREEZING_MEETING_2 = TRANSITIONS_FOR_PUBLISHING_MEETING_2 = (
        "setInCommittee",
        "setInCouncil",
    )

    TRANSITIONS_FOR_ACCEPTING_ITEMS_MEETING_1 = (
        "freeze",
        "decide",
    )
    TRANSITIONS_FOR_ACCEPTING_ITEMS_MEETING_2 = (
        "setInCommittee",
        "setInCouncil",
    )
