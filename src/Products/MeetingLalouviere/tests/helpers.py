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
from copy import deepcopy

from Products.MeetingCommunes.tests.helpers import MeetingCommunesTestingHelpers
from Products.PloneMeeting.profiles import MeetingConfigDescriptor

from Products.MimetypesRegistry.mime_types.magic import magicTest


class MeetingLalouviereTestingHelpers(MeetingCommunesTestingHelpers):
    """Override some values of PloneMeetingTestingHelpers."""
    TRANSITIONS_FOR_FREEZING_MEETING_2 = ("freeze", "publish", "decide",)

    TRANSITIONS_FOR_PROPOSING_ITEM_FIRST_LEVEL_1 = ("proposeToServiceHead",)

    TRANSITIONS_FOR_PROPOSING_ITEM_FIRST_LEVEL_2 = ("proposeToDirector",)

    TRANSITIONS_FOR_PROPOSING_ITEM_1 = (
        "proposeToServiceHead",
        "proposeToOfficeManager",
        "proposeToDivisionHead",
        "proposeToDirector",
        "proposeToDg",
        "proposeToAlderman",
    )
    TRANSITIONS_FOR_PROPOSING_ITEM_2 = (
        "proposeToDirector",
    )

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
        "proposeToDg",
        "proposeToAlderman",
        "validate",
        "present",
    )
    TRANSITIONS_FOR_PRESENTING_ITEM_2 = (
        "proposeToDirector",
        "validate",
        "present",
    )

    BACK_TO_WF_PATH_1 = {
        # Meeting
        "created": ("backToDecided", "backToPublished", "backToFrozen", "backToCreated",),
        # MeetingItem
        "itemcreated": (
            "backToItemFrozen",
            "backToPresented",
            "backToValidated",
            "backToProposedToAlderman",
            "backToProposedToDg",
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
            "backToProposedToAlderman",
            "backToProposedToDg",
            "backToProposedToDirector",
        ),
        "proposed_to_alderman": (
            "backToItemFrozen",
            "backToPresented",
            "backToValidated",
            "backToProposedToAlderman",
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
        "proposed": (
            "backToItemFrozen",
            "backToPresented",
            "backToValidated",
            "backToProposedToDirector",
        ),
        "validated": ("backToItemFrozen", "backToPresented", "backToValidated",),
    }

    WF_ITEM_STATE_NAME_MAPPINGS_1 = {
        "itemcreated": "itemcreated",
        'proposed_first_level': 'proposed_to_servicehead',
        "proposed": "proposed_to_alderman",
        "validated": "validated",
        "presented": "presented",
        "itemfrozen": "itemfrozen",
    }

    WF_ITEM_STATE_NAME_MAPPINGS_2 = {
        "itemcreated": "itemcreated",
        'proposed_first_level': 'proposed_to_director',
        "proposed": "proposed_to_director",
        "validated": "validated",
        "presented": "presented",
        "itemfrozen": "itemfrozen",
    }

    def _setUpDefaultItemWFValidationLevels(self, cfg):
        """Setup default itemWFValidationLevels for given p_cfg,
           used to avoid a custom profile breaking the tests."""
        # make sure we use default itemWFValidationLevels,
        # useful when test executed with custom profile
        defValues = deepcopy(MeetingConfigDescriptor.get().itemWFValidationLevels)
        suffix_mapping = {
            'creators': 'creators',
            'level1reviewers': 'serviceheads',
            'level2reviewers': 'officemanagers',
            'level3reviewers': 'divisionheads',
            'level4reviewers': 'directors',
            'level5reviewers': 'directors',
            'reviewers': 'directors',
        }
        for value in defValues:
            value['suffix'] = suffix_mapping[value['suffix']]
        cfg.setItemWFValidationLevels(defValues)
        cfg.at_post_edit_script()

    def apply_meeting_transition_to_late_state(self, meeting, as_manager=False, clean_memoize=True):
        if meeting.portal_type == "MeetingCouncil":
            self.decideMeeting(meeting, as_manager, clean_memoize)
        else:
            super(MeetingLalouviereTestingHelpers, self).apply_meeting_transition_to_late_state(meeting,
                                                                                          as_manager,
                                                                                          clean_memoize)

    def _enablePrevalidation(self, cfg, enable_extra_suffixes=False):
        if self._testMethodName in ('test_pm_WFA_waiting_advices_with_prevalidation',):
            super(MeetingLalouviereTestingHelpers, self)._enablePrevalidation(cfg, enable_extra_suffixes)
        cfg.at_post_edit_script()

    def _enable_mc_Prevalidation(self, cfg, enable_extra_suffixes=False):
        self._setUpDefaultItemWFValidationLevels(cfg)
        super(MeetingLalouviereTestingHelpers, self)._enablePrevalidation(cfg, enable_extra_suffixes)
