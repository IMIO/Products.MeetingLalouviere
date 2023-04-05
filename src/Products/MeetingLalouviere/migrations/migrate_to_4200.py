# -*- coding: utf-8 -*-
from datetime import datetime

from DateTime import DateTime
from plone import api
from Products.MeetingCommunes.migrations.migrate_to_4200 import Migrate_To_4200 as MCMigrate_To_4200
from Products.MeetingLalouviere.config import LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS, LLO_APPLYED_COUNCIL_WFA, \
    LLO_APPLYED_COLLEGE_WFA
from Products.MeetingLalouviere.config import LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS
from Products.PloneMeeting.config import NO_COMMITTEE
import logging

from plone.app.textfield import RichTextValue

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

Travaux_Finances_Patrimoine = "committee_2020-01-01.2501162132"
AG_Enseignement_Culture_Sport_Sante = "committee_2019-01-01.2501153343"
Cadre_Vie = "committee_2013-01-01.2501163335"
Police = "committee_2012-01-01.9920407131"
Speciale = "committee_2012-01-01.5810485069"
Travaux = 'committee_old_2012.5267121837'
Enseignement = 'committee_old_2012.5810478389'
Cadre_Vie_Logement = 'committee_old_2012.5810479936'
AG = 'committee_old_2012.5810473741'
Finances_Patrimoine = 'committee_old_2012.9920391524'
AG_Finances_Enseignement_Culture_Sport_Sante = 'committee_old_2013.2501155949'
Travaux_Finances = 'committee_old_2019.2501156983'
Cadre_Vie_Patrimoine = 'committee_old_2013.2501159941'
Conseillers2 = 'points-conseillers-2eme-supplement'
Conseillers3 = 'points-conseillers-3eme-supplement'

