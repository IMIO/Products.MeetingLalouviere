# -*- coding: utf-8 -*-
#
# File: testMeetingItem.py
#
# Copyright (c) 2007-2012 by CommunesPlone.org
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

from Products.MeetingCommunes.tests.testMeetingItem import testMeetingItem as mctmi
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import (
    MeetingLalouviereTestCase,
)

from imio.helpers.cache import cleanRamCache
from imio.helpers.content import get_vocab
from plone import api
from plone.app.testing.bbb import _createMemberarea


class testMeetingItem(MeetingLalouviereTestCase, mctmi):
    """
        Tests the MeetingItem class methods.
    """

    def _extraNeutralFields(self):
        """This method is made to be overrided by subplugins that added
           neutral fields to the MeetingItem schema."""
        return ["followUp", "neededFollowUp", "providedFollowUp"]

    def _get_developers_all_reviewers_groups(self):
        return [self.developers_officemanagers,
                self.developers_serviceheads,
                self.developers_divisionheads,
                self.developers_directors,
                self.developers_reviewers,
                self.developers_alderman]

    def _users_to_remove_for_mailling_list(self):
        return ['pmAlderman1',
                'pmDirector1',
                'pmDivisionHead1',
                'pmDivisionHead1',
                'pmOfficeManager1',
                'pmServiceHead1',
                'pmFollowup1',
                'pmBudgetReviewer1',
                'pmBudgetReviewer2',
                'pmAlderman2',
                'pmDirector2',
                'pmDivisionHead2',
                'pmFollowup2',
                'pmOfficeManager2',
                'pmServiceHead2',
                'pmDg'
                ]

    def test_pm_AssociatedGroupsVocabulary(self):
        '''MeetingItem.associatedGroups vocabulary.'''
        self.changeUser('pmManager')
        # create an item to test the vocabulary
        item = self.create('MeetingItem')
        self.assertListEqual(item.Vocabulary('associatedGroups')[0].keys(),
                             [self.developers_uid, self.direction_generale_uid, self.vendors_uid])
        # now select the 'developers' as associatedGroup for the item
        item.setAssociatedGroups((self.developers_uid,))
        # still the complete vocabulary
        self.assertListEqual(item.Vocabulary('associatedGroups')[0].keys(),
                             [self.developers_uid, self.direction_generale_uid, self.vendors_uid])
        # disable developers organization
        self.changeUser('admin')
        self._select_organization(self.developers_uid, remove=True)
        self.changeUser('pmManager')
        # still in the vocabulary because selected on the item
        # but added at the end of the vocabulary
        self.assertListEqual(item.Vocabulary('associatedGroups')[0].keys(),
                             [self.direction_generale_uid, self.vendors_uid, self.developers_uid])
        # unselect 'developers' on the item, it will not appear anymore in the vocabulary
        item.setAssociatedGroups(())
        cleanRamCache()
        self.assertListEqual(item.Vocabulary('associatedGroups')[0].keys(),
                             [self.direction_generale_uid, self.vendors_uid, ])
        # 'associatedGroups' may be selected in 'MeetingConfig.ItemFieldsToKeepConfigSortingFor'
        cfg = self.meetingConfig
        cfg.setOrderedAssociatedOrganizations((self.vendors_uid, self.developers_uid, self.endUsers_uid))
        # sorted alphabetically by default
        self.assertFalse('associatedGroups' in cfg.getItemFieldsToKeepConfigSortingFor())
        cleanRamCache()
        self.assertListEqual(item.Vocabulary('associatedGroups')[0].keys(),
                             [self.developers_uid, self.endUsers_uid, self.vendors_uid, ])
        cfg.setItemFieldsToKeepConfigSortingFor(('associatedGroups',))
        cleanRamCache()
        self.assertListEqual(item.Vocabulary('associatedGroups')[0].keys(),
                             list(cfg.getOrderedAssociatedOrganizations()))
        # when nothing defined in MeetingConfig.orderedAssociatedOrganizations
        # so when selected organizations displayed, sorted alphabetically
        cfg.setOrderedAssociatedOrganizations(())
        cleanRamCache()
        self.assertListEqual(item.Vocabulary('associatedGroups')[0].keys(),
                             [self.direction_generale_uid, self.vendors_uid])
        self._select_organization(self.developers_uid)
        self._select_organization(self.endUsers_uid)
        cleanRamCache()
        self.assertListEqual(item.Vocabulary('associatedGroups')[0].keys(),
                             [self.developers_uid, self.direction_generale_uid, self.endUsers_uid, self.vendors_uid])

    def test_pm_ItemProposingGroupsVocabulary(self):
        '''Check MeetingItem.proposingGroup vocabulary.'''
        # test that if a user is cretor for a group but only reviewer for
        # another, it only returns the groups the user is creator for...  This
        # test the bug of ticket #643
        # adapt the pmReviewer1 user : add him to a creator group and create is
        # personal folder.
        self.changeUser('admin')
        # pmReviser1 is member of developer_reviewers and developers_observers
        # add him to a creator group different from his reviwer group
        vendors_creators = api.group.get(self.vendors_creators)
        vendors_creators.addMember('pmReviewer1')
        # create his personal area because he is a creator now
        _createMemberarea(self.portal, 'pmReviewer1')
        self.changeUser('pmReviewer1')
        item = self.create('MeetingItem')
        vocab = get_vocab(
            item, "Products.PloneMeeting.vocabularies.userproposinggroupsvocabulary", only_factory=True)
        self.assertEqual(vocab(item).by_value.keys(), [self.vendors_uid, ])
        # a 'Manager' will be able to select any proposing group
        # no matter he is a creator or not
        self.changeUser('admin')
        self.assertEqual([term.value for term in vocab(item)._terms],
                         [self.developers_uid, self.direction_generale_uid, self.vendors_uid, ])
        # if 'developers' was selected on the item, it will be available to 'pmReviewer1'
        item.setProposingGroup(self.developers_uid)
        self.changeUser('pmReviewer1')
        self.assertEqual([term.value for term in vocab(item)._terms],
                         [self.developers_uid, self.vendors_uid, ])

    def test_pm_ItemProposingGroupsVocabularyKeepConfigSorting(self):
        """If 'proposingGroup' selected in MeetingConfig.itemFieldsToKeepConfigSortingFor,
           the vocabulary keeps config order, not sorted alphabetically."""
        cfg = self.meetingConfig
        # activate endUsers group
        self.changeUser('siteadmin')
        self._select_organization(self.endUsers_uid)
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        vocab = get_vocab(
            item, "Products.PloneMeeting.vocabularies.userproposinggroupsvocabulary", only_factory=True)
        self.changeUser('siteadmin')
        # not in itemFieldsToKeepConfigSortingFor for now
        self.assertFalse('proposingGroup' in cfg.getItemFieldsToKeepConfigSortingFor())
        self.assertListEqual([term.value for term in vocab(item)._terms],
                         [self.developers_uid, self.direction_generale_uid, self.endUsers_uid, self.vendors_uid])
        cfg.setItemFieldsToKeepConfigSortingFor(('proposingGroup', ))
        # invalidate vocabularies caching
        cfg.at_post_edit_script()
        self.assertListEqual([term.value for term in vocab(item)._terms],
                         [self.developers_uid, self.vendors_uid, self.direction_generale_uid, self.endUsers_uid])

    def _reviewers_may_edit_itemcreated(self):
        return True


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from mctmi
    suite.addTest(makeSuite(testMeetingItem, prefix="test_"))
    return suite
