# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
# File: adapters.py
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
# ------------------------------------------------------------------------------
from AccessControl import ClassSecurityInfo
from appy.gen import No
from collections import OrderedDict
from DateTime import DateTime
from Globals import InitializeClass
from zope.interface import implements
from zope.i18n import translate

from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import DisplayList
from plone import api

from imio.helpers.xhtml import xhtmlContentIsEmpty
from Products.PloneMeeting.adapters import ItemPrettyLinkAdapter
from Products.PloneMeeting.config import NOT_GIVEN_ADVICE_VALUE
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.PloneMeeting.interfaces import IMeetingGroupCustom
from Products.PloneMeeting.interfaces import IMeetingConfigCustom
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.Meeting import MeetingWorkflowActions
from Products.PloneMeeting.Meeting import MeetingWorkflowConditions
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingGroup import MeetingGroup
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowActions
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowConditions
from Products.PloneMeeting.model import adaptations

from Products.MeetingLalouviere import logger
from Products.MeetingLalouviere.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingLalouviere.interfaces import IMeetingItemCollegeLalouviereWorkflowConditions
from Products.MeetingLalouviere.interfaces import IMeetingItemCollegeLalouviereWorkflowActions
from Products.MeetingLalouviere.interfaces import IMeetingCollegeLalouviereWorkflowConditions
from Products.MeetingLalouviere.interfaces import IMeetingCollegeLalouviereWorkflowActions
from Products.MeetingLalouviere.interfaces import IMeetingItemCouncilLalouviereWorkflowConditions
from Products.MeetingLalouviere.interfaces import IMeetingItemCouncilLalouviereWorkflowActions
from Products.MeetingLalouviere.interfaces import IMeetingCouncilLalouviereWorkflowConditions
from Products.MeetingLalouviere.interfaces import IMeetingCouncilLalouviereWorkflowActions
from Products.MeetingLalouviere.config import COUNCIL_COMMISSION_IDS
from Products.MeetingLalouviere.config import COUNCIL_COMMISSION_IDS_2013
from Products.MeetingLalouviere.config import COUNCIL_MEETING_COMMISSION_IDS_2013
from Products.MeetingLalouviere.config import COMMISSION_EDITORS_SUFFIX
from Products.MeetingLalouviere.config import FINANCE_GROUP_ID

# disable most of wfAdaptations
customWfAdaptations = ('archiving', 'local_meeting_managers', 'return_to_proposing_group', )
MeetingConfig.wfAdaptations = customWfAdaptations

# configure parameters for the returned_to_proposing_group wfAdaptation
# we keep also 'itemfrozen' and 'itempublished' in case this should be activated for meeting-config-college...

RETURN_TO_PROPOSING_GROUP_MAPPINGS = {'backTo_item_in_committee_from_returned_to_proposing_group': ['in_committee', ],
                                      'backTo_item_in_council_from_returned_to_proposing_group': ['in_council', ],
                                      }
adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS.update(RETURN_TO_PROPOSING_GROUP_MAPPINGS)
RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'itemfrozen', 'itempublished',
                                              'item_in_committee', 'item_in_council', )
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES
RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {
    # view permissions
    'Access contents information':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'View':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read budget infos':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read decision':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read optional advisers':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read decision annex':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read item observations':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'MeetingLalouviere: Read commission transcript':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    # edit permissions
    'Modify portal content':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
    'PloneMeeting: Write budget infos':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', 'MeetingBudgetImpactEditor'],
    'PloneMeeting: Write decision':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
    'Review portal content':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
    'Add portal content':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
    'PloneMeeting: Add annex':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
    'PloneMeeting: Add MeetingFile':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
    'PloneMeeting: Write decision annex':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
    'PloneMeeting: Write optional advisers':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
    # MeetingManagers edit permissions
    'Delete objects':
    ['Manager', 'MeetingManager', ],
    'PloneMeeting: Write item observations':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
    'MeetingLalouviere: Write commission transcript':
    ['Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', ],
}

adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS

RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = {'meetingitemcollegelalouviere_workflow': 'meetingitemcollegelalouviere_workflow.itemcreated'}
adaptations.RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE

