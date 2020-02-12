# -*- coding: utf-8 -*-
from copy import deepcopy

from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data

from Products.PloneMeeting.profiles import UserDescriptor, PloneGroupDescriptor

data = deepcopy(mc_import_data.data)

# USERS
pmServiceHead1 = UserDescriptor("pmServiceHead1", [])
pmServiceHead2 = UserDescriptor("pmServiceHead2", [])
pmOfficeManager1 = UserDescriptor("pmOfficeManager1", [])
pmOfficeManager2 = UserDescriptor("pmOfficeManager2", [])
pmDivisionHead1 = UserDescriptor("pmDivisionHead1", [])
pmDivisionHead2 = UserDescriptor("pmDivisionHead2", [])
pmDirector1 = UserDescriptor("pmDirector1", [])
pmDirector2 = UserDescriptor("pmDirector2", [])
pmCreator2 = UserDescriptor("pmCreator2", [])
pmAdviser1 = UserDescriptor("pmAdviser1", [])
pmAdviser2 = UserDescriptor("pmAdviser2", [])
voter1 = UserDescriptor("voter1", [], fullname="M. Voter One")
voter2 = UserDescriptor("voter2", [], fullname="M. Voter Two")

# Commission editors
commissioneditor = UserDescriptor(
    "commissioneditor",
    [],
    email="commissioneditor@plonemeeting.org",
    fullname="M. Commission Editor",
)
commissioneditor2 = UserDescriptor(
    "commissioneditor2",
    [],
    email="commissioneditor2@plonemeeting.org",
    fullname="M. Commission Editor 2",
)

pmAlderman = UserDescriptor(
    "pmAlderman", [], email="pmalderman@plonemeeting.org", fullname="M. PMAlderman One"
)

# Inherited users
pmReviewer1 = deepcopy(pm_import_data.pmReviewer1)
pmReviewer2 = deepcopy(pm_import_data.pmReviewer2)
pmReviewerLevel1 = deepcopy(pm_import_data.pmReviewerLevel1)
pmReviewerLevel2 = deepcopy(pm_import_data.pmReviewerLevel2)
pmManager = deepcopy(pm_import_data.pmManager)

# GROUPS
developers = data.orgs[0]
# custom groups
developers.serviceheads.append(pmReviewer1)
developers.serviceheads.append(pmServiceHead1)
developers.serviceheads.append(pmManager)
developers.officemanagers.append(pmOfficeManager1)
developers.officemanagers.append(pmReviewer1)
developers.officemanagers.append(pmManager)
developers.divisionheads.append(pmDivisionHead1)
developers.divisionheads.append(pmReviewer1)
developers.divisionheads.append(pmManager)
developers.directors.append(pmDirector1)
developers.directors.append(pmReviewer1)
developers.directors.append(pmReviewerLevel2)
developers.directors.append(pmManager)
developers.followupwriters.append(pmManager)
developers.budgetimpactreviewers.append(pmManager)
developers.alderman.append(pmManager)
developers.alderman.append(pmAlderman)
developers.commissioneditors.append(commissioneditor)
developers.commissioneditors.append(commissioneditor2)

vendors = data.orgs[1]
vendors.serviceheads.append(pmReviewer2)
vendors.serviceheads.append(pmServiceHead2)
vendors.serviceheads.append(pmManager)
vendors.officemanagers.append(pmOfficeManager2)
vendors.officemanagers.append(pmReviewer2)
vendors.officemanagers.append(pmManager)
vendors.divisionheads.append(pmDivisionHead2)
vendors.divisionheads.append(pmReviewer2)
vendors.divisionheads.append(pmManager)
vendors.directors.append(pmDirector2)
vendors.directors.append(pmReviewer2)
vendors.directors.append(pmReviewerLevel2)
vendors.directors.append(pmManager)
vendors.followupwriters.append(pmManager)
vendors.budgetimpactreviewers.append(pmManager)
vendors.alderman.append(pmManager)
vendors.alderman.append(pmAlderman)
vendors.commissioneditors.append(commissioneditor2)

# COLLEGE
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)
collegeMeeting.itemWorkflow = "meetingitemcollegelalouviere_workflow"
collegeMeeting.meetingWorkflow = "meetingcollegelalouviere_workflow"
collegeMeeting.itemConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowConditions"
)
collegeMeeting.itemActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowActions"
)
collegeMeeting.meetingConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowConditions"
)
collegeMeeting.meetingActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowActions"
)
collegeMeeting.itemDecidedStates = [
    "accepted",
    "refused",
    "delayed",
    "accepted_but_modified",
]
collegeMeeting.itemPositiveDecidedStates = ["accepted", "accepted_but_modified"]