COMMITTEES_TO_APPLY = (
    {'acronym': 'Trav',
     'auto_from': [],
     'default_assembly': "Monsieur J-C WARGNIE, Président,\nMadame L. ANCIAUX, Vice-présidente,\n"
                         "Messieurs F. ROMEO, J. CHRISTIAENS, G. CALUCCI, Madame M. MULA, Messieurs M. PRIVITERA,\n"
                         "S. ARNONE, Madame L. RUSSO, Monsieur C. BAISE, Madame P. TREMERIE,\n"
                         "Messieurs A. HERMANT, M. PUDDU, X. PAPIER, Conseillers communaux",
     'default_attendees': [],
     'default_place': 'Salle du Conseil, 1er étage',
     'default_signatories': [],
     'default_signatures': '',
     'enable_editors': '1',
     'enabled': '1',
     'label': 'I. Travaux/Finances/Patrimoine',
     'row_id': Travaux_Finances_Patrimoine,
     'supplements': '1',
     'using_groups': []},
    {'acronym': 'AG',
     'auto_from': [],
     'default_assembly': 'Madame M. SPANO, Présidente,\nMonsieur A. AYCIK, Vice-président,\n'
                         'Monsieur J-C WARGNIE, Madame D. STAQUET, Monsieur M. BURY, Madame M. MULA, Monsieur M. DI MATTIA,\n'
                         'Mesdames Ö. KAZANCI, L. LEONI, Monsieur M. SIASSIA-BULA,\n'
                         'Mesdames A. LECOCQ, L. LUMIA, Messieurs O. DESTREBECQ, O. LAMAND, Conseillers communaux',
     'default_attendees': [],
     'default_place': 'Salle du Collège, 2ème étage',
     'default_signatories': [],
     'default_signatures': '',
     'enable_editors': '1',
     'enabled': '1',
     'label': 'II. AG/Enseignement/Culture/Sport/Sant\xc3\xa9',
     'row_id': AG_Enseignement_Culture_Sport_Sante,
     'supplements': '1',
     'using_groups': []},
    {'acronym': 'Vie',
     'auto_from': [],
     'default_assembly': 'Madame L. RUSSO, Présidente,\n'
                         'Monsieur M. DI MATTIA, Vice-président,\n'
                         'Madame O. ZRIHEN, Monsieur A. AYCIK, Mesdames M. SPANO, Ö. KAZANCI,\n'
                         'Messieurs S. ARNONE, J. CHRISTIAENS, M. BURY, O. DESTREBECQ,\n'
                         'Messieurs M. SIASSIA-BULA, A. CLEMENT,\n'
                         'Madame A. SOMMEREYNS, Monsieur L. RESINELLI, Conseillers communaux',
     'default_attendees': [],
     'default_place': 'Salle du Conseil,1er étage',
     'default_signatories': [],
     'default_signatures': '',
     'enable_editors': '1',
     'enabled': '1',
     'label': 'III. Cadre de Vie',
     'row_id': Cadre_Vie,
     'supplements': '1',
     'using_groups': []},
    {'acronym': 'Police',
     'auto_from': [],
     'default_assembly': 'Madame D. STAQUET, Présidente,\n'
                         'Madame D. STAQUET, Vice-présidente,\n'
                         'Messieurs F. ROMEO, M. PRIVITERA, Mesdames Ö. KAZANCI, L. ANCIAUX, M. SPANO,\n'
                         'Messieurs J. CHRISTIAENS, M. BURY, M. BAISE, Madame P. TREMERIE,\n'
                         'Monsieur A. CLEMENT, Madame A. SOMMEREYNS, Monsieur M. VAN HOOLAND,\nConseillers communaux',
     'default_attendees': [],
     'default_place': 'Salle du Collège, 2ème étage',
     'default_signatories': [],
     'default_signatures': '',
     'enable_editors': '1',
     'enabled': '1',
     'label': 'IV. Police',
     'row_id': Police,
     'supplements': '1',
     'using_groups': []},
    {'acronym': 'Spe',
     'auto_from': [],
     'default_assembly': '',
     'default_attendees': [],
     'default_place': '',
     'default_signatories': [],
     'default_signatures': '',
     'enable_editors': '1',
     'enabled': '1',
     'label': 'V. Sp\xc3\xa9ciale',
     'row_id': Speciale,
     'supplements': '1',
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
     'row_id': Travaux,
     'supplements': '1',
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
     'row_id': Enseignement,
     'supplements': '1',
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
     'row_id': Cadre_Vie_Logement,
     'supplements': '1',
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
     'row_id': AG,
     'supplements': '1',
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
     'row_id': Finances_Patrimoine,
     'supplements': '1',
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
     'row_id': AG_Finances_Enseignement_Culture_Sport_Sante,
     'supplements': '1',
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
     'row_id': Cadre_Vie_Patrimoine,
     'supplements': '1',
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
     'row_id': Travaux_Finances,
     'supplements': '1',
     'using_groups': []},
    {'acronym': '',
     'auto_from': [],
     'default_assembly': '',
     'default_attendees': [],
     'default_place': '',
     'default_signatories': [],
     'default_signatures': '',
     'enable_editors': '0',
     'enabled': 'item_only',
     'label': 'Points conseillers (2ème supplément)',
     'row_id': Conseillers2,
     'supplements': '0',
     'using_groups': []},
    {'acronym': '',
     'auto_from': [],
     'default_assembly': '',
     'default_attendees': [],
     'default_place': '',
     'default_signatories': [],
     'default_signatures': '',
     'enable_editors': '0',
     'enabled': 'item_only',
     'label': 'Points conseillers (3ème supplément)',
     'row_id': Conseillers3,
     'supplements': '0',
     'using_groups': []},
)

COMMITTEES_2020 = [Travaux_Finances_Patrimoine, AG_Enseignement_Culture_Sport_Sante, Cadre_Vie, Police, Speciale]
COMMITTEES_2019 = [Travaux_Finances, AG_Enseignement_Culture_Sport_Sante, Cadre_Vie_Patrimoine, Police, Speciale]
COMMITTEES_2013 = [Travaux, AG_Finances_Enseignement_Culture_Sport_Sante, Cadre_Vie_Patrimoine, Police, Speciale]
COMMITTEES_2012 = [Travaux, Enseignement, Cadre_Vie_Logement, AG, Finances_Patrimoine, Police, Speciale]


