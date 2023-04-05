# -*- coding: utf-8 -*-
#
# File: config.py
#
# Copyright (c) 2016 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.
import copy
import os
from collections import OrderedDict

from Products.PloneMeeting import config as PMconfig

from Products.CMFCore.permissions import setDefaultRoles

__author__ = """Gauthier Bastien <g.bastien@imio.be>, 
Stephan Geulette <s.geulette@imio.be>, 
Olivier Delaere <olivier.delaere@imio.be>"""
__docformat__ = "plaintext"

PROJECTNAME = "MeetingLalouviere"

# Permissions
DEFAULT_WRITE_FOLLOWUP_PERMISSION = "MeetingLalouviere: Write followUp"
setDefaultRoles(DEFAULT_WRITE_FOLLOWUP_PERMISSION, ('Manager', 'MeetingManager'))

DEFAULT_WRITE_NEEDED_FOLLOWUP_PERMISSION = "MeetingLalouviere: Write neededFollowUp"
setDefaultRoles(DEFAULT_WRITE_NEEDED_FOLLOWUP_PERMISSION, ('Manager', 'MeetingManager'))

DEFAULT_WRITE_PROVIDED_FOLLOWUP_PERMISSION = "MeetingLalouviere: Write providedFollowUp"
setDefaultRoles(DEFAULT_WRITE_PROVIDED_FOLLOWUP_PERMISSION, ('Manager', 'MeetingManager', 'MeetingFollowUpWriter'))

product_globals = globals()

DG_GROUP_ID = "direction-generale"
FALLBACK_DG_GROUP_ID = "dirgen"

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

# the id of the collection querying finance advices
PMconfig.EXTRA_GROUP_SUFFIXES = [
    {
        "fct_id": u"budgetimpactreviewers",
        "fct_title": u"Correspondants Financier",
        "fct_orgs": [],
        "enabled": True,
        "fct_management": False,
    },
    {
        "fct_id": u"serviceheads",
        "fct_title": u"Chef de Service",
        "fct_orgs": [],
        "enabled": True,
        "fct_management": False,
    },
    {
        "fct_id": u"officemanagers",
        "fct_title": u"Chef de Bureau",
        "fct_orgs": [],
        "enabled": True,
        "fct_management": False,
    },
    {
        "fct_id": u"divisionheads",
        "fct_title": u"Chef de Division",
        "fct_orgs": [],
        "enabled": True,
        "fct_management": False,
    },
    {
        "fct_id": u"directors",
        "fct_title": u"Directeur",
        "fct_orgs": [],
        "enabled": True,
        "fct_management": False,
    },
    {
        "fct_id": u"followupwriters",
        "fct_title": u"Rédacteur de Suivi",
        "fct_orgs": [],
        "enabled": True,
        "fct_management": False,
    },
    {
        "fct_id": u"alderman",
        "fct_title": u"Échevin",
        "fct_orgs": [],
        "enabled": True,
        "fct_management": False,
    },
]

LALOUVIERE_MEETING_STATES_ACCEPTING_ITEMS = (
    "created",
    "frozen",
    "published",
    "decided",
    "in_committee",
    "in_council",
)
PMconfig.MEETING_STATES_ACCEPTING_ITEMS = LALOUVIERE_MEETING_STATES_ACCEPTING_ITEMS

# id of finance advice group
FINANCE_GROUP_ID = "avis-directeur-financier-2200020ac"

# if True, a positive finances advice may be signed by a finances reviewer
# if not, only the finances manager may sign advices
POSITIVE_FINANCE_ADVICE_SIGNABLE_BY_REVIEWER = False

LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS = (
    {'state': 'itemcreated',
     'state_title': 'itemcreated',
     'leading_transition': '-',
     'leading_transition_title': '-',
     'back_transition': 'backToItemCreated',
     'back_transition_title': 'backToItemCreated',
     'suffix': 'creators',
     # only creators may manage itemcreated item
     'extra_suffixes': ['serviceheads', 'officemanagers', 'divisionheads', 'directors'],
     'enabled': '1',
     },
    {'state': 'proposed_to_director',
     'state_title': 'proposed_to_director',
     'leading_transition': 'proposeToDirector',
     'leading_transition_title': 'proposeToDirector',
     'back_transition': 'backToProposedToDirector',
     'back_transition_title': 'backToProposedToDirector',
     'suffix': 'directors',
     'enabled': '1',
     'extra_suffixes': [],
     },
)

LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS = (
    {'state': 'itemcreated',
     'state_title': 'itemcreated',
     'leading_transition': '-',
     'leading_transition_title': '-',
     'back_transition': 'backToItemCreated',
     'back_transition_title': 'backToItemCreated',
     'suffix': 'creators',
     'extra_suffixes': ['serviceheads', 'officemanagers', 'divisionheads', 'directors'],
     'enabled': '1',
     },
    {'state': 'proposed_to_servicehead',
     'state_title': 'proposed_to_servicehead',
     'leading_transition': 'proposeToServiceHead',
     'leading_transition_title': 'proposeToServiceHead',
     'back_transition': 'backToProposedToServiceHead',
     'back_transition_title': 'backToProposedToServiceHead',
     'suffix': 'serviceheads',
     'extra_suffixes': ['officemanagers', 'divisionheads', 'directors'],
     'enabled': '1',
     },
    {'state': 'proposed_to_officemanager',
     'state_title': 'proposed_to_officemanager',
     'leading_transition': 'proposeToOfficeManager',
     'leading_transition_title': 'proposeToOfficeManager',
     'back_transition': 'backToProposedToOfficeManager',
     'back_transition_title': 'backToProposedToOfficeManager',
     'suffix': 'officemanagers',
     'enabled': '1',
     'extra_suffixes': ['divisionheads', 'directors'],
     },
    {'state': 'proposed_to_divisionhead',
     'state_title': 'proposed_to_divisionhead',
     'leading_transition': 'proposeToDivisionHead',
     'leading_transition_title': 'proposeToDivisionHead',
     'back_transition': 'backToProposedToDivisionHead',
     'back_transition_title': 'backToProposedToDivisionHead',
     'suffix': 'divisionheads',
     'enabled': '1',
     'extra_suffixes': ['directors'],
     },
    {'state': 'proposed_to_director',
     'state_title': 'proposed_to_director',
     'leading_transition': 'proposeToDirector',
     'leading_transition_title': 'proposeToDirector',
     'back_transition': 'backToProposedToDirector',
     'back_transition_title': 'backToProposedToDirector',
     'suffix': 'directors',
     'enabled': '1',
     'extra_suffixes': [],
     },
    {'state': 'proposed_to_dg',
     'state_title': 'proposed_to_dg',
     'leading_transition': 'proposeToDg',
     'leading_transition_title': 'proposeToDg',
     'back_transition': 'backToProposedToDg',
     'back_transition_title': 'backToProposedToDg',
     'suffix': 'directors',
     'enabled': '1',
     'extra_suffixes': [],
     },
    {'state': 'proposed_to_alderman',
     'state_title': 'proposed_to_alderman',
     'leading_transition': 'proposeToAlderman',
     'leading_transition_title': 'proposeToAlderman',
     'back_transition': 'backToProposedToAlderman',
     'back_transition_title': 'backToProposedToAlderman',
     'suffix': 'alderman',
     'enabled': '1',
     'extra_suffixes': [],
     },
)

LLO_APPLYED_COLLEGE_WFA = (
    "accepted_but_modified",
    "pre_accepted",
    "refused",
    "delayed",
    "removed",
    "return_to_proposing_group",
    "no_publication",
    'propose_to_budget_reviewer',
    'waiting_advices',
    'waiting_advices_proposing_group_send_back',
    'item_validation_shortcuts',
)

LLO_APPLYED_COUNCIL_WFA = (
    "accepted_but_modified",
    "pre_accepted",
    "refused",
    "delayed",
    "removed",
    "return_to_proposing_group",
    'apply_council_state_label',
    'propose_to_budget_reviewer',
    'waiting_advices',
    'waiting_advices_proposing_group_send_back',
    'item_validation_shortcuts',
)
