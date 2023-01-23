# -*- coding: utf-8 -*-

from DateTime import DateTime
from plone import api
from Products.MeetingCommunes.migrations.migrate_to_4200 import Migrate_To_4200 as MCMigrate_To_4200
from Products.MeetingLalouviere.config import LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS, LLO_APPLYED_COUNCIL_WFA, \
    LLO_APPLYED_COLLEGE_WFA
from Products.MeetingLalouviere.config import LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS
import logging

logger = logging.getLogger('MeetingLalouviere')

# ids of commissions used as categories for MeetingItemCouncil
# before 2013, commission ids were :
COUNCIL_COMMISSION_IDS = (
    "commission-travaux",
    "commission-enseignement",
    "commission-cadre-de-vie-et-logement",
    "commission-ag",
    "commission-finances-et-patrimoine",
    "commission-police",
    "commission-speciale",
)
# until 2013, commission ids are :
# changes are about 'commission-enseignement', 'commission-cadre-de-vie-et-logement' and
# 'commission-finances-et-patrimoine' that are splitted in smaller commissions
COUNCIL_COMMISSION_IDS_2013 = (
    "commission-ag",
    "commission-finances",
    "commission-enseignement",
    "commission-culture",
    "commission-sport",
    "commission-sante",
    "commission-police",
    "commission-cadre-de-vie",
    "commission-patrimoine",
    "commission-travaux",
    "commission-speciale",
)
# commissions taken into account on the Meeting
# since 2013, some commissions are made of several categories...
COUNCIL_MEETING_COMMISSION_IDS_2013 = (
    "commission-travaux",
    (
        "commission-ag",
        "commission-finances",
        "commission-enseignement",
        "commission-culture",
        "commission-sport",
        "commission-sante",
    ),
    ("commission-cadre-de-vie", "commission-patrimoine",),
    "commission-police",
    "commission-speciale",
)

# commissions taken into account on the Meeting
# since 2019, travaux and finance are merge. ag and enseignement are merged
COUNCIL_MEETING_COMMISSION_IDS_2019 = (
    ("commission-travaux", "commission-finances"),
    (
        "commission-ag",
        "commission-enseignement",
        "commission-culture",
        "commission-sport",
        "commission-sante",
    ),
    ("commission-cadre-de-vie", "commission-patrimoine",),
    "commission-police",
    "commission-speciale",
)

# commissions taken into account on the Meeting
# since 2020, patrimoine is moved with travaux and finance
COUNCIL_MEETING_COMMISSION_IDS_2020 = (
    ("commission-travaux", "commission-finances", "commission-patrimoine"),
    (
        "commission-ag",
        "commission-enseignement",
        "commission-culture",
        "commission-sport",
        "commission-sante",
    ),
    "commission-cadre-de-vie",
    "commission-police",
    "commission-speciale",
)

# suffix of specific groups containing commission transcript editors
COMMISSION_EDITORS_SUFFIX = "commissioneditors"

