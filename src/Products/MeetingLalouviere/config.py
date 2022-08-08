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
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ("Manager", "Owner", "Contributor"))

product_globals = globals()

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

# ids of commissions used as categories for MeetingItemCouncil
# before 2013, commission ids were :
COUNCIL_COMMISSION_IDS = (
    "commission-travaux",
    "commission-enseignement",
    "commission-cadre-de-vie-et-logement",
    "commission-ag",
    "commission-finances-et-patrimoine",
    "commission-police",
    "commission-speciale",
)
# until 2013, commission ids are :
# changes are about 'commission-enseignement', 'commission-cadre-de-vie-et-logement' and
# 'commission-finances-et-patrimoine' that are splitted in smaller commissions
COUNCIL_COMMISSION_IDS_2013 = (
    "commission-ag",
    "commission-finances",
    "commission-enseignement",
    "commission-culture",
    "commission-sport",
    "commission-sante",
    "commission-police",
    "commission-cadre-de-vie",
    "commission-patrimoine",
    "commission-travaux",
    "commission-speciale",
)
# commissions taken into account on the Meeting
# since 2013, some commissions are made of several categories...
COUNCIL_MEETING_COMMISSION_IDS_2013 = (
    "commission-travaux",
    (
        "commission-ag",
        "commission-finances",
        "commission-enseignement",
        "commission-culture",
        "commission-sport",
        "commission-sante",
    ),
    ("commission-cadre-de-vie", "commission-patrimoine",),
    "commission-police",
    "commission-speciale",
)

# commissions taken into account on the Meeting
# since 2019, travaux and finance are merge. ag and enseignement are merged
COUNCIL_MEETING_COMMISSION_IDS_2019 = (
    ("commission-travaux", "commission-finances"),
    (
        "commission-ag",
        "commission-enseignement",
        "commission-culture",
        "commission-sport",
        "commission-sante",
    ),
    ("commission-cadre-de-vie", "commission-patrimoine",),
    "commission-police",
    "commission-speciale",
)

# commissions taken into account on the Meeting
# since 2020, patrimoine is moved with travaux and finance
COUNCIL_MEETING_COMMISSION_IDS_2020 = (
    ("commission-travaux", "commission-finances", "commission-patrimoine"),
    (
        "commission-ag",
        "commission-enseignement",
        "commission-culture",
        "commission-sport",
        "commission-sante",
    ),
    "commission-cadre-de-vie",
    "commission-police",
    "commission-speciale",
)

# suffix of specific groups containing commission transcript editors
COMMISSION_EDITORS_SUFFIX = "commissioneditors"

# id of finance advice group
FINANCE_GROUP_ID = "avis-directeur-financier-2200020ac"

# if True, a positive finances advice may be signed by a finances reviewer
# if not, only the finances manager may sign advices
POSITIVE_FINANCE_ADVICE_SIGNABLE_BY_REVIEWER = False

COLLEGE_DEFAULT_MOTIVATION = (
    "<p>Vu l'arrêté du Gouvernement Wallon du 22 avril 2004 portant codification de la "
    "législation relative aux pouvoirs locaux; dit le code de la démocratie locale et de "
    "la décentralisation;"
    "</p><p>&nbsp;</p>"
    "<p>Vu le décret du 27 mai 2004 portant confirmation dudit arrêté du gouvernement "
    "Wallon du 22 avril 2004;</p>"
    "<p>&nbsp;</p>"
    "<p>Vu l'article 123 de la nouvelle Loi communale;</p>"
    "<p>&nbsp;</p>"
    "<p>Vu l'article L1123-23 du code de la Démocratie locale et de la Décentralisation;</p>"
)

COUNCIL_DEFAULT_MOTIVATION = (
    "<p>Le Conseil,</p>"
    "<p>&nbsp;</p>"
    "<p>Vu, d'une part, l'arrêté du Gouvernement Wallon du 22 avril 2004 portant "
    "codification de la législation relative aux pouvoirs locaux et d'autre part, "
    "le décret du 27 mai 2004 portant confirmation dudit arrêté;</p>"
    "<p>&nbsp;</p>"
    "<p>Vu l'article 117 de la nouvelle Loi Communale;</p>"
    "<p>&nbsp;</p>"
    "<p>Vu l'article L 1122-30 du Code de Démocratie Locale et de la Décentralisation;</p>"
)

LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS = (
    {'state': 'itemcreated',
     'state_title': 'itemcreated',
     'leading_transition': '-',
     'leading_transition_title': '-',
     'back_transition': 'backToItemCreated',
     'back_transition_title': 'backToItemCreated',
     'suffix': 'creators',
     # only creators may manage itemcreated item
     'extra_suffixes': [],
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
     'extra_suffixes': [],
     'enabled': '1',
     },
    {'state': 'proposed_to_servicehead',
     'state_title': 'proposed_to_servicehead',
     'leading_transition': 'proposeToServiceHead',
     'leading_transition_title': 'proposeToServiceHead',
     'back_transition': 'backToProposedToServiceHead',
     'back_transition_title': 'backToProposedToServiceHead',
     'suffix': 'serviceheads',
     'extra_suffixes': [],
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
     'extra_suffixes': [],
     },
    {'state': 'proposed_to_divisionhead',
     'state_title': 'proposed_to_divisionhead',
     'leading_transition': 'proposeToDivisionHead',
     'leading_transition_title': 'proposeToDivisionHead',
     'back_transition': 'backToProposedToDivisionHead',
     'back_transition_title': 'backToProposedToDivisionHead',
     'suffix': 'divisionheads',
     'enabled': '1',
     'extra_suffixes': [],
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
     'suffix': '',
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
    "removed",
    "delayed",
    "no_publication",
    "return_to_proposing_group",
)

LLO_APPLYED_COUNCIL_WFA = (
    "accepted_but_modified",
    "pre_accepted",
    "refused",
    "removed",
    "delayed",
    "no_decide",
    "return_to_proposing_group",
)
