# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import GroupDescriptor
from Products.PloneMeeting.profiles import ItemAnnexSubTypeDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import MeetingUserDescriptor
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
# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('agendaTemplate', 'Meeting agenda')
agendaTemplate.odt_file = 'Agenda.odt'
agendaTemplate.pod_portal_types = ['MeetingCollege']
agendaTemplate.tal_condition = ''

decisionsTemplate = PodTemplateDescriptor('decisionsTemplate',
                                          'Meeting decisions')
decisionsTemplate.odt_file = 'Decisions.odt'
decisionsTemplate.pod_portal_types = ['MeetingCollege']
decisionsTemplate.tal_condition = 'python:here.adapted().isDecided()'

itemTemplate = PodTemplateDescriptor('itemTemplate', 'Meeting item')
itemTemplate.odt_file = 'Item.odt'
itemTemplate.pod_portal_types = ['MeetingItemCollege']
itemTemplate.tal_condition = ''

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

jgobert_mu = MeetingUserDescriptor('jgobert', duty='Bourgmestre', usages=['asker', ], active=False)
asabbatini_mu = MeetingUserDescriptor('asabbatini', gender='f', duty='1er Echevin', usages=['asker', ], active=False)
jgodin_mu = MeetingUserDescriptor('jgodin', gender='m', duty='2ème Echevin', usages=['asker', ], active=False)
odestrebecq_mu = MeetingUserDescriptor('odestrebecq', duty='3ème Echevin', usages=['asker', ], active=False)
ghaine_mu = MeetingUserDescriptor('ghaine', duty='4ème Echevin', usages=['asker', ], active=False)
adupont_mu = MeetingUserDescriptor('adupont', gender='f', duty='5ème Echevin', usages=['asker', ], active=False)
fghiot_mu = MeetingUserDescriptor('fghiot', gender='f', duty='6ème Echevin', usages=['asker', ], active=False)
jcwargnie_mu = MeetingUserDescriptor('jcwargnie', duty='7ème Echevin', usages=['asker', ], active=False)
dstaquet_mu = MeetingUserDescriptor('dstaquet', gender='f', duty='Présidente du CPAS', usages=['asker', ])
bliebin_mu = MeetingUserDescriptor('bliebin', duty='Conseiller communal', usages=['asker', ])
cburgeon_mu = MeetingUserDescriptor('cburgeon', gender='f', duty='Conseillère communale', usages=['asker', ])
mdubois_mu = MeetingUserDescriptor('mdubois', duty='Conseiller communal', usages=['asker', ])
ydrugmand_mu = MeetingUserDescriptor('ydrugmand', duty='Conseiller communal', usages=['asker', ])
gmaggiordomo_mu = MeetingUserDescriptor('gmaggiordomo', duty='Conseiller communal', usages=['asker', ])
ozrihen_mu = MeetingUserDescriptor('ozrihen', gender='f', duty='Conseillère communale', usages=['asker', ])
mdimattia_mu = MeetingUserDescriptor('mdimattia', duty='Conseiller communal', usages=['asker', ])
trotolo_mu = MeetingUserDescriptor('trotolo', gender='f', duty='Conseillère communale', usages=['asker', ])
fromeo_mu = MeetingUserDescriptor('fromeo', duty='Conseiller communal', usages=['asker', ])
mhanot_mu = MeetingUserDescriptor('mhanot', gender='f', duty='Conseillère communale', usages=['asker', ])
ivansteen_mu = MeetingUserDescriptor('ivansteen', gender='f', duty='Conseillère communale', usages=['asker', ])
jkeijzer_mu = MeetingUserDescriptor('jkeijzer', duty='Conseiller communal', usages=['asker', ])
afagbemi_mu = MeetingUserDescriptor('afagbemi', duty='Conseiller communal', usages=['asker', ])
agava_mu = MeetingUserDescriptor('agava', duty='Conseiller communal', usages=['asker', ])
apourbaix_mu = MeetingUserDescriptor('apourbaix', duty='Conseiller communal', usages=['asker', ])
lduval_mu = MeetingUserDescriptor('lduval', duty='Conseiller communal', usages=['asker', ])
jchristiaens_mu = MeetingUserDescriptor('jchristiaens', duty='Conseiller communal', usages=['asker', ])
mvanhooland_mu = MeetingUserDescriptor('mvanhooland', duty='Conseiller communal', usages=['asker', ])
frmili_mu = MeetingUserDescriptor('frmili', gender='f', duty='Conseillère communale', usages=['asker', ])
pwaterlot_mu = MeetingUserDescriptor('pwaterlot', duty='Conseiller communal', usages=['asker', ])
abuscemi_mu = MeetingUserDescriptor('abuscemi', duty='Conseiller communal', usages=['asker', ])
lwimlot_mu = MeetingUserDescriptor('lwimlot', duty='Conseiller communal', usages=['asker', ])
cboulangier_mu = MeetingUserDescriptor('cboulangier', gender='f', duty='Conseillère communale', usages=['asker', ])
vlibois_mu = MeetingUserDescriptor('vlibois', duty='Conseiller communal', usages=['asker', ])
ammarin_mu = MeetingUserDescriptor('ammarin', gender='f', duty='Conseillère communale', usages=['asker', ])
agorez_mu = MeetingUserDescriptor('agorez', duty='Conseiller communal', usages=['asker', ])
jpmichiels_mu = MeetingUserDescriptor('jpmichiels', duty='Conseiller communal', usages=['asker', ])
cdelplancq_mu = MeetingUserDescriptor('cdelplancq', duty='Conseiller communal', usages=['asker', ])
fvermeer_mu = MeetingUserDescriptor('fvermeer', gender='f', duty='Conseillère communale', usages=['asker', ])
lbaccareladurso_mu = MeetingUserDescriptor('lbaccareladurso', gender='f',
                                           duty='Conseillère communale', usages=['asker', ])
