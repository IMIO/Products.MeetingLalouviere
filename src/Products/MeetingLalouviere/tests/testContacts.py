# -*- coding: utf-8 -*-
#
# File: testMeetingGroup.py
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
import os

import Products
from collective.contact.plonegroup.utils import get_own_organization
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.MeetingCommunes.tests.testContacts import testContacts as mctc
from Products.PloneMeeting.Extensions.imports import import_contacts


from plone import api


class testContacts(mctc, MeetingLalouviereTestCase):
    '''Tests the contacts related methods.'''

    def test_pm_ImportContactsCSV(self):
        """ """
        self.changeUser('pmManager')
        contacts = self.portal.contacts
        # initialy, we have 4 persons and 4 held_positions
        own_org = get_own_organization()
        self.assertIsNone(own_org.acronym)
        # 5 internal and 2 external organizations
        self.assertEqual(len(api.content.find(context=contacts, portal_type='organization')), 7)
        self.assertEqual(len(api.content.find(context=contacts, portal_type='person')), 4)
        self.assertEqual(len(api.content.find(context=contacts, portal_type='held_position')), 4)
        path = os.path.join(os.path.dirname(Products.PloneMeeting.__file__), 'profiles/testing')
        output = import_contacts(self.portal, path=path)
        self.assertEqual(output, 'You must be a zope manager to run this script')
        self.changeUser('siteadmin')
        output = import_contacts(self.portal, path=path)
        self.assertEqual(output, 'You must be a zope manager to run this script')

        # import contacts as Zope admin
        self.changeUser('admin')
        import_contacts(self.portal, path=path)
        # we imported 10 organizations and 15 persons/held_positions
        self.assertEqual(len(api.content.find(context=contacts, portal_type='organization')), 16)
        self.assertEqual(len(api.content.find(context=contacts, portal_type='person')), 19)
        self.assertEqual(len(api.content.find(context=contacts, portal_type='held_position')), 19)
        # organizations are imported with an acronym
        self.assertEqual(own_org.acronym, u'OwnOrg')
        org_gc = contacts.get('groupe-communes')
        self.assertEqual(org_gc.acronym, u'GComm')
        # hp of agent-interne is correctly linked to plonegroup-organization
        own_org = get_own_organization()
        agent_interne_hp = contacts.get('agent-interne').objectValues()[0]
        self.assertEqual(agent_interne_hp.portal_type, 'held_position')
        self.assertEqual(agent_interne_hp.get_organization(), own_org)
        # we can import organizations into another, we imported 4 orgs under my org
        self.assertListEqual(
            [org.id for org in own_org.objectValues()],
            ['developers',
             'vendors',
             'endUsers',
             'direction-generale',
             'service-1',
             'service-2',
             'service-associe-1',
             'service-associe-2'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testContacts, prefix='test_'))
    return suite
