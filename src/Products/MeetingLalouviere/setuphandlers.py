# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2013 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier Bastien <g.bastien@imio.be>, Stephan Geulette <s.geulette@imio.be>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('MeetingLalouviere: setuphandlers')
from Products.MeetingLalouviere.config import PROJECTNAME
from Products.MeetingLalouviere.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
from Products.PloneMeeting.utils import updateIndexes
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.config import TOPIC_TYPE, TOPIC_SEARCH_SCRIPT, TOPIC_TAL_EXPRESSION
from Products.MeetingLalouviere.config import COUNCIL_COMMISSION_IDS, \
    COUNCIL_COMMISSION_IDS_2013, COMMISSION_EDITORS_SUFFIX
##/code-section HEAD

def isNotMeetingLalouviereProfile(context):
    return context.readDataFile("MeetingLalouviere_marker.txt") is None



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotMeetingLalouviereProfile(context): return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotMeetingLalouviereProfile(context):
        return
    site = context.getSite()
    # Reinstall PloneMeeting
    reinstallPloneMeeting(context, site)
    # Add additional indexes
    addAdditionalIndexes(context, site)
    # Add groups for council commissions that will contain MeetingCommissionEditors
    addCommissionEditorGroups(context, site)
    # Add some more topics
    addSearches(context, site)
    # Set a default value for each MeetingConfig.defaultMeetingItemDecision
    setDefaultMeetingItemMotivation(context, site)
    # Set a default value for each MeetingConfig.preMeetingAssembly_default
    setDefaultPreMeetingsAssembly(context, site)
    # Add the "highlight-red" style to FCKeditor so it is useable
    adaptFCKMenuStyles(context, site)
    # Make sure the 'home' tab is shown
    showHomeTab(context, site)
    # Reinstall plonemeetingskin
    reinstallPloneMeetingSkin(context, site)



##code-section FOOT
def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" % (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isNotMeetingLalouviereLalouviereProfile(context):
    return context.readDataFile("MeetingLalouviere_lalouviere_marker.txt") is None


def installMeetingLalouviere(context):
    """ Run the default profile before bing able to run the lalouviere profile"""
    if isNotMeetingLalouviereLalouviereProfile(context):
        return

    logStep("installMeetingLalouviere", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingLalouviere:default')


def reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    if isNotMeetingLalouviereProfile(context):
        return

    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context)
    # launch skins step for MeetingLalouviere so MeetingLalouviere skin layers are before PM ones
    site.portal_setup.runImportStepFromProfile('profile-Products.MeetingLalouviere:default', 'skins')


def _installPloneMeeting(context):
    site = context.getSite()
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)


