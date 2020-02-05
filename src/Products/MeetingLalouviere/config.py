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

import os
from collections import OrderedDict
from Products.CMFCore.permissions import setDefaultRoles
from Products.PloneMeeting import config as PMconfig

__author__ = """Gauthier Bastien <g.bastien@imio.be>, Stephan Geulette <s.geulette@imio.be>"""
__docformat__ = 'plaintext'

PROJECTNAME = "MeetingLalouviere"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

# the id of the collection querying finance advices
FINANCE_ADVICES_COLLECTION_ID = 'searchitemswithfinanceadvice'

PMconfig.EXTRA_GROUP_SUFFIXES = [
    {'fct_title': u'budgetimpactreviewers', 'fct_id': u'budgetimpactreviewers', 'fct_orgs': []},
    {'fct_title': u'serviceheads', 'fct_id': u'serviceheads', 'fct_orgs': []},
    {'fct_title': u'officemanagers', 'fct_id': u'officemanagers', 'fct_orgs': []},
    {'fct_title': u'divisionheads', 'fct_id': u'divisionheads', 'fct_orgs': []},
    {'fct_title': u'directors', 'fct_id': u'directors', 'fct_orgs': []},
    {'fct_title': u'followupwriters', 'fct_id': u'followupwriters', 'fct_orgs': []},
    {'fct_title': u'alderman', 'fct_id': u'alderman', 'fct_orgs': []},
]

LALOUVIEREMEETINGREVIEWERS = OrderedDict([('alderman', 'proposed_to_alderman'),
                                          ('directors', 'proposed_to_director'),
                                          ('divisionheads', 'proposed_to_divisionhead'),
                                          ('officemanagers', 'proposed_to_officemanager'),
                                          ('serviceheads', 'proposed_to_servicehead'), ])
PMconfig.MEETINGREVIEWERS = LALOUVIEREMEETINGREVIEWERS
LALOUVIERE_MEETING_STATES_ACCEPTING_ITEMS = ('created', 'frozen', 'published', 'decided', 'in_committee', 'in_council')
PMconfig.MEETING_STATES_ACCEPTING_ITEMS = LALOUVIERE_MEETING_STATES_ACCEPTING_ITEMS

# url of the DEF application
DEFURL = os.environ.get('DEFURL', 'http://192.168.1.106/def')

# ids of commissions used as categories for MeetingItemCouncil
# before 2013, commission ids were :
COUNCIL_COMMISSION_IDS = ('commission-travaux', 'commission-enseignement',
                          'commission-cadre-de-vie-et-logement', 'commission-ag',
                          'commission-finances-et-patrimoine', 'commission-police',
                          'commission-speciale',)
# until 2013, commission ids are :
# changes are about 'commission-enseignement', 'commission-cadre-de-vie-et-logement' and
# 'commission-finances-et-patrimoine' that are splitted in smaller commissions
COUNCIL_COMMISSION_IDS_2013 = ('commission-ag', 'commission-finances', 'commission-enseignement',
                               'commission-culture', 'commission-sport', 'commission-sante',
                               'commission-police', 'commission-cadre-de-vie', 'commission-patrimoine',
                               'commission-travaux', 'commission-speciale',)
# commissions taken into account on the Meeting
# since 2013, some commissions are made of several categories...
COUNCIL_MEETING_COMMISSION_IDS_2013 = ('commission-travaux',

                                       ('commission-ag', 'commission-finances', 'commission-enseignement',
                                        'commission-culture', 'commission-sport', 'commission-sante',),

                                       ('commission-cadre-de-vie', 'commission-patrimoine',),

                                       'commission-police',

                                       'commission-speciale',)

# commissions taken into account on the Meeting
# since 2019, travaux and finance are merge. ag and enseignement are merged
COUNCIL_MEETING_COMMISSION_IDS_2019 = (('commission-travaux',
                                        'commission-finances'),

                                       ('commission-ag',
                                        'commission-enseignement',
                                        'commission-culture',
                                        'commission-sport',
                                        'commission-sante',),

                                       ('commission-cadre-de-vie',
                                        'commission-patrimoine',),
                                       'commission-police',

                                       'commission-speciale',)

# suffix of specific groups containing commission transcript editors
COMMISSION_EDITORS_SUFFIX = '_commissioneditors'

# id of finance advice group
FINANCE_GROUP_ID = 'avis-directeur-financier-2200020ac'

# if True, a positive finances advice may be signed by a finances reviewer
# if not, only the finances manager may sign advices
POSITIVE_FINANCE_ADVICE_SIGNABLE_BY_REVIEWER = False
