# -*- coding: utf-8 -*-
import transaction
from Products.GenericSetup.tool import DEPENDENCY_STRATEGY_NEW
from Products.MeetingCommunes.migrations.migrate_to_4_1 import (
    Migrate_To_4_1 as MCMigrate_To_4_1,
)

from collective.contact.plonegroup.config import get_registry_functions, set_registry_functions
from plone import api

import logging


logger = logging.getLogger("MeetingLalouviere")


class Migrate_To_4_1(MCMigrate_To_4_1):
    def remove_useless_functions(self):
        """
        Remove groups that are not used in our custom workflow
        """
        groups = api.group.get_groups()
        for group in groups:
            grp_id = group.id
            if grp_id.endswith("_reviewers") or grp_id.endswith("_prereviewers"):
                for member in  group.getAllGroupMemberIds():
                    group.removeMember(member)

        functions = get_registry_functions()
        functions_result = []
        for function in functions:
            if function['fct_id'] not in (u'prereviewers', u'reviewers'):
                functions_result.append(function)

        set_registry_functions(functions_result)

    def reapply_meetingconfigs_config(self):
        # fix item reference TAL
        for cfg in self.tool.objectValues('MeetingConfig'):
            cfg.setItemReferenceFormat("python: item.adapted().compute_item_ref()")
            cfg.reindexObject()

    def run(self, **kwargs):
        self.ps.upgradeProfile("profile-plonetheme.imioapps:default")
        # reapply the actions.xml of collective.iconifiedcategory
        self.ps.runImportStepFromProfile(
            "profile-collective.iconifiedcategory:default", "actions"
        )
        self.ps.runImportStepFromProfile(
            "profile-Products.MeetingLalouviere:default", "workflow"
        )
        transaction.commit()
        super(Migrate_To_4_1, self).run(
            extra_omitted=["Products.MeetingLalouviere:default"]
        )
        transaction.commit()
        self.remove_useless_functions()
        transaction.commit()
        self.reinstall(
            profiles=[u"profile-Products.MeetingLalouviere:default"],
            ignore_dependencies=True,
            dependency_strategy=DEPENDENCY_STRATEGY_NEW,
        )
        self.reapply_meetingconfigs_config()


def migrate(context):
    """This migration will:

       1) Execute Products.MeetingCommunes migration.
    """
    migrator = Migrate_To_4_1(context)
    migrator.run()
    migrator.finish()
