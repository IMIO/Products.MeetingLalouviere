# -*- coding: utf-8 -*-
import logging

from Products.MeetingCommunes.Extensions.add_portal_categories import (
    add_portal_category,
)
from Products.PloneMeeting.migrations import Migrator

from plone import api

logger = logging.getLogger("MeetingLalouviere")


class Migrate_To_4_1_5_4(Migrator):
    def create_classifiers(self):
        folder = self.council.classifiers
        for category in self.council.getCategories():
            if category.enabled and category.id != "recurrent":
                api.content.copy(source=category, target=folder, id=category.id)
            category.enabled = False
            category.reindexObject(idxs=["enabled"])

    def migrate_item_commissions_classifiers(self):
        brains = self.portal.portal_catalog(
            portal_type=[
                self.council.getItemTypeName(),
                self.council.getItemTypeName(configType="MeetingItemRecurring"),
                self.council.getItemTypeName(configType="MeetingItemTemplate"),
            ]
        )
        for brain in brains:
            if brain.getCategory:
                item = brain.getObject()
                if brain.getCategory == "recurrent":
                    item.setCategory("administration")
                    item.reindexObject(idxs=["getCategory"])
                else:
                    item.setClassifier(item.getCategory())
                    item.reindexObject(idxs=["getRawClassifier"])

    def run(self, **kwargs):
        self.council = self.portal.portal_plonemeeting.get("meeting-config-council")
        if "classifier" not in self.council.getUsedItemAttributes():
            item_attr = self.council.getUsedItemAttributes() + tuple(["classifier"])
            self.council.setUsedItemAttributes(item_attr)
        self.create_classifiers()
        add_portal_category(self.portal)
        self.migrate_item_commissions_classifiers()


def migrate(context):
    """
    """
    migrator = Migrate_To_4_1_5_4(context)
    migrator.run()
    migrator.finish()