COMMITTEE_TO_APPLY = ({'acronym': '',
  'auto_from': [],
  'default_assembly': 'Monsieur J-C WARGNIE, Pr\xc3\xa9sident,\r\nMadame L. ANCIAUX, Vice-pr\xc3\xa9sidente,\r\n'
                      'Messieurs F. ROMEO, J. CHRISTIAENS, A. FAGBEMI, Madame M. MULA, Messieurs M. PRIVITERA,\r\n'
                      'S. ARNONE, Madame L. RUSSO, Monsieur C. BAISE, Madame P. TREMERIE,\r\n'
                      'Messieurs A. HERMANT, M. PUDDU, X. PAPIER, Conseillers communaux',
  'default_attendees': [],
  'default_place': 'Salle du Conseil, 1er \xc3\xa9tage',
  'default_signatories': [],
  'default_signatures': '',
  'enabled': '1',
  'label': 'Commission Travaux/Finances/Patrimoine',
  'row_id': 'committee_2023-01-23.1146059833',
  'supplements': '2',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': 'Madame M. SPANO, Pr\xc3\xa9sidente, Monsieur A. AYCIK, Vice-pr\xc3\xa9sident, '
                      'Monsieur J-C WARGNIE, Madame D. STAQUET, Monsieur M. BURY, Madame M. MULA, '
                      'Monsieur M. DI MATTIA, Mesdames \xc3\x96. KAZANCI, L. LEONI, Monsieur M. SIASSIA-BULA, '
                      'Mesdames A. LECOCQ, L. LUMIA, Messieurs O. DESTREBECQ, O. LAMAND, Conseillers communaux',
  'default_attendees': [],
  'default_place': 'Salle du Coll\xc3\xa8ge, 2\xc3\xa8me \xc3\xa9tage',
  'default_signatories': [],
  'default_signatures': '',
  'enabled': '1',
  'label': 'Commission AG/Enseignement/Culture/Sport/Sant\xc3\xa9',
  'row_id': 'committee_2023-01-23.1146059532',
  'supplements': '2',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': 'Madame L. RUSSO, Pr\xc3\xa9sidente, Monsieur M. DI MATTIA, Vice-pr\xc3\xa9sident, '
                      'Madame O. ZRIHEN, Monsieur A. AYCIK, Mesdames M. SPANO, \xc3\x96. KAZANCI, Messieurs S. ARNONE, '
                      'J. CHRISTIAENS, M. BURY, O. DESTREBECQ, Messieurs M. SIASSIA-BULA, A. CLEMENT, Madame A. '
                      'SOMMEREYNS, Monsieur L. RESINELLI, Conseillers communaux',
  'default_attendees': [],
  'default_place': 'Salle du Conseil, 1er \xc3\xa9tage',
  'default_signatories': [],
  'default_signatures': '',
  'enabled': '1',
  'label': 'Commission Cadre de Vie',
  'row_id': 'committee_2023-01-23.1146069051',
  'supplements': '2',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': 'Monsieur A. FAGBEMI, Pr\xc3\xa9sident, Madame D. STAQUET, Vice-pr\xc3\xa9sidente, '
                      'Messieurs F. ROMEO, M. PRIVITERA, Mesdames \xc3\x96. KAZANCI, L. ANCIAUX, M. SPANO, '
                      'Messieurs J. CHRISTIAENS, M. BURY, M. BAISE, Madame P. TREMERIE, Monsieur A. CLEMENT, '
                      'Madame A. SOMMEREYNS, Monsieur M. VAN HOOLAND, Conseillers communaux',
  'default_attendees': [],
  'default_place': 'Salle du Coll\xc3\xa8ge, 2\xc3\xa8me \xc3\xa9tage',
  'default_signatories': [],
  'default_signatures': '',
  'enabled': '1',
  'label': 'Commission Police',
  'row_id': 'committee_2023-01-23.1146062191',
  'supplements': '2',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enabled': '1',
  'label': 'Commission Sp\xc3\xa9ciale',
  'row_id': 'committee_2023-01-23.1146069731',
  'supplements': '0',
  'using_groups': []})