collegeMeeting.transitionsForPresentingAnItem = (
    "proposeToServiceHead",
    "proposeToOfficeManager",
    "proposeToDivisionHead",
    "proposeToDirector",
    "validate",
    "present",
)
collegeMeeting.workflowAdaptations = []
collegeMeeting.itemAdviceStates = [
    "proposed_to_director",
]
collegeMeeting.itemAdviceEditStates = ["proposed_to_director", "validated"]

# COUNCIL
councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.itemWorkflow = "meetingitemcouncillalouviere_workflow"
councilMeeting.meetingWorkflow = "meetingcouncillalouviere_workflow"
councilMeeting.itemConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowConditions"
)
councilMeeting.itemActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowActions"
)
councilMeeting.meetingConditionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowConditions"
)
councilMeeting.meetingActionsInterface = (
    "Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowActions"
)
councilMeeting.itemDecidedStates = [
    "accepted",
    "refused",
    "delayed",
    "accepted_but_modified",
]
councilMeeting.itemPositiveDecidedStates = ["accepted", "accepted_but_modified"]

councilMeeting.transitionsForPresentingAnItem = (
    "proposeToDirector",
    "validate",
    "present",
)
councilMeeting.workflowAdaptations = []
councilMeeting.itemAdviceStates = [
    "proposed_to_director",
]
councilMeeting.itemAdviceEditStates = ["proposed_to_director", "validated"]
councilMeeting.itemCopyGroupsStates = [
    "proposed_to_director",
    "validated",
    "item_in_committee",
    "item_in_council",
]

councilMeeting.onMeetingTransitionItemActionToExecute = (
    {'meeting_transition': 'setInCommittee',
     'item_action': 'setItemInCommittee',
     'tal_expression': ''},
    {'meeting_transition': 'setInCouncil',
     'item_action': 'setItemInCouncil',
     'tal_expression': ''},
    {'meeting_transition': 'backToCreated',
     'item_action': 'backToPresented',
     'tal_expression': ''},
    {'meeting_transition': 'backToInCommittee',
     'item_action': 'backToItemInCouncil',
     'tal_expression': ''},
    {'meeting_transition': 'backToInCommittee',
     'item_action': 'backToItemInCommittee',
     'tal_expression': ''},
)

data.meetingConfigs = (collegeMeeting, councilMeeting)

