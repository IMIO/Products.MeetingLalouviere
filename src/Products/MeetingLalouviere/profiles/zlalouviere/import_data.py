# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import ItemAnnexSubTypeDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import RecurringItemDescriptor
from Products.PloneMeeting.profiles import UserDescriptor

data = deepcopy(mc_import_data.data)
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

# Users and groups -------------------------------------------------------------
dgen = UserDescriptor('dgen', [], email="test@test.be", fullname="Henry Directeur")
dfin = UserDescriptor('dfin', [], email="test@test.be", fullname="Directeur Financier")
secretaire = UserDescriptor('secretaire', ['MeetingManager'], email="test@test.be")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be")
agentPers = UserDescriptor('agentPers', [], email="test@test.be")
agentTrav = UserDescriptor('agentTrav', [], email="test@test.be")
chefPers = UserDescriptor('chefPers', [], email="test@test.be")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be")
chefBureauCompta = UserDescriptor('chefBureauCompta', [], email="test@test.be")
echevinPers = UserDescriptor('echevinPers', [], email="test@test.be")
emetteuravisPers = UserDescriptor('emetteuravisPers', [], email="test@test.be")
jgobert = UserDescriptor('jgobert',  ['MeetingPowerObserver'],
                         fullname='Jaques Gobert', email="jgobert@lalouviere.be")
asabbatini = UserDescriptor('asabbatini', ['MeetingPowerObserver'],
                            fullname='Annie Sabbatini', email="asabbatini@lalouviere.be")
jgodin = UserDescriptor('jgodin', ['MeetingPowerObserver'],
                        fullname='Jean Godin', email="jgodin@lalouviere.be")
odestrebecq = UserDescriptor('odestrebecq', ['MeetingPowerObserver'],
                             fullname='Olivier Destrebecq', email="odestrebecq@lalouviere.be")
ghaine = UserDescriptor('ghaine', ['MeetingPowerObserver'],
                        fullname='Georges Haine', email="ghaine@lalouviere.be")
adupont = UserDescriptor('adupont', ['MeetingPowerObserver'],
                         fullname='Alexandra Dupont', email="adupont@lalouviere.be")
fghiot = UserDescriptor('fghiot', ['MeetingPowerObserver'],
                        fullname='Françoise Ghiot', email="fghiot@lalouviere.be")
jcwargnie = UserDescriptor('jcwargnie', ['MeetingPowerObserver'],
                           fullname='Jean-Claude Wargnie', email="jcwargnie@lalouviere.be")
dstaquet = UserDescriptor('dstaquet', ['MeetingPowerObserver'],
                          fullname='Danièle Staquet', email="dstaquet@lalouviere.be")
bliebin = UserDescriptor('bliebin', ['MeetingPowerObserver'],
                         fullname='Bernard Liebin', email="bliebin@lalouviere.be")
cburgeon = UserDescriptor('cburgeon', ['MeetingPowerObserver'],
                          fullname='Colette Burgeon', email="cburgeon@lalouviere.be")
mdubois = UserDescriptor('mdubois', ['MeetingPowerObserver'],
                         fullname='Michel Dubois', email="mdubois@lalouviere.be")
ydrugmand = UserDescriptor('ydrugmand', ['MeetingPowerObserver'],
                           fullname='Yves Drugmand', email="ydrugmand@lalouviere.be")
gmaggiordomo = UserDescriptor('gmaggiordomo', ['MeetingPowerObserver'],
                              fullname='Giuseppe Maggiordomo', email="gmaggiordomo@lalouviere.be")
ozrihen = UserDescriptor('ozrihen', ['MeetingPowerObserver'],
                         fullname='Olga Zrihen', email="ozrihen@lalouviere.be")
mdimattia = UserDescriptor('mdimattia', ['MeetingPowerObserver'],
                           fullname='Michele Di Mattia', email="mdimattia@lalouviere.be")
trotolo = UserDescriptor('trotolo', ['MeetingPowerObserver'],
                         fullname='Térèsa Rotolo', email="trotolo@lalouviere.be")
fromeo = UserDescriptor('fromeo', ['MeetingPowerObserver'],
                        fullname='Francesco Romeo', email="fromeo@lalouviere.be")
