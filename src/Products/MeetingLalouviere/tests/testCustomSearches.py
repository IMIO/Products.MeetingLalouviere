from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)
from collective.compoundcriterion.interfaces import ICompoundCriterionFilter
from imio.helpers.cache import cleanRamCacheFor
from zope.component import getAdapter


class testCustomSearches(MeetingLalouviereTestCase):
    """

    """
    def test_pm_SearchItemsOfMyCommissions(self):
        self.add_commission_plone_groups()
        """Test the 'items-of-my-commissions' adapter that returns items using category
         if it matches the right commissions for the user."""
        cfg = self.meetingConfig2
        itemTypeName = cfg.getItemTypeName()

        # siteadmin is not member of any commissions.
        adapter = getAdapter(
            cfg, ICompoundCriterionFilter, name="items-of-my-commissions"
        )
        self.changeUser("siteadmin")
        self.assertEqual(
            adapter.query,
            {"portal_type": {"query": itemTypeName}, "getRawClassifier": {"query": []}},
        )

        # commissioneditor is member of 'commission-ag'
        self.changeUser("commissioneditor")
        cleanRamCacheFor(
            "Products.MeetingLalouviere.adapters.query_itemsofmycommissions"
        )
        self.assertEqual(
            adapter.query,
            {
                "portal_type": {"query": "MeetingItemCouncil"},
                "getRawClassifier": {
                    "query": ["commission-ag", "commission-ag-1er-supplement"]
                },
            },
        )

        self.changeUser("commissioneditor2")
        cleanRamCacheFor(
            "Products.MeetingLalouviere.adapters.query_itemsofmycommissions"
        )
        self.assertDictEqual(
            adapter.query,
            {
                "portal_type": {"query": "MeetingItemCouncil"},
                "getRawClassifier": {
                    "query": [
                        "commission-patrimoine",
                        "commission-patrimoine-1er-supplement"
                    ]
                },
            },
        )

        self.changeUser("pmManager")
        cleanRamCacheFor(
            "Products.MeetingLalouviere.adapters.query_itemsofmycommissions"
        )
        self.assertDictEqual(
            adapter.query,
            {
                "portal_type": {"query": "MeetingItemCouncil"},
                "getRawClassifier": {
                    "query": []
                },
            },
        )


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomSearches, prefix='test_'))
    return suite
