# -*- coding: utf-8 -*-
#
# File: testCustomMeeting.py
#
# Copyright (c) 2007-2013 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Products.MeetingLalouviere.config import (
    COUNCIL_MEETING_COMMISSION_IDS_2019,
    COUNCIL_MEETING_COMMISSION_IDS_2013,
    COUNCIL_COMMISSION_IDS,
)
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)
from Products.MeetingCommunes.tests.testCustomViews import testCustomViews as mctcv

from DateTime import DateTime


class testCustomViews(mctcv, MeetingLalouviereTestCase):
    """
        Tests the custom views
    """

    def _set_view(self, meeting):
        # set the view
        pod_template = self.meetingConfig.podtemplates.agendaTemplate
        self.request.set("template_uid", pod_template.UID())
        self.request.set("output_format", "odt")
        view = meeting.restrictedTraverse("@@document-generation")
        view()
        return view.get_generation_context_helper()

    def _setup_commissions_categories(self, commission_version):
        # add MEETING_COMMISSION's categories
        self.changeUser("admin")

        # wipe all previous cats
        ids = self.meetingConfig.categories.keys()
        if len(ids) > 0:
            ids = list(ids)
            self.meetingConfig.categories.manage_delObjects(ids)

        # flatten commission_version
        commission_categories = []
        for i in commission_version:
            if isinstance(i, tuple):
                for j in i:
                    commission_categories.append(j)
            else:
                commission_categories.append(i)

        # create 1st-supplement for each cat
        commission_categories = commission_categories + [
            cat + "-1er-supplement" for cat in commission_categories
        ]

        # add categories to the meetingConfig
        for cat in commission_categories:
            new_cat_id = self.meetingConfig.categories.invokeFactory(
                "MeetingCategory", id=cat, title="commissionCat"
            )
            new_cat = getattr(self.meetingConfig.categories, new_cat_id)
            new_cat.processForm()

    def _test_get_commission_items_by_date(self, year, month):
        # Create a meeting with a given year and month and the view
        self.changeUser("pmManager")
        meeting = self.create("Meeting", date="{}/{}/1 18:00:00".format(year, month))
        view = self._set_view(meeting)
        # Creates items needed for the test
        item = self.create("MeetingItem")
        item.setCategory(view.get_categories_for_commission(1)[0])  # First commission
        item2 = self.create("MeetingItem")
        item2.setCategory(view.get_categories_for_commission(2)[0])  # Second commission
        item3 = self.create("MeetingItem")
        item3.setCategory(view.get_categories_for_commission(2)[0])  # Second commission

        item_s = self.create("MeetingItem")
        item_s.setCategory(
            view.get_categories_for_commission(1)[0] + "-1er-supplement"
        )  # First commission, 1st supp
        item2_s = self.create("MeetingItem")
        item2_s.setCategory(
            view.get_categories_for_commission(2)[0] + "-1er-supplement"
        )  # Second commission, 1st supp
        item3_s = self.create("MeetingItem")
        item3_s.setCategory(
            view.get_categories_for_commission(2)[0] + "-1er-supplement"
        )  # Second commission, 1st supp

        items = (item, item2, item3, item_s, item2_s, item3_s)
        for i in items:
            self.presentItem(i)
        item_uids = [i.UID() for i in items]

        # Tests cases with type='normal'
        comm_no1_normal_items = [item]
        self.assertListEqual(
            view.get_commission_items(item_uids, 1), comm_no1_normal_items
        )

        comm_no2_normal_items = [item2, item3]
        self.assertListEqual(
            view.get_commission_items(item_uids, 2), comm_no2_normal_items
        )

        comm_no3_normal_items = []
        self.assertListEqual(
            view.get_commission_items(item_uids, 3), comm_no3_normal_items
        )

        # Tests cases with type='supp'
        comm_no1_supp_items = [item_s]
        self.assertListEqual(
            view.get_commission_items(item_uids, 1, type="supplement"),
            comm_no1_supp_items,
        )

        comm_no2_supp_items = [item2_s, item3_s]
        self.assertListEqual(
            view.get_commission_items(item_uids, 2, type="supplement"),
            comm_no2_supp_items,
        )

        comm_no3_supp_items = []
        self.assertListEqual(
            view.get_commission_items(item_uids, 3, type="supplement"),
            comm_no3_supp_items,
        )

        # Tests cases with type='*', get all items for each commission regardless of type
        comm_no1_items = comm_no1_normal_items + comm_no1_supp_items
        self.assertListEqual(
            view.get_commission_items(item_uids, 1, type="*"), comm_no1_items
        )

        comm_no2_items = comm_no2_normal_items + comm_no2_supp_items
        self.assertListEqual(
            view.get_commission_items(item_uids, 2, type="*"), comm_no2_items
        )

        comm_no3_items = []
        self.assertListEqual(
            view.get_commission_items(item_uids, 3, type="*"), comm_no3_items
        )

        self.deleteAsManager(
            meeting.UID()
        )  # we don't need the meeting and it's items anymore

    def test_get_commission_items(self):
        # Commissions are only present in council so we use it instead of college
        self.meetingConfig = self.meetingConfig2

        commissions_versions = [
            {
                "commissions": COUNCIL_MEETING_COMMISSION_IDS_2019,
                "year": "2019",
                "month": "09",
            },
            {
                "commissions": COUNCIL_MEETING_COMMISSION_IDS_2013,
                "year": "2013",
                "month": "06",
            },
            {"commissions": COUNCIL_COMMISSION_IDS, "year": "2010", "month": "01"},
        ]
        for cv in commissions_versions:
            self._setup_commissions_categories(cv["commissions"])
            self._test_get_commission_items_by_date(cv["year"], cv["month"])

    def test_format_commission_pre_meeting_date(self):
        # Commissions are only present in council so we use it instead of college
        self.meetingConfig = self.meetingConfig2
        # Create the meeting and the view
        self.changeUser("pmManager")
        meeting = self.create("Meeting", date="2019/09/1 18:00:00")
        view = self._set_view(meeting)
        # Set pre-meeting date and place
        meeting.setPreMeetingDate(DateTime(2019, 9, 1, 4, 20, 0))
        meeting.setPreMeetingPlace("Pays des bisounours")
        meeting.setPreMeetingDate_2(DateTime(2019, 9, 2, 4, 20, 0))
        meeting.setPreMeetingPlace_2("Pays des merveilles")

        self.assertEqual(
            view.format_commission_pre_meeting_date(1),
            "(Sunday 01 september 2019 (04H20), Pays des bisounours)",
        )
        self.assertEqual(
            view.format_commission_pre_meeting_date(2),
            "(Monday 02 september 2019 (04H20), Pays des merveilles)",
        )

    def test_get_commission_assembly(self):
        # Commissions are only present in council so we use it instead of college
        self.meetingConfig = self.meetingConfig2
        # Create the meeting and the view
        self.changeUser("pmManager")
        meeting = self.create("Meeting", date="2019/09/1 18:00:00")
        view = self._set_view(meeting)
        # Set pre-meeting assembly
        meeting.setPreMeetingAssembly("myAssembly")
        meeting.setPreMeetingAssembly_2("myAssembly 2")
        self.assertEqual(
            meeting.getPreMeetingAssembly(), view.get_commission_assembly(1)
        )
        self.assertEqual(
            meeting.getPreMeetingAssembly_2(), view.get_commission_assembly(2)
        )


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomViews, prefix='test_'))
    return suite