mhanot = UserDescriptor('mhanot', ['MeetingPowerObserver'],
                        fullname='Muriel Hanot', email="mhanot@lalouviere.be")
ivansteen = UserDescriptor('ivansteen', ['MeetingPowerObserver'],
                           fullname='Isabelle Van Steen', email="ivansteen@lalouviere.be")
jkeijzer = UserDescriptor('jkeijzer', ['MeetingPowerObserver'],
                          fullname='Jan Keijzer', email="jkeijzer@lalouviere.be")
afagbemi = UserDescriptor('afagbemi', ['MeetingPowerObserver'],
                          fullname='Affissou Fagbemi', email="afagbemi@lalouviere.be")
agava = UserDescriptor('agava', ['MeetingPowerObserver'],
                       fullname='Antonio Gava', email="agava@lalouviere.be")
apourbaix = UserDescriptor('apourbaix', ['MeetingPowerObserver'],
                           fullname='Alain Pourbaix', email="apourbaix@lalouviere.be")
lduval = UserDescriptor('lduval', ['MeetingPowerObserver'],
                        fullname='Lucien Duval', email="lduval@lalouviere.be")
jchristiaens = UserDescriptor('jchristiaens', ['MeetingPowerObserver'],
                              fullname='Jonathan Christiaens', email="jchristiaens@lalouviere.be")
mvanhooland = UserDescriptor('mvanhooland', ['MeetingPowerObserver'],
                             fullname='Michaël Van Hooland', email="mvanhooland@lalouviere.be")
frmili = UserDescriptor('frmili', ['MeetingPowerObserver'],
                        fullname='Fatima Rmili', email="frmili@lalouviere.be")
pwaterlot = UserDescriptor('pwaterlot', ['MeetingPowerObserver'],
                           fullname='Philippe Waterlot', email="pwaterlot@lalouviere.be")
abuscemi = UserDescriptor('abuscemi', ['MeetingPowerObserver'],
                          fullname='Antonio Buscemi', email="abuscemi@lalouviere.be")
lwimlot = UserDescriptor('lwimlot', ['MeetingPowerObserver'],
                         fullname='Laurent Wimlot', email="lwimlot@lalouviere.be")
cboulangier = UserDescriptor('cboulangier', ['MeetingPowerObserver'],
                             fullname='Cécile Boulangier', email="cboulangier@lalouviere.be")
vlibois = UserDescriptor('vlibois', ['MeetingPowerObserver'],
                         fullname='Vincent Libois', email="vlibois@lalouviere.be")
ammarin = UserDescriptor('ammarin', ['MeetingPowerObserver'],
                         fullname='Anne-Marie Marin', email="ammarin@lalouviere.be")
agorez = UserDescriptor('agorez', ['MeetingPowerObserver'],
                        fullname='André Gorez', email="agorez@lalouviere.be")
jpmichiels = UserDescriptor('jpmichiels', ['MeetingPowerObserver'],
                            fullname='Jean-Pierre Michiels', email="jpmichiels@lalouviere.be")
cdelplancq = UserDescriptor('cdelplancq', ['MeetingPowerObserver'],
                            fullname='Christophe Delplancq', email="cdelplancq@lalouviere.be")
fvermeer = UserDescriptor('fvermeer', ['MeetingPowerObserver'],
                          fullname='Fabienne Vermeer', email="fvermeer@lalouviere.be")
lbaccareladurso = UserDescriptor('lbaccareladurso', ['MeetingPowerObserver'],
                                 fullname='Louisa Baccarela d\'Urso', email="lbaccareladurso@lalouviere.be")
clicata = UserDescriptor('clicata', ['MeetingPowerObserver'],
                         fullname='Cosimo Licata', email="clicata@lalouviere.be")
mroland = UserDescriptor('mroland', ['MeetingPowerObserver'],
                         fullname='Marie Roland', email="mroland@lalouviere.be")
collegecommunal = UserDescriptor('collegecommunal', ['MeetingPowerObserver'],
                                 fullname='Collège communal', email="collegecommunal@lalouviere.be")
