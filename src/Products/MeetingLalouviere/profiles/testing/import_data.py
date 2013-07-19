# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import *

# File types -------------------------------------------------------------------

annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgetaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
itemAnnex = MeetingFileTypeDescriptor('item-annex', 'Other annex(es)', 'attach.png', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe a la decision', 'attach.png', '', True)
# Some type of annexes taken from the default PloneMeeting test profile
marketingAnalysis = MeetingFileTypeDescriptor(
    'marketing-annex', 'Marketing annex(es)', 'attach.png', '', True,
    active=False)
overheadAnalysis = MeetingFileTypeDescriptor(
    'overhead-analysis', 'Administrative overhead analysis',
    'attach.png', '')

# Pod templates ----------------------------------------------------------------
# MeetingItem
councilDelibTemplate = PodTemplateDescriptor('conseil-deliberation', 'Délibération')
councilDelibTemplate.podTemplate = 'conseil_deliberation.odt'
councilDelibTemplate.podCondition = 'python:(here.meta_type=="MeetingItem") and ' \
                              'here.queryState() in ["accepted", "refused", "delayed", "accepted_but_modified",]'
councilProjetDelibTemplate = PodTemplateDescriptor('conseil-projet-deliberation', 'Projet délibération')
councilProjetDelibTemplate.podTemplate = 'conseil_projet_deliberation.odt'
councilProjetDelibTemplate.podCondition = 'python:(here.meta_type=="MeetingItem")'

councilNoteExplTemplate = PodTemplateDescriptor('conseil-note-explicative', 'Note explicative')
councilNoteExplTemplate.podTemplate = 'conseil_note_explicative.odt'
councilNoteExplTemplate.podCondition = 'python:(here.meta_type=="MeetingItem")'

# Meeting
councilOJExplanatoryTemplate = PodTemplateDescriptor('conseil-oj-notes-explicatives', 'OJ (notes explicatives)')
councilOJExplanatoryTemplate.podTemplate = 'conseil_oj_notes_explicatives.odt'
councilOJExplanatoryTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilFardesTemplate = PodTemplateDescriptor('conseil-fardes', 'Fardes')
councilFardesTemplate.podTemplate = 'conseil_fardes.odt'
councilFardesTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilAvisTemplate = PodTemplateDescriptor('conseil-avis', 'Avis')
councilAvisTemplate.podTemplate = 'conseil_avis_affiche_aux_valves.odt'
councilAvisTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvPresseTemplate = PodTemplateDescriptor('conseil-convocation-presse', 'Convocation presse')
councilOJConvPresseTemplate.podTemplate = 'conseil_convocation_presse.odt'
councilOJConvPresseTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvConsTemplate = PodTemplateDescriptor('conseil-convocation-conseillers', 'Convocation conseillers')
councilOJConvConsTemplate.podTemplate = 'conseil_convocation_conseillers.odt'
councilOJConvConsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvConsPremSupplTemplate = PodTemplateDescriptor('conseil-convocation-conseillers-1er-supplement', 'Convocation conseillers (1er supplément)')
councilOJConvConsPremSupplTemplate.podTemplate = 'conseil_convocation_conseillers_1er_supplement.odt'
councilOJConvConsPremSupplTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvConsDeuxSupplTemplate = PodTemplateDescriptor('conseil-convocation-conseillers-2eme-supplement', 'Convocation conseillers (2ème supplément)')
councilOJConvConsDeuxSupplTemplate.podTemplate = 'conseil_convocation_conseillers_2eme_supplement.odt'
councilOJConvConsDeuxSupplTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvCommTravTemplate = PodTemplateDescriptor('conseil-oj-commission-travaux', 'Comm. Trav.')
councilOJConvCommTravTemplate.podTemplate = 'conseil_oj_commission_travaux.odt'
councilOJConvCommTravTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvCommEnsTemplate = PodTemplateDescriptor('conseil-oj-commission-enseignement', 'Comm. Ens.')
councilOJConvCommEnsTemplate.podTemplate = 'conseil_oj_commission_enseignement.odt'
councilOJConvCommEnsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvCommLogTemplate = PodTemplateDescriptor('conseil-oj-commission-logement', 'Comm. Log.')
councilOJConvCommLogTemplate.podTemplate = 'conseil_oj_commission_logement.odt'
councilOJConvCommLogTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvCommAGTemplate = PodTemplateDescriptor('conseil-oj-commission-ag', 'Comm. AG.')
councilOJConvCommAGTemplate.podTemplate = 'conseil_oj_commission_ag.odt'
councilOJConvCommAGTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvCommAGSupplTemplate = PodTemplateDescriptor('conseil-oj-commission-ag-suppl', 'Comm. AG. (Suppl.)')
councilOJConvCommAGSupplTemplate.podTemplate = 'conseil_oj_commission_ag_supplement.odt'
councilOJConvCommAGSupplTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvCommFinTemplate = PodTemplateDescriptor('conseil-oj-commission-finances', 'Comm. Fin.')
councilOJConvCommFinTemplate.podTemplate = 'conseil_oj_commission_finances.odt'
councilOJConvCommFinTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvCommPolTemplate = PodTemplateDescriptor('conseil-oj-commission-police', 'Comm. Pol.')
councilOJConvCommPolTemplate.podTemplate = 'conseil_oj_commission_police.odt'
councilOJConvCommPolTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilOJConvCommSpecTemplate = PodTemplateDescriptor('conseil-oj-commission-speciale', 'Comm. Spec.')
councilOJConvCommSpecTemplate.podTemplate = 'conseil_oj_commission_speciale.odt'
councilOJConvCommSpecTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilPVConvCommTravTemplate = PodTemplateDescriptor('conseil-pv-commission-travaux', 'PV Comm. Trav.')
councilPVConvCommTravTemplate.podTemplate = 'conseil_pv_commission_travaux.odt'
councilPVConvCommTravTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilPVConvCommEnsTemplate = PodTemplateDescriptor('conseil-pv-commission-enseignement', 'PV Comm. Ens.')
councilPVConvCommEnsTemplate.podTemplate = 'conseil_pv_commission_enseignement.odt'
councilPVConvCommEnsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilPVConvCommLogTemplate = PodTemplateDescriptor('conseil-pv-commission-logement', 'PV Comm. Log.')
councilPVConvCommLogTemplate.podTemplate = 'conseil_pv_commission_logement.odt'
councilPVConvCommLogTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilPVConvCommAgTemplate = PodTemplateDescriptor('conseil-pv-commission-ag', 'PV Comm. AG.')
councilPVConvCommAgTemplate.podTemplate = 'conseil_pv_commission_ag.odt'
councilPVConvCommAgTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilPVConvCommFinTemplate = PodTemplateDescriptor('conseil-pv-commission-fin', 'PV Comm. Fin.')
councilPVConvCommFinTemplate.podTemplate = 'conseil_pv_commission_finances.odt'
councilPVConvCommFinTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilPVConvCommPolTemplate = PodTemplateDescriptor('conseil-pv-commission-police', 'PV Comm. Pol.')
councilPVConvCommPolTemplate.podTemplate = 'conseil_pv_commission_police.odt'
councilPVConvCommPolTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilPVConvCommSpecTemplate = PodTemplateDescriptor('conseil-pv-commission-speciale', 'PV Comm. Spec.')
councilPVConvCommSpecTemplate.podTemplate = 'conseil_pv_commission_speciale.odt'
councilPVConvCommSpecTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'
councilPVTemplate = PodTemplateDescriptor('conseil-pv', 'PV')
councilPVTemplate.podTemplate = 'conseil_pv.odt'
councilPVTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

collegeTemplates = []
councilTemplates = [councilOJExplanatoryTemplate, councilFardesTemplate, councilOJConvPresseTemplate,
                    councilOJConvConsTemplate, councilOJConvConsPremSupplTemplate,
                    councilOJConvConsDeuxSupplTemplate, councilOJConvCommTravTemplate,
                    councilOJConvCommEnsTemplate, councilOJConvCommLogTemplate,
                    councilOJConvCommAGTemplate, councilOJConvCommFinTemplate,
                    councilOJConvCommPolTemplate, councilOJConvCommSpecTemplate,
                    councilPVConvCommTravTemplate, councilPVConvCommEnsTemplate,
                    councilPVConvCommLogTemplate, councilPVConvCommAgTemplate,
                    councilPVConvCommFinTemplate, councilPVConvCommPolTemplate,
                    councilPVConvCommSpecTemplate, councilPVTemplate,
                    councilNoteExplTemplate, councilProjetDelibTemplate, councilDelibTemplate]

# Categories -------------------------------------------------------------------
categories = [
    CategoryDescriptor('deployment', 'Deployment topics'),
    CategoryDescriptor('maintenance', 'Maintenance topics'),
    CategoryDescriptor('development', 'Development topics'),
    CategoryDescriptor('events', 'Events'),
    CategoryDescriptor('research', 'Research topics'),
    CategoryDescriptor('projects', 'Projects'),
    # A vintage category
    CategoryDescriptor('marketing', 'Marketing', active=False),
    # usingGroups category
    CategoryDescriptor('subproducts', 'Subproducts wishes', usingGroups=('vendors',)),
    # first suppl categories
    CategoryDescriptor('deployment-1er-supplement', 'Deployment topics (1er supplement)'),
    CategoryDescriptor('maintenance-1er-supplement', 'Maintenance topics (1er supplement)'),
    CategoryDescriptor('development-1er-supplement', 'Development topics (1er supplement)'),
    CategoryDescriptor('events-1er-supplement', 'Events (1er supplement)'),
    CategoryDescriptor('research-1er-supplement', 'Research topics (1er supplement)'),
    CategoryDescriptor('projects-1er-supplement', 'Projects (1er supplement)'),
    CategoryDescriptor('marketing-1er-supplement', 'Marketing (1er supplement)', active=False),
    CategoryDescriptor('subproducts-1er-supplement', 'Subproducts wishes (1er supplement)', usingGroups=('vendors',)),
    # second suppl categories
    CategoryDescriptor('points-conseillers-2eme-supplement', 'Points conseillers (2eme supplement)'),
    # third suppl categories
    CategoryDescriptor('points-conseillers-3eme-supplement', 'Points conseillers (3eme supplement)'),
]

# Users and groups -------------------------------------------------------------
admin = UserDescriptor('admin', ['Manager', 'MeetingManager'])
pmManager = UserDescriptor('pmManager', ['MeetingManager'])
pmCreator1 = UserDescriptor('pmCreator1', [])
pmCreator1b = UserDescriptor('pmCreator1b', [])
pmReviewer1 = UserDescriptor('pmReviewer1', [])
pmCreator2 = UserDescriptor('pmCreator2', [])
pmReviewer2 = UserDescriptor('pmReviewer2', [])
pmAdviser1 = UserDescriptor('pmAdviser1', [])
voter1 = UserDescriptor('voter1', [], fullname='M. Voter One')
voter2 = UserDescriptor('voter2', [], fullname='M. Voter Two')
powerobserver1 = UserDescriptor('powerobserver1', [], fullname='M. Power Observer1')
# powerobserver1 is MeetingPowerObserverLocal because in the meetingPma '_powerobservers' group
plonemeeting_assembly_powerobservers = PloneGroupDescriptor('meeting-config-council_powerobservers',
                                                            'meeting-config-council_powerobservers',
                                                            [])
powerobserver1.ploneGroups = [plonemeeting_assembly_powerobservers, ]
powerobserver2 = UserDescriptor('powerobserver2', [], fullname='M. Power Observer2')

# Add a vintage group
endUsers = GroupDescriptor('endUsers', 'End users', 'EndUsers', active=False)

developers = GroupDescriptor('developers', 'Developers', 'Devel', givesMandatoryAdviceOn="python:False")
developers.creators.append(pmCreator1)
developers.creators.append(pmCreator1b)
developers.creators.append(pmManager)
developers.creators.append(admin)
developers.directors.append(pmReviewer1)
developers.directors.append(pmManager)
developers.directors.append(admin)
developers.reviewers.append(pmReviewer1)
developers.reviewers.append(pmManager)
developers.reviewers.append(admin)
developers.observers.append(pmReviewer1)
developers.observers.append(pmManager)
developers.observers.append(admin)
developers.advisers.append(pmAdviser1)
setattr(developers, 'signatures', 'developers signatures')
setattr(developers, 'echevinServices', 'developers')

#give an advice on recurring items
vendors = GroupDescriptor('vendors', 'Vendors', 'Devil', givesMandatoryAdviceOn="python: item.id == 'recurringagenda1'")
vendors.creators.append(pmCreator2)
vendors.directors.append(pmReviewer2)
vendors.reviewers.append(pmReviewer2)
vendors.observers.append(pmReviewer2)
vendors.advisers.append(pmReviewer2)
setattr(vendors, 'signatures', '')

# Do voters able to see items to vote for
developers.observers.append(voter1)
developers.observers.append(voter2)
vendors.observers.append(voter1)
vendors.observers.append(voter2)

pmManager_observer = MeetingUserDescriptor('pmManager',
                                           duty='Secretaire de la Chancellerie',
                                           usages=['assemblyMember'])
cadranel_signer = MeetingUserDescriptor('cadranel', duty='Secretaire',
                                        usages=['assemblyMember', 'signer'],
                                        signatureImage='SignatureCadranel.jpg',
                                        signatureIsDefault=True)
# Add meeting users (voting purposes)
muser_voter1 = MeetingUserDescriptor('voter1', duty='Voter1',
                                     usages=['assemblyMember', 'voter', ])
muser_voter2 = MeetingUserDescriptor('voter2', duty='Voter2',
                                     usages=['assemblyMember', 'voter', ])


# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-college', 'Collège Communal',
    'Collège communal', isDefault=True)
collegeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
collegeMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
collegeMeeting.categories = categories
collegeMeeting.shortName = 'College'
collegeMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, itemAnnex,
                                   annexeDecision, overheadAnalysis, marketingAnalysis]
collegeMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
collegeMeeting.xhtmlTransformFields = ('description', 'detailedDescription', 'decision', 'observations', 'interventions', 'commissionTranscript')
collegeMeeting.xhtmlTransformTypes = ('removeBlanks',)
collegeMeeting.itemWorkflow = 'meetingitemcollegelalouviere_workflow'
collegeMeeting.meetingWorkflow = 'meetingcollegelalouviere_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowActions'
collegeMeeting.itemTopicStates = ('itemcreated', 'proposedToServiceHead', 'proposedToOfficeManager', 'proposedToDivisionHead', 'proposedToDirector', 'validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'delayed', 'pre_accepted', 'removed',)
collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.itemAdviceStates = ('validated',)
collegeMeeting.recordItemHistoryStates = ['', ]
collegeMeeting.useGroupsAsCategories = True
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'topic_searchmyitems'
collegeMeeting.itemDocFormats = ('odt', 'pdf')
collegeMeeting.meetingDocFormats = ('odt', 'pdf')
collegeMeeting.useAdvices = True
collegeMeeting.enforceAdviceMandatoriness = False
collegeMeeting.enableAdviceInvalidation = False
collegeMeeting.useCopies = True
collegeMeeting.selectableCopyGroups = [developers.getIdSuffixed('reviewers'), vendors.getIdSuffixed('reviewers'), ]
collegeMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
collegeMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
collegeMeeting.podTemplates = collegeTemplates
collegeMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
collegeMeeting.useGroupsAsCategories = True
collegeMeeting.meetingUsers = []

collegeMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recItem1',
        description='<p>This is the first recurring item.</p>',
        title='Recurring item #1',
        proposingGroup='',
        category='developers',
        decision='First recurring item approved'),

    RecurringItemDescriptor(
        id='recItem2',
        title='Recurring item #2',
        description='<p>This is the second recurring item.</p>',
        proposingGroup='',
        category='developers',
        decision='Second recurring item approved'),
]

