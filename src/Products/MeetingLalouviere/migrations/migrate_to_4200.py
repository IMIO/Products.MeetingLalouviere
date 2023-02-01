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

COMMITTEES_TO_APPLY = (
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '1',
  'enabled': '1',
  'label': 'Travaux/Finances/Patrimoine',
  'row_id': 'committee_2020-01-01.2501162132',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '1',
  'enabled': '1',
  'label': 'AG/Enseignement/Culture/Sport/Sant\xc3\xa9',
  'row_id': 'committee_2019-01-01.2501153343',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '1',
  'enabled': '1',
  'label': 'Cadre de Vie',
  'row_id': 'committee_2013-01-01.2501163335',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '1',
  'enabled': '1',
  'label': 'Police',
  'row_id': 'committee_2012-01-01.9920407131',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '1',
  'enabled': '1',
  'label': 'Sp\xc3\xa9ciale',
  'row_id': 'committee_2012-01-01.5810485069',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '0',
  'enabled': '0',
  'label': 'Travaux',
  'row_id': 'committee_old_2012.5267121837',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '0',
  'enabled': '0',
  'label': 'Enseignement',
  'row_id': 'committee_old_2012.5810478389',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '0',
  'enabled': '0',
  'label': 'Cadre de Vie et Logement',
  'row_id': 'committee_old_2012.5810479936',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '0',
  'enabled': '0',
  'label': 'AG',
  'row_id': 'committee_old_2012.5810473741',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '0',
  'enabled': '0',
  'label': 'Finances et Patrimoine',
  'row_id': 'committee_old_2012.9920391524',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '0',
  'enabled': '0',
  'label': 'AG/Finances/Enseignement/Culture/Sport/Sant\xc3\xa9',
  'row_id': 'committee_old_2013.2501155949',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '0',
  'enabled': '0',
  'label': 'Cadre de Vie/Patrimoine',
  'row_id': 'committee_old_2013.2501159941',
  'supplements': '3',
  'using_groups': []},
 {'acronym': '',
  'auto_from': [],
  'default_assembly': '',
  'default_attendees': [],
  'default_place': '',
  'default_signatories': [],
  'default_signatures': '',
  'enable_editors': '0',
  'enabled': '0',
  'label': 'Travaux/Finances',
  'row_id': 'committee_old_2019.2501156983',
  'supplements': '3',
  'using_groups': []},
)


class Migrate_To_4200(MCMigrate_To_4200):

    def _fixCfgs(self):
        def _replace_columns(columns_tuple):
            columns = list(columns_tuple)
            if 'actions' in columns:
                columns.remove('actions')
                columns.append('actions_async')
            if 'council' in cfg.getId() and 'review_state' in columns:
                columns.remove('review_state')
                columns.append('review_state_title')
            return tuple(columns)

        """meetingseraing_workflow/meetingitemseraing_workflow do not exist anymore,
           we use meeting_workflow/meetingitem_workflow."""
        logger.info("Adapting 'meetingWorkflow/meetingItemWorkflow' for every MeetingConfigs...")
        for cfg in self.tool.objectValues('MeetingConfig'):
            if 'council' in cfg.getId():
                cfg.setCommittees(COMMITTEES_TO_APPLY)
            # replace action and review_state column by async actions
            cfg.setItemColumns(_replace_columns(cfg.getItemColumns()))
            cfg.setAvailableItemsListVisibleColumns(_replace_columns(cfg.getAvailableItemsListVisibleColumns()))
            cfg.setItemsListVisibleColumns(_replace_columns(cfg.getItemsListVisibleColumns()))
            cfg.setMeetingColumns(_replace_columns(cfg.getMeetingColumns()))
            # Force init some fields
            cfg.setItemCommitteesStates(('presented', 'itemfrozen', 'itempublished'))
            cfg.setItemCommitteesViewStates(('presented', 'itemfrozen', 'itempublished', 'accepted',
                                             'accepted_but_modified', 'pre_accepted', 'refused', 'delayed', 'removed',
                                             'returned_to_proposing_group'))
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
        self._fixCfgs()
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