def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current
       profile.'''
    if isNotMeetingLalouviereLalouviereProfile(context):
        return

    logStep("initializeTool", context)
    _installPloneMeeting(context)
    return ToolInitializer(context, PROJECTNAME).run()


def addAdditionalIndexes(context, portal):
    '''
       Add some specific indexes used by MeetingLalouviere
    '''
    if isNotMeetingLalouviereProfile(context):
        return

    indexInfo = {
        'previous_review_state': 'FieldIndex',
        'getFollowUp': 'FieldIndex',
    }

    logStep("addAdditionalIndexes", context)
    # Create or update indexes
    updateIndexes(portal, indexInfo, logger)


def addCommissionEditorGroups(context, portal):
    '''
       Add groups for council commissions that will contain MeetingCommissionEditors
    '''
    if isNotMeetingLalouviereProfile(context):
        return

    logStep("addCommissionEditorGroups", context)
    existingPloneGroupIds = portal.portal_groups.getGroupIds()
    for commissionId in COUNCIL_COMMISSION_IDS+COUNCIL_COMMISSION_IDS_2013:
        groupId = commissionId + COMMISSION_EDITORS_SUFFIX
        if not groupId in existingPloneGroupIds:
            #add the Plone group
            groupTitle = groupId.replace('-', ' ').capitalize() + u' (RÃ©dacteurs PV)'.encode('utf-8')
            portal.portal_groups.addGroup(groupId, title=groupTitle)


def addSearches(context, portal):
    '''
       Add additional searches
    '''
    if isNotMeetingLalouviereProfile(context):
        return

    logStep("addCouncilSearches", context)
    topicsInfo = {}
    topicsInfo['meeting-config-council'] = (
    # Items in state 'proposed_to_officemanager'
    ( 'searchproposeditems',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), ('proposed_to_officemanager', ), '', 'python: not here.portal_plonemeeting.userIsAmong("officemanagers")',
    ),
    # Items in state 'proposed_to_director'
    # Used in the "todo" portlet
    ( 'searchitemstovalidate',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), ('proposed_to_director', ), '', 'python: here.portal_plonemeeting.userIsAmong("directors")',
    ),
    # Items in state 'validated'
    ( 'searchvalidateditems',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), ('validated', ), '', '',
    ),
    # Items in state 'returned_to_service
    ( 'searchreturnedtoserviceitems',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), ('returned_to_service', ), '', 'python: here.portal_plonemeeting.userIsAmong("officemanagers") or here.portal_plonemeeting.userIsAmong("creators")',
    ),
    # Items returned to secretary after corrections
    ( 'searchcorrecteditems',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), (), 'searchCorrectedItems', 'python: here.portal_plonemeeting.isManager()',
    ),
    # Items of my commissions
    ( 'searchitemsofmycommissions',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), (), 'searchItemsOfMyCommissions', 'python: here.portal_plonemeeting.userIsAmong("commissioneditors")',
    ),
    # Items of my commissions I can edit
    ( 'searchitemsofmycommissionstoedit',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), (), 'searchItemsOfMyCommissionsToEdit', 'python: here.portal_plonemeeting.userIsAmong("commissioneditors")',
    ),
    # All 'decided' items
    ( 'searchdecideditems',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), ('accepted', 'refused', 'delayed', 'accepted_but_modified'), '', '',
    ),
    )

    topicsInfo['meeting-config-college'] = (
    # Items that need a follow-up (getFollowUp == follow_up_yes)
    ( 'searchitemstofollow',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'), ('getFollowUp', 'ATSimpleStringCriterion', 'follow_up_yes'),
    ), (), '', 'python: here.portal_plonemeeting.isManager()',
    ),
    # Items that needed a follow-up that has been provided (getFollowUp == follow_up_provided)
    ( 'searchitemswithfollowupprovided',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'), ('getFollowUp', 'ATListCriterion', ['follow_up_provided', 'follow_up_provided_not_printed', ]),
    ), (), '', 'python: here.portal_plonemeeting.isManager()',
    ),
    # The follow-up dashboard showing items with follow_up_needed and items with follow_up_confirmed to print
    ( 'searchitemsfollowupdashboard',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'), ('getFollowUp', 'ATListCriterion', ['follow_up_yes', 'follow_up_provided', ]),
    ), (), '', '',
    ),
    )

    mcs = portal.portal_plonemeeting.objectValues("MeetingConfig")
    if not mcs:
        return

    #Add these searches by meeting config
    for meetingConfig in mcs:
        mcId = meetingConfig.getId()
        if not mcId in topicsInfo.keys():
            continue
        for topicId, topicCriteria, stateValues, topicSearchScript, topicTalExpr in topicsInfo[mcId]:
            #if reinstalling, we need to check if the topic does not already exist
            if hasattr(meetingConfig.topics, topicId):
                continue
            meetingConfig.topics.invokeFactory('Topic', topicId)
            topic = getattr(meetingConfig.topics, topicId)
            topic.setExcludeFromNav(True)
            topic.setTitle(topicId)
            for criterionName, criterionType, criterionValue in topicCriteria:
                criterion = topic.addCriterion(field=criterionName,
                                               criterion_type=criterionType)
                if criterionName == 'Type':
                    topic.manage_addProperty(TOPIC_TYPE, criterionValue, 'string')
                    criterionValue = '%s%s' % (criterionValue, meetingConfig.getShortName())
                    criterion.setValue([criterionValue])
                else:
                    criterion.setValue(criterionValue)

            stateCriterion = topic.addCriterion(field='review_state', criterion_type='ATListCriterion')
            stateCriterion.setValue(stateValues)
            topic.manage_addProperty(TOPIC_SEARCH_SCRIPT, topicSearchScript, 'string')
            topic.manage_addProperty(TOPIC_TAL_EXPRESSION, topicTalExpr, 'string')
            topic.setLimitNumber(True)
            topic.setItemCount(20)
            topic.setSortCriterion('created', True)
            topic.setCustomView(True)
            topic.setCustomViewFields(['Title', 'CreationDate', 'Creator', 'review_state'])
            topic.reindexObject()

    # define some parameters for 'meeting-config-council'
    mc_council = getattr(portal.portal_plonemeeting, 'meeting-config-council')
    # add some topcis to the portlet_todo
    mc_council.setToDoListTopics([
        getattr(mc_council.topics, 'searchdecideditems'),
        getattr(mc_council.topics, 'searchitemstovalidate'),
        getattr(mc_council.topics, 'searchreturnedtoserviceitems'),
        getattr(mc_council.topics, 'searchcorrecteditems'),
        getattr(mc_council.topics, 'searchitemsofmycommissionstoedit'),
        getattr(mc_council.topics, 'searchallitemstoadvice'),
        getattr(mc_council.topics, 'searchallitemsincopy'),
    ])


def setDefaultMeetingItemMotivation(context, portal):
    '''
       Define the MeetingConfig.defaultItemMotivation for 'meeting-config-college'
       and 'meeting-config-council
    '''
    if isNotMeetingLalouviereProfile(context):
        return

    logStep("setDefaultMeetingItemMotivation", context)

    data = {'meeting-config-college':"""<p>Vu l'arrÃªtÃ© du Gouvernement Wallon du 22 avril 2004 portant codification de la lÃ©gislation relative aux pouvoirs locaux; dit le code de la dÃ©mocratie locale et de la dÃ©centralisation;</p>
<p>Vu le dÃ©cret du 27 mai 2004 portant confirmation dudit arrÃªtÃ© du gouvernement Wallon du 22 avril 2004;</p>
<p>Vu la nouvelle Loi communale;</p>
<p>Vu l'article 123 de la nouvelle Loi communale;</p>
<p>Vu l'article L1123-23 du code de la DÃ©mocratie locale et de la DÃ©centralisation;</p>""",
    'meeting-config-council':"""<p>Vu, d'une part, l'arrÃªtÃ© du Gouvernement Wallon du 22 avril 2004 portant codification de la lÃ©gislation relative aux pouvoirs locaux et d'autre part, le dÃ©cret du 27 mai 2004 portant confirmation dudit arrÃªtÃ©;</p>
<p>Vu l'article 117 de la nouvelle Loi Communale;</p>
<p>Vu l'article L 1122-30 du Code de DÃ©mocratie Locale et de la DÃ©centralisation;</p>""",
}

    for mc in portal.portal_plonemeeting.objectValues("MeetingConfig"):
        defaultMeetingItemMotivation = mc.getDefaultMeetingItemMotivation()
        #only update values for 'college' and 'council' if the field is empty
        if not mc.getId() in ['meeting-config-council', 'meeting-config-college', ] \
           or defaultMeetingItemMotivation:
            continue
        mc.setDefaultMeetingItemMotivation(data[mc.getId()])


def setDefaultPreMeetingsAssembly(context, portal):
    '''
       Define a default value for each MeetingConfig.preMeetingAssembly_default
    '''
    if isNotMeetingLalouviereProfile(context): return

    logStep("setDefaultPreMeetingsAssembly", context)

    mc = getattr(portal.portal_plonemeeting, 'meeting-config-council', None)
    if not mc:
        return
    # Commission Travaux
    data = """M.P.WATERLOT, PrÃ©sident,
Mme T.ROTOLO, M.J.CHRISTIAENS, Vice-prÃ©sidents,
MM.Y.DRUGMAND, G.MAGGIORDOMO, Mme O.ZRIHEN, M.R.ROMEO,Mme M.HANOT,
M.J.KEIJZER, Mmes C.BOULANGIER, F.VERMEER, L.BACCARELLA, M.C.LICATA,
Mme M.ROLAND, Conseillers communaux"""
    mc.setPreMeetingAssembly_default(data)
    # Commission Enseignement
    data="""M.A.GAVA, PrÃ©sident,
MM.L.WIMLOT, V.LIBOIS, Vice-prÃ©sidents,
MM.M.DUBOIS, M.DI MATTIA, J.KEIJZER, A.FAGBEMI, Mme F.RMILI,
M.A.BUSCEMI, Mme A-M.MARIN, MM.A.GOREZ, J-P.MICHIELS, C.DELPLANCQ,
Mme L.BACCARELLA, Conseillers communaux"""
    mc.setPreMeetingAssembly_2_default(data)
    # Commission Cadre de vie
    data = """Mme I.VAN STEEN, PrÃ©sidente,
M.F.ROMEO, Vice-prÃ©sident,
MM.B.LIEBIN, M.DUBOIS, J.KEIJZER, A.FAGBEMI, A.GAVA, L.DUVAL,
L.WIMLOT, V.LIBOIS, J-P.MICHIELS, Mme L.BACCARELLA, M.C.LICATA,
Mme M.ROLAND, Conseillers communaux"""
    mc.setPreMeetingAssembly_3_default(data)
    # Commission AG
    data = """M.M.DI MATTIA, PrÃ©sident,
Mme C.BOULANGIER, Vice-prÃ©sidente,
M.B.LIEBIN, Mme C.BURGEON, M.G.MAGGIORDOMO, Mmes T.ROTOLO, M.HANOT,
MM.J.KEIJZER, J.CHRISTIAENS, M.VAN HOOLAND, Mme F.RMILI, MM.P.WATERLOT,
A.BUSCEMI, Mme F.VERMEER, Conseillers communaux
"""
    mc.setPreMeetingAssembly_4_default(data)
    # Commission Finances
    data = """M.J.CHRISTIAENS, PrÃ©sident,
M.M.VAN HOOLAND, Mme F.RMILI, Vice-prÃ©sident,
MM.B.LIEBIN, Y.DRUGMAND, Mme T.ROTOLO, M.F.ROMEO, Mme M.HANOT,
MM.J.KEIJZER, A.BUSCEMI, Mme C.BOULANGIER, MM.V.LIBOIS,
C.DELPLANCQ, Mme M.ROLAND, Conseillers communaux
"""
    mc.setPreMeetingAssembly_5_default(data)
    # Commission Police
    data = """M.A.FAGBEMI, PrÃ©sident,
Mme A-M.MARIN, Vice-prÃ©sidente,
Mme C.BURGEON, M.M.DI MATTIA, Mme I.VAN STEEN, MM.J.KEIJZER,
A.GAVA, L.DUVAL, P.WATERLOT, L.WIMLOT, A.GOREZ, J-P.MICHIELS
Mme L.BACCARELLA, M.C.LICATA, Conseillers communaux
    """
    mc.setPreMeetingAssembly_6_default(data)


def adaptFCKMenuStyles(context, portal):
    '''
       Add the "highlight-red" style to the FCK menu styles
    '''
    if isNotMeetingLalouviereProfile(context):
        return

    logStep("adaptFCKMenuStyles", context)

    fckeditor_properties = getattr(portal.portal_properties, 'fckeditor_properties', None)

    if fckeditor_properties:
        fck_menu_styles = fckeditor_properties.fck_menu_styles
        if not "highlight-red" in fck_menu_styles:
            # Add the style
            newStyle = """
<Style name="Mettre en Ã©vidence" element="span">
<Attribute name="class" value="highlight-red" />
</Style>"""
            fck_menu_styles = fck_menu_styles+newStyle
            fckeditor_properties.manage_changeProperties(fck_menu_styles=fck_menu_styles)


def showHomeTab(context, site):
    """
       Make sure the 'home' tab is shown...
    """
    if isNotMeetingLalouviereProfile(context):
        return

    logStep("showHomeTab", context)

    index_html = getattr(site.portal_actions.portal_tabs, 'index_html', None)
    if index_html:
        index_html.visible = True
    else:
        logger.info("The 'Home' tab does not exist !!!")


def reinstallPloneMeetingSkin(context, site):
    """
       Reinstall Products.plonemeetingskin as the reinstallation of MeetingCommunes
       change the portal_skins layers order
    """
    if isNotMeetingLalouviereProfile(context):
        return

    logStep("reinstallPloneMeetingSkin", context)
    profileId = u'profile-Products.plonemeetingskin:default'
    try:
        site.portal_setup.runAllImportStepsFromProfile(profileId)
    except KeyError:
        # if the Products.plonemeetingskin profile is not available
        # (not using plonemeetingskin or in tests?) we pass...
        pass


def onMeetingItemTransition(obj, event):
    '''Called whenever a transition has been fired on a meetingItem.
       Reindex the previous_review_state index.'''
    if not event.transition or (obj != event.object):
        return
    obj.reindexObject(idxs=['previous_review_state', ])
##/code-section FOOT
