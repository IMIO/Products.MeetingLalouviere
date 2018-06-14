# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import GroupDescriptor
from Products.PloneMeeting.profiles import ItemAnnexSubTypeDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration

from DateTime import DateTime

today = DateTime().strftime('%Y/%m/%d')

# Annex types
annexe = ItemAnnexTypeDescriptor('annexe', 'Annexe', u'attach.png')
annexeDecision = ItemAnnexTypeDescriptor('annexeDecision', 'Annexe à la décision',
                                         u'attach.png', relatedTo='item_decision')
annexeAvis = AnnexTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                 u'attach.png', relatedTo='advice')
annexeSeance = AnnexTypeDescriptor('annexe', 'Annexe',
                                   u'attach.png', relatedTo='meeting')

# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('category1', 'Catégorie 1'),
              CategoryDescriptor('category2', 'Catégorie 2'),
              CategoryDescriptor('category3', 'Catégorie 3'),
              CategoryDescriptor('category4', 'Catégorie 4'),
              CategoryDescriptor('category5', 'Catégorie 5')]

# Pod templates ----------------------------------------------------------------
bourgmestreTemplates = []

# Users and groups -------------------------------------------------------------
groups = [GroupDescriptor('groupe_bourgmestre', 'Groupe BOURGMESTRE', 'ordopol')]

# Meeting configurations -------------------------------------------------------
# Bourgmestre
bourgmestreMeeting = MeetingConfigDescriptor(
    'meeting-config-bourgmestre', 'Bourgmestre',
    'Bourgmestre')
bourgmestreMeeting.meetingManagers = []
bourgmestreMeeting.assembly = 'Pierre Dupont - Président,\n' \
                              'Charles Exemple - Premier membre assemblée,\n' \
                              'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                              'Jacqueline Exemple, Observateur'
bourgmestreMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Vraiment Présent',
     'function': u'Le Secrétaire communal',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Charles Exemple',
     'function': u'Le Bourgmestre',
     'date_from': '',
     'date_to': '',
     },
]
bourgmestreMeeting.places = """Place1\r
Place2\r
Place3\r"""
bourgmestreMeeting.categories = categories
bourgmestreMeeting.shortName = 'Bourgmestre'
bourgmestreMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
bourgmestreMeeting.usedItemAttributes = ['detailedDescription',
                                         'budgetInfos',
                                         'observations',
                                         'toDiscuss',
                                         'itemAssembly',
                                         'itemIsSigned', ]
bourgmestreMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
bourgmestreMeeting.recordMeetingHistoryStates = []
bourgmestreMeeting.xhtmlTransformFields = ()
bourgmestreMeeting.xhtmlTransformTypes = ()
bourgmestreMeeting.itemWorkflow = 'meetingitemcollegelalouviere_workflow'
bourgmestreMeeting.meetingWorkflow = 'meetingcollegelalouviere_workflow'
bourgmestreMeeting.maxShownListings = '100'
bourgmestreMeeting.itemConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowConditions'
bourgmestreMeeting.itemActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowActions'
bourgmestreMeeting.meetingConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowConditions'
bourgmestreMeeting.meetingActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowActions'
bourgmestreMeeting.meetingTopicStates = ('created', 'frozen')
bourgmestreMeeting.decisionTopicStates = ('decided', 'closed')
bourgmestreMeeting.enforceAdviceMandatoriness = False
bourgmestreMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                                 'reverse': '0'}, )
bourgmestreMeeting.recordItemHistoryStates = []
bourgmestreMeeting.maxShownMeetings = 5
bourgmestreMeeting.maxDaysDecisions = 60
bourgmestreMeeting.meetingAppDefaultView = 'searchallitems'
bourgmestreMeeting.useAdvices = True
bourgmestreMeeting.selectableAdvisers = []
bourgmestreMeeting.itemAdviceStates = ('validated',)
bourgmestreMeeting.itemAdviceEditStates = ('validated',)
bourgmestreMeeting.itemAdviceViewStates = ('validated',
                                           'presented',
                                           'itemfrozen',
                                           'accepted',
                                           'refused',
                                           'accepted_but_modified',
                                           'delayed',)
bourgmestreMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
bourgmestreMeeting.enableAdviceInvalidation = False
bourgmestreMeeting.itemAdviceInvalidateStates = []
bourgmestreMeeting.customAdvisers = []
bourgmestreMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
bourgmestreMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified']
# bourgmestreMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group']
bourgmestreMeeting.transitionsForPresentingAnItem = ['proposeToServiceHead', 'proposeToOfficeManager', 'proposeToDivisionHead',
                                                 'proposeToDirector', 'validate', 'present', ]
bourgmestreMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le bourgmestre décide de reporter le point.</p>"},))
bourgmestreMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
                                                                  'item_transition': 'itemfreeze'},

                                                                 {'meeting_transition': 'decide',
                                                                  'item_transition': 'itemfreeze'},

                                                                 {'meeting_transition': 'publish_decisions',
                                                                  'item_transition': 'itemfreeze'},
                                                                 {'meeting_transition': 'publish_decisions',
                                                                  'item_transition': 'accept'},

                                                                 {'meeting_transition': 'close',
                                                                  'item_transition': 'itemfreeze'},
                                                                 {'meeting_transition': 'close',
                                                                  'item_transition': 'accept'},)
bourgmestreMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
bourgmestreMeeting.powerAdvisersGroups = ('dirgen', 'dirfin', )
bourgmestreMeeting.itemBudgetInfosStates = ('proposed_to_budgetimpact_reviewer', )
bourgmestreMeeting.useCopies = True
bourgmestreMeeting.selectableCopyGroups = []
bourgmestreMeeting.podTemplates = bourgmestreTemplates
bourgmestreMeeting.meetingConfigsToCloneTo = []
bourgmestreMeeting.recurringItems = []
bourgmestreMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(bourgmestreMeeting, ),
                                 groups=groups)
# ------------------------------------------------------------------------------
