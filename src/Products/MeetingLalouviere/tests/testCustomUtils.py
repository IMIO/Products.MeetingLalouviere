# -*- coding: utf-8 -*-
#
# File: testCustomUtils.py
#
# Copyright (c) 2017 by Imio.be
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

from AccessControl import Unauthorized
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.MeetingCommunes.tests.testCustomUtils import testCustomUtils as mctcu


class testCustomUtils(mctcu, MeetingLalouviereTestCase):
    """
        Tests the Extensions/utils methods.
    """
    def test_ExportOrgs(self):
        """
          Check that calling this method returns the right content
        """
        self.changeUser('admin')
        expected = {
            'vendors': ('Vendors', '', u'Devil'),
            'endUsers': ('End users', '', u'EndUsers'),
            'direction-generale': ('Dg', '', u'Dg'),
            'developers': ('Developers', '', u'Devel')}
        res = self._exportOrgs()
        self.assertEqual(expected, res)

    def test_ImportOrgs(self):
        """
          Check that calling this method creates the organizations if not exist
        """
        self.changeUser('admin')
        # if we pass a dict containing the existing groups, it does nothing but
        # returning that the groups already exist
        data = self._exportOrgs()
        expected = 'Organization endUsers already exists\n' \
                   'Organization vendors already exists\n' \
                   'Organization developers already exists\n' \
                   'Organization direction-generale already exists'
        res = self._importOrgs(data)
        self.assertEqual(expected, res)
        # but it can also add an organization if it does not exist
        data['newGroup'] = ('New group title', 'New group description', 'NGAcronym', 'python:False')
        expected = 'Organization endUsers already exists\n' \
                   'Organization vendors already exists\n' \
                   'Organization newGroup added\n' \
                   'Organization direction-generale already exists\n' \
                   'Organization developers already exists'
        res = self._importOrgs(data)
        self.assertEqual(expected, res)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomUtils, prefix='test_'))
    return suite