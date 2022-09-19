# -*- coding: utf-8 -*-
#
# File: testFaceted.py
#
# Copyright (c) 2007-2015 by imio.be
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

from Products.MeetingCommunes.tests.testFaceted import testFaceted as mctf
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)

from imio.helpers.content import get_vocab
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class testFaceted(MeetingLalouviereTestCase, mctf):
    """Tests the faceted navigation."""

    def _orgs_to_exclude_from_filter(self):
        return (self.direction_generale_uid, )

    def test_pm_ProposingGroupsVocabularies(self):
        '''Test proposingGroup related cached vocabularies.'''
        self.changeUser('siteadmin')
        pmFolder = self.getMeetingFolder()
        vocab1 = get_vocab(
            pmFolder,
            "Products.PloneMeeting.vocabularies.proposinggroupsvocabulary",
            only_factory=True)
        vocab2 = get_vocab(
            pmFolder,
            "Products.PloneMeeting.vocabularies.everyorganizationsacronymsvocabulary",
            only_factory=True)
        vocab3 = get_vocab(
            pmFolder,
            "Products.PloneMeeting.vocabularies.proposinggroupsforfacetedfiltervocabulary",
            only_factory=True)
        vocab4 = get_vocab(
            pmFolder,
            "Products.PloneMeeting.vocabularies.associatedgroupsvocabulary",
            only_factory=True)
        # once get, it is cached
        self.assertEqual(len(vocab1(pmFolder)), 4)
        # contains My organization and external organizations
        self.assertEqual(len(vocab2(pmFolder)), 7)
        self.assertEqual(len(vocab3(pmFolder)), 4)
        # when nothing in config, just displays the orgs selected in plonegroup
        self.assertEqual(len(vocab4(pmFolder)), 3)

        # if we add/remove/edit an organozation, then the cache is cleaned
        # add an organization
        new_org = self.create('organization', title='NewOrg', acronym='N.O.')
        new_org_uid = new_org.UID()
        self._select_organization(new_org_uid)
        # cache was cleaned
        self.assertEqual(len(vocab1(pmFolder)), 5)
        self.assertEqual(len(vocab2(pmFolder)), 8)
        self.assertEqual(len(vocab3(pmFolder)), 5)
        self.assertEqual(len(vocab4(pmFolder)), 4)

        # edit a group
        self.assertEqual(vocab1(pmFolder).by_token[new_org_uid].title, new_org.Title())
        self.assertEqual(vocab2(pmFolder).by_token[new_org_uid].title, new_org.acronym)
        self.assertEqual(vocab3(pmFolder).by_token[new_org_uid].title, new_org.Title())
        self.assertEqual(vocab4(pmFolder).by_token[new_org_uid].title, new_org.Title())
        new_org.title = u'Modified title'
        new_org.acronym = u'Modified acronym'
        notify(ObjectModifiedEvent(new_org))
        # cache was cleaned
        self.assertEqual(vocab1(pmFolder).by_token[new_org_uid].title, new_org.Title())
        self.assertEqual(vocab2(pmFolder).by_token[new_org_uid].title, new_org.acronym)
        self.assertEqual(vocab3(pmFolder).by_token[new_org_uid].title, new_org.Title())
        self.assertEqual(vocab4(pmFolder).by_token[new_org_uid].title, new_org.Title())

        # remove an organization (unselect it first)
        self._select_organization(new_org_uid, remove=True)
        self.portal.restrictedTraverse('@@delete_givenuid')(new_org_uid)
        # cache was cleaned
        self.assertEqual(len(vocab1(pmFolder)), 4)
        self.assertEqual(len(vocab2(pmFolder)), 7)
        self.assertEqual(len(vocab3(pmFolder)), 4)
        self.assertEqual(len(vocab4(pmFolder)), 3)
        # activate "End users"
        self.assertEqual(
            [term.title for term in vocab1(pmFolder)],
            [u'Developers', u'Dg', u'Vendors', u'End users (Inactive)'])
        self.assertEqual(
            [term.title for term in vocab2(pmFolder)],
            [u'None', u'Devel', u'Devil', u'EndUsers', u'Dg', u'OrgOutside1', u'OrgOutside2'])
        self.assertEqual(
            [term.title for term in vocab3(pmFolder)],
            [u'Developers', u'Dg', u'Vendors', u'End users (Inactive)'])
        self.assertEqual(
            [term.title for term in vocab4(pmFolder)],
            [u'Developers', u'Dg', u'Vendors'])
        self._select_organization(self.endUsers_uid)
        self.assertEqual(
            [term.title for term in vocab1(pmFolder)],
            [u'Developers', u'Dg', u'End users', u'Vendors'])
        self.assertEqual(
            [term.title for term in vocab2(pmFolder)],
            [u'None', u'Devel', u'Devil', u'EndUsers', u'Dg', u'OrgOutside1', u'OrgOutside2'])
        self.assertEqual(
            [term.title for term in vocab3(pmFolder)],
            [u'Developers', u'Dg', u'End users', u'Vendors'])
        self.assertEqual(
            [term.title for term in vocab4(pmFolder)],
            [u'Developers', u'Dg', u'End users', u'Vendors'])


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testFaceted, prefix="test_"))
    return suite
