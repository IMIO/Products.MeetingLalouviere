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

from collective.eeafaceted.dashboard.utils import addFacetedCriteria
from dexterity.localroles.utils import add_fti_configuration
from plone import api

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
    reinstallPloneMeeting(context, site)
    showHomeTab(context, site)
    reorderSkinsLayers(context, site)


def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" %
                (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isMeetingLalouviereConfigureProfile(context):
    return context.readDataFile("MeetingLalouviere_examples_fr_marker.txt") or \
        context.readDataFile("MeetingLalouviere_cpas_marker.txt") or \
        context.readDataFile("MeetingLalouviere_bourgmestre_marker.txt") or \
        context.readDataFile("MeetingLalouviere_codir_marker.txt") or \
        context.readDataFile("MeetingLalouviere_ca_marker.txt") or \
        context.readDataFile("MeetingLalouviere_coges_marker.txt") or \
        context.readDataFile("MeetingLalouviere_testing_marker.txt")


def isMeetingLalouviereTestingProfile(context):
    return context.readDataFile("MeetingLalouviere_testing_marker.txt")


def isMeetingLalouviereMigrationProfile(context):
    return context.readDataFile("MeetingLalouviere_migrations_marker.txt")


def installMeetingLalouviere(context):
    """ Run the default profile"""
    if not isMeetingLalouviereConfigureProfile(context):
        return
    logStep("installMeetingLalouviere", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingLalouviere:default')


def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current
       profile.'''
    if not isMeetingLalouviereConfigureProfile(context):
        return

    logStep("initializeTool", context)
    # PloneMeeting is no more a dependency to avoid
    # magic between quickinstaller and portal_setup
    # so install it manually
    _installPloneMeeting(context)
    return ToolInitializer(context, PROJECTNAME).run()


def reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    if isNotMeetingLalouviereProfile(context):
        return

    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context)


def _installPloneMeeting(context):
    site = context.getSite()
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)


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


def reorderSkinsLayers(context, site):
    """
       Re-apply MeetingLalouviere skins.xml step as the reinstallation of
       MeetingLalouviere and PloneMeeting changes the portal_skins layers order
    """
    if isNotMeetingLalouviereProfile(context) and not isMeetingLalouviereConfigureProfile(context):
        return

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


def _addFacetedCriteria(context, site):
    """ """
    logStep("addFacetedCriteria", context)
    tool = api.portal.get_tool('portal_plonemeeting')
    xmlpath = os.path.join(os.path.dirname(__file__),
                           'faceted_conf/meetingLalouviere_dashboard_items_widgets.xml')
    for cfg in tool.objectValues('MeetingConfig'):
        obj = cfg.searches.searches_items
        addFacetedCriteria(obj, xmlpath)


def reorderCss(context):
    """
       Make sure CSS are correctly reordered in portal_css so things
       work as expected...
    """
    if isNotMeetingLalouviereProfile(context) and \
       not isMeetingLalouviereConfigureProfile(context):
        return

    site = context.getSite()

    logStep("reorderCss", context)

    portal_css = site.portal_css
    css = ['plonemeeting.css',
           'meeting.css',
           'meetingitem.css',
           'meetingLalouviere.css',
           'imioapps.css',
           'plonemeetingskin.css',
           'imioapps_IEFixes.css',
           'ploneCustom.css']
    for resource in css:
        portal_css.moveResourceToBottom(resource)