# # Annex types
# overheadAnalysisSubtype = ItemAnnexSubTypeDescriptor(
#     'overhead-analysis-sub-annex',
#     'Overhead analysis sub annex',
#     other_mc_correspondences=(
#         'meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis', ))
#
# overheadAnalysis = ItemAnnexTypeDescriptor(
#     'overhead-analysis', 'Administrative overhead analysis',
#     u'overheadAnalysis.png',
#     subTypes=[overheadAnalysisSubtype],
#     other_mc_correspondences=(
#         'meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis_-_budget-analysis-sub-annex', ))
#
# financialAnalysisSubAnnex = ItemAnnexSubTypeDescriptor(
#     'financial-analysis-sub-annex',
#     'Financial analysis sub annex')
#
# financialAnalysis = ItemAnnexTypeDescriptor(
#     'financial-analysis', 'Financial analysis', u'financialAnalysis.png',
#     u'Predefined title for financial analysis', subTypes=[financialAnalysisSubAnnex])
#
# legalAnalysis = ItemAnnexTypeDescriptor(
#     'legal-analysis', 'Legal analysis', u'legalAnalysis.png')
#
# budgetAnalysisCfg2Subtype = ItemAnnexSubTypeDescriptor(
#     'budget-analysis-sub-annex',
#     'Budget analysis sub annex')
#
# budgetAnalysisCfg2 = ItemAnnexTypeDescriptor(
#     'budget-analysis', 'Budget analysis', u'budgetAnalysis.png',
#     subTypes=[budgetAnalysisCfg2Subtype])
#
# budgetAnalysisCfg1Subtype = ItemAnnexSubTypeDescriptor(
#     'budget-analysis-sub-annex',
#     'Budget analysis sub annex',
#     other_mc_correspondences=(
#         'meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis_-_budget-analysis-sub-annex', ))
#
# budgetAnalysisCfg1 = ItemAnnexTypeDescriptor(
#     'budget-analysis', 'Budget analysis', u'budgetAnalysis.png',
#     subTypes=[budgetAnalysisCfg1Subtype],
#     other_mc_correspondences=('meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis', ))
#
# itemAnnex = ItemAnnexTypeDescriptor(
#     'item-annex', 'Other annex(es)', u'itemAnnex.png')
# # Could be used once we
# # will digitally sign decisions ? Indeed, once signed, we will need to
# # store them (together with the signature) as separate files.
# decision = ItemAnnexTypeDescriptor(
#     'decision', 'Decision', u'decision.png', relatedTo='item_decision')
# decisionAnnex = ItemAnnexTypeDescriptor(
#     'decision-annex', 'Decision annex(es)', u'decisionAnnex.png', relatedTo='item_decision')
# # A vintage annex type
# marketingAnalysis = ItemAnnexTypeDescriptor(
#     'marketing-annex', 'Marketing annex(es)', u'legalAnalysis.png', relatedTo='item_decision',
#     enabled=False)
# # Advice annex types
# adviceAnnex = AnnexTypeDescriptor(
#     'advice-annex', 'Advice annex(es)', u'itemAnnex.png', relatedTo='advice')
# adviceLegalAnalysis = AnnexTypeDescriptor(
#     'advice-legal-analysis', 'Advice legal analysis', u'legalAnalysis.png', relatedTo='advice')
# # Meeting annex types
# meetingAnnex = AnnexTypeDescriptor(
#     'meeting-annex', 'Meeting annex(es)', u'itemAnnex.png', relatedTo='meeting')
#
# # Pod templates ----------------------------------------------------------------
# agendaTemplate = PodTemplateDescriptor('agendaTemplate', 'Meeting agenda')
# agendaTemplate.odt_file = 'Agenda.odt'
# agendaTemplate.pod_portal_types = ['MeetingCollege']
# agendaTemplate.tal_condition = ''
#
# decisionsTemplate = PodTemplateDescriptor('decisionsTemplate',
#                                           'Meeting decisions')
# decisionsTemplate.odt_file = 'Decisions.odt'
# decisionsTemplate.pod_portal_types = ['MeetingCollege']
# decisionsTemplate.tal_condition = 'python:here.adapted().isDecided()'
#
# itemTemplate = PodTemplateDescriptor('itemTemplate', 'Meeting item')
# itemTemplate.odt_file = 'Item.odt'
# itemTemplate.pod_portal_types = ['MeetingItemCollege']
# itemTemplate.tal_condition = ''
# # item templates
# template1 = ItemTemplateDescriptor(id='template1',
#                                    title='Tutelle CPAS',
#                                    description='<p>Tutelle CPAS</p>',
#                                    category='',
#                                    proposingGroup='developers',
#                                    templateUsingGroups=['developers', 'vendors'],
#                                    decision="""<p>Vu la loi du 8 juillet 1976 organique des centres publics d'action sociale et plus particulièrement son article 111;</p>
# <p>Vu l'Arrêté du Gouvernement Wallon du 22 avril 2004 portant codification de la législation relative aux pouvoirs locaux tel que confirmé par le décret du 27 mai 2004 du Conseil régional wallon;</p>
# <p>Attendu que les décisions suivantes du Bureau permanent/du Conseil de l'Action sociale du XXX ont été reçues le XXX dans le cadre de la tutelle générale sur les centres publics d'action sociale :</p>
# <p>- ...;</p>
# <p>- ...;</p>
# <p>- ...</p>
# <p>Attendu que ces décisions sont conformes à la loi et à l'intérêt général;</p>
# <p>Déclare à l'unanimité que :</p>
# <p><strong>Article 1er :</strong></p>
# <p>Les décisions du Bureau permanent/Conseil de l'Action sociale visées ci-dessus sont conformes à la loi et à l'intérêt général et qu'il n'y a, dès lors, pas lieu de les annuler.</p>
# <p><strong>Article 2 :</strong></p>
# <p>Copie de la présente délibération sera transmise au Bureau permanent/Conseil de l'Action sociale.</p>""")
# template2 = ItemTemplateDescriptor(id='template2',
#                                    title='Contrôle médical systématique agent contractuel',
#                                    description='<p>Contrôle médical systématique agent contractuel</p>',
#                                    category='',
#                                    proposingGroup='vendors',
#                                    templateUsingGroups=['vendors', ],
#                                    decision="""<p>Vu la loi du 26 mai 2002 instituant le droit à l’intégration sociale;</p>
# <p>Vu la délibération du Conseil communal du 29 juin 2009 concernant le cahier spécial des charges relatif au marché de services portant sur le contrôle des agents communaux absents pour raisons médicales;</p>
# <p>Vu sa délibération du 17 décembre 2009 désignant le docteur XXX en qualité d’adjudicataire pour la mission de contrôle médical des agents de l’Administration communale;</p>
# <p>Vu également sa décision du 17 décembre 2009 d’opérer les contrôles médicaux de manière systématique et pour une période d’essai d’un trimestre;</p>
# <p>Attendu qu’un certificat médical a été  reçu le XXX concernant XXX la couvrant du XXX au XXX, avec la mention « XXX »;</p>
# <p>Attendu que le Docteur XXX a transmis au service du Personnel, par fax, le même jour à XXX le rapport de contrôle mentionnant l’absence de XXX ce XXX à XXX;</p>
# <p>Considérant que XXX avait été informée par le Service du Personnel de la mise en route du système de contrôle systématique que le médecin-contrôleur;</p>
# <p>Considérant qu’ayant été absent(e) pour maladie la semaine précédente elle avait reçu la visite du médecin-contrôleur;</p>
# <p>DECIDE :</p>
# <p><strong>Article 1</strong> : De convoquer XXX devant  Monsieur le Secrétaire communal f.f. afin de lui rappeler ses obligations en la matière.</p>
# <p><strong>Article 2</strong> :  De prévenir XXX, qu’en cas de récidive, il sera proposé par le Secrétaire communal au Collège de transformer les jours de congés de maladie en absence injustifiée (retenue sur traitement avec application de la loi du 26 mai 2002 citée ci-dessus).</p>
# <p><strong>Article 3</strong> : De charger le service du personnel du suivi de ce dossier.</p>""")
#
#
# # Categories -------------------------------------------------------------------
# deployment = CategoryDescriptor('deployment', 'Deployment topics')
# maintenance = CategoryDescriptor('maintenance', 'Maintenance topics')
# development = CategoryDescriptor('development', 'Development topics')
# events = CategoryDescriptor('events', 'Events')
# research = CategoryDescriptor('research', 'Research topics')
# projects = CategoryDescriptor('projects', 'Projects')
# # A vintage category
# marketing = CategoryDescriptor('marketing', 'Marketing', active=False)
# # usingGroups category
# subproducts = CategoryDescriptor('subproducts', 'Subproducts wishes', usingGroups=('vendors',))
#
# # Classifiers
# classifier1 = CategoryDescriptor('classifier1', 'Classifier 1')
# classifier2 = CategoryDescriptor('classifier2', 'Classifier 2')
# classifier3 = CategoryDescriptor('classifier3', 'Classifier 3')
#
# # Users and groups -------------------------------------------------------------
# pmManager = UserDescriptor('pmManager', [], email="pmmanager@plonemeeting.org", fullname='M. PMManager')
# pmCreator1 = UserDescriptor('pmCreator1', [], email="pmcreator1@plonemeeting.org", fullname='M. PMCreator One')
# pmCreator1b = UserDescriptor('pmCreator1b', [], email="pmcreator1b@plonemeeting.org", fullname='M. PMCreator One bee')
# pmObserver1 = UserDescriptor('pmObserver1', [], email="pmobserver1@plonemeeting.org", fullname='M. PMObserver One')
# pmReviewer1 = UserDescriptor('pmReviewer1', [])
# pmAlderman = UserDescriptor('pmAlderman', [], email="pmalderman@plonemeeting.org", fullname='M. PMAlderman One')
# pmReviewerLevel1 = UserDescriptor('pmReviewerLevel1', [],
#                                   email="pmreviewerlevel1@plonemeeting.org", fullname='M. PMReviewer Level One')
# pmServiceHead1 = UserDescriptor('pmServiceHead1', [])
# pmOfficeManager1 = UserDescriptor('pmOfficeManager1', [])
# pmDivisionHead1 = UserDescriptor('pmDivisionHead1', [])
# pmDirector1 = UserDescriptor('pmDirector1', [])
# pmCreator2 = UserDescriptor('pmCreator2', [])
# pmReviewer2 = UserDescriptor('pmReviewer2', [])
# pmReviewerLevel2 = UserDescriptor('pmReviewerLevel2', [],
#                                   email="pmreviewerlevel2@plonemeeting.org", fullname='M. PMReviewer Level Two')
# pmDirector2 = UserDescriptor('pmDirector2', [])
# pmAdviser1 = UserDescriptor('pmAdviser1', [])
# voter1 = UserDescriptor('voter1', [], fullname='M. Voter One')
# voter2 = UserDescriptor('voter2', [], fullname='M. Voter Two')
# powerobserver1 = UserDescriptor('powerobserver1',
#                                 [],
#                                 email="powerobserver1@plonemeeting.org",
#                                 fullname='M. Power Observer1')
# # powerobserver1 is 'power observer' because in the meeting-config-college '_powerobservers' group
# college_powerobservers = PloneGroupDescriptor('meeting-config-college_powerobservers',
#                                               'meeting-config-college_powerobservers',
#                                               [])
# powerobserver1.ploneGroups = [college_powerobservers, ]
# powerobserver2 = UserDescriptor('powerobserver2',
#                                 [],
#                                 email="powerobserver2@plonemeeting.org",
#                                 fullname='M. Power Observer2')
# restrictedpowerobserver1 = UserDescriptor('restrictedpowerobserver1',
#                                           [],
#                                           email="restrictedpowerobserver1@plonemeeting.org",
#                                           fullname='M. Restricted Power Observer 1')
# college_restrictedpowerobservers = PloneGroupDescriptor('meeting-config-college_restrictedpowerobservers',
#                                                         'meeting-config-college_restrictedpowerobservers',
#                                                         [])
# restrictedpowerobserver1.ploneGroups = [college_restrictedpowerobservers, ]
# restrictedpowerobserver2 = UserDescriptor('restrictedpowerobserver2',
#                                           [],
#                                           email="restrictedpowerobserver2@plonemeeting.org",
#                                           fullname='M. Restricted Power Observer 2')
# council_restrictedpowerobservers = PloneGroupDescriptor('meeting-config-council_restrictedpowerobservers',
#                                                         'meeting-config-council_restrictedpowerobservers',
#                                                         [])
# restrictedpowerobserver2.ploneGroups = [council_restrictedpowerobservers, ]
#
# # Commission editors
# commissioneditor = UserDescriptor('commissioneditor',
#                                     [],
#                                     email="commissioneditor@plonemeeting.org",
#                                     fullname='M. Commission Editor')
#
# commission_ag_commissioneditors = PloneGroupDescriptor('commission-ag_commissioneditors',
#                                                                  'Commission ag (Rédacteurs PV)',
#                                                                  [])
# commissioneditor.ploneGroups = [commission_ag_commissioneditors]
#
# commissioneditor2 = UserDescriptor('commissioneditor2',
#                                     [],
#                                     email="commissioneditor2@plonemeeting.org",
#                                     fullname='M. Commission Editor')
#
# commission_patrimoine_commissioneditors = PloneGroupDescriptor('commission-patrimoine_commissioneditors',
#                                                                  'Commission patrimoine (Rédacteurs PV)',
#                                                                  [])
# commissioneditor2.ploneGroups = [commission_ag_commissioneditors, commission_patrimoine_commissioneditors]
#
# # Add a vintage group
# endUsers = GroupDescriptor('endUsers', 'End users', 'EndUsers', active=False)
#
# developers = GroupDescriptor('developers', 'Developers', 'Devel')
# developers.creators.append(pmCreator1)
# developers.creators.append(pmCreator1b)
# developers.creators.append(pmManager)
# developers.serviceheads.append(pmReviewer1)
# developers.serviceheads.append(pmServiceHead1)
# developers.serviceheads.append(pmManager)
# developers.officemanagers.append(pmOfficeManager1)
# developers.officemanagers.append(pmManager)
# developers.divisionheads.append(pmDivisionHead1)
# developers.divisionheads.append(pmManager)
# developers.directors.append(pmDirector1)
# developers.directors.append(pmReviewer1)
# developers.directors.append(pmReviewerLevel2)
# developers.directors.append(pmManager)
# developers.reviewers.append(pmReviewer1)
# developers.reviewers.append(pmManager)
# developers.reviewers.append(commissioneditor)
# developers.reviewers.append(commissioneditor2)
# developers.observers.append(pmObserver1)
# developers.observers.append(pmReviewer1)
# developers.observers.append(pmManager)
# developers.advisers.append(pmAdviser1)
# developers.advisers.append(pmManager)
# developers.followupwriters.append(pmManager)
# developers.budgetimpactreviewers.append(pmManager)
# developers.alderman.append(pmManager)
# developers.alderman.append(pmAlderman)
# setattr(developers, 'signatures', 'developers signatures')
# setattr(developers, 'echevinServices', 'developers')
# # put pmReviewerLevel1 in first level of reviewers from what is in MEETINGREVIEWERS
# getattr(developers, MEETINGREVIEWERS.keys()[-1]).append(pmReviewerLevel1)
# # put pmReviewerLevel2 in second level of reviewers from what is in MEETINGREVIEWERS
# getattr(developers, MEETINGREVIEWERS.keys()[0]).append(pmReviewerLevel2)
#
# # give an advice on recurring items
# vendors = GroupDescriptor('vendors', 'Vendors', 'Devil')
# vendors.creators.append(pmCreator2)
# vendors.directors.append(pmReviewer2)
# vendors.directors.append(pmDirector2)
# vendors.reviewers.append(pmReviewer2)
# vendors.reviewers.append(commissioneditor)
# vendors.reviewers.append(commissioneditor2)
# vendors.observers.append(pmReviewer2)
# vendors.advisers.append(pmReviewer2)
# vendors.advisers.append(pmManager)
# setattr(vendors, 'signatures', '')
#
# # Do voters able to see items to vote for
# developers.observers.append(voter1)
# developers.observers.append(voter2)
# vendors.observers.append(voter1)
# vendors.observers.append(voter2)
#
# # Add a vintage group
# endUsers = GroupDescriptor('endUsers', 'End users', 'EndUsers', active=False)
#
# pmManager_observer = MeetingUserDescriptor('pmManager',
#                                            duty='Secretaire de la Chancellerie',
#                                            usages=['assemblyMember'])
# cadranel_signer = MeetingUserDescriptor('cadranel', duty='Secretaire',
#                                         usages=['assemblyMember', 'signer'],
#                                         signatureImage='SignatureCadranel.jpg',
#                                         signatureIsDefault=True)
# # Add meeting users (voting purposes)
# muser_voter1 = MeetingUserDescriptor('voter1', duty='Voter1',
#                                      usages=['assemblyMember', 'voter', ])
# muser_voter2 = MeetingUserDescriptor('voter2', duty='Voter2',
#                                      usages=['assemblyMember', 'voter', ])
#
# # budget impact editors
# budgetimpacteditor = UserDescriptor('budgetimpacteditor',
#                                     [],
#                                     email="budgetimpacteditor@plonemeeting.org",
#                                     fullname='M. Budget Impact Editor')
# college_budgetimpacteditors = PloneGroupDescriptor('meeting-config-college_budgetimpacteditors',
#                                                    'meeting-config-college_budgetimpacteditors',
#                                                    [])
# budgetimpacteditor.ploneGroups = [college_budgetimpacteditors,
#                                   college_powerobservers]
#
# # Meeting configurations -------------------------------------------------------
# # college
# collegeMeeting = MeetingConfigDescriptor(
#     'meeting-config-college', 'College Communal',
#     'College communal', isDefault=True)
# collegeMeeting.meetingManagers = ['pmManager',]
# collegeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
#                           'Charles Exemple - 1er Echevin,\n' \
#                           'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
#                           'Jacqueline Exemple, Responsable du CPAS'
# collegeMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, Secrétaire communal'
# collegeMeeting.certifiedSignatures = []
# collegeMeeting.categories = [development, research]
# collegeMeeting.classifiers = [classifier1, classifier2, classifier3]
# collegeMeeting.shortName = 'College'
# collegeMeeting.annexTypes = [financialAnalysis, budgetAnalysisCfg1, overheadAnalysis,
#                              itemAnnex, decisionAnnex, marketingAnalysis,
#                              adviceAnnex, adviceLegalAnalysis, meetingAnnex]
# collegeMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned', 'observations',)
# collegeMeeting.maxShownListings = '100'
# collegeMeeting.itemWorkflow = 'meetingitemcollegelalouviere_workflow'
# collegeMeeting.meetingWorkflow = 'meetingcollegelalouviere_workflow'
# collegeMeeting.itemConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowConditions'
# collegeMeeting.itemActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowActions'
# collegeMeeting.meetingConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowConditions'
# collegeMeeting.meetingActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowActions'
# collegeMeeting.transitionsForPresentingAnItem = ['proposeToServiceHead', 'proposeToOfficeManager', 'proposeToDivisionHead',
#                                                  'proposeToDirector', 'validate', 'present', ]
# collegeMeeting.transitionsToConfirm = []
# collegeMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
#                                                               'item_transition': 'itemfreeze'},
#
#                                                              {'meeting_transition': 'decide',
#                                                               'item_transition': 'itemfreeze'},
#
#                                                              {'meeting_transition': 'publish_decisions',
#                                                               'item_transition': 'itemfreeze'},
#                                                              {'meeting_transition': 'publish_decisions',
#                                                               'item_transition': 'accept'},
#
#                                                              {'meeting_transition': 'close',
#                                                               'item_transition': 'itemfreeze'},
#                                                              {'meeting_transition': 'close',
#                                                               'item_transition': 'accept'},
#
#                                                              {'meeting_transition': 'backToCreated',
#                                                               'item_transition': 'backToPresented'},)
#
# collegeMeeting.itemTopicStates = ('itemcreated', 'proposed_to_servicehead', 'proposed_to_officemanager',
#                                   'proposed_to_divisionhead', 'proposed_to_director', 'validated',
#                                   'presented', 'itemfrozen', 'accepted', 'refused',
#                                   'delayed', 'pre_accepted', 'removed',)
# collegeMeeting.meetingTopicStates = ('created', 'frozen')
# collegeMeeting.decisionTopicStates = ('decided', 'closed')
# collegeMeeting.recordItemHistoryStates = []
# collegeMeeting.itemAdviceStates = ['proposed_to_director', ]
# collegeMeeting.itemAdviceEditStates = ['proposed_to_director', 'validated']
# collegeMeeting.itemAdviceViewStates = ['presented', ]
# collegeMeeting.recordItemHistoryStates = ['', ]
# collegeMeeting.maxShownMeetings = 5
# collegeMeeting.maxDaysDecisions = 60
# collegeMeeting.meetingAppDefaultView = 'searchallitems'
# collegeMeeting.itemDocFormats = ('odt', 'pdf')
# collegeMeeting.meetingDocFormats = ('odt', 'pdf')
# collegeMeeting.useAdvices = True
# collegeMeeting.selectableAdvisers = ['developers', 'vendors']
# collegeMeeting.itemAdviceStates = ['proposed_to_director', ]
# collegeMeeting.itemAdviceEditStates = ['proposed_to_director', 'validated']
# collegeMeeting.itemAdviceViewStates = ['presented', ]
# collegeMeeting.transitionsReinitializingDelays = ('backToItemCreated', )
# collegeMeeting.enforceAdviceMandatoriness = False
# collegeMeeting.enableAdviceInvalidation = False
# collegeMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
# collegeMeeting.useCopies = True
# collegeMeeting.selectableCopyGroups = [developers.getIdSuffixed('reviewers'), vendors.getIdSuffixed('reviewers'), ]
# collegeMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
# collegeMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified']
# collegeMeeting.workflowAdaptations = []
# collegeMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
#                                              'reverse': '0'}, )
# collegeMeeting.useGroupsAsCategories = True
# collegeMeeting.meetingUsers = []
# collegeMeeting.podTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]
# collegeMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'meeting-config-council',
#                                            'trigger_workflow_transitions_until': '__nothing__'}, ]
# collegeMeeting.itemAutoSentToOtherMCStates = ('accepted', 'accepted_but_modified', )
# collegeMeeting.recurringItems = [
#     RecurringItemDescriptor(
#         id='recItem1',
#         description='<p>This is the first recurring item.</p>',
#         title='Recurring item #1',
#         proposingGroup='developers',
#         decision='First recurring item approved'),
#
#     RecurringItemDescriptor(
#         id='recItem2',
#         title='Recurring item #2',
#         description='<p>This is the second recurring item.</p>',
#         proposingGroup='developers',
#         decision='Second recurring item approved'),
# ]
# collegeMeeting.itemTemplates = (template1, template2)
#
# # Conseil communal
# councilMeeting = MeetingConfigDescriptor(
#     'meeting-config-council', 'Conseil Communal',
#     'Conseil Communal')
# councilMeeting.meetingManagers = ['pmManager',]
# councilMeeting.assembly = """M.J.GOBERT, Bourgmestre-Président
# Mme A.SABBATINI, MM.J.GODIN, O.DESTREBECQ, G.HAINE,
# Mmes A.DUPONT, F.GHIOT, M.J.C.WARGNIE, Echevins
# Mme D.STAQUET, Présidente du CPAS
# M.B.LIEBIN, Mme C.BURGEON, MM.M.DUBOIS, Y.DRUGMAND,
# G.MAGGIORDOMO, O.ZRIHEN, M.DI MATTIA, Mme T.ROTOLO, M.F.ROMEO,
# Mmes M.HANOT, I.VAN STEEN, MM.J.KEIJZER, A.FAGBEMI,
# A.GAVA, A.POURBAIX, L.DUVAL, J.CHRISTIAENS, M.VAN HOOLAND,
# Mme F.RMILI, MM.P.WATERLOT, A.BUSCEMI, L.WIMLOT,
# Mme C.BOULANGIER, M.V.LIBOIS, Mme A.M.MARIN, MM.A.GOREZ,
# J.P.MICHIELS, C.DELPLANCQ, Mmes F.VERMEER, L.BACCARELLA D'URSO,
# M.C.LICATA et Mme M.ROLAND, Conseillers communaux
# M.R.ANKAERT, Secrétaire
# En présence de M.L.DEMOL, Chef de Corps, en ce qui concerne les points « Police »"""
# councilMeeting.signatures = """Le Secrétaire,
# R.ANKAERT
# Le Président,
# J.GOBERT"""
# councilMeeting.categories = [deployment, maintenance, development, events, research, projects, marketing, subproducts]
# councilMeeting.classifiers = [classifier1, classifier2, classifier3]
# councilMeeting.shortName = 'Council'
# councilMeeting.annexTypes = [financialAnalysis, legalAnalysis,
#                              budgetAnalysisCfg2, itemAnnex, decisionAnnex,
#                              adviceAnnex, adviceLegalAnalysis, meetingAnnex]
# councilMeeting.usedItemAttributes = ('oralQuestion', 'itemInitiator', 'observations',
#                                      'privacy', 'itemAssembly', 'itemIsSigned',
#                                      'motivation', 'observations',)
# councilMeeting.usedMeetingAttributes = (
#     'place', 'observations', 'signatures', 'assembly', 'preMeetingDate', 'preMeetingPlace', 'preMeetingAssembly',
#     'preMeetingDate_2', 'preMeetingPlace_2', 'preMeetingAssembly_2', 'preMeetingDate_3', 'preMeetingPlace_3',
#     'preMeetingAssembly_3', 'preMeetingDate_4', 'preMeetingPlace_4', 'preMeetingAssembly_4', 'preMeetingDate_5',
#     'preMeetingPlace_5', 'preMeetingAssembly_5', 'preMeetingDate_6', 'preMeetingPlace_6', 'preMeetingAssembly_6',
#     'preMeetingDate_7', 'preMeetingPlace_7', 'preMeetingAssembly_7', 'startDate', 'endDate', )
# councilMeeting.recordMeetingHistoryStates = []
# councilMeeting.itemWorkflow = 'meetingitemcouncillalouviere_workflow'
# councilMeeting.meetingWorkflow = 'meetingcouncillalouviere_workflow'
# councilMeeting.itemConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowConditions'
# councilMeeting.itemActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowActions'
# councilMeeting.meetingConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowConditions'
# councilMeeting.meetingActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowActions'
# #show every items states
# councilMeeting.itemTopicStates = ('itemcreated', 'proposed_to_director', 'validated', 'presented', 'itemfrozen',
#                                   'item_in_committee', 'item_in_council', 'returned_to_service', 'accepted',
#                                   'accepted_but_modified', 'refused', 'delayed')
# councilMeeting.meetingTopicStates = ('created', 'frozen', 'in_committee')
# councilMeeting.decisionTopicStates = ('in_council', 'closed')
# councilMeeting.itemAdviceStates = ['proposed_to_director', ]
# councilMeeting.itemAdviceEditStates = ['proposed_to_director', 'validated']
# councilMeeting.itemAdviceViewStates = ['presented', ]
# councilMeeting.transitionReinitializingDelays = 'backToItemCreated'
# councilMeeting.recordItemHistoryStates = ['', ]
# councilMeeting.maxShownMeetings = 5
# councilMeeting.maxDaysDecisions = 60
# councilMeeting.meetingAppDefaultView = 'searchallitems'
# councilMeeting.useAdvices = False
# councilMeeting.selectableAdvisers = []
# councilMeeting.transitionsReinitializingDelays = ('backToItemCreated', )
# councilMeeting.enforceAdviceMandatoriness = False
# councilMeeting.enableAdviceInvalidation = False
# councilMeeting.useCopies = True
# councilMeeting.selectableCopyGroups = [developers.getIdSuffixed('reviewers'), vendors.getIdSuffixed('reviewers'), ]
# councilMeeting.itemPowerObserversStates = collegeMeeting.itemPowerObserversStates
# councilMeeting.meetingPowerObserversStates = []
# councilMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified']
# councilMeeting.workflowAdaptations = []
# councilMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_categories',
#                                              'reverse': '0'}, )
# agendaTemplate = PodTemplateDescriptor('agendaTemplate', 'Meeting agenda')
# agendaTemplate.odt_file = 'Agenda.odt'
# agendaTemplate.pod_portal_types = ['MeetingCouncil']
# agendaTemplate.tal_condition = ''
# councilMeeting.podTemplates = [agendaTemplate]
# councilMeeting.transitionsToConfirm = []
# councilMeeting.transitionsForPresentingAnItem = ['proposeToDirector', 'validate', 'present', ]
# councilMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'setInCommittee',
#                                                               'item_transition': 'setItemInCommittee'},
#                                                              {'meeting_transition': 'backToInCommittee',
#                                                               'item_transition': 'backToItemInCommittee'},
#                                                              {'meeting_transition': 'setInCouncil',
#                                                               'item_transition': 'setItemInCommittee'},
#                                                              {'meeting_transition': 'setInCouncil',
#                                                               'item_transition': 'setItemInCouncil'},
#                                                              {'meeting_transition': 'close',
#                                                               'item_transition': 'accept'})
#
# councilMeeting.sortingMethodOnAddItem = 'on_categories'
# councilMeeting.useGroupsAsCategories = False
# councilMeeting.meetingUsers = [muser_voter1, muser_voter2, ]
# councilMeeting.recurringItems = []
# councilMeeting.itemTemplates = (template1, template2)
#
# # no recurring items for this meetingConfig, only for tests !!!
# # so we can test a meetingConfig with recurring items (college) and without (council)
#
# data = PloneMeetingConfiguration(
#     meetingFolderTitle='Mes seances',
#     meetingConfigs=(collegeMeeting, councilMeeting),
#     groups=(developers, vendors, endUsers))
# # necessary for testSetup.test_pm_ToolAttributesAreOnlySetOnFirstImportData
# data.restrictUsers = False
# data.usersOutsideGroups = [voter1, voter2, powerobserver1, powerobserver2,
#                            restrictedpowerobserver1, restrictedpowerobserver2,
#                            budgetimpacteditor, commissioneditor, commissioneditor2]
# # ------------------------------------------------------------------------------
