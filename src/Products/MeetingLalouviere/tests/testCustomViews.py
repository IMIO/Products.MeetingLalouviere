# -*- coding: utf-8 -*-

from Products.MeetingCommunes.tests.testCustomViews import testCustomViews as mctcv
from Products.MeetingLalouviere.config import (
    COUNCIL_MEETING_COMMISSION_IDS_2020,
    COUNCIL_MEETING_COMMISSION_IDS_2019,
    COUNCIL_MEETING_COMMISSION_IDS_2013,
    COUNCIL_COMMISSION_IDS,
)
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)

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

    def _setup_commissions_classifiers(self, commission_version):
        # add MEETING_COMMISSION's classifiers
        self.changeUser("admin")

        # wipe all previous classifiers
        ids = self.meetingConfig.classifiers.keys()
        if len(ids) > 0:
            ids = list(ids)
            self.meetingConfig.classifiers.manage_delObjects(ids)

        # flatten commission_version
        commission_classifiers = []
        for i in commission_version:
            if isinstance(i, tuple):
                for j in i:
                    commission_classifiers.append(j)
            else:
                commission_classifiers.append(i)

        # create 1st-supplement for each classifier
        commission_classifiers = commission_classifiers + [
            classifier + "-1er-supplement" for classifier in commission_classifiers
        ]

        # add classifiers to the meetingConfig
        for classifier in commission_classifiers:
            self.create("meetingcategory", id=classifier, title="commissionClf", is_classifier=True)

    def _test_get_commission_items_by_date(self, year, month, day):
        # Create a meeting with a given year and month and the view
        self.changeUser("pmManager")
        meeting = self.create(
            "Meeting", date="{}/{}/{} 18:00:00".format(year, month, day)
        )
        view = self._set_view(meeting)
        # Creates items needed for the test
        item = self.create("MeetingItem")
        item.setClassifier(view.get_classifiers_for_commission(1)[0])  # First commission
        item2 = self.create("MeetingItem")
        item2.setClassifier(view.get_classifiers_for_commission(2)[0])  # Second commission
        item3 = self.create("MeetingItem")
        item3.setClassifier(view.get_classifiers_for_commission(2)[0])  # Third commission

        item_s = self.create("MeetingItem")
        item_s.setClassifier(
            view.get_classifiers_for_commission(1)[0] + "-1er-supplement"
        )  # First commission, 1st supp
        item2_s = self.create("MeetingItem")
        item2_s.setClassifier(
            view.get_classifiers_for_commission(2)[0] + "-1er-supplement"
        )  # Second commission, 1st supp
        item3_s = self.create("MeetingItem")
        item3_s.setClassifier(
            view.get_classifiers_for_commission(2)[0] + "-1er-supplement"
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
                "commissions": COUNCIL_MEETING_COMMISSION_IDS_2020,
                "year": 2999,
                "month": 9,
                "day": 30,
            },
            {
                "commissions": COUNCIL_MEETING_COMMISSION_IDS_2020,
                "year": 2020,
                "month": 9,
                "day": 1,
            },
            {
                "commissions": COUNCIL_MEETING_COMMISSION_IDS_2019,
                "year": 2020,
                "month": 8,
                "day": 31,
            },
            {
                "commissions": COUNCIL_MEETING_COMMISSION_IDS_2019,
                "year": 2019,
                "month": 9,
                "day": 1,
            },
            {
                "commissions": COUNCIL_MEETING_COMMISSION_IDS_2013,
                "year": 2013,
                "month": 6,
                "day": 1,
            },
            {
                "commissions": COUNCIL_COMMISSION_IDS,
                "year": 2010,
                "month": 1,
                "day": 1,
            },
        ]
        for cv in commissions_versions:
            self._setup_commissions_classifiers(cv["commissions"])
            self._test_get_commission_items_by_date(cv["year"], cv["month"], cv["day"])

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

        for date in (
            "2019/09/1 18:00:00",
            "2020/09/1 18:00:00",
        ):
            meeting = self.create("Meeting", date=date)
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
    suite.addTest(makeSuite(testCustomViews, prefix="test_"))
    return suite
