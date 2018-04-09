# -*- coding: utf-8 -*-

import logging

from Products.PloneMeeting.migrations import Migrator

logger = logging.getLogger('MeetingLalouviere')


# The migration class ----------------------------------------------------------
class MigrateToAddSearches(Migrator):

    def _add_searches(self):
        logger.info('Add somes searches')

        for cfg in self.tool.objectValues('MeetingConfig'):
            cfg_id = cfg.getId()
            logger.info('Add searches for {0}'.format(cfg_id))
            # call _createSubFolder and createSearches so new searches are added to
            # a Plone Site that was already migrated in PM4 and is upgraded after new searches
            # have been added to the code
            cfg.createSearches(cfg._searchesInfo())
        logger.info('Done.')

    def run(self, step=None):
        logger.info('Adding somes searches')
        self._add_searches()


# The migrate function -------------------------------------------------------
def migrate(context):
    """This upgrade-step function will:
       add somes searches, defines in adapter, for all Meeting Config
    """
    migrator = MigrateToAddSearches(context)
    migrator.run()
    migrator.finish()
