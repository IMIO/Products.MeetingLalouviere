# -*- coding: utf-8 -*-

from ftw.labels.interfaces import ILabelJar
from ftw.labels.labeling import ILabeling
from imio.helpers.catalog import removeIndexes
from imio.helpers.content import safe_delattr
from Products.CMFPlone.utils import base_hasattr
from Products.MeetingLalouviere import logger
from Products.PloneMeeting.migrations import Migrator
from Products.PloneMeeting.utils import reindex_object
from zope.component import getAdapter


class MigrateTo4201(Migrator):

    def _update_follow_up(self):
        """Move custom followUp to existing followUp."""
        labels_config = (
            {'edit_groups': [],
             'view_groups': [],
             'view_groups_excluding': '0',
             'view_access_on': '',
             'view_access_on_cache': '1',
             'label_id': '*',
             'edit_access_on_cache': '0',
             'view_states': [],
             'edit_groups_excluding': '0',
             'edit_states': [],
             'update_local_roles': '0',
             'edit_access_on': 'python: cfg.isManager(cfg) or checkPermission("Modify portal content", context)'},
            {'edit_groups': ['configgroup_meetingmanagers'],
             'view_groups': [
                'configgroup_meetingmanagers',
                'suffix_proposing_group_creators',
                'suffix_proposing_group_observers',
                'suffix_proposing_group_alderman',
                'suffix_proposing_group_officemanagers',
                'suffix_proposing_group_divisionheads',
                'suffix_proposing_group_serviceheads',
                'suffix_proposing_group_directors'],
             'view_groups_excluding': '0',
             'view_access_on': '',
             'view_access_on_cache': '1',
             'label_id': 'needed-follow-up',
             'edit_access_on_cache': '1',
             'view_states': [],
             'edit_groups_excluding': '0',
             'edit_states': [
                'accepted',
                'accepted_but_modified',
                'accepted_out_of_meeting',
                'itemfrozen',
                'presented',
                'refused',
                'delayed',
                'postponed_next_meeting',
                'removed',
                'returned_to_proposing_group'],
             'update_local_roles': '0',
             'edit_access_on': ''},
            {'edit_groups': ['configgroup_meetingmanagers'],
             'view_groups': [
                'configgroup_meetingmanagers',
                'suffix_proposing_group_creators',
                'suffix_proposing_group_observers',
                'suffix_proposing_group_alderman',
                'suffix_proposing_group_officemanagers',
                'suffix_proposing_group_divisionheads',
                'suffix_proposing_group_serviceheads',
                'suffix_proposing_group_directors'],
             'view_groups_excluding': '0',
             'view_access_on': '',
             'view_access_on_cache': '1',
             'label_id': 'provided-follow-up',
             'edit_access_on_cache': '1',
             'view_states': [],
             'edit_groups_excluding': '0',
             'edit_states': [
                'accepted',
                'accepted_but_modified',
                'accepted_out_of_meeting',
                'itemfrozen',
                'presented',
                'refused',
                'delayed',
                'postponed_next_meeting',
                'removed',
                'returned_to_proposing_group'],
             'update_local_roles': '2',
             'edit_access_on': ''},
            {'edit_groups': ['configgroup_meetingmanagers'],
             'view_groups': [
                'configgroup_meetingmanagers',
                'suffix_proposing_group_creators',
                'suffix_proposing_group_observers',
                'suffix_proposing_group_alderman',
                'suffix_proposing_group_officemanagers',
                'suffix_proposing_group_divisionheads',
                'suffix_proposing_group_serviceheads',
                'suffix_proposing_group_directors'],
             'view_groups_excluding': '0',
             'view_access_on': '',
             'view_access_on_cache': '1',
             'label_id': 'closed-follow-up',
             'edit_access_on_cache': '1',
             'view_states': [],
             'edit_groups_excluding': '0',
             'edit_states': [
                'accepted',
                'accepted_but_modified',
                'accepted_out_of_meeting',
                'itemfrozen',
                'presented',
                'refused',
                'delayed',
                'postponed_next_meeting',
                'removed',
                'returned_to_proposing_group'],
             'update_local_roles': '0',
             'edit_access_on': "python: bool(utils.get_labels(item, include_personal_labels=False, label_ids=['provided-follow-up', 'closed-follow-up']))"})

        logger.info('Migrating follow-up...')
        for cfg in self.tool.objectValues('MeetingConfig'):
            cfg_id = cfg.getId()
            # enable only in College for now
            if cfg_id != 'meeting-config-college':
                self.update_used_attrs(to_remove=['providedFollowUp'], cfg_ids=[cfg_id])
            # create follow-up labels if using field providedFollowUp
            # enable "neededFollowUp"
            self.update_used_attrs(to_add=['neededFollowUp'], cfg_ids=[cfg_id])
            # configure labels
            labeljar = getAdapter(cfg, ILabelJar)
            if 'needed-follow-up' in labeljar.storage:
                return self._already_migrated()
            labeljar.add('Needed follow-up', 'orange', False)
            labeljar.add('Provided follow-up', 'green', False)
            labeljar.add('Closed follow-up', 'cornflowerblue-light', False)
            # configure labelsConfig
            if cfg_id == 'meeting-config-college':
                cfg.setLabelsConfig(labels_config)
            # configure itemFieldsConfig
            config = cfg.getItemFieldsConfig()
            config[1]['view'] = "python: item.may_view_follow_up()"
            config[1]['edit'] = "python: item.may_edit_follow_up(suffixes=['followupwriters'])"
            cfg.setItemFieldsConfig(config)
            # migrate items
            brains = self.catalog(
                portal_type=cfg.getItemTypeName(),
                getFollowUp=[
                    'follow_up_yes',
                    'follow_up_provided',
                    'follow_up_provided_not_printed'])
            for brain in brains:
                # update labels
                item = brain.getObject()
                labeling = ILabeling(item)
                labeling_values = [label for label in labeling.storage]
                if item.followUp == 'follow_up_yes':
                    labeling_values.append('needed-follow-up')
                elif item.followUp == 'follow_up_provided':
                    labeling_values.append('provided-follow-up')
                elif item.followUp == 'follow_up_provided_not_printed':
                    labeling_values.append('closed-follow-up')
                labeling.update(labeling_values)
                reindex_object(item, idxs=['labels'], update_metadata=0)
                # clean item
                safe_delattr(item, 'followUp')
        # finally remove no more used getFollowUp index
        removeIndexes(self.portal, indexes=['getFollowUp'])
        logger.info('Done.')

    def _migrate_interventions(self):
        """Migrate MeetingItem.interventions to MeetingItem.notes."""
        logger.info('Migrating field \"interventions\" to \"notes\"...')
        self.update_used_attrs(
            to_replace={'interventions': 'notes'},
            cfg_ids=['meeting-config-council'])
        brains = self.catalog(portal_type='MeetingItemCouncil')
        for brain in brains:
            item = brain.getObject()
            if not base_hasattr(item, 'interventions'):
                return self._already_migrated()
            text = item.interventions.getRaw().strip()
            if text:
                item.setNotes(text)
            safe_delattr(item, 'interventions')
        self.updatePODTemplatesCode(
            replacements={
                '.getInterventions(': ".getNotes("})
        logger.info('Done.')

    def run(self, **kwargs):
        logger.info('Migrating to MeetingLalouviere 4201...')
        # this will upgrade dependencies
        self.upgradeAll(omit=['Products.PloneMeeting:default',
                              self.profile_name.replace('profile-', '')])
        self._update_follow_up()
        self._migrate_interventions()
        logger.info('Migrating to MeetingLalouviere 4201... Done.')


def migrate(context):
    """ """
    migrator = MigrateTo4201(context)
    migrator.run()
    migrator.finish()