groupeps = UserDescriptor('groupeps', ['MeetingPowerObserver'],
                          fullname='Groupe PS', email="groupeps@lalouviere.be")
groupemr = UserDescriptor('groupemr', ['MeetingPowerObserver'],
                          fullname='Groupe MR', email="groupemr@lalouviere.be")
groupecdh = UserDescriptor('groupecdh', ['MeetingPowerObserver'],
                           fullname='Groupe cdH', email="groupecdh@lalouviere.be")
groupeecolo = UserDescriptor('groupeecolo', ['MeetingPowerObserver'],
                             fullname='Groupe Ecolo', email="groupeecolo@lalouviere.be")
groupeptb = UserDescriptor('groupeptb', ['MeetingPowerObserver'],
                           fullname='Groupe PTB+', email="groupeptb@lalouviere.be")
groupefn = UserDescriptor('groupefn', ['MeetingPowerObserver'],
                          fullname='Groupe FN', email="groupefn@lalouviere.be")
groupeindependant = UserDescriptor('groupeindependant', ['MeetingPowerObserver'],
                                   fullname='Groupe Indépendant', email="groupeindependant@lalouviere.be")

# Meeting configurations -------------------------------------------------------
# college
# COLLEGE
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)
collegeMeeting.itemWorkflow = "meetingitemcollegelalouviere_workflow"
collegeMeeting.meetingWorkflow = "meetingcollegelalouviere_workflow"
collegeMeeting.itemConditionsInterface = "Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowConditions"
collegeMeeting.itemActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowActions"
)
collegeMeeting.meetingConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowConditions"
)
collegeMeeting.meetingActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowActions"
)
collegeMeeting.shortName = 'College'
collegeMeeting.annexTypes = [financialAnalysis, budgetAnalysisCfg1, overheadAnalysis,
                             itemAnnex, decisionAnnex, marketingAnalysis,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
collegeMeeting.usedItemAttributes = ['budgetInfos', 'observations', 'toDiscuss',
                                     'motivation', 'neededFollowUp', 'providedFollowUp', ]

collegeMeeting.transitionsForPresentingAnItem = ['proposeToServiceHead', 'proposeToOfficeManager', 'proposeToDivisionHead',
                                                 'proposeToDirector', 'validate', 'present', ]

collegeMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
                                                              'item_transition': 'itemfreeze'},
                                                             {'meeting_transition': 'decide',
                                                              'item_transition': 'itemfreeze'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'itemfreeze'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept'})

collegeMeeting.itemTopicStates = ('itemcreated', 'proposedToServiceHead', 'proposedToOfficeManager',
                                  'proposedToDivisionHead', 'proposedToDirector', 'proposedToAlderman',
                                  'validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'delayed',
                                  'pre_accepted', 'removed', 'accepted_but_modified', )

collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.itemBudgetInfosStates = ('proposed_to_budgetimpact_reviewer', )
collegeMeeting.meetingAppDefaultView = 'searchallitems'
collegeMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'meeting-config-council',
                                           'trigger_workflow_transitions_until': '__nothing__'}, ]
collegeMeeting.useGroupsAsCategories = True