class Migrate_To_4200(MCMigrate_To_4200):

    def _replace_user_committee_editors(self):
        binding = {
            "commission-travaux_commissioneditors": Travaux_Finances_Patrimoine,
            "commission-sport_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
            "commission-speciale_commissioneditors": Speciale,
            "commission-sante_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
            "commission-police_commissioneditors": Police,
            "commission-patrimoine_commissioneditors": Travaux_Finances_Patrimoine,
            "commission-finances_commissioneditors": Travaux_Finances_Patrimoine,
            "commission-enseignement_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
            "commission-cadre-de-vie_commissioneditors": Cadre_Vie,
            "commission-ag_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
            "commission-culture_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
        }
        group_tool = self.portal.portal_groups
        meetingmanagers = group_tool.getGroupById('meeting-config-council_meetingmanagers').getAllGroupMemberIds()
        for old_commission in binding:
            group = group_tool.getGroupById(old_commission)
            if group:
                members = group.getAllGroupMemberIds()
                new_group = group_tool.getGroupById("meeting-config-council_" + binding[old_commission])
                for member in members:
                    group.removeMember(member)
                    if new_group and member not in meetingmanagers:
                        new_group.addMember(member)
                group_tool.removeGroup(group.getId())

    def _applyMeetingConfig_fixtures(self):
        logger.info('applying meetingconfig fixtures...')
        self.updateTALConditions("year()", "year")
        self.updateTALConditions("month()", "month")
        self.cleanUsedItemAttributes(['classifier', 'commissionTranscript'])
        self.cleanUsedMeetingAttributes(["preMeetingDate", "preMeetingPlace", "preMeetingAssembly",
                                         "preMeetingDate_2", "preMeetingPlace_2", "preMeetingAssembly_2",
                                         "preMeetingDate_3", "preMeetingPlace_3", "preMeetingAssembly_3",
                                         "preMeetingDate_4", "preMeetingPlace_4", "preMeetingAssembly_4",
                                         "preMeetingDate_5", "preMeetingPlace_5", "preMeetingAssembly_5",
                                         "preMeetingDate_6", "preMeetingPlace_6", "preMeetingAssembly_6",
                                         "preMeetingDate_7", "preMeetingPlace_7", "preMeetingAssembly_7",
                                         "first_item_number",
                                         ])
        logger.info("Adapting 'meetingWorkflow/meetingItemWorkflow' for every MeetingConfigs...")
        for cfg in self.tool.objectValues('MeetingConfig'):
            if 'council' in cfg.getId():
                cfg.setCommittees(COMMITTEES_TO_APPLY)
                cfg.createCommitteeEditorsGroups()
                self._replace_user_committee_editors()
                # Force init some fields
                cfg.setItemCommitteesStates(('presented', 'itemfrozen', 'itempublished'))
                cfg.setItemCommitteesViewStates(('presented', 'itemfrozen', 'itempublished', 'accepted',
                                                 'accepted_but_modified', 'pre_accepted', 'refused', 'delayed',
                                                 'removed',
                                                 'returned_to_proposing_group'))
                used_meeting_attr = list(cfg.getUsedMeetingAttributes())
                used_meeting_attr.append("committees")
                used_meeting_attr.append("committees_assembly")
                used_meeting_attr.append("committees_place")
                # meeting_number will be used in convocations in meeting reference field
                for attribute in ("pre_meeting_date", "pre_meeting_place"):
                    if attribute in used_meeting_attr:
                        used_meeting_attr.remove(attribute)
                cfg.setUsedMeetingAttributes(tuple(used_meeting_attr))
                used_item_attr = list(cfg.getUsedItemAttributes())
                used_item_attr.append("committeeTranscript")
                used_item_attr.append("votesResult")
                cfg.setUsedItemAttributes(tuple(used_item_attr))
                cfg.setWorkflowAdaptations(LLO_APPLYED_COUNCIL_WFA)
                cfg.setDashboardItemsListingsFilters(
                    self.replace_in_list("c24", "c31", cfg.getDashboardItemsListingsFilters()))
                cfg.setDashboardMeetingAvailableItemsFilters(
                    self.replace_in_list("c24", "c31", cfg.getDashboardMeetingAvailableItemsFilters()))
                cfg.setDashboardMeetingLinkedItemsFilters(
                    self.replace_in_list("c24", "c31", cfg.getDashboardMeetingLinkedItemsFilters()))
            else:
                cfg.setWorkflowAdaptations(LLO_APPLYED_COLLEGE_WFA)
                cfg.setMeetingColumns(cfg.getMeetingColumns() + ('static_meeting_number',))
            # replace action and review_state column by async actions
            self.updateColumns(to_replace={'actions': 'async_actions',
                                           'review_state': 'review_state_title',
                                           'getRawClassifier': 'committees_index'})
            # remove old attrs
            old_attrs = ('preMeetingAssembly_default', 'preMeetingAssembly_2_default', 'preMeetingAssembly_3_default',
                         'preMeetingAssembly_4_default', 'preMeetingAssembly_5_default', 'preMeetingAssembly_6_default',
                         'preMeetingAssembly_7_default')
            for field in old_attrs:
                if hasattr(cfg, field):
                    delattr(cfg, field)

            cfg.setItemBudgetInfosStates(self.replace_in_list(u'proposed_to_budgetimpact_reviewer',
                                                              u'proposed_to_budget_reviewer',
                                                              cfg.getItemBudgetInfosStates())
                                         )
            cfg.setItemAdviceStates(self.replace_in_list(u'proposed_to_budgetimpact_reviewer',
                                                         u'proposed_to_budget_reviewer',
                                                         cfg.getItemAdviceStates())
                                    )
            cfg.setItemAdviceViewStates(self.replace_in_list(u'proposed_to_budgetimpact_reviewer',
                                                             u'proposed_to_budget_reviewer',
                                                             cfg.getItemAdviceViewStates())
                                        )
            cfg.setItemAdviceEditStates(self.replace_in_list(u'proposed_to_budgetimpact_reviewer',
                                                             u'proposed_to_budget_reviewer',
                                                             cfg.getItemAdviceEditStates())
                                        )
            cfg.setToDoListSearches(tuple())
            cfg.setUseVotes(True)
            cfg.setVotesResultTALExpr("python: pm_utils.print_votes(item, include_total_voters=True)")

    def replace_in_list(self, to_replace, new_value, list):
        result = set()
        for value in list:
            if value == to_replace:
                result.add(new_value)
            else:
                result.add(value)
        return tuple(result)

    def _fixUsedMeetingWFs(self):
        # remap states and transitions
        for cfg in self.tool.objectValues('MeetingConfig'):
            # ensure attr exists
            cfg.getCommittees()
            cfg.getItemCommitteesStates()
            cfg.getItemCommitteesViewStates()
            cfg.getItemPreferredMeetingStates()
            cfg.getItemObserversStates()
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

    def _hook_custom_meeting_to_dx(self, old, new):

        def get_committee(date, assembly, place, row_id):
            date._timezone_naive = True
            datetime = date.asdatetime()
            return {'assembly': RichTextValue(assembly.raw, 'text/plain', 'text/x-html-safe'),
                    'attendees': None,
                    'committee_observations': None,
                    'convocation_date': None,
                    'date': datetime,  # fill selected date in old
                    'place': place,  # fill place value in old
                    'row_id': row_id,  # fill row_id un cfg
                    'signatories': None,
                    'signatures': None}

        if new.portal_type == 'MeetingCouncil':
            committees = []
            if old.preMeetingDate:
                committees.append(get_committee(old.preMeetingDate, old.preMeetingAssembly,
                                                old.preMeetingPlace, self.find_committee_row_id(1, old.getDate())))
            if hasattr(old, 'preMeetingDate_2') and old.preMeetingDate_2:
                committees.append(get_committee(old.preMeetingDate_2, old.preMeetingAssembly_2,
                                                old.preMeetingPlace_2, self.find_committee_row_id(2, old.getDate())))
            if hasattr(old, 'preMeetingDate_3') and old.preMeetingDate_3:
                committees.append(get_committee(old.preMeetingDate_3, old.preMeetingAssembly_3,
                                                old.preMeetingPlace_3, self.find_committee_row_id(3, old.getDate())))
            if hasattr(old, 'preMeetingDate_4') and old.preMeetingDate_4:
                committees.append(get_committee(old.preMeetingDate_4, old.preMeetingAssembly_4,
                                                old.preMeetingPlace_4, self.find_committee_row_id(4, old.getDate())))
            if hasattr(old, 'preMeetingDate_5') and old.preMeetingDate_5:
                committees.append(get_committee(old.preMeetingDate_5, old.preMeetingAssembly_5,
                                                old.preMeetingPlace_5, self.find_committee_row_id(5, old.getDate())))
            if old.getDate().year() <= 2013 and old.getDate().month() < 6:
                if hasattr(old, 'preMeetingDate_6') and old.preMeetingDate_6:
                    committees.append(get_committee(old.preMeetingDate_6, old.preMeetingAssembly_6,
                                                    old.preMeetingPlace_6,
                                                    self.find_committee_row_id(6, old.getDate())))
                if hasattr(old, 'preMeetingDate_7') and old.preMeetingDate_7:
                    committees.append(get_committee(old.preMeetingDate_7, old.preMeetingAssembly_7,
                                                    old.preMeetingPlace_7,
                                                    self.find_committee_row_id(7, old.getDate())))
            new.committees = committees
        new.pre_meeting_date = None
        new.pre_meeting_place = None

    def _hook_after_meeting_to_dx(self):
        self._applyMeetingConfig_fixtures()
        self._adaptWFHistoryForItemsAndMeetings()
        self._adapt_council_items()
        self.update_wf_states_and_transitions()

    def update_wf_states_and_transitions(self):
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

    def find_committee_row_id(self, number, date):
        if not date or date.year() > 2020 or (date.year() == 2020 and date.month() > 8):
            return COMMITTEES_2020[number - 1]
        elif date.year() >= 2019 and date.month() > 8:
            return COMMITTEES_2019[number - 1]
        elif date.year() >= 2013 and date.month() > 5:
            return COMMITTEES_2013[number - 1]
        else:
            return COMMITTEES_2012[number - 1]

    def find_item_committee_row_id(self, date, item_classifier):
        suffix = ""
        if "1er-supplement" in item_classifier:
            suffix = "__suppl__1"
            item_classifier = '-'.join(item_classifier.split('-')[:-2])
        if not date or date.year > 2020 or (date.year == 2020 and date.month > 8):
            binding = {
                "commission-travaux": Travaux_Finances_Patrimoine,
                "commission-sport": AG_Enseignement_Culture_Sport_Sante,
                "commission-speciale": Speciale,
                "commission-sante": AG_Enseignement_Culture_Sport_Sante,
                "commission-police": Police,
                "commission-patrimoine": Travaux_Finances_Patrimoine,
                "commission-finances": Travaux_Finances_Patrimoine,
                "commission-enseignement": AG_Enseignement_Culture_Sport_Sante,
                "commission-cadre-de-vie": Cadre_Vie,
                "commission-ag": AG_Enseignement_Culture_Sport_Sante,
                "commission-culture": AG_Enseignement_Culture_Sport_Sante,
                "points-conseillers-2eme-supplement": Conseillers2,
                "points-conseillers-3eme-supplement": Conseillers3
            }
        elif date.year > 2019 or (date.year == 2019 and date.month > 8):
            binding = {
                "commission-travaux": Travaux_Finances,
                "commission-sport": AG_Enseignement_Culture_Sport_Sante,
                "commission-speciale": Speciale,
                "commission-sante": AG_Enseignement_Culture_Sport_Sante,
                "commission-police": Police,
                "commission-patrimoine": Cadre_Vie_Patrimoine,
                "commission-finances": Travaux_Finances,
                "commission-enseignement": AG_Enseignement_Culture_Sport_Sante,
                "commission-cadre-de-vie": Cadre_Vie_Patrimoine,
                "commission-ag": AG_Enseignement_Culture_Sport_Sante,
                "commission-culture": AG_Enseignement_Culture_Sport_Sante,
                "points-conseillers-2eme-supplement": Conseillers2,
                "points-conseillers-3eme-supplement": Conseillers3
            }
        elif date.year > 2013 or (date.year == 2013 and date.month > 5):
            binding = {
                "commission-travaux": Travaux,
                "commission-sport": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-speciale": Speciale,
                "commission-sante": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-police": Police,
                "commission-patrimoine": Travaux_Finances_Patrimoine,
                "commission-finances": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-enseignement": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-cadre-de-vie": Cadre_Vie,
                "commission-ag": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-culture": AG_Finances_Enseignement_Culture_Sport_Sante,
                "points-conseillers-2eme-supplement": Conseillers2,
                "points-conseillers-3eme-supplement": Conseillers3
            }
        else:
            binding = {
                "commission-travaux": Travaux,
                "commission-sport": AG,
                "commission-speciale": Speciale,
                "commission-sante": AG,
                "commission-police": Police,
                "commission-patrimoine": Finances_Patrimoine,
                "commission-finances": Finances_Patrimoine,
                "commission-enseignement": Enseignement,
                "commission-cadre-de-vie": Cadre_Vie_Logement,
                "commission-ag": AG,
                "commission-culture": AG,
                "commission-cadre-de-vie-et-logement": Cadre_Vie_Logement,
                "commission-finances-et-patrimoine": Finances_Patrimoine,
                "points-conseillers-2eme-supplement": Conseillers2,
                "points-conseillers-3eme-supplement": Conseillers3
            }
        committee = binding.get(item_classifier, None)
        if committee:
            return committee + suffix
        else:
            return NO_COMMITTEE

    def _adapt_council_items(self):
        logger.info('adapting council items...')
        brains = self.catalog(portal_type='MeetingItemCouncil')
        treshold_datetime = datetime(2000, 1, 1)
        substitute_datetime = datetime.now()
        for brain in brains:
            if brain.getRawClassifier:
                meeting_date = brain.meeting_date
                if meeting_date < treshold_datetime:
                    meeting_date = substitute_datetime
                committee_id = self.find_item_committee_row_id(meeting_date, brain.getRawClassifier)
                if committee_id == NO_COMMITTEE:
                    logger.warning("Committee not found for {} at {}, classifier = {} committee = {}".format(
                        brain.portal_type,
                        brain.getPath(),
                        brain.getRawClassifier,
                        committee_id))
                item = brain.getObject()
                item.setCommittees((committee_id,))

    def _remove_old_dashboardcollection(self):
        for cfg in self.tool.objectValues('MeetingConfig'):
            items = cfg.searches.searches_items
            meetings = cfg.searches.searches_items
            decided = cfg.searches.searches_items
            for folder in (items, meetings, decided):
                api.content.delete(objects=folder.listFolderContents())

    def run(self,
            profile_name=u'profile-Products.MeetingLalouviere:default',
            extra_omitted=[]):
        self._remove_old_dashboardcollection()
        super(Migrate_To_4200, self).run(extra_omitted=extra_omitted)
        logger.info('Done migrating to MeetingLalouviere 4200...')


# The migration function -------------------------------------------------------
def migrate(context):
    '''
    This migration function:
       1) Change MeetingConfig workflows to use meeting_workflow/meetingitem_workflow;
       2) Call PloneMeeting migration to 4200 and 4201;
       3) In _after_reinstall hook, adapt items and meetings workflow_history
          to reflect new defined workflow done in 1);
    '''
    migrator = Migrate_To_4200(context)
    migrator.run()
    migrator.finish()
