# -*- coding: utf-8 -*-
#
# File: testViews.py
#
# GNU General Public License (GPL)
#

from plone import api
from Products.MeetingCommunes.tests.testViews import testViews as mctv
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testViews(MeetingLalouviereTestCase, mctv):
    """ """

    def _display_user_groups_sub_groups_false(self):
        return [
            (1, api.user.get("pmCreator1")),
            (1, api.user.get("pmCreator1b")),
            (1, api.user.get("pmManager")),
            (0, api.user.get("pmFollowup1")),
            (0, api.user.get("pmObserver1")),
            (0, api.user.get("pmReviewer1")),
        ]

    def _display_user_groups_sub_groups_true(self):
        return [
            (1, api.group.get(self.developers_creators)),
            (2, api.user.get("pmCreator1")),
            (2, api.user.get("pmCreator1b")),
            (2, api.user.get("pmManager")),
            (0, api.user.get("pmFollowup1")),
            (0, api.user.get("pmManager")),
            (0, api.user.get("pmObserver1")),
            (0, api.user.get("pmReviewer1")),
        ]

    def test_pm_UpdateProposingGroupBatchActionForm(self):
        """Define a not selected group in charge for "direction-generale-validation"
           and "referent-integrite" so they are not in the vocabulary."""
        self.direction_generale_validation.groups_in_charge = (self.endUsers_uid, )
        self.referent_integrite.groups_in_charge = (self.endUsers_uid, )
        super(testViews, self).test_pm_UpdateProposingGroupBatchActionForm()


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testViews, prefix="test_"))
    return suite