# Conseil communal
# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('recurrent', 'Point récurrent',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-travaux', 'Commission Travaux'),
              CategoryDescriptor('commission-enseignement',
                                 'Commission Enseignement'),
              CategoryDescriptor('commission-culture',
                                 'Commission Culture'),
              CategoryDescriptor('commission-sport',
                                 'Commission Sport'),
              CategoryDescriptor('commission-sante',
                                 'Commission Santé'),
              CategoryDescriptor('commission-cadre-de-vie', 'Commission Cadre de Vie'),
              CategoryDescriptor('commission-ag', 'Commission AG'),
              CategoryDescriptor('commission-finances', 'Commission Finances'),
              CategoryDescriptor('commission-patrimoine', 'Commission Patrimoine'),
              CategoryDescriptor('commission-police', 'Commission Police'),
              CategoryDescriptor('commission-speciale', 'Commission Spéciale',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),

              CategoryDescriptor('commission-travaux-1er-supplement', 'Commission Travaux (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-enseignement-1er-supplement',
                                 'Commission Enseignement (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-culture-1er-supplement',
                                 'Commission Culture (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-sport-1er-supplement',
                                 'Commission Sport (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-sante-1er-supplement',
                                 'Commission Santé (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-cadre-de-vie-1er-supplement', 'Commission Cadre de Vie (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-ag-1er-supplement', 'Commission AG (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-finances-1er-supplement', 'Commission Finances (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-patrimoine-1er-supplement', 'Commission Patrimoine (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-police-1er-supplement', 'Commission Police (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-speciale-1er-supplement', 'Commission Spéciale (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),

              CategoryDescriptor('points-conseillers-2eme-supplement', 'Points conseillers (2ème supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('points-conseillers-3eme-supplement', 'Points conseillers (3ème supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen'))]

councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.itemWorkflow = "meetingitemcouncillalouviere_workflow"
councilMeeting.meetingWorkflow = "meetingcouncillalouviere_workflow"
councilMeeting.itemConditionsInterface = "Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowConditions"
councilMeeting.itemActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowActions"
)
councilMeeting.meetingConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowConditions"
)
councilMeeting.meetingActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowActions"
)
councilMeeting.categories = categories
councilMeeting.annexTypes = [financialAnalysis, legalAnalysis,
                             budgetAnalysisCfg2, itemAnnex, decisionAnnex,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
councilMeeting.usedItemAttributes = ['oralQuestion', 'itemInitiator', 'observations',
                                     'privacy', 'itemAssembly', 'motivation']
councilMeeting.usedMeetingAttributes = ('place', 'observations', 'signatures', 'assembly', 'preMeetingDate',
                                        'preMeetingPlace', 'preMeetingAssembly', 'preMeetingDate_2',
                                        'preMeetingPlace_2', 'preMeetingAssembly_2', 'preMeetingDate_3',
                                        'preMeetingPlace_3', 'preMeetingAssembly_3', 'preMeetingDate_4',
                                        'preMeetingPlace_4', 'preMeetingAssembly_4', 'preMeetingDate_5',
                                        'preMeetingPlace_5', 'preMeetingAssembly_5', 'preMeetingDate_6',
                                        'preMeetingPlace_6', 'preMeetingAssembly_6', 'preMeetingDate_7',
                                        'preMeetingPlace_7', 'preMeetingAssembly_7', 'startDate', 'endDate', )
councilMeeting.workflowAdaptations = ['return_to_proposing_group', ]
councilMeeting.transitionsForPresentingAnItem = ['proposeToDirector', 'validate', 'present', ]
councilMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'setInCommittee',
                                                              'item_transition': 'setItemInCommittee'},
                                                             {'meeting_transition': 'backToInCommittee',
                                                              'item_transition': 'backToItemInCommittee'},
                                                             {'meeting_transition': 'setInCouncil',
                                                              'item_transition': 'setItemInCommittee'},
                                                             {'meeting_transition': 'setInCouncil',
                                                              'item_transition': 'setItemInCouncil'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept'})

#show every items states
councilMeeting.itemTopicStates = ('itemcreated',
                                  'proposed_to_officemanager',
                                  'validated',
                                  'presented',
                                  'itemfrozen',
                                  'item_in_committee',
                                  'item_in_council',
                                  'returned_to_service',
                                  'accepted',
                                  'accepted_but_modified',
                                  'refused',
                                  'delayed')
councilMeeting.meetingTopicStates = ('created',
                                     'frozen',
                                     'in_committee')
councilMeeting.decisionTopicStates = ('in_council',
                                      'closed')
councilMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurrent-approuve-pv',
        title='Approbation du procès-verbal du Conseil communal du ...',
        description='',
        category='recurrent',
        proposingGroup='secretariat',
        decision='',
        meetingTransitionInsertingMe='setInCommittee'),
    RecurringItemDescriptor(
        id='recurrent-questions-actualite',
        title='Questions d\'actualités',
        description='',
        category='recurrent',
        proposingGroup='secretariat',
        decision='',
        meetingTransitionInsertingMe='setInCommittee'),
]
# ------------------------------------------------------------------------------