class CustomMeeting(Meeting):
    '''Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom.'''

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting

    # define same validator for every preMeetingDate_X than the one used for preMeetingDate
    Meeting.validate_preMeetingDate_2 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_3 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_4 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_5 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_6 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_7 = Meeting.validate_preMeetingDate

    security.declarePublic('isDecided')

    def isDecided(self):
        """
          The meeting is supposed 'decided', if at least in state :
          - 'in_council' for MeetingCouncil
          - 'decided' for MeetingCollege
        """
        meeting = self.getSelf()
        return meeting.queryState() in ('in_council', 'decided', 'closed', 'archived')

    # Implements here methods that will be used by templates
    security.declarePublic('getPrintableItems')

    def getPrintableItems(self, itemUids, listTypes=['normal'], ignore_review_states=[],
                          privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                          excludedCategories=[], groupIds=[], excludedGroupIds=[],
                          firstNumber=1, renumber=False):

        '''Returns a list of items.
           An extra list of review states to ignore can be defined.
           A privacy can also be given, and the fact that the item is an
           oralQuestion or not (or both). Idem with toDiscuss.
           Some specific categories can be given or some categories to exclude.
           We can also receive in p_groupIds MeetingGroup ids to take into account.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'''
        # We just filter ignore_review_states here and privacy and call
        # getItems(uids), passing the correct uids and removing empty uids.
        # privacy can be '*' or 'public' or 'secret' or 'public_heading' or 'secret_heading'
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)

        # check filters
        filteredItemUids = []
        uid_catalog = self.context.uid_catalog
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if obj.queryState() in ignore_review_states:
                continue
            elif not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (oralQuestion == 'both' or obj.getOralQuestion() == oralQuestion):
                continue
            elif not (toDiscuss == 'both' or obj.getToDiscuss() == toDiscuss):
                continue
            elif categories and not obj.getCategory() in categories:
                continue
            elif groupIds and not obj.getProposingGroup() in groupIds:
                continue
            elif excludedCategories and obj.getCategory() in excludedCategories:
                continue
            elif excludedGroupIds and obj.getProposingGroup() in excludedGroupIds:
                continue
            filteredItemUids.append(itemUid)
        #in case we do not have anything, we return an empty list
        if not filteredItemUids:
            return []
        else:
            items = self.context.getItems(uids=filteredItemUids, listTypes=listTypes, ordered=True)
            if renumber:
                #returns a list of tuple with first element the number and second element the item itself
                i = firstNumber
                res = []
                for item in items:
                    res.append((i, item))
                    i = i + 1
                items = res
            return items

    #helper methods used in templates

    security.declarePublic('getNormalCategories')

    def getNormalCategories(self):
        '''Returns the 'normal' categories'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        categories = mc.getCategories(onlySelectable=False)
        res = []
        firstSupplCatIds = self.getFirstSupplCategories()
        secondSupplCatIds = self.getSecondSupplCategories()
        thirdSupplCatIds = self.getThirdSupplCategories()
        for cat in categories:
            catId = cat.getId()
            if not catId in firstSupplCatIds and \
               not catId in secondSupplCatIds and \
               not catId in thirdSupplCatIds:
                res.append(catId)
        return res
    Meeting.getNormalCategories = getNormalCategories

    security.declarePublic('getFirstSupplCategories')

    def getFirstSupplCategories(self):
        '''Returns the '1er-supplement' categories'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        categories = mc.getCategories(onlySelectable=False)
        res = []
        for cat in categories:
            catId = cat.getId()
            if catId.endswith('1er-supplement'):
                res.append(catId)
        return res
    Meeting.getFirstSupplCategories = getFirstSupplCategories

    security.declarePublic('getSecondSupplCategories')

    def getSecondSupplCategories(self):
        '''Returns the '2eme-supplement' categories'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        categories = mc.getCategories(onlySelectable=False)
        res = []
        for cat in categories:
            catId = cat.getId()
            if catId.endswith('2eme-supplement'):
                res.append(catId)
        return res
    Meeting.getSecondSupplCategories = getSecondSupplCategories

    security.declarePublic('getThirdSupplCategories')

    def getThirdSupplCategories(self):
        '''Returns the '3eme-supplement' categories'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        categories = mc.getCategories(onlySelectable=False)
        res = []
        for cat in categories:
            catId = cat.getId()
            if catId.endswith('3eme-supplement'):
                res.append(catId)
        return res
    Meeting.getThirdSupplCategories = getThirdSupplCategories

    security.declarePublic('getNumberOfItems')

    def getNumberOfItems(self, itemUids, privacy='*', categories=[], listTypes=['normal']):
        '''Returns the number of items depending on parameters.
           This is used in templates to know how many items of a particular kind exist and
           often used to determine the 'firstNumber' parameter of getPrintableItems/getPrintableItemsByCategory.'''
        # sometimes, some empty elements are inserted in itemUids, remove them...
        itemUids = [itemUid for itemUid in itemUids if itemUid != '']
        if not categories and privacy == '*':
            return len(self.context.getItems(uids=itemUids, listTypes=listTypes))
        # Either, we will have to filter (privacy, categories, late)
        filteredItemUids = []
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (categories == [] or obj.getCategory() in categories):
                continue
            elif not obj.isLate() == bool(listTypes == ['late']):
                continue
            filteredItemUids.append(itemUid)
        return len(filteredItemUids)

    def getItemsFirstSuppl(self, itemUids, privacy='public'):
        '''Returns the items presented as first supplement'''
        normalCategories = self.getNormalCategories()
        firstSupplCategories = self.getFirstSupplCategories()
        firstNumber = self.getNumberOfItems(itemUids,
                                            privacy=privacy,
                                            categories=normalCategories) + 1
        return self.adapted().getPrintableItems(itemUids,
                                                privacy=privacy,
                                                categories=firstSupplCategories,
                                                firstNumber=firstNumber,
                                                renumber=True)
    Meeting.getItemsFirstSuppl = getItemsFirstSuppl

    def getItemsSecondSuppl(self, itemUids, privacy='public'):
        '''Returns the items presented as second supplement'''
        normalCategories = self.getNormalCategories()
        firstSupplCategories = self.getFirstSupplCategories()
        secondSupplCategories = self.getSecondSupplCategories()
        firstNumber = self.getNumberOfItems(itemUids,
                                            privacy=privacy,
                                            categories=normalCategories+firstSupplCategories) + 1
        return self.adapted().getPrintableItems(itemUids,
                                                privacy=privacy,
                                                categories=secondSupplCategories,
                                                firstNumber=firstNumber,
                                                renumber=True)
    Meeting.getItemsSecondSuppl = getItemsSecondSuppl

    def getItemsThirdSuppl(self, itemUids, privacy='public'):
        '''Returns the items presented as third supplement'''
        normalCategories = self.getNormalCategories()
        firstSupplCategories = self.getFirstSupplCategories()
        secondSupplCategories = self.getSecondSupplCategories()
        thirdSupplCategories = self.getThirdSupplCategories()
        firstNumber = self.getNumberOfItems(itemUids,
                                            privacy=privacy,
                                            categories=normalCategories+firstSupplCategories+secondSupplCategories) + 1
        return self.adapted().getPrintableItems(itemUids,
                                                privacy=privacy,
                                                categories=thirdSupplCategories,
                                                firstNumber=firstNumber,
                                                renumber=True)
    Meeting.getItemsThirdSuppl = getItemsThirdSuppl

    security.declarePublic('getLabelDescription')

    def getLabelDescription(self):
        '''Returns the label to use for field MeetingItem.description
          The label is different between college and council'''
        if self.portal_type == 'MeetingItemCouncil':
            return self.utranslate("MeetingLalouviere_label_councildescription", domain="PloneMeeting")
        else:
            return self.utranslate("PloneMeeting_label_description", domain="PloneMeeting")
    MeetingItem.getLabelDescription = getLabelDescription

    security.declarePublic('getLabelCategory')

    def getLabelCategory(self):
        '''Returns the label to use for field MeetingItem.category
          The label is different between college and council'''
        if self.portal_type == 'MeetingItemCouncil':
            return self.utranslate("MeetingLalouviere_label_councilcategory", domain="PloneMeeting")
        else:
            return self.utranslate("PloneMeeting_label_category", domain="PloneMeeting")
    MeetingItem.getLabelCategory = getLabelCategory

    security.declarePublic('getLabelObservations')

    def getLabelObservations(self):
        '''Returns the label to use for field Meeting.observations
           The label is different between college and council'''
        if self.portal_type == 'MeetingCouncil':
            return self.utranslate("MeetingLalouviere_label_meetingcouncilobservations", domain="PloneMeeting")
        else:
            return self.utranslate("PloneMeeting_label_meetingObservations", domain="PloneMeeting")
    Meeting.getLabelObservations = getLabelObservations

    security.declarePublic('getCommissionTitle')

    def getCommissionTitle(self, commissionNumber=1):
        '''
          Given a commissionNumber, return the commission title depending on corresponding categories
        '''
        meeting = self.getSelf()
        commissionCategories = meeting.getCommissionCategories()
        if not len(commissionCategories) >= commissionNumber:
            return ''
        commissionCat = commissionCategories[commissionNumber-1]
        # build title
        if isinstance(commissionCat, tuple):
            res = 'Commission ' + '/'.join([subcat.Title().replace('Commission ', '') for subcat in commissionCat])
        else:
            res = commissionCat.Title()
        return res

    security.declarePublic('getCommissionCategories')

    def getCommissionCategories(self):
        '''Returns the list of categories used for Commissions.
           Since june 2013, some commission are aggregating several categories, in this case,
           a sublist of categories is returned...'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        # creating a new Meeting or editing an existing meeting with date >= june 2013
        if not self.getDate() or \
           (self.getDate().year() >= 2013 and self.getDate().month() > 5) or \
           (self.getDate().year() > 2013):
            # since 2013 commissions does NOT correspond to commission as MeetingItem.category
            # several MeetingItem.category are taken for one single commission...
            commissionCategoryIds = COUNCIL_MEETING_COMMISSION_IDS_2013
        else:
            commissionCategoryIds = COUNCIL_COMMISSION_IDS

        res = []
        for categoryId in commissionCategoryIds:
            # check if we have subcategories, aka a commission made of several categories
            if isinstance(categoryId, tuple):
                res2 = []
                for subcatId in categoryId:
                    res2.append(getattr(mc.categories, subcatId))
                res.append(tuple(res2))
            else:
                res.append(getattr(mc.categories, categoryId))
        return tuple(res)
    Meeting.getCommissionCategories = getCommissionCategories

    security.declarePrivate('getDefaultPreMeetingAssembly')

    def getDefaultPreMeetingAssembly(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly = getDefaultPreMeetingAssembly

    security.declarePrivate('getDefaultPreMeetingAssembly_2')

    def getDefaultPreMeetingAssembly_2(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_2_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_2 = getDefaultPreMeetingAssembly_2

    security.declarePrivate('getDefaultPreMeetingAssembly_3')

    def getDefaultPreMeetingAssembly_3(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_3_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_3 = getDefaultPreMeetingAssembly_3

    security.declarePrivate('getDefaultPreMeetingAssembly_4')

    def getDefaultPreMeetingAssembly_4(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_4_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_4 = getDefaultPreMeetingAssembly_4

    security.declarePrivate('getDefaultPreMeetingAssembly_5')

    def getDefaultPreMeetingAssembly_5(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_5_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_5 = getDefaultPreMeetingAssembly_5

    security.declarePrivate('getDefaultPreMeetingAssembly_6')

    def getDefaultPreMeetingAssembly_6(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_6_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_6 = getDefaultPreMeetingAssembly_6

    security.declarePrivate('getDefaultPreMeetingAssembly_7')

    def getDefaultPreMeetingAssembly_7(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_7_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_7 = getDefaultPreMeetingAssembly_7


class CustomMeetingItem(MeetingItem):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom.'''
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    customMeetingTransitionsAcceptingRecurringItems = ('_init_', 'freeze', 'decide', 'setInCommittee', 'setInCouncil', )
    MeetingItem.meetingTransitionsAcceptingRecurringItems = customMeetingTransitionsAcceptingRecurringItems

    def __init__(self, item):
        self.context = item

    security.declarePublic('listFollowUps')

    def listFollowUps(self):
        '''List available values for vocabulary of the 'followUp' field.'''
        d = 'PloneMeeting'
        u = self.utranslate
        res = DisplayList((
            ("follow_up_no", u('follow_up_no', domain=d)),
            ("follow_up_yes", u('follow_up_yes', domain=d)),
            ("follow_up_provided", u('follow_up_provided', domain=d)),
            ("follow_up_provided_not_printed", u('follow_up_provided_not_printed', domain=d)),
        ))
        return res
    MeetingItem.listFollowUps = listFollowUps

    security.declarePublic('activateFollowUp')

    def activateFollowUp(self):
        '''Activate follow-up by setting followUp to 'follow_up_yes'.'''
        self.setFollowUp('follow_up_yes')
        #initialize the neededFollowUp field with the available content of the 'decision' field
        if not self.getNeededFollowUp():
            self.setNeededFollowUp(self.getDecision())
        self.reindexObject(idxs=['getFollowUp', ])
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + '#followup')
    MeetingItem.activateFollowUp = activateFollowUp

    security.declarePublic('deactivateFollowUp')

    def deactivateFollowUp(self):
        '''Deactivate follow-up by setting followUp to 'follow_up_no'.'''
        self.setFollowUp('follow_up_no')
        self.reindexObject(idxs=['getFollowUp', ])
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + '#followup')
    MeetingItem.deactivateFollowUp = deactivateFollowUp

    security.declarePublic('confirmFollowUp')

    def confirmFollowUp(self):
        '''Confirm follow-up by setting followUp to 'follow_up_provided'.'''
        self.setFollowUp('follow_up_provided')
        self.reindexObject(idxs=['getFollowUp', ])
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + '#followup')
    MeetingItem.confirmFollowUp = confirmFollowUp

    security.declarePublic('followUpNotPrinted')

    def followUpNotPrinted(self):
        '''While follow-up is confirmed, we may specify that we do not want it printed in the dashboard.'''
        self.setFollowUp('follow_up_provided_not_printed')
        self.reindexObject(idxs=['getFollowUp', ])
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + '#followup')
    MeetingItem.followUpNotPrinted = followUpNotPrinted

    security.declarePublic('onDuplicated')

    def onDuplicated(self, original):
        '''Hook when a item is duplicated (called by MeetingItem.clone).'''
        # while an item is cloned to the meeting-config-council,
        # add the council specific 'motivation' at the top of existing 'motivation'
        item = self.getSelf()
        # only apply if we are actually creating a MeetingItemCouncil from another MeetingConfig
        if not (item.portal_type == 'MeetingItemCouncil' and original.portal_type != 'MeetingItemCouncil'):
            return
        existingMotivation = item.getMotivation()
        defaultCouncilMotivation = item.Schema()['motivation'].getDefault(item)
        item.setMotivation(defaultCouncilMotivation + '<p>&nbsp;</p><p>&nbsp;</p>' + existingMotivation)

    security.declareProtected('Modify portal content', 'onEdit')

    def onEdit(self, isCreated):
        '''Depending on the selected Council commission (category),
           give the 'MeetingCommissionEditor' role to the relevant Plone group'''
        # if the current category id startswith a given Plone group, this is the correspondance
        # for example, category 'commission-travaux' correspond to Plone
        # group 'commission-travaux_COMMISSION_EDITORS_SUFFIX'
        # category 'commission-travaux-1er-supplement' correspond to Plone
        # group 'commission-travaux_COMMISSION_EDITORS_SUFFIX'
        # first, remove previously set local roles for the Plone group commission
        # this is only done for MeetingItemCouncil
        if not self.context.portal_type == 'MeetingItemCouncil':
            return
        #existing commission Plone groups
        commissionEditorsGroupIds = [(commissionId + COMMISSION_EDITORS_SUFFIX) for commissionId in
                                     set(COUNCIL_COMMISSION_IDS).union(set(COUNCIL_COMMISSION_IDS_2013))]
        groupsTool = getToolByName(self.context, 'portal_groups')
        commissionPloneGroupIds = [groupId for groupId in groupsTool.getGroupIds()
                                   if groupId in commissionEditorsGroupIds]
        toRemove = []
        for principalId, localRoles in self.context.get_local_roles():
            if (principalId in commissionPloneGroupIds):
                toRemove.append(principalId)
        self.context.manage_delLocalRoles(toRemove)
        #now add the new local roles
        for groupId in commissionPloneGroupIds:
            if self.context.getCategory().startswith(groupId[:-len(COMMISSION_EDITORS_SUFFIX)]):
                #we found the relevant group
                self.context.manage_addLocalRoles(groupId, ('MeetingCommissionEditor',))

    security.declarePublic('isPrivacyViewable')

    def isPrivacyViewable(self):
        '''Override so privacy is not taken into account while accessing an item.
           We just need privacy to be an information here, not an access management.'''
        return True
    MeetingItem.isPrivacyViewable = isPrivacyViewable

    def _initDecisionFieldIfEmpty(self):
        '''
          If decision field is empty, it will be initialized
          with data coming from title and description.
        '''
        # set keepWithNext to False as it will add a 'class' and so
        # xhtmlContentIsEmpty will never consider it empty...
        if xhtmlContentIsEmpty(self.getDecision(keepWithNext=False)):
            self.setDecision("<p>%s</p>%s" % (self.Title(),
                                              self.Description()))
            self.reindexObject()
    MeetingItem._initDecisionFieldIfEmpty = _initDecisionFieldIfEmpty

    def mayGenerateFinanceAdvice(self):
        '''
          Condition used in the 'Avis DF' PodTemplate.
        '''
        if FINANCE_GROUP_ID in self.context.adviceIndex and \
           self.context.adviceIndex[FINANCE_GROUP_ID]['delay'] and \
           self.context.adviceIndex[FINANCE_GROUP_ID]['type'] != NOT_GIVEN_ADVICE_VALUE:
            return True
        return False

    def getExtraFieldsToCopyWhenCloning(self, cloned_to_same_mc):
        '''
          Keep some new fields when item is cloned (to another mc or from itemtemplate).
        '''
        res = ['interventions', 'commissionTranscript', 'followUp', 'neededFollowUp', 'providedFollowUp']
        if cloned_to_same_mc:
            res = res + []
        return res

    def adviceDelayIsTimedOutWithRowId(self, groupId, rowIds=[]):
        ''' Check if advice with delay from a certain p_groupId and with
            a row_id contained in p_rowIds is timed out.
        '''
        self = self.getSelf()
        if self.getAdviceDataFor(self) and groupId in self.getAdviceDataFor(self):
            adviceRowId = self.getAdviceDataFor(self, groupId)['row_id']
        else:
            return False

        if not rowIds or adviceRowId in rowIds:
            return self._adviceDelayIsTimedOut(groupId)
        else:
            return False

    def showFinanceAdviceTemplate(self):
        """ """
        item = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(item)
        return bool(set(cfg.adapted().getUsedFinanceGroupIds(item)).
                    intersection(set(item.adviceIndex.keys())))


