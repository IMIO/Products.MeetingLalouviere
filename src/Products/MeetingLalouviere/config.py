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

__author__ = """Gauthier Bastien <g.bastien@imio.be>, Stephan Geulette <s.geulette@imio.be>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
from collections import OrderedDict
import os

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

##code-section config-bottom #fill in your manual code here
from Products.PloneMeeting import config as PMconfig
LALOUVIEREROLES = {}
LALOUVIEREROLES['budgetimpactreviewers'] = 'MeetingBudgetImpactReviewer'
LALOUVIEREROLES['serviceheads'] = 'MeetingServiceHead'
LALOUVIEREROLES['officemanagers'] = 'MeetingOfficeManager'
LALOUVIEREROLES['divisionheads'] = 'MeetingDivisionHead'
LALOUVIEREROLES['directors'] = 'MeetingDirector'
LALOUVIEREROLES['followupwriters'] = 'MeetingFollowUpWriter'
PMconfig.MEETINGROLES.update(LALOUVIEREROLES)
PMconfig.MEETING_GROUP_SUFFIXES = PMconfig.MEETINGROLES.keys()

LALOUVIEREMEETINGREVIEWERS = OrderedDict([('directors', 'proposed_to_director'),
                                          ('divisionheads', 'proposed_to_divisionhead'),
                                          ('officemanagers', 'proposed_to_officemanager'),
                                          ('serviceheads', 'proposed_to_servicehead'), ])
PMconfig.MEETINGREVIEWERS = LALOUVIEREMEETINGREVIEWERS

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

# suffix of specific groups containing commission transcript editors
COMMISSION_EDITORS_SUFFIX = '_commissioneditors'

# id of finance advice group
FINANCE_GROUP_ID = 'avis-directeur-financier-2200020ac'

# if True, a positive finances advice may be signed by a finances reviewer
# if not, only the finances manager may sign advices
POSITIVE_FINANCE_ADVICE_SIGNABLE_BY_REVIEWER = False