# Conseil communal
councilMeeting = MeetingConfigDescriptor(
    'meeting-config-council', 'Conseil Communal',
    'Conseil Communal')
councilMeeting.assembly = """M.J.GOBERT, Bourgmestre-Président
Mme A.SABBATINI, MM.J.GODIN, O.DESTREBECQ, G.HAINE,
Mmes A.DUPONT, F.GHIOT, M.J.C.WARGNIE, Echevins
Mme D.STAQUET, Présidente du CPAS
M.B.LIEBIN, Mme C.BURGEON, MM.M.DUBOIS, Y.DRUGMAND,
G.MAGGIORDOMO, O.ZRIHEN, M.DI MATTIA, Mme T.ROTOLO, M.F.ROMEO,
Mmes M.HANOT, I.VAN STEEN, MM.J.KEIJZER, A.FAGBEMI,
A.GAVA, A.POURBAIX, L.DUVAL, J.CHRISTIAENS, M.VAN HOOLAND,
Mme F.RMILI, MM.P.WATERLOT, A.BUSCEMI, L.WIMLOT,
Mme C.BOULANGIER, M.V.LIBOIS, Mme A.M.MARIN, MM.A.GOREZ,
J.P.MICHIELS, C.DELPLANCQ, Mmes F.VERMEER, L.BACCARELLA D'URSO,
M.C.LICATA et Mme M.ROLAND, Conseillers communaux
M.R.ANKAERT, Secrétaire
En présence de M.L.DEMOL, Chef de Corps, en ce qui concerne les points « Police »"""
councilMeeting.signatures = """Le Secrétaire,
R.ANKAERT
Le Président,
J.GOBERT"""
councilMeeting.categories = categories
councilMeeting.shortName = 'Council'
councilMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, itemAnnex, annexeDecision]
councilMeeting.xhtmlTransformFields = ('description', 'detailedDescription', 'decision', 'observations', 'interventions', 'commissionTranscript')
councilMeeting.xhtmlTransformTypes = ('removeBlanks',)
councilMeeting.usedItemAttributes = ['oralQuestion', 'itemInitiator', 'observations', 'privacy', 'itemAssembly', 'itemIsSigned', ]
councilMeeting.usedMeetingAttributes = ('place', 'observations', 'signatures', 'assembly', 'preMeetingDate', 'preMeetingPlace', 'preMeetingAssembly', \
                                        'preMeetingDate_2', 'preMeetingPlace_2', 'preMeetingAssembly_2', 'preMeetingDate_3', 'preMeetingPlace_3', 'preMeetingAssembly_3', \
                                        'preMeetingDate_4', 'preMeetingPlace_4', 'preMeetingAssembly_4', 'preMeetingDate_5', 'preMeetingPlace_5', 'preMeetingAssembly_5', \
                                        'preMeetingDate_6', 'preMeetingPlace_6', 'preMeetingAssembly_6', 'preMeetingDate_7', 'preMeetingPlace_7', 'preMeetingAssembly_7',
                                        'startDate', 'endDate',
)
councilMeeting.recordMeetingHistoryStates = []
councilMeeting.itemWorkflow = 'meetingitemcouncillalouviere_workflow'
councilMeeting.meetingWorkflow = 'meetingcouncillalouviere_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowActions'
#show every items states
councilMeeting.itemTopicStates = ('itemcreated', 'proposed_to_officemanager', 'validated', 'presented', 'itemfrozen', 'item_in_committee', 'item_in_council', 'returned_to_service', 'accepted', 'accepted_but_modified', 'refused', 'delayed')
councilMeeting.meetingTopicStates = ('created', 'frozen', 'in_committee')
councilMeeting.decisionTopicStates = ('in_council', 'closed')
councilMeeting.itemAdviceStates = ('validated',)
councilMeeting.recordItemHistoryStates = ['',]
councilMeeting.maxShownMeetings = 5
councilMeeting.maxDaysDecisions = 60
councilMeeting.meetingAppDefaultView = 'topic_searchmyitems'
councilMeeting.itemDocFormats = ('odt', 'pdf')
councilMeeting.meetingDocFormats = ('odt', 'pdf')
councilMeeting.useAdvices = True
councilMeeting.enforceAdviceMandatoriness = False
councilMeeting.enableAdviceInvalidation = False
councilMeeting.useCopies = True
councilMeeting.selectableCopyGroups = [developers.getIdSuffixed('reviewers'), vendors.getIdSuffixed('reviewers'), ]
councilMeeting.itemPowerObserversStates = collegeMeeting.itemPowerObserversStates
councilMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified']
councilMeeting.podTemplates = councilTemplates
councilMeeting.transitionsToConfirm = ['MeetingItem.return_to_service', ]
councilMeeting.sortingMethodOnAddItem = 'on_categories'
councilMeeting.useGroupsAsCategories = False
councilMeeting.meetingUsers = [muser_voter1, muser_voter2, ]
councilMeeting.recurringItems = []

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes seances',
    meetingConfigs=(collegeMeeting, councilMeeting),
    groups=(developers, vendors, endUsers))
data.unoEnabledPython = '/usr/bin/python'
data.usersOutsideGroups = [voter1, voter2, powerobserver1, powerobserver2]
# ------------------------------------------------------------------------------
