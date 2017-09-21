# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.config import MEETINGREVIEWERS
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import GroupDescriptor
from Products.PloneMeeting.profiles import ItemAnnexSubTypeDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import ItemTemplateDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import MeetingUserDescriptor
from Products.PloneMeeting.profiles import PloneGroupDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import RecurringItemDescriptor
from Products.PloneMeeting.profiles import UserDescriptor


today = DateTime().strftime('%Y/%m/%d')

# Annex types
overheadAnalysisSubtype = ItemAnnexSubTypeDescriptor(
    'overhead-analysis-sub-annex',
    'Overhead analysis sub annex',
    other_mc_correspondences=(
        'meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis', ))

overheadAnalysis = ItemAnnexTypeDescriptor(
    'overhead-analysis', 'Administrative overhead analysis',
    u'overheadAnalysis.png',
    subTypes=[overheadAnalysisSubtype],
    other_mc_correspondences=(
        'meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis_-_budget-analysis-sub-annex', ))

financialAnalysisSubAnnex = ItemAnnexSubTypeDescriptor(
    'financial-analysis-sub-annex',
    'Financial analysis sub annex')

financialAnalysis = ItemAnnexTypeDescriptor(
    'financial-analysis', 'Financial analysis', u'financialAnalysis.png',
    u'Predefined title for financial analysis', subTypes=[financialAnalysisSubAnnex])

legalAnalysis = ItemAnnexTypeDescriptor(
    'legal-analysis', 'Legal analysis', u'legalAnalysis.png')

budgetAnalysisCfg2Subtype = ItemAnnexSubTypeDescriptor(
    'budget-analysis-sub-annex',
    'Budget analysis sub annex')

budgetAnalysisCfg2 = ItemAnnexTypeDescriptor(
    'budget-analysis', 'Budget analysis', u'budgetAnalysis.png',
    subTypes=[budgetAnalysisCfg2Subtype])

budgetAnalysisCfg1Subtype = ItemAnnexSubTypeDescriptor(
    'budget-analysis-sub-annex',
    'Budget analysis sub annex',
    other_mc_correspondences=(
        'meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis_-_budget-analysis-sub-annex', ))

budgetAnalysisCfg1 = ItemAnnexTypeDescriptor(
    'budget-analysis', 'Budget analysis', u'budgetAnalysis.png',
    subTypes=[budgetAnalysisCfg1Subtype],
    other_mc_correspondences=('meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis', ))

itemAnnex = ItemAnnexTypeDescriptor(
    'item-annex', 'Other annex(es)', u'itemAnnex.png')
# Could be used once we
# will digitally sign decisions ? Indeed, once signed, we will need to
# store them (together with the signature) as separate files.
decision = ItemAnnexTypeDescriptor(
    'decision', 'Decision', u'decision.png', relatedTo='item_decision')
decisionAnnex = ItemAnnexTypeDescriptor(
    'decision-annex', 'Decision annex(es)', u'decisionAnnex.png', relatedTo='item_decision')
# A vintage annex type
marketingAnalysis = ItemAnnexTypeDescriptor(
    'marketing-annex', 'Marketing annex(es)', u'legalAnalysis.png', relatedTo='item_decision',
    enabled=False)
# Advice annex types
adviceAnnex = AnnexTypeDescriptor(
    'advice-annex', 'Advice annex(es)', u'itemAnnex.png', relatedTo='advice')
adviceLegalAnalysis = AnnexTypeDescriptor(
    'advice-legal-analysis', 'Advice legal analysis', u'legalAnalysis.png', relatedTo='advice')
# Meeting annex types
meetingAnnex = AnnexTypeDescriptor(
    'meeting-annex', 'Meeting annex(es)', u'itemAnnex.png', relatedTo='meeting')

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
bourgmestreMeeting.annexTypes = [financialAnalysis, budgetAnalysisCfg1, overheadAnalysis,
                             itemAnnex, decisionAnnex, marketingAnalysis,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
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
                                           'delayed',
                                           'pre_accepted',)
bourgmestreMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
bourgmestreMeeting.enableAdviceInvalidation = False
bourgmestreMeeting.itemAdviceInvalidateStates = []
bourgmestreMeeting.customAdvisers = []
bourgmestreMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
bourgmestreMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
bourgmestreMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group']
bourgmestreMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
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
bourgmestreMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
bourgmestreMeeting.useCopies = True
bourgmestreMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers')]
bourgmestreMeeting.podTemplates = bourgmestreTemplates
bourgmestreMeeting.meetingConfigsToCloneTo = []
bourgmestreMeeting.recurringItems = []
bourgmestreMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(bourgmestreMeeting, ),
                                 groups=groups)
# ------------------------------------------------------------------------------
