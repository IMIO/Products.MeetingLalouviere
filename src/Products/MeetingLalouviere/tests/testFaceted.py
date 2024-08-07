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
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase


class testFaceted(MeetingLalouviereTestCase, mctf):
    """Tests the faceted navigation."""

    def _orgs_to_exclude_from_filter(self):
        return (self.direction_generale_uid,)


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testFaceted, prefix="test_"))
    return suite