clicata_mu = MeetingUserDescriptor('clicata', duty='Conseiller communal', usages=['asker', ])
mroland_mu = MeetingUserDescriptor('mroland', gender='f', duty='Conseillère communale', usages=['asker', ])
collegecommunal_mu = MeetingUserDescriptor('collegecommunal', gender='', duty='', usages=['asker', ])
groupeps_mu = MeetingUserDescriptor('groupeps', gender='', duty='', usages=['asker', ])
groupemr_mu = MeetingUserDescriptor('groupemr', gender='', duty='', usages=['asker', ])
groupecdh_mu = MeetingUserDescriptor('groupecdh', gender='', duty='', usages=['asker', ])
groupeecolo_mu = MeetingUserDescriptor('groupeecolo', gender='', duty='', usages=['asker', ])
groupeptb_mu = MeetingUserDescriptor('groupeptb', gender='', duty='', usages=['asker', ])
groupefn_mu = MeetingUserDescriptor('groupefn', gender='', duty='', usages=['asker', ])
groupeindependant_mu = MeetingUserDescriptor('groupeindependant', gender='', duty='', usages=['asker', ])

groups = [GroupDescriptor('dirgen', 'Directeur Général', 'DG'),
          GroupDescriptor('secretariat', 'Secretariat communal', 'Secr',
                          asCopyGroupOn="python: item.getProposingGroup()=='informatique' and ['reviewers',] or []"),
          GroupDescriptor('informatique', 'Service informatique', 'Info'),
          GroupDescriptor('personnel', 'Service du personnel', 'Pers'),
          GroupDescriptor('dirfin', 'Directeur Financier', 'DF'),
          GroupDescriptor('comptabilite', 'Service comptabilité', 'Compt'),
          GroupDescriptor('travaux', 'Service travaux', 'Trav'),
          GroupDescriptor('conseillers', 'Conseillers', 'Conseillers'),
          GroupDescriptor('secretaire-communal', 'Secrétaire communal', 'SecrComm'),
          GroupDescriptor('secretaire-communal-adj', 'Secrétaire communal ADJ', 'SecrCommAdj')]

# MeetingManager
groups[0].creators.append(secretaire)
groups[0].officemanagers.append(secretaire)
groups[0].observers.append(secretaire)
groups[0].advisers.append(secretaire)
groups[0].creators.append(dgen)
groups[0].officemanagers.append(dgen)
groups[0].observers.append(dgen)
groups[0].advisers.append(dgen)

