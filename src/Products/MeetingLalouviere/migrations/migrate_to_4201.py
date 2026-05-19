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
        logger.info('Migrating follow-up...')
        for cfg in self.tool.objectValues('MeetingConfig'):
            if 'providedFollowUp' not in cfg.getUsedItemAttributes():
                continue
            # create follow-up labels if using field providedFollowUp
            labeljar = getAdapter(cfg, ILabelJar)
            if 'needed-follow-up' in labeljar.storage:
                return self._already_migrated()
            labeljar.add('Needed follow-up', 'orange', False)
            labeljar.add('Provided follow-up', 'green', False)
            labeljar.add('Closed follow-up', 'cornflowerblue-light', False)
            # configure itemFieldsConfig
            config = cfg.getItemFieldsConfig()
            config[0]['view'] = "python: item.may_view_follow_up(restricted=True)"
            config[0]['edit'] = "python: item.may_edit_follow_up(suffixes=['followupwriters'])"
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
            item.setNotes(item.interventions.getRaw())
            safe_delattr(item, 'interventions')
        self.updatePODTemplatesCode(
            replacements={
                '.getInterventions(': ".getNotes("})
        logger.info('Done.')

    def run(self, **kwargs):
        logger.info('Migrating to MeetingLalouviere 4201...')
        self._update_follow_up()
        self._migrate_interventions()
        logger.info('Migrating to MeetingLalouviere 4201... Done.')


def migrate(context):
    """ """
    migrator = MigrateTo4201(context)
    migrator.run()
    migrator.finish()
