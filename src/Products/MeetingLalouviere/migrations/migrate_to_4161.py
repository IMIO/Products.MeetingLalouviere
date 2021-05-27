# -*- coding: utf-8 -*-
import logging

from Products.MeetingCommunes.Extensions.add_portal_configuration import (
    add_category, add_lisTypes
)
from Products.PloneMeeting.migrations import Migrator

from plone import api

logger = logging.getLogger("MeetingLalouviere")


class Migrate_To_4_1_5_4(Migrator):
    def patch_config(self):
        def insert_in_tuple_after(base_tuple, new, after):
            lst = list(base_tuple)
            lst.insert(lst.index(after) + 1, new)
            return tuple(lst)

        if "classifier" not in self.council.getUsedItemAttributes():
            item_attr = self.council.getUsedItemAttributes() + tuple(["classifier"])
            self.council.setUsedItemAttributes(item_attr)

        if "getRawClassifier" not in self.council.itemColumns:
            self.council.itemColumns = insert_in_tuple_after(
                self.council.itemColumns,
                u"getRawClassifier",
                u"getCategory"
            )

        if "getRawClassifier" not in self.council.availableItemsListVisibleColumns:
            self.council.availableItemsListVisibleColumns = insert_in_tuple_after(
                self.council.availableItemsListVisibleColumns,
                u"getRawClassifier",
                u"getCategory",
            )

        if "getRawClassifier" not in self.council.itemsListVisibleColumns:
            self.council.itemsListVisibleColumns = insert_in_tuple_after(
                self.council.itemsListVisibleColumns,
                u"getRawClassifier",
                u"getCategory",
            )

        if "c24" not in self.council.dashboardItemsListingsFilters:
            self.council.dashboardItemsListingsFilters = insert_in_tuple_after(
                self.council.dashboardItemsListingsFilters, u"c24", u"c5"
            )

        if "c24" not in self.council.dashboardMeetingAvailableItemsFilters:
            self.council.dashboardMeetingAvailableItemsFilters = insert_in_tuple_after(
                self.council.dashboardMeetingAvailableItemsFilters, u"c24", u"c5"
            )

        if "c24" not in self.council.dashboardMeetingLinkedItemsFilters:
            self.council.dashboardMeetingLinkedItemsFilters = insert_in_tuple_after(
                self.council.dashboardMeetingLinkedItemsFilters, u"c24", u"c5"
            )

        for insertingMethod in self.council.insertingMethodsOnAddItem:
            if insertingMethod["insertingMethod"] == "on_categories":
                insertingMethod["insertingMethod"] = "on_classifiers"

        self.council.at_post_edit_script()

    def create_classifiers(self):
        # for items without commission
        api.content.create(
            container=self.council.classifiers,
            type="meetingcategory",
            id="administration",
            title="Administration générale",
        )

        for category in self.council.getCategories():
            if category.enabled and category.id != "recurrent":
                old_category = api.content.copy(
                    source=category,
                    target=self.council.categories,
                    id=category.id + "-old",
                )
                api.content.move(
                    source=category, target=self.council.classifiers, id=category.id
                )
                category.reindexObject()
                category = old_category

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
        count = 0
        for brain in brains:
            if brain.getCategory:
                item = brain.getObject()
                if item.portal_type == self.council.getItemTypeName(
                    configType="MeetingItemRecurring"
                ):
                    item.setCategory("administration")
                    item.setClassifier("administration")
                elif item.getCategory() == "recurrent":
                    item.setClassifier("administration")
                else:
                    item.setClassifier(item.getCategory())
                    item.setCategory(item.getCategory() + "-old")

                item.reindexObject(idxs=["getCategory", "getRawClassifier"])

            count += 1
            if count % 200 == 0:
                logger.info("Migrating council items {}/{}".format(count, len(brains)))

    def run(self, **kwargs):
        self.council = self.portal.portal_plonemeeting.get("meeting-config-council")
        logger.info("Patching meeting-config-council")
        self.patch_config()
        logger.info("Creating commission classifiers")
        self.create_classifiers()
        logger.info("Creating deliberation.be categories using MC script")
        add_category(self.portal)
        logger.info("Creating deliberation.be listTypes using MC script")
        add_lisTypes(self.portal)
        logger.info("Migrating council items")
        self.migrate_item_commissions_classifiers()


def migrate(context):
    """
    """
    migrator = Migrate_To_4_1_5_4(context)
    migrator.run()
    migrator.finish()