class Migrate_To_4200(MCMigrate_To_4200):

    def _fixUsedWFs(self):
        """meetingseraing_workflow/meetingitemseraing_workflow do not exist anymore,
           we use meeting_workflow/meetingitem_workflow."""
        logger.info("Adapting 'meetingWorkflow/meetingItemWorkflow' for every MeetingConfigs...")
        for cfg in self.tool.objectValues('MeetingConfig'):
            # Force init some fields
            cfg.getItemCommitteesStates()
            cfg.getItemCommitteesViewStates()
            # remove old attrs
            delattr(cfg, 'preMeetingAssembly_default')
            delattr(cfg, 'preMeetingAssembly_2_default')
            delattr(cfg, 'preMeetingAssembly_3_default')
            delattr(cfg, 'preMeetingAssembly_4_default')
            delattr(cfg, 'preMeetingAssembly_5_default')
            delattr(cfg, 'preMeetingAssembly_6_default')
            delattr(cfg, 'preMeetingAssembly_7_default')

            cfg.setMeetingWorkflow('meeting_workflow')
            cfg.setItemWorkflow('meetingitem_workflow')
            cfg.setItemConditionsInterface(
                'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions')
            cfg.setItemActionsInterface(
                'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions')
            cfg.setMeetingConditionsInterface(
                'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions')
            cfg.setMeetingActionsInterface(
                'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions')
        # remap states and transitions
        self.updateWFStatesAndTransitions(
            query={'portal_type': ('MeetingItemCouncil',)},
            review_state_mappings={
                'item_in_committee': 'itemfrozen',
                'item_in_council': 'itempublished',
            },
            transition_mappings={
                'setItemInCommittee': 'itemfreeze',
                'setItemInCouncil': 'itempublish',
            },
            # will be done by next step in migration
            update_local_roles=False)
        self.updateWFStatesAndTransitions(
            related_to="Meeting",
            query={'portal_type': ('MeetingCouncil',)},
            review_state_mappings={
                'in_committee': 'frozen',
                'in_council': 'decided',
            },
            transition_mappings={
                'setInCommittee': 'freeze',
                'setInCouncil': 'decide',
            },
            # will be done by next step in migration
            update_local_roles=False)
        # delete old unused workflows
        wfs_to_delete = [wfId for wfId in self.wfTool.listWorkflows()
                         if any(x in wfId for x in (
                'meetingcollegelalouviere_workflow',
                'meetingcouncillalouviere_workflow',
                'meetingitemcollegelalouviere_workflow',
                'meetingitemcouncillalouviere_workflow'))]
        if wfs_to_delete:
            self.wfTool.manage_delObjects(wfs_to_delete)
        logger.info('Done.')

    def _get_wh_key(self, itemOrMeeting):
        """Get workflow_history key to use, in case there are several keys, we take the one
           having the last event."""
        keys = itemOrMeeting.workflow_history.keys()
        if len(keys) == 1:
            return keys[0]
        else:
            lastEventDate = DateTime('1950/01/01')
            keyToUse = None
            for key in keys:
                if itemOrMeeting.workflow_history[key][-1]['time'] > lastEventDate:
                    lastEventDate = itemOrMeeting.workflow_history[key][-1]['time']
                    keyToUse = key
            return keyToUse

    def _adaptWFHistoryForItemsAndMeetings(self):
        """We use PM default WFs, no more meeting(item)lalouviere_workflow..."""
        logger.info('Updating WF history items and meetings to use new WF id...')
        catalog = api.portal.get_tool('portal_catalog')
        for cfg in self.tool.objectValues('MeetingConfig'):
            # this will call especially part where we duplicate WF and apply WFAdaptations
            cfg.registerPortalTypes()
            for brain in catalog(portal_type=(cfg.getItemTypeName(), cfg.getMeetingTypeName())):
                itemOrMeeting = brain.getObject()
                itemOrMeetingWFId = self.wfTool.getWorkflowsFor(itemOrMeeting)[0].getId()
                if itemOrMeetingWFId not in itemOrMeeting.workflow_history:
                    wf_history_key = self._get_wh_key(itemOrMeeting)
                    itemOrMeeting.workflow_history[itemOrMeetingWFId] = \
                        tuple(itemOrMeeting.workflow_history[wf_history_key])
                    del itemOrMeeting.workflow_history[wf_history_key]
                    # do this so change is persisted
                    itemOrMeeting.workflow_history = itemOrMeeting.workflow_history
                else:
                    # already migrated
                    break
        logger.info('Done.')

    def _doConfigureItemWFValidationLevels(self, cfg):
        """Apply correct itemWFValidationLevels and fix WFAs."""
        cfg.setItemWFValidationLevels(cfg.getId() == 'meeting-config-council' and
                                      LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS or
                                      LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS)

        cfg.setWorkflowAdaptations(cfg.getId() == 'meeting-config-council' and
                                   LLO_APPLYED_COUNCIL_WFA or
                                   LLO_APPLYED_COLLEGE_WFA)

    def run(self,
            profile_name=u'profile-Products.MeetingLalouviere:default',
            extra_omitted=[]):
        self._fixUsedWFs()
        super(Migrate_To_4200, self).run(extra_omitted=extra_omitted)
        self._adaptWFHistoryForItemsAndMeetings()

        logger.info('Done migrating to MeetingLalouviere 4200...')


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:
       1) Change MeetingConfig workflows to use meeting_workflow/meetingitem_workflow;
       2) Call PloneMeeting migration to 4200 and 4201;
       3) In _after_reinstall hook, adapt items and meetings workflow_history
          to reflect new defined workflow done in 1);
    '''
    migrator = Migrate_To_4200(context)
    migrator.run()
    migrator.finish()