groups[1].creators.append(agentInfo)
groups[1].creators.append(secretaire)
groups[1].creators.append(dgen)
groups[1].officemanagers.append(agentInfo)
groups[1].officemanagers.append(secretaire)
groups[1].officemanagers.append(dgen)
groups[1].observers.append(agentInfo)
groups[1].advisers.append(agentInfo)

groups[2].creators.append(agentPers)
groups[2].observers.append(agentPers)
groups[2].creators.append(secretaire)
groups[2].officemanagers.append(secretaire)
groups[2].creators.append(dgen)
groups[2].officemanagers.append(dgen)
groups[2].creators.append(chefPers)
groups[2].officemanagers.append(chefPers)
groups[2].observers.append(chefPers)
groups[2].observers.append(echevinPers)
groups[2].advisers.append(emetteuravisPers)

groups[3].creators.append(agentCompta)
groups[3].creators.append(chefCompta)
groups[3].creators.append(chefBureauCompta)
groups[3].creators.append(secretaire)
groups[3].creators.append(dgen)
groups[3].serviceheads.append(chefCompta)
groups[3].officemanagers.append(chefBureauCompta)
groups[3].officemanagers.append(secretaire)
groups[3].officemanagers.append(dgen)
groups[3].observers.append(agentCompta)
groups[3].advisers.append(chefCompta)
groups[3].advisers.append(chefBureauCompta)

groups[4].creators.append(agentTrav)
groups[4].creators.append(secretaire)
groups[4].creators.append(dgen)
groups[4].reviewers.append(agentTrav)
groups[4].reviewers.append(secretaire)
groups[4].reviewers.append(dgen)
groups[4].observers.append(agentTrav)
groups[4].advisers.append(agentTrav)

groups[5].observers.append(jgobert)
groups[5].observers.append(asabbatini)
groups[5].observers.append(jgodin)
groups[5].observers.append(odestrebecq)
groups[5].observers.append(ghaine)
groups[5].observers.append(adupont)
groups[5].observers.append(fghiot)
groups[5].observers.append(jcwargnie)
groups[5].observers.append(dstaquet)
groups[5].observers.append(bliebin)
groups[5].observers.append(cburgeon)
groups[5].observers.append(mdubois)
groups[5].observers.append(ydrugmand)
groups[5].observers.append(gmaggiordomo)
groups[5].observers.append(ozrihen)
groups[5].observers.append(mdimattia)
groups[5].observers.append(trotolo)
groups[5].observers.append(fromeo)
groups[5].observers.append(mhanot)
groups[5].observers.append(ivansteen)
groups[5].observers.append(jkeijzer)
groups[5].observers.append(afagbemi)
groups[5].observers.append(agava)
groups[5].observers.append(apourbaix)
groups[5].observers.append(lduval)
groups[5].observers.append(jchristiaens)
groups[5].observers.append(mvanhooland)
groups[5].observers.append(frmili)
groups[5].observers.append(pwaterlot)
groups[5].observers.append(abuscemi)
groups[5].observers.append(lwimlot)
groups[5].observers.append(cboulangier)
groups[5].observers.append(vlibois)
groups[5].observers.append(ammarin)
groups[5].observers.append(agorez)
groups[5].observers.append(jpmichiels)
groups[5].observers.append(cdelplancq)
groups[5].observers.append(fvermeer)
groups[5].observers.append(lbaccareladurso)
groups[5].observers.append(clicata)
groups[5].observers.append(mroland)
groups[5].observers.append(collegecommunal)
groups[5].observers.append(groupeps)
groups[5].observers.append(groupemr)
groups[5].observers.append(groupecdh)
groups[5].observers.append(groupeecolo)
groups[5].observers.append(groupeptb)
groups[5].observers.append(groupefn)
groups[5].observers.append(groupeindependant)

# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-college', 'Collège Communal',
    'Collège communal', isDefault=True)
collegeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
collegeMeeting.meetingManagers = ['dgen', ]
collegeMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
collegeMeeting.categories = []
collegeMeeting.shortName = 'College'
collegeMeeting.annexTypes = [financialAnalysis, budgetAnalysisCfg1, overheadAnalysis,
                             itemAnnex, decisionAnnex, marketingAnalysis,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
collegeMeeting.usedItemAttributes = ['budgetInfos', 'observations', 'toDiscuss',
                                     'motivation', 'neededFollowUp', 'providedFollowUp', ]
collegeMeeting.xhtmlTransformFields = ('MeetingItem.description', 'MeetingItem.detailedDescription',
                                       'MeetingItem.decision', 'MeetingItem.observations',
                                       'MeetingItem.interventions', 'MeetingItem.commissionTranscript')
collegeMeeting.xhtmlTransformTypes = ('removeBlanks',)
collegeMeeting.itemWorkflow = 'meetingitemcollegelalouviere_workflow'
collegeMeeting.meetingWorkflow = 'meetingcollegelalouviere_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCollegeLalouviereWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCollegeLalouviereWorkflowActions'
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
collegeMeeting.itemAdviceStates = ('validated',)
collegeMeeting.itemAdviceEditStates = ('validated',)
collegeMeeting.recordItemHistoryStates = ['']
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'searchallitems'
collegeMeeting.useAdvices = True
collegeMeeting.selectableAdvisers = []
collegeMeeting.enforceAdviceMandatoriness = False
collegeMeeting.enableAdviceInvalidation = False
collegeMeeting.useCopies = True
collegeMeeting.selectableCopyGroups = []
collegeMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
collegeMeeting.meetingPowerObserversStates = []
collegeMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'meeting-config-council',
                                           'trigger_workflow_transitions_until': '__nothing__'}, ]
collegeMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
collegeMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                             'reverse': '0'}, )
collegeMeeting.useGroupsAsCategories = True
collegeMeeting.budgetDefault = """<table border="1" cellpadding="1" cellspacing="1" style="width: 468px; height: 174px;">
    <tbody>
        <tr>
            <td>
                DEPENSES</td>
            <td>
                &nbsp;</td>
        </tr>
        <tr>
            <td>
                Prévu au budget</td>
            <td>
                &nbsp;OUI - NON</td>
        </tr>
        <tr>
            <td>
                A prévoir en modification budgétaire</td>
            <td>
                &nbsp;OUI - NON</td>
        </tr>
        <tr>
            <td>
                Article budgétaire</td>
            <td>
                &nbsp;</td>
        </tr>
        <tr>
            <td>
                Crédit inscrit (ou à inscrire) au budget</td>
            <td>
                &nbsp;</td>
        </tr>
        <tr>
            <td>
                Crédit disponible à la date du</td>
            <td>
                &nbsp;</td>
        </tr>
        <tr>
            <td>
                Estimation de la dépense totale, TVA comprise</td>
            <td>
                &nbsp;</td>
        </tr>
    </tbody>
</table>
"""
collegeMeeting.defaultMeetingItemMotivation = """<p>Vu l'arrêté du Gouvernement Wallon du 22 avril 2004 portant
codification de la législation relative aux pouvoirs locaux; dit le code de la démocratie locale et de la
décentralisation;</p>
<p>Vu le décret du 27 mai 2004 portant confirmation dudit arrêté du gouvernement Wallon du 22 avril 2004;</p>
<p>Vu la nouvelle Loi communale;</p> <p>Vu l'article 123 de la nouvelle Loi communale;</p>
<p>Vu l'article L1123-23 du code de la Démocratie locale et de la Décentralisation;</p>"""
collegeMeeting.recurringItems = []
collegeMeeting.meetingUsers = []
collegeMeeting.podTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Conseil communal
# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('recurrent', 'Point récurrent',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-travaux', 'Commission Travaux'),
              CategoryDescriptor('commission-enseignement',
                                 'Commission Enseignement/Culture/Sport/Santé'),
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
              CategoryDescriptor('commission-enseignement-culture-sport-sante-1er-supplement',
                                 'Commission Enseignement/Culture/Sport/Santé (1er supplément)',
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

councilMeeting = MeetingConfigDescriptor(
    'meeting-config-council', 'Conseil Communal',
    'Conseil Communal')
councilMeeting.meetingManagers = ['dgen']
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
councilMeeting.annexTypes = [financialAnalysis, legalAnalysis,
                             budgetAnalysisCfg2, itemAnnex, decisionAnnex,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
councilMeeting.xhtmlTransformFields = ('MeetingItem.description', 'MeetingItem.detailedDescription',
                                       'MeetingItem.decision', 'MeetingItem.observations',
                                       'MeetingItem.interventions', 'MeetingItem.commissionTranscript')
councilMeeting.xhtmlTransformTypes = ('removeBlanks',)
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
councilMeeting.recordMeetingHistoryStates = []
councilMeeting.workflowAdaptations = ['return_to_proposing_group', ]
councilMeeting.itemWorkflow = 'meetingitemcouncillalouviere_workflow'
councilMeeting.meetingWorkflow = 'meetingcouncillalouviere_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingItemCouncilLalouviereWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingLalouviere.interfaces.IMeetingCouncilLalouviereWorkflowActions'
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
councilMeeting.itemAdviceStates = ('itemcreated',)
councilMeeting.itemAdviceEditStates = ('itemcreated',)
councilMeeting.recordItemHistoryStates = ['']
councilMeeting.maxShownMeetings = 5
councilMeeting.maxDaysDecisions = 60
councilMeeting.meetingAppDefaultView = 'searchallitems'
councilMeeting.useAdvices = True
councilMeeting.selectableAdvisers = []
councilMeeting.enforceAdviceMandatoriness = False
councilMeeting.enableAdviceInvalidation = False
councilMeeting.useCopies = True
councilMeeting.selectableCopyGroups = []
councilMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
councilMeeting.meetingPowerObserversStates = []
councilMeeting.transitionsToConfirm = []
councilMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                             'reverse': '0'}, )
councilMeeting.useGroupsAsCategories = False
councilMeeting.defaultMeetingItemMotivation = """<p>Le Conseil,</p>
<p>&nbsp;</p>
<p>Vu, d'une part, l'arrêté du Gouvernement  Wallon du 22 avril 2004 portant codification de la législation relative aux
pouvoirs locaux et d'autre part, le décret du 27 mai 2004 portant  confirmation dudit arrêté;</p>
<p>&nbsp;</p>
<p>Vu l'article 117 de la nouvelle Loi Communale;</p>
<p>&nbsp;</p>
<p>Vu l'article L 1122-30 du Code de Démocratie Locale et de la Décentralisation;</p>"""
councilMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurrent-approuve-pv',
        title='Approbation du procès-verbal du Conseil communal du ...',
        description='',
        category='recurrent',
        proposingGroup='secretariat',
        decision='',
        meetingTransitionInsertingMe='setInCouncil'),
    RecurringItemDescriptor(
        id='recurrent-questions-actualite',
        title='Questions d\'actualités',
        description='',
        category='recurrent',
        proposingGroup='secretariat',
        decision='',
        meetingTransitionInsertingMe='setInCouncil'),
]
councilMeeting.meetingUsers = [jgobert_mu, asabbatini_mu, jgodin_mu, odestrebecq_mu, ghaine_mu,
                               adupont_mu, fghiot_mu, jcwargnie_mu, dstaquet_mu, bliebin_mu, cburgeon_mu,
                               mdubois_mu, ydrugmand_mu, gmaggiordomo_mu, ozrihen_mu, mdimattia_mu, trotolo_mu,
                               fromeo_mu, mhanot_mu, ivansteen_mu, jkeijzer_mu, afagbemi_mu, agava_mu,
                               apourbaix_mu, lduval_mu, jchristiaens_mu, mvanhooland_mu, frmili_mu, pwaterlot_mu,
                               abuscemi_mu, lwimlot_mu, cboulangier_mu, vlibois_mu, ammarin_mu, agorez_mu,
                               jpmichiels_mu, cdelplancq_mu, fvermeer_mu, lbaccareladurso_mu, clicata_mu, mroland_mu,
                               collegecommunal_mu, groupeps_mu, groupemr_mu, groupecdh_mu, groupeecolo_mu,
                               groupeptb_mu, groupefn_mu, groupeindependant_mu, ]
councilMeeting.podTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(collegeMeeting, councilMeeting),
                                 groups=groups)
# ------------------------------------------------------------------------------
