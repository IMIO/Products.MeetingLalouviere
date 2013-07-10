# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
from Acquisition import aq_base
from Products.PloneMeeting.profiles.migrations import Migrator
import logging
logger = logging.getLogger('MeetingLalouviere')
from Products.CMFPlone.utils import base_hasattr


# The migration class ----------------------------------------------------------
class Migrate_To_2_1_3(Migrator):
    def __init__(self, context):
        Migrator.__init__(self, context)

    def _migrateDefaultMeetingItemMotivation(self):
        '''Migrate the field MeetingConfig.DefaultMeetingItemDecision to DefaultMeetingItemMotivation.'''
        logger.info('Migrating old MeetingConfig.defaultMeetingItemDecision attribute '
                    'to MeetingConfig.defaultMeetingItemMotivation...')
        cfgs = self.portal.portal_plonemeeting.objectValues('MeetingConfig')
        for cfg in cfgs:
            if hasattr(aq_base(cfg), 'defaultMeetingItemDecision'):
                cfg.setDefaultMeetingItemMotivation(cfg.defaultMeetingItemDecision)
                delattr(cfg, 'defaultMeetingItemDecision')
            else:
                logger.info('The attribute was already migrated!')
                return
        logger.info('Done.')

    def _migrateCouncilCommissions(self):
        '''Some commissions have changed after 2013.'''
        logger.info('Adapting commissions for council...')
        cfg = getattr(self.portal.portal_plonemeeting, 'meeting-config-council')
        wft = self.portal.portal_workflow
        # add new commissions and deactivate useless ones...
        uselessCommissions = ['commission-cadre-de-vie-et-logement',
                              'commission-finances-et-patrimoine',
                              'commission-cadre-de-vie-et-logement-1er-supplement',
                              'commission-finances-et-patrimoine-1er-supplement', ]
        newCommissions = {'commission-culture': ('Commission Culture',),
                          'commission-sport': ('Commission Sport',),
                          'commission-sante': ('Commission Santé',),
                          'commission-cadre-de-vie': ('Commission Cadre de Vie',),
                          'commission-finances': ('Commission Finances',),
                          'commission-patrimoine': ('Commission Patrimoine',),
                          'commission-culture-1er-supplement': ('Commission Culture (1er supplément)', ('secretaire-communal', 'secretaire-communal-adj', 'secretariat', ),),
                          'commission-sport-1er-supplement': ('Commission Sport (1er supplément)', ('secretaire-communal', 'secretaire-communal-adj', 'secretariat', ),),
                          'commission-sante-1er-supplement': ('Commission Santé (1er supplément)', ('secretaire-communal', 'secretaire-communal-adj', 'secretariat', ),),
                          'commission-cadre-de-vie-1er-supplement': ('Commission Cadre de Vie (1er supplément)', ('secretaire-communal', 'secretaire-communal-adj', 'secretariat', ),),
                          'commission-finances-1er-supplement': ('Commission Finances (1er supplément)', ('secretaire-communal', 'secretaire-communal-adj', 'secretariat', ),),
                          'commission-patrimoine-1er-supplement': ('Commission Patrimoine (1er supplément)', ('secretaire-communal', 'secretaire-communal-adj', 'secretariat', ),),
                         }
        # deactivate useless commissions
        for uselessCommission in uselessCommissions:
            obj = getattr(cfg.categories, uselessCommission)
            if 'deactivate' in [tr['name'] for tr in wft.getTransitionsFor(obj)]:
                wft.doActionFor(obj, 'deactivate')
                obj.reindexObject()
        # add new commissions
        for newCommission in newCommissions:
            if base_hasattr(cfg.categories, newCommission):
                continue
            newCat = cfg.categories.invokeFactory('MeetingCategory',
                                                  id=newCommission,
                                                  title=newCommissions[newCommission][0])
            newCatObj = getattr(cfg.categories, newCat)
            # check if we have usingGroups to define
            if len(newCommissions[newCommission]) > 1:
                newCatObj.setUsingGroups(newCommissions[newCommission][1])
            newCatObj.reindexObject()
        # now reorder commissions
        rightOrder = ['recurrent',
                      'commission-travaux',
                      'commission-enseignement',
                      'commission-culture',
                      'commission-sport',
                      'commission-sante',
                      'commission-cadre-de-vie',
                      'commission-cadre-de-vie-et-logement',
                      'commission-ag',
                      'commission-finances-et-patrimoine',
                      'commission-finances',
                      'commission-patrimoine',
                      'commission-police',
                      'commission-speciale',
                      'commission-travaux-1er-supplement',
                      'commission-enseignement-1er-supplement',
                      'commission-culture-1er-supplement',
                      'commission-sport-1er-supplement',
                      'commission-sante-1er-supplement',
                      'commission-cadre-de-vie-1er-supplement',
                      'commission-cadre-de-vie-et-logement-1er-supplement',
                      'commission-ag-1er-supplement',
                      'commission-finances-et-patrimoine-1er-supplement',
                      'commission-finances-1er-supplement',
                      'commission-patrimoine-1er-supplement',
                      'commission-police-1er-supplement',
                      'commission-speciale-1er-supplement',
                      'points-conseillers-2eme-supplement',
                      'points-conseillers-3eme-supplement']
        rightOrder.reverse()
        for catId in rightOrder:
            cfg.categories.moveObjectsToTop(catId)
        # adapt conditions for some templates adding the fact that it is not active after 2013
        #templatesToAdapt = ['conseil-oj-commission-enseignement',
        #                    'conseil-oj-commission-logement',
        #                    'conseil-oj-commission-ag',
        #                    'conseil-oj-commission-finances',
        #                    'conseil-oj-commission-police',
        #                    'conseil-oj-commission-speciale',
        #                    'conseil-pv-commission-enseignement',
        #                    'conseil-pv-commission-logement',
        #                    'conseil-pv-commission-ag',
        #                    'conseil-pv-commission-fin',
        #                    'conseil-pv-commission-police',
        #                    'conseil-pv-commission-speciale',
        #                    ]
        #for template in templatesToAdapt:
        #    obj = getattr(cfg.podtemplates, template)
        #    # do not show these templates if the Meeting.date is >= 2013
        #    podCondition = obj.getPodCondition()
        #    if not '2013' in podCondition:
        #        obj.setPodCondition(podCondition + ' and (here.getDate().year() < 2013 and here.getDate().month() < 6)')
        #    obj.setDescription('Avant 2013')
        #    obj.reindexObject()
        # add some new templates
        from Products.PloneMeeting.profiles import PodTemplateDescriptor
        # commissions OJs
        councilOJConvCommAGFinEnsTemplate = PodTemplateDescriptor('conseil-oj-commission-ag-finances-enseignement', 'Comm. AG/Fin/Ens.')
        councilOJConvCommAGFinEnsTemplate.podTemplate = 'conseil_oj_commission_ag_fin_ens_2013.odt'
        councilOJConvCommAGFinEnsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager() and here.getDate().year() >= 2013'
        councilOJConvCommCadreViePatrimoineTemplate = PodTemplateDescriptor('conseil-oj-commission-cadre-vie-patrimoine', 'Comm. Cadre Vie/Patrimoine')
        councilOJConvCommCadreViePatrimoineTemplate.podTemplate = 'conseil_oj_commission_cadre_vie_patrimoine_2013.odt'
        councilOJConvCommCadreViePatrimoineTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager() and here.getDate().year() >= 2013'
        councilOJConvCommPoliceTemplate = PodTemplateDescriptor('conseil-oj-commission-police-2013', 'Comm. Police')
        councilOJConvCommPoliceTemplate.podTemplate = 'conseil_oj_commission_police_2013.odt'
        councilOJConvCommPoliceTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager() and here.getDate().year() >= 2013'
        councilOJConvCommSpecialeTemplate = PodTemplateDescriptor('conseil-oj-commission-speciale-2013', 'Comm. Spéciale')
        councilOJConvCommSpecialeTemplate.podTemplate = 'conseil_oj_commission_speciale_2013.odt'
        councilOJConvCommSpecialeTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager() and here.getDate().year() >= 2013'
        # commissions PVs
        councilPVConvCommAGFinEnsTemplate = PodTemplateDescriptor('conseil-pv-commission-ag-finances-enseignement', 'PV Comm. AG/Fin/Ens.')
        councilPVConvCommAGFinEnsTemplate.podTemplate = 'conseil_pv_commission_ag_fin_ens_2013.odt'
        councilPVConvCommAGFinEnsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager() and here.getDate().year() >= 2013'
        councilPVConvCommCadreViePatrimoineTemplate = PodTemplateDescriptor('conseil-pv-commission-cadre-vie-patrimoine', 'PV Comm. Cadre Vie/Patrimoine')
        councilPVConvCommCadreViePatrimoineTemplate.podTemplate = 'conseil_pv_commission_cadre_vie_patrimoine_2013.odt'
        councilPVConvCommCadreViePatrimoineTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager() and here.getDate().year() >= 2013'
        councilPVConvCommPoliceTemplate = PodTemplateDescriptor('conseil-pv-commission-police-2013', 'PV Comm. Police')
        councilPVConvCommPoliceTemplate.podTemplate = 'conseil_pv_commission_police_2013.odt'
        councilPVConvCommPoliceTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager() and here.getDate().year() >= 2013'
        councilPVConvCommSpecialeTemplate = PodTemplateDescriptor('conseil-pv-commission-speciale-2013', 'PV Comm. Spéciale')
        councilPVConvCommSpecialeTemplate.podTemplate = 'conseil_pv_commission_speciale_2013.odt'
        councilPVConvCommSpecialeTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager() and here.getDate().year() >= 2013'

        from Products.MeetingLalouviere.profiles import lalouviere
        from Products.CMFCore.exceptions import BadRequest
        source = lalouviere.__path__[0]
        try:
            cfg.addPodTemplate(councilOJConvCommAGFinEnsTemplate, source)
        except BadRequest:
            pass
        try:
            cfg.addPodTemplate(councilOJConvCommCadreViePatrimoineTemplate, source)
        except BadRequest:
            pass
        try:
            cfg.addPodTemplate(councilOJConvCommPoliceTemplate, source)
        except BadRequest:
            pass
        try:
            cfg.addPodTemplate(councilOJConvCommSpecialeTemplate, source)
        except BadRequest:
            pass
        try:
            cfg.addPodTemplate(councilPVConvCommAGFinEnsTemplate, source)
        except BadRequest:
            pass
        try:
            cfg.addPodTemplate(councilPVConvCommCadreViePatrimoineTemplate, source)
        except BadRequest:
            pass
        try:
            cfg.addPodTemplate(councilPVConvCommPoliceTemplate, source)
        except BadRequest:
            pass
        try:
            cfg.addPodTemplate(councilPVConvCommSpecialeTemplate, source)
        except BadRequest:
            pass
        # now reorder templates
        rightOrder = ['conseil-avis',
                      'conseil-oj-notes-explicatives',
                      'conseil-fardes',
                      'conseil-convocation-presse',
                      'conseil-convocation-conseillers',
                      'conseil-oj-commission-travaux',
                      'conseil-oj-commission-enseignement',
                      'conseil-oj-commission-logement',
                      'conseil-oj-commission-ag',
                      'conseil-oj-commission-finances',
                      'conseil-oj-commission-police',
                      'conseil-oj-commission-speciale',

                      'conseil-oj-commission-ag-finances-enseignement',
                      'conseil-oj-commission-cadre-vie-patrimoine',
                      'conseil-oj-commission-police-2013',
                      'conseil-oj-commission-speciale-2013',

                      'conseil-pv-commission-travaux',
                      'conseil-pv-commission-enseignement',
                      'conseil-pv-commission-logement',
                      'conseil-pv-commission-ag',
                      'conseil-pv-commission-fin',
                      'conseil-pv-commission-police',
                      'conseil-pv-commission-speciale',

                      'conseil-pv-commission-ag-finances-enseignement',
                      'conseil-pv-commission-cadre-vie-patrimoine',
                      'conseil-pv-commission-police-2013',
                      'conseil-pv-commission-speciale-2013',

                      'conseil-convocation-conseillers-1er-supplement',
                      'conseil-convocation-conseillers-2eme-supplement',
                      'conseil-convocation-conseillers-3eme-supplement',
                      'conseil-pv'
                      ]
        rightOrder.reverse()
        for templateId in rightOrder:
            cfg.podtemplates.moveObjectsToTop(templateId)
        logger.info('Done.')

    def _addFollowUpWriterGroups(self):
        '''Adds, for every existing MeetingGroup, the new Plone group for
           follow-up writers.'''
        logger.info('Adding new Plone groups for follow-up writers...')
        groups = self.portal.acl_users.source_groups
        for meetingGroup in self.tool.objectValues('MeetingGroup'):
            ploneGroupId = meetingGroup.getPloneGroupId('followupwriters')
            if ploneGroupId not in groups.listGroupIds():
                meetingGroup._createPloneGroup('followupwriters')
        logger.info('Done.')

    def _updateEveryItemsLocalRoles(self):
        '''Update local roles so new role 'MeetingFollowUpWriter' is taken into account.'''
        brains = self.portal.portal_catalog(meta_type='MeetingItem')
        logger.info('Updating local roles for every items: updating %s '
                    'MeetingItem objects...' % len(brains))
        for brain in brains:
            item = brain.getObject()
            item.updateLocalRoles()
        logger.info('Done.')

    def _initItemMotivation(self):
        '''MeetingItem.Motivation has a default value that must not be used for old items
           because the motivation was defined in the MeetingItem.decision field.'''
        brains = self.portal.portal_catalog(meta_type='MeetingItem')
        logger.info('Initializing "motivation" for every items: updating %s '
                    'MeetingItem objects...' % len(brains))
        for brain in brains:
            item = brain.getObject()
            item.setMotivation('')
        logger.info('Done.')

    def run(self, refreshCatalogs=False, refreshWorkflows=False):
        logger.info('Migrating to MeetingLalouviere 2.1.3...')
        #self._migrateDefaultMeetingItemMotivation()
        self._migrateCouncilCommissions()
        #self._addFollowUpWriterGroups()
        #self._updateEveryItemsLocalRoles()
        #remove this or at least comment!!!
        #self._initItemMotivation()
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Migrate the field MeetingConfig.DefaultMeetingItemDecision to DefaultMeetingItemMotivation.
    '''
    if context.readDataFile("MeetingLalouviere_migrations_marker.txt") is None:
        return
    Migrate_To_2_1_3(context).run()
# ------------------------------------------------------------------------------
