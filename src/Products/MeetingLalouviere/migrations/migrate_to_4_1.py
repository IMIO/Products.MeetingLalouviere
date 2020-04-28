# -*- coding: utf-8 -*-
from Products.GenericSetup.tool import DEPENDENCY_STRATEGY_NEW
from Products.MeetingCommunes.migrations.migrate_to_4_1 import (
    Migrate_To_4_1 as MCMigrate_To_4_1,
)
from collective.contact.plonegroup.config import (
    get_registry_functions,
    set_registry_functions,
)
from plone import api

import logging


logger = logging.getLogger("MeetingLalouviere")


class Migrate_To_4_1(MCMigrate_To_4_1):
    def remove_useless_functions(self):
        """
        Remove groups that are not used in our custom workflow
        """
        def filter_list(list, filter_out):
            kept = []
            for item in list:
                if item not in filter_out:
                    kept.append(item)
            return kept

        for cfg in self.tool.objectValues("MeetingConfig"):
            adviceAnnexConfidentialVisibleFor = filter_list(
                list(cfg.getAdviceAnnexConfidentialVisibleFor()),
                [
                    "suffix_proposing_group_prereviewers",
                    "suffix_proposing_group_budgetimpactreviewers",
                    "suffix_proposing_group_reviewers",
                ],
            )
            cfg.setAdviceAnnexConfidentialVisibleFor(adviceAnnexConfidentialVisibleFor)

            itemAnnexConfidentialVisibleFor = filter_list(
                list(cfg.getItemAnnexConfidentialVisibleFor()),
                [
                    "suffix_proposing_group_prereviewers",
                    "suffix_proposing_group_budgetimpactreviewers",
                    "suffix_proposing_group_reviewers",
                ],
            )
            cfg.setItemAnnexConfidentialVisibleFor(itemAnnexConfidentialVisibleFor)

            meetingAnnexConfidentialVisibleFor = filter_list(
                list(cfg.getMeetingAnnexConfidentialVisibleFor()),
                [
                    "suffix_profile_prereviewers",
                    "suffix_profile_budgetimpactreviewers",
                    "suffix_profile_reviewers",
                ],
            )
            cfg.setMeetingAnnexConfidentialVisibleFor(meetingAnnexConfidentialVisibleFor)
            cfg.processForm()
            cfg.reindexObject()

        groups = api.group.get_groups()
        for group in groups:
            grp_id = group.id
            if grp_id.endswith("_reviewers") or grp_id.endswith("_prereviewers"):
                for member in group.getAllGroupMemberIds():
                    group.removeMember(member)

        functions = get_registry_functions()
        functions_result = []
        for function in functions:
            if function["fct_id"] not in (u"prereviewers", u"reviewers"):
                functions_result.append(function)

        set_registry_functions(functions_result)

    def _fixWFA(self):
        for cfg in self.tool.objectValues("MeetingConfig"):
            if cfg.id == 'meeting-config-college':
                wfa = ('refused', 'removed', 'return_to_proposing_group', 'validate_by_dg_and_alderman')
            else:
                wfa = ('refused', 'removed', 'return_to_proposing_group')
            cfg.setWorkflowAdaptations(wfa)
            cfg.registerPortalTypes()

    def patch_meetingconfigs(self):
        # fix item reference TAL
        # enable labels and show them in dashboards, filters ... ?
        for cfg in self.tool.objectValues("MeetingConfig"):
            cfg.setItemReferenceFormat("python: item.adapted().compute_item_ref()")
            # cfg.processForm()
            # cfg.reindexObject()

    def run(self, **kwargs):
        self.ps.runImportStepFromProfile(
            "profile-Products.MeetingLalouviere:default", "workflow"
        )
        self._fixWFA()
        super(Migrate_To_4_1, self).run(
            extra_omitted=["Products.MeetingLalouviere:default"]
        )
        self.remove_useless_functions()
        self.reinstall(
            profiles=[u"profile-Products.MeetingLalouviere:default"],
            ignore_dependencies=True,
            dependency_strategy=DEPENDENCY_STRATEGY_NEW,
        )
        self.patch_meetingconfigs()


def migrate(context):
    """This migration will:

       1) Execute Products.MeetingCommunes migration.
    """
    migrator = Migrate_To_4_1(context)
    migrator.run()
    migrator.finish()
