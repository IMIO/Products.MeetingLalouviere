# -*- coding: utf-8 -*-

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)
from Products.MeetingCommunes.tests.testCustomMeeting import testCustomMeeting as mctcm


class testCustomMeeting(mctcm, MeetingLalouviereTestCase):
    """
        Tests the Meeting adapted methods
    """

    def test_getCategories(self):
        """
          Check what are returned while getting different types of categories
          This method is used in "meeting-config-council"
        """
        self.meetingConfig = self.meetingConfig2
        # add some "Suppl" categories
        self.changeUser("admin")
        supplCategories = [
            "deployment-1er-supplement",
            "maintenance-1er-supplement",
            "development-1er-supplement",
            "events-1er-supplement",
            "research-1er-supplement",
            "projects-1er-supplement",
            "marketing-1er-supplement",
            "subproducts-1er-supplement",
            "points-conseillers-2eme-supplement",
            "points-conseillers-3eme-supplement",
        ]
        for supplCat in supplCategories:
            self.create("meetingcategory", id=supplCat, title="supplCat")
        self.changeUser("pmManager")
        m = self.create("Meeting", date="2009/11/26 09:00:00")
        expectedNormal = [
            "deployment",
            "maintenance",
            "development",
            "events",
            "research",
            "projects",
            "marketing",
            "subproducts",
        ]
        self.assertEquals(m.getNormalCategories(), expectedNormal)

        expectedFirstSuppl = [
            "deployment-1er-supplement",
            "maintenance-1er-supplement",
            "development-1er-supplement",
            "events-1er-supplement",
            "research-1er-supplement",
            "projects-1er-supplement",
            "marketing-1er-supplement",
            "subproducts-1er-supplement",
        ]
        self.assertEquals(m.getFirstSupplCategories(), expectedFirstSuppl)
        expectedSecondSuppl = ["points-conseillers-2eme-supplement"]
        self.assertEquals(m.getSecondSupplCategories(), expectedSecondSuppl)
        expectedThirdSuppl = ["points-conseillers-3eme-supplement"]
        self.assertEquals(m.getThirdSupplCategories(), expectedThirdSuppl)

    def test_getAvailableItems(self):
        """
          Already tested in MeetingLaouviere.tests.testMeeting.py
        """
        pass

    def test_get_commission_classifiers_ids(self):
        """
        Test if commission classifiers are returned properly and accordingly with the meeting date.
        """

        self.meetingConfig = self.meetingConfig2

        classifiers = (
            "commission-cadre-de-vie-et-logement",
            "commission-finances-et-patrimoine",
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
            "commission-ag-1er-supplement",
            "commission-finances-1er-supplement",
            "commission-enseignement-1er-supplement",
            "commission-culture-1er-supplement",
            "commission-sport-1er-supplement",
            "commission-sante-1er-supplement",
            "commission-police-1er-supplement",
            "commission-cadre-de-vie-1er-supplement",
            "commission-patrimoine-1er-supplement",
            "commission-travaux-1er-supplement",
            "commission-speciale-1er-supplement",
        )

        self.changeUser("admin")

        for classifier in classifiers:
            self.create("meetingcategory", id=classifier, title="supplClf", is_classifier=True)

        self.changeUser("pmManager")
        meeting2009 = self.create("Meeting", date="2009/11/26 09:00:00")
        meeting2014 = self.create("Meeting", date="2014/11/26 09:00:00")
        meeting2019 = self.create("Meeting", date="2019/11/26 09:00:00")
        meeting2020 = self.create("Meeting", date="2020/11/26 09:00:00")
        meeting2050 = self.create("Meeting", date="2050/01/26 09:00:00")
        meeting2060 = self.create("Meeting", date="2060/12/26 09:00:00")

        self.maxDiff = None

        self.assertTupleEqual(
            meeting2009.adapted().get_commission_classifiers_ids(),
            (
                "commission-travaux",
                "commission-enseignement",
                "commission-cadre-de-vie-et-logement",
                "commission-ag",
                "commission-finances-et-patrimoine",
                "commission-police",
                "commission-speciale",
            ),
        )

        self.assertTupleEqual(
            meeting2014.adapted().get_commission_classifiers_ids(),
            (
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
            ),
        )

        self.assertTupleEqual(
            meeting2019.adapted().get_commission_classifiers_ids(),
            (
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
            ),
        )

        self.assertTupleEqual(
            meeting2020.adapted().get_commission_classifiers_ids(),
            (
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
            ),
        )

        self.assertTupleEqual(
            meeting2050.adapted().get_commission_classifiers_ids(),
            (
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
            ),
        )
        self.assertTupleEqual(
            meeting2060.adapted().get_commission_classifiers_ids(),
            (
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
            ),
        )


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomMeeting, prefix='test_'))
    return suite