class CustomMeetingGroup(MeetingGroup):
    '''Adapter that adapts a meetingGroup implementing IMeetingGroup to the
       interface IMeetingGroupCustom.'''

    implements(IMeetingGroupCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePrivate('validate_signatures')

    def validate_signatures(self, value):
        '''Validate the MeetingGroup.signatures field.'''
        if value.strip() and not len(value.split('\n')) == 12:
            return self.utranslate('signatures_length_error', domain='PloneMeeting')
    MeetingGroup.validate_signatures = validate_signatures

    def listEchevinServices(self):
        '''Returns a list of groups that can be selected on an group (without isEchevin).'''
        res = []
        tool = getToolByName(self, 'portal_plonemeeting')
        # Get every Plone group related to a MeetingGroup
        for group in tool.getMeetingGroups():
            res.append((group.id, group.getProperty('title')))

        return DisplayList(tuple(res))
    MeetingGroup.listEchevinServices = listEchevinServices


class CustomMeetingConfig(MeetingConfig):
    '''Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom.'''

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePublic('getUsedFinanceGroupIds')

    def getUsedFinanceGroupIds(self, item=None):
        """Possible finance advisers group ids are defined on
           the FINANCE_ADVICES_COLLECTION_ID collection."""
        cfg = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        collection = getattr(cfg.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID, None)
        res = []
        if not collection:
            logger.warn(
                "Method 'getUsedFinanceGroupIds' could not find the '{0}' collection!".format(
                    FINANCE_ADVICES_COLLECTION_ID))
            return res
        # if collection is inactive, we just return an empty list
        # for convenience, the collection is added to every MeetingConfig, even if not used
        wfTool = api.portal.get_tool('portal_workflow')
        if wfTool.getInfoFor(collection, 'review_state') == 'inactive':
            return res
        # get the indexAdvisers value defined on the collection
        # and find the relevant group, indexAdvisers form is :
        # 'delay_real_group_id__2014-04-16.9996934488', 'real_group_id_directeur-financier'
        # it is either a customAdviser row_id or a MeetingGroup id
        values = [term['v'] for term in collection.getRawQuery()
                  if term['i'] == 'indexAdvisers'][0]

        for v in values:
            rowIdOrGroupId = v.replace('delay_real_group_id__', '').replace('real_group_id__', '')
            if hasattr(tool, rowIdOrGroupId):
                groupId = rowIdOrGroupId
                # append it only if not already into res and if
                # we have no 'row_id' for this adviser in adviceIndex
                if item and groupId not in res and \
                   (groupId in item.adviceIndex and not item.adviceIndex[groupId]['row_id']):
                    res.append(groupId)
                elif not item:
                    res.append(groupId)
            else:
                groupId = cfg._dataForCustomAdviserRowId(rowIdOrGroupId)['group']
                # append it only if not already into res and if
                # we have a 'row_id' for this adviser in adviceIndex
                if item and groupId not in res and \
                    (groupId in item.adviceIndex and
                     item.adviceIndex[groupId]['row_id'] == rowIdOrGroupId):
                    res.append(groupId)
                elif not item:
                    res.append(groupId)
        # remove duplicates
        return list(set(res))

    def _extraSearchesInfo(self, infos):
        """Add some specific searches."""
        cfg = self.getSelf()
        itemType = cfg.getItemTypeName()
        extra_infos = OrderedDict(
            [
                # Items in state 'proposed'
                ('searchproposeditems',
                 {
                     'subFolderId': 'searches_items',
                     'active': True,
                     'query':
                         [
                             {'i': 'portal_type',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': [itemType, ]},
                             {'i': 'review_state',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': ['proposed']}
                         ],
                     'sort_on': u'created',
                     'sort_reversed': True,
                     'showNumberOfItems': False,
                     'tal_condition': "python: not tool.userIsAmong(['reviewers'])",
                     'roles_bypassing_talcondition': ['Manager', ]
                 }
                 ),
                # Items in state 'validated'
                ('searchvalidateditems',
                 {
                     'subFolderId': 'searches_items',
                     'active': True,
                     'query':
                         [
                             {'i': 'portal_type',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': [itemType, ]},
                             {'i': 'review_state',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': ['validated']}
                         ],
                     'sort_on': u'created',
                     'sort_reversed': True,
                     'showNumberOfItems': False,
                     'tal_condition': "",
                     'roles_bypassing_talcondition': ['Manager', ]
                 }
                 ),
            ]
        )
        infos.update(extra_infos)
        return infos

    security.declarePublic('getMeetingsAcceptingItems')

    def getMeetingsAcceptingItems(self, review_states=('created', 'frozen'), inTheFuture=False):
        '''This returns meetings that are still accepting items.'''
        cfg = self.getSelf()
        tool = getToolByName(cfg, 'portal_plonemeeting')
        catalog = getToolByName(cfg, 'portal_catalog')
        # If the current user is a meetingManager (or a Manager),
        # he is able to add a meetingitem to a 'decided' meeting.
        # except if we specifically restricted given p_review_states.
        if review_states == ('created', 'frozen') and tool.isManager(cfg):
            # XXX begin change by MeetingLalouviere
            review_states += ('decided', 'in_committee', 'in_council', )
            # XXX end change by MeetingLalouviere

        query = {'portal_type': cfg.getMeetingTypeName(),
                 'review_state': review_states,
                 'sort_on': 'getDate'}

        if inTheFuture:
            query['getDate'] = {'query': DateTime(), 'range': 'min'}

        return catalog.unrestrictedSearchResults(**query)


class MeetingCollegeLalouviereWorkflowActions(MeetingWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeLalouviereWorkflowActions'''

    implements(IMeetingCollegeLalouviereWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doDecide')

    def doDecide(self, stateChange):
        '''We pass every item that is 'presented' in the 'itemfrozen'
           state.  It is the case for late items. Moreover, if
           MeetingConfig.initItemDecisionIfEmptyOnDecide is True, we
           initialize the decision field with content of Title+Description
           if decision field is empty.'''
        tool = getToolByName(self.context, 'portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        initializeDecision = cfg.getInitItemDecisionIfEmptyOnDecide()
        for item in self.context.getAllItems(ordered=True):
            if initializeDecision:
                # If deliberation (motivation+decision) is empty,
                # initialize it the decision field
                item._initDecisionFieldIfEmpty()


class MeetingCollegeLalouviereWorkflowConditions(MeetingWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeLalouviereWorkflowConditions'''

    implements(IMeetingCollegeLalouviereWorkflowConditions)
    security = ClassSecurityInfo()

    security.declarePublic('mayDecide')

    def mayDecide(self):
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res


class MeetingItemCollegeLalouviereWorkflowActions(MeetingItemWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCollegeLalouviereWorkflowActions'''

    implements(IMeetingItemCollegeLalouviereWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doAccept_but_modify')

    def doAccept_but_modify(self, stateChange):
        pass

    security.declarePrivate('doRemove')

    def doRemove(self, stateChange):
        pass

    security.declarePrivate('doProposeToServiceHead')

    def doProposeToServiceHead(self, stateChange):
        pass

    security.declarePrivate('doWaitAdvices')

    def doWaitAdvices(self, stateChange):
        pass

    security.declarePrivate('doProposeToDirector')

    def doProposeToDirector(self, stateChange):
        pass

    security.declarePrivate('doProposeToOfficeManager')

    def doProposeToOfficeManager(self, stateChange):
        pass

    security.declarePrivate('doProposeToDivisionHead')

    def doProposeToDivisionHead(self, stateChange):
        pass

    security.declarePrivate('doValidateByBudgetImpactReviewer')

    def doValidateByBudgetImpactReviewer(self, stateChange):
        pass

    security.declarePrivate('doProposeToBudgetImpactReviewer')

    def doProposeToBudgetImpactReviewer(self, stateChange):
        pass

    security.declarePrivate('doAsk_advices_by_itemcreator')

    def doAsk_advices_by_itemcreator(self, stateChange):
        pass


class MeetingItemCollegeLalouviereWorkflowConditions(MeetingItemWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCollegeLalouviereWorkflowConditions'''

    implements(IMeetingItemCollegeLalouviereWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem

    security.declarePublic('mayDecide')

    def mayDecide(self):
        '''We may decide an item if the linked meeting is in the 'decided'
           state.'''
        res = False
        meeting = self.context.getMeeting()
        if _checkPermission(ReviewPortalContent, self.context) and \
           meeting and meeting.adapted().isDecided():
            res = True
        return res

    security.declarePublic('mayRefuse')

    def mayRefuse(self):
        '''Only 'Manager' may refuse an item, it is for history reasons because now this is not
           used anymore but some old items were 'refused'...'''
        tool = getToolByName(self.context, 'portal_plonemeeting')
        if tool.isManager(self.context, realManagers=True):
            return True
        return False

    security.declarePublic('mayDelay')

    def mayDelay(self):
        '''Only 'Manager' may delay an item, it is for history reasons because now this is not
           used anymore but some old items were 'delayed'...'''
        tool = getToolByName(self.context, 'portal_plonemeeting')
        if tool.isManager(self.context, realManagers=True):
            return True
        return False

    security.declarePublic('mayValidate')

    def mayValidate(self):
        """
          Either the Director or the MeetingManager can validate
          The MeetingManager can bypass the validation process and validate an item
          that is in the state 'itemcreated'
        """
        res = False
        #first of all, the use must have the 'Review portal content permission'
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
            #if the current item state is 'itemcreated', only the MeetingManager can validate
            tool = getToolByName(self.context, 'portal_plonemeeting')
            if self.context.queryState() in ('itemcreated',) and not tool.isManager(self.context):
                res = False
        return res

    security.declarePublic('mayFreeze')

    def mayFreeze(self):
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in ('frozen', 'decided', 'closed')):
                res = True
        return res

    security.declarePublic('mayCorrect')

    def mayCorrect(self):
        # Check with the default PloneMeeting method and our test if res is
        # False. The diffence here is when we correct an item from itemfrozen to
        # presented, we have to check if the Meeting is in the "created" state
        # and not "published".
        res = MeetingItemWorkflowConditions.mayCorrect(self)
        # Manage our own behaviour now when the item is linked to a meeting,
        # a MeetingManager can correct anything except if the meeting is closed
        if res is not True:
            if _checkPermission(ReviewPortalContent, self.context):
                # Get the meeting
                meeting = self.context.getMeeting()
                if meeting:
                    # Meeting can be None if there was a wf problem leading
                    # an item to be in a "presented" state with no linked
                    # meeting.
                    meetingState = meeting.queryState()
                    # A user having ReviewPortalContent permission can correct
                    # an item in any case except if the meeting is closed.
                    if meetingState != 'closed':
                        res = True
                else:
                    res = True
        return res

    security.declarePublic('mayWaitAdvices')

    def mayWaitAdvices(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if not self.context.getCategory():
            return No(translate('required_category_ko',
                                domain="PloneMeeting",
                                context=self.context.REQUEST))
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToServiceHead')

    def mayProposeToServiceHead(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if not self.context.getCategory():
            return No(translate('required_category_ko',
                                domain="PloneMeeting",
                                context=self.context.REQUEST))
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToOfficeManager')

    def mayProposeToOfficeManager(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToDivisionHead')

    def mayProposeToDivisionHead(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToDirector')

    def mayProposeToDirector(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayRemove')

    def mayRemove(self):
        """
          We may remove an item if the linked meeting is in the 'decided'
          state.  It is kept for backward compatibility, but for now, only allow real
          managers to do that so MeetingManagers are not bothered with the icon.
        """
        tool = getToolByName(self.context, 'portal_plonemeeting')
        if tool.isManager(self.context, realManagers=True):
            return True
        return False

    security.declarePublic('mayValidateByBudgetImpactReviewer')

    def mayValidateByBudgetImpactReviewer(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToBudgetImpactReviewer')

    def mayProposeToBudgetImpactReviewer(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if not self.context.getCategory():
            return No(translate('required_category_ko',
                                domain="PloneMeeting",
                                context=self.context.REQUEST))
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res


class MeetingCouncilLalouviereWorkflowActions(MeetingWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCouncilLalouviereWorkflowActions'''

    implements(IMeetingCouncilLalouviereWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doSetInCommittee')

    def doSetInCommittee(self, stateChange):
        '''When setting the meeting in committee, every items must be
           automatically set to "item_in_committee", it is done using
           Meetingconfig.onMeetingTransitionItemTransitionToTrigger.'''
        # manage meeting number
        self.initSequenceNumber()

    security.declarePrivate('doSetInCouncil')

    def doSetInCouncil(self, stateChange):
        '''When setting the meeting in council, every items must be automatically
           set to "item_in_council", it is done using
           Meetingconfig.onMeetingTransitionItemTransitionToTrigger.'''
        pass

    security.declarePrivate('doBackToCreated')

    def doBackToCreated(self, stateChange):
        '''When a meeting go back to the "created" state, for example the
           meeting manager wants to add an item, we do not do anything.'''
        pass

    security.declarePrivate('doBackToInCommittee')

    def doBackToInCommittee(self, stateChange):
        '''When a meeting go back to the "in_committee" we set every items
        'in_council' back to 'in_committee', it is done using
           Meetingconfig.onMeetingTransitionItemTransitionToTrigger.'''
        pass

    security.declarePrivate('doBackToInCouncil')

    def doBackToInCouncil(self, stateChange):
        '''When a meeting go back to the "in_council" we do not do anything.'''
        pass


class MeetingCouncilLalouviereWorkflowConditions(MeetingWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCouncilLalouviereWorkflowConditions'''

    implements(IMeetingCouncilLalouviereWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting
        customAcceptItemsStates = ('created', 'in_committee', 'in_council', )
        self.acceptItemsStates = customAcceptItemsStates

    security.declarePublic('maySetInCommittee')

    def maySetInCommittee(self):
        res = False
        # The user just needs the "Review portal content" permission
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('maySetInCouncil')

    def maySetInCouncil(self):
        # The user just needs the "Review portal content" permission
        if not _checkPermission(ReviewPortalContent, self.context):
            return False
        return True

    security.declarePublic('mayClose')

    def mayClose(self):
        res = False
        # The user just needs the "Review portal content" permission on the
        # object to close it.
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayChangeItemsOrder')

    def mayChangeItemsOrder(self):
        '''We can change the order if the meeting is not closed'''
        res = False
        if _checkPermission(ModifyPortalContent, self.context) and \
           self.context.queryState() not in ('closed', ):
            res = True
        return res

    def mayCorrect(self):
        '''Take the default behaviour except if the meeting is frozen
           we still have the permission to correct it.'''
        from Products.PloneMeeting.Meeting import MeetingWorkflowConditions
        res = MeetingWorkflowConditions.mayCorrect(self)
        currentState = self.context.queryState()
        if res is not True and currentState in ('in_committee', 'in_council', ):
            # Change the behaviour for being able to correct a frozen meeting
            # back to created.
            if _checkPermission(ReviewPortalContent, self.context):
                return True
        return res

    def mayDecide(self):
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res


class MeetingItemCouncilLalouviereWorkflowActions(MeetingItemWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCouncilWorkflowActions'''

    implements(IMeetingItemCouncilLalouviereWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doProposeToDirector')

    def doProposeToDirector(self, stateChange):
        pass

    security.declarePrivate('doSetItemInCommittee')

    def doSetItemInCommittee(self, stateChange):
        pass

    security.declarePrivate('doSetItemInCouncil')

    def doSetItemInCouncil(self, stateChange):
        pass

    security.declarePrivate('doReturn_to_proposing_group')

    def doReturn_to_proposing_group(self, stateChange):
        '''Send an email to the creator and to the officemanagers'''
        self.context.sendMailIfRelevant('returnedToProposingGroup', 'MeetingMember', isRole=True)
        self.context.sendMailIfRelevant('returnedToProposingGroup', 'MeetingOfficeManager', isRole=True)

    security.declarePrivate('doBackToItemInCommittee')

    def doBackToItemInCommittee(self, stateChange):
        pass

    security.declarePrivate('doBackToItemInCouncil')

    def doBackToItemInCouncil(self, stateChange):
        pass

    security.declarePrivate('doAccept_but_modify')

    def doAccept_but_modify(self, stateChange):
        pass

    security.declarePrivate('doDelay')

    def doDelay(self, stateChange):
        '''When an item is delayed, by default it is duplicated but we do not
           duplicate it here'''
        pass


class MeetingItemCouncilLalouviereWorkflowConditions(MeetingItemWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCouncilWorkflowConditions'''

    implements(IMeetingItemCouncilLalouviereWorkflowConditions)
    security = ClassSecurityInfo()

    useHardcodedTransitionsForPresentingAnItem = True
    transitionsForPresentingAnItem = ('proposeToDirector', 'validate', 'present')

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem

    security.declarePublic('mayProposeToDirector')

    def mayProposeToDirector(self):
        """
          Check that the user has the 'Review portal content'
          If the item comes from the college, check that it has a defined
          'category'
        """
        # In the case the item comes from the college
        if not self.context.getCategory():
            return False
        if _checkPermission(ReviewPortalContent, self.context) and \
           (not self.context.isDefinedInTool()):
            return True
        return False

    security.declarePublic('isLateFor')

    def isLateFor(self, meeting):
        """
          No late functionnality for Council
        """
        return False

    security.declarePublic('maySetItemInCommittee')

    def maySetItemInCommittee(self):
        """
          Check that the user has the 'Review portal content'
          And that the linked meeting is in the correct state
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in
                    ('in_committee', 'in_council', 'closed')):
                res = True
        return res

    security.declarePublic('maySetItemInCouncil')

    def maySetItemInCouncil(self):
        """
          Check that the user has the 'Review portal content'
          And that the linked meeting is in the correct state
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in
                    ('in_council', 'closed')):
                res = True
        return res

    security.declarePublic('mayDecide')

    def mayDecide(self):
        '''We may decide an item if the linked meeting is in the 'decided'
           state.'''
        res = False
        meeting = self.context.getMeeting()
        if _checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['in_council', 'closed']):
            res = True
        return res

    security.declarePublic('mayRefuse')

    def mayRefuse(self):
        '''Only 'Manager' may refuse an item, it is for history reasons because now this is not
           used anymore but some old items were 'refused'...'''
        tool = getToolByName(self.context, 'portal_plonemeeting')
        if tool.isManager(self.context, realManagers=True):
            return True
        return False

# ------------------------------------------------------------------------------
InitializeClass(CustomMeetingItem)
InitializeClass(CustomMeeting)
InitializeClass(CustomMeetingConfig)
InitializeClass(CustomMeetingGroup)
InitializeClass(MeetingCollegeLalouviereWorkflowActions)
InitializeClass(MeetingCollegeLalouviereWorkflowConditions)
InitializeClass(MeetingItemCollegeLalouviereWorkflowActions)
InitializeClass(MeetingItemCollegeLalouviereWorkflowConditions)
InitializeClass(MeetingCouncilLalouviereWorkflowActions)
InitializeClass(MeetingCouncilLalouviereWorkflowConditions)
InitializeClass(MeetingItemCouncilLalouviereWorkflowActions)
InitializeClass(MeetingItemCouncilLalouviereWorkflowConditions)
# ------------------------------------------------------------------------------


class MLItemPrettyLinkAdapter(ItemPrettyLinkAdapter):
    """
      Override to take into account MeetingLiege use cases...
    """

    def _leadingIcons(self):
        """
          Manage icons to display before the icons managed by PrettyLink._icons.
        """
        # Default PM item icons
        icons = super(MLItemPrettyLinkAdapter, self)._leadingIcons()

        item = self.context

        if item.isDefinedInTool():
            return icons

        itemState = item.queryState()
        # add some icons specific for dashboard if we are actually on the dashboard...
        if itemState in item.itemDecidedStates and \
                        item.REQUEST.form.get('topicId', '') == 'searchitemsfollowupdashboard':
            itemFollowUp = item.getFollowUp()
            if itemFollowUp == 'follow_up_yes':
                icons.append(('follow_up_yes.png', 'icon_help_follow_up_needed'))
            elif itemFollowUp == 'follow_up_provided':
                icons.append(('follow_up_provided.png', 'icon_help_follow_up_provided'))

        # Add our icons for wf states
        if itemState == 'proposed_to_director':
            icons.append(('proposeToDirector.png', 'icon_help_proposed_to_director'))
        elif itemState == 'proposed_to_divisionhead':
            icons.append(('proposeToDivisionHead.png', 'icon_help_proposed_to_divisionhead'))
        elif itemState == 'proposed_to_officemanager':
            icons.append(('proposeToOfficeManager.png', 'icon_help_proposed_to_officemanager'))
        elif itemState == 'item_in_council':
            icons.append(('item_in_council.png', 'icon_help_item_in_council'))
        elif itemState == 'item_in_committee':
            icons.append(('item_in_committee.png', 'icon_help_item_in_committee'))
        elif itemState == 'proposed_to_servicehead':
            icons.append(('proposeToServiceHead.png', 'icon_help_proposed_to_servicehead'))
        elif itemState == 'proposed_to_budgetimpact_reviewer':
            icons.append(('proposeToBudgetImpactReviewer.png', 'icon_help_proposed_to_budgetimpact_reviewer'))
        elif itemState == 'itemcreated_waiting_advices':
            icons.append(('ask_advices_by_itemcreator.png', 'icon_help_itemcreated_waiting_advices'))
        return icons