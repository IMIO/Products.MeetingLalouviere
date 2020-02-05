# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2016 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

import logging
import os

from Products.MeetingLalouviere.config import PROJECTNAME
from Products.PloneMeeting.exportimport.content import ToolInitializer

from dexterity.localroles.utils import add_fti_configuration

logger = logging.getLogger('MeetingLalouviere: setuphandlers')


def isNotMeetingLalouviereProfile(context):
    return context.readDataFile("MeetingLalouviere_marker.txt") is None


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotMeetingLalouviereProfile(context):
        return
    logStep("postInstall", context)
    site = context.getSite()
    # need to reinstall PloneMeeting after reinstalling MC workflows to re-apply wfAdaptations
    _reinstallPloneMeeting(context, site)
    _showHomeTab(context, site)
    _reorderSkinsLayers(context, site)


def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" %
                (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isMeetingLalouviereConfigureProfile(context):
    return context.readDataFile("MeetingLalouviere_marker.txt") or \
        context.readDataFile("MeetingLalouviere_lalouviere_marker.txt") or \
        context.readDataFile("MeetingLalouviere_bourgmestre_marker.txt") or \
        context.readDataFile("MeetingLalouviere_testing_marker.txt") or \
        context.readDataFile("MeetingLalouviere_codir_marker.txt")


def isMeetingLalouviereTestingProfile(context):
    return context.readDataFile("MeetingLalouviere_testing_marker.txt")


def isMeetingLalouviereMigrationProfile(context):
    return context.readDataFile("MeetingLalouviere_migrations_marker.txt")


def installMeetingLalouviere(context):
    if not isMeetingLalouviereConfigureProfile(context):
        return
    logStep("installMeetingLalouviere", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingLalouviere:default')


def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current profile.'''
    if not isMeetingLalouviereConfigureProfile(context):
        return

    logStep("initializeTool", context)
    # PloneMeeting is no more a dependency to avoid
    # magic between quickinstaller and portal_setup
    # so install it manually
    site = context.getSite()
    _installPloneMeeting(context, site)
    return ToolInitializer(context, PROJECTNAME).run()


def _reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context, site)


def _installPloneMeeting(context, site):
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)


def _showHomeTab(context, site):
    """Make sure the 'home' tab is shown..."""
    logStep("showHomeTab", context)

    index_html = getattr(site.portal_actions.portal_tabs, 'index_html', None)
    if index_html:
        index_html.visible = True
    else:
        logger.info("The 'Home' tab does not exist !!!")


def _reorderSkinsLayers(context, site):
    """
       Re-apply MeetingLalouviere skins.xml step as the reinstallation of
       MeetingLalouviere and PloneMeeting changes the portal_skins layers order
    """
    logStep("reorderSkinsLayers", context)
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingLalouviere:default', 'skins')


def _configureDexterityLocalRolesField():
    """Configure field meetingadvice.advice_group for meetingadvicefinances."""
    # meetingadvicefinances
    roles_config = {
        'advice_group': {
            'advice_given': {
                'advisers': {'roles': [], 'rel': ''}},
            'advicecreated': {
                u'financialprecontrollers': {'roles': [u'Editor', u'Reviewer'], 'rel': ''}},
            'proposed_to_financial_controller': {
                u'financialcontrollers': {'roles': [u'Editor', u'Reviewer'], 'rel': ''}},
            'proposed_to_financial_editor': {
                u'financialeditors': {'roles': [u'Editor', u'Reviewer'], 'rel': ''}},
            'proposed_to_financial_manager': {
                u'financialmanagers': {'roles': [u'Editor', u'Reviewer'], 'rel': ''}},
            'financial_advice_signed': {
                u'financialmanagers': {'roles': [u'Reviewer'], 'rel': ''}},
            'proposed_to_financial_reviewer': {
                u'financialreviewers': {'roles': [u'Editor', u'Reviewer'], 'rel': ''}
            }
        }
    }
    msg = add_fti_configuration(portal_type='meetingadvicefinances',
                                configuration=roles_config['advice_group'],
                                keyname='advice_group',
                                force=True)
    if msg:
        logger.warn(msg)
