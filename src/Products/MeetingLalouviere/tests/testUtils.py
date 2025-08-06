# -*- coding: utf-8 -*-
#
# File: testUtils.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testUtils import testUtils as mctu
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testUtils(MeetingLalouviereTestCase, mctu):
    """ """

    def _default_permission_mail_recipents(self):
        return [
            u"M. Budget Impact Editor <budgetimpacteditor@plonemeeting.org>",
            u"M. PMCreator One <pmcreator1@plonemeeting.org>",
            u"M. PMCreator One bee <pmcreator1b@plonemeeting.org>",
            u"M. PMObserver One <pmobserver1@plonemeeting.org>",
            u"M. PMReviewer Level One <pmreviewerlevel1@plonemeeting.org>",
            u"M. PMReviewer Level Two <pmreviewerlevel2@plonemeeting.org>",
            u"M. PMReviewer One <pmreviewer1@plonemeeting.org>",
            u"M. Power Observer1 <powerobserver1@plonemeeting.org>",
            u"Site administrator <siteadmin@plonemeeting.org>",
            u"pmDirector1 <pmdirector1@plonemeeting.org>",
            u"pmDivisionHead1 <pmdivisionhead1@plonemeeting.org>",
            u"pmFollowup1 <pmfollowup1@plonemeeting.org>",
            u"pmOfficeManager1 <pmofficemanager1@plonemeeting.org>",
            u"pmServiceHead1 <pmservicehead1@plonemeeting.org>",
        ]

    def _modify_permission_mail_recipents(self):
        return [
            u"M. PMCreator One <pmcreator1@plonemeeting.org>",
            u"M. PMCreator One bee <pmcreator1b@plonemeeting.org>",
            u"M. PMReviewer Level One <pmreviewerlevel1@plonemeeting.org>",
            u"M. PMReviewer Level Two <pmreviewerlevel2@plonemeeting.org>",
            u"M. PMReviewer One <pmreviewer1@plonemeeting.org>",
            u"Site administrator <siteadmin@plonemeeting.org>",
            u"pmDirector1 <pmdirector1@plonemeeting.org>",
            u"pmDivisionHead1 <pmdivisionhead1@plonemeeting.org>",
            u"pmOfficeManager1 <pmofficemanager1@plonemeeting.org>",
            u"pmServiceHead1 <pmservicehead1@plonemeeting.org>",
        ]


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testUtils, prefix="test_"))
    return suite
