# -*- coding: utf-8 -*-
#
# File: testAdvices.py
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

from AccessControl import Unauthorized
from zope.schema.interfaces import RequiredMissing

from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import createContentInContainer

from Products.CMFCore.permissions import View

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.MeetingCommunes.tests.testAdvices import testAdvices as mcta


class testAdvices(MeetingLalouviereTestCase, mcta):
    '''Tests various aspects of advices management.
       Advices are enabled for PloneGov Assembly, not for PloneMeeting Assembly.'''

    def test_subproduct_call_AddEditDeleteAdvices(self):
        '''This is a copy/paste from test in PloneMeeting, just look the XXX MeetingLalouviere,
           this is for PM 3.2 and is fixed in PM 3.3...'''
        # creator for group 'developers'
        self.changeUser('pmCreator1')
        # create an item and ask the advice of group 'vendors'
        data = {
            'title': 'Item to advice',
            'category': 'maintenance'
        }
        item1 = self.create('MeetingItem', **data)
        self.assertEquals(item1.displayAdvices(), False)
        item1.setOptionalAdvisers(('vendors',))
        item1.at_post_edit_script()
        self.assertEquals(item1.displayAdvices(), True)
        # 'pmCreator1' has no addable nor editable advice to give
        self.assertEquals(item1.getAdvicesGroupsInfosForUser(), ([], []))
        self.changeUser('pmReviewer2')
        self.failIf(self.hasPermission(View, item1))
        self.changeUser('pmCreator1')
        self.proposeItem(item1)
        # a user able to View the item can not add an advice, even if he tries...
        self.assertRaises(Unauthorized,
                          createContentInContainer,
                          item1,
                          'meetingadvice')
        self.assertEquals(item1.getAdvicesGroupsInfosForUser(), ([], []))
        self.changeUser('pmReviewer2')
        # 'pmReviewer2' has one advice to give for 'vendors' and no advice to edit
        self.assertEquals(item1.getAdvicesGroupsInfosForUser(), ([('vendors', u'Vendors')], []))
        self.assertEquals(item1.hasAdvices(), False)
        # fields 'advice_type' and 'advice_group' are mandatory
        form = item1.restrictedTraverse('++add++meetingadvice').form_instance
        form.update()
        errors = form.extractData()[1]
        self.assertEquals(errors[0].error, RequiredMissing('advice_group'))
        self.assertEquals(errors[1].error, RequiredMissing('advice_type'))
        # value used for 'advice_type' and 'advice_group' must be correct
        form.request.set('form.widgets.advice_type', u'wrong_value')
        errors = form.extractData()[1]
        self.assertEquals(errors[1].error, RequiredMissing('advice_type'))
        # but if the value is correct, the field renders correctly
        form.request.set('form.widgets.advice_type', u'positive')
        data = form.extractData()[0]
        self.assertEquals(data['advice_type'], u'positive')
        # regarding 'advice_group' value, only correct are the ones in the vocabulary
        # so using another will fail, for example, can not give an advice for another group
        form.request.set('form.widgets.advice_group', self.portal.portal_plonemeeting.developers.getId())
        data = form.extractData()[0]
        self.assertFalse('advice_group' in data)
        # we can use the values from the vocabulary
        vocab = form.widgets.get('advice_group').terms.terms
        self.failUnless('vendors' in vocab)
        self.failUnless(len(vocab) == 1)
        # give the advice, select a valid 'advice_group' and save
        form.request.set('form.widgets.advice_group', u'vendors')
        # the 3 fields 'advice_group', 'advice_type' and 'advice_comment' are handled correctly
        data = form.extractData()[0]
        # XXX begin change by MeetingLalouviere, we added field 'advice_comment'
        self.assertTrue('advice_group' in data and
                        'advice_type' in data and
                        'advice_comment' in data and
                        'advice_reference' in data and
                        'advice_row_id' in data and
                        'advice_observations' in data and
                        'advice_hide_during_redaction' in data)
        self.assertTrue(len(data) == 7)
        # XXX end change by MeetingLalouviere, we added field 'advice_comment'
        form.request.form['advice_group'] = u'vendors'
        form.request.form['advice_type'] = u'positive'
        form.request.form['advice_comment'] = RichTextValue(u'My comment')
        form.createAndAdd(form.request.form)
        self.assertEquals(item1.hasAdvices(), True)
        # 'pmReviewer2' has no more addable advice (as already given) but has now an editable advice
        self.assertEquals(item1.getAdvicesGroupsInfosForUser(), ([], ['vendors']))
        # given advice is correctly stored
        self.assertEquals(item1.adviceIndex['vendors']['type'], 'positive')
        self.assertEquals(item1.adviceIndex['vendors']['comment'], u'My comment')
        self.changeUser('pmReviewer1')
        self.validateItem(item1)
        # now 'pmReviewer2' can't add (already given) an advice
        # but he can still edit the advice he just gave
        self.changeUser('pmReviewer2')
        self.failUnless(self.hasPermission(View, item1))
        self.assertEquals(item1.getAdvicesGroupsInfosForUser(), ([], ['vendors', ]))
        given_advice = getattr(item1, item1.adviceIndex['vendors']['advice_id'])
        self.failUnless(self.hasPermission('Modify portal content', given_advice))
        # another member of the same _advisers group may also edit the given advice
        self.changeUser('pmManager')
        self.assertEquals(item1.getAdvicesGroupsInfosForUser(), ([], ['vendors', ]))
        self.failUnless(self.hasPermission('Modify portal content', given_advice))
        # if a user that can not remove the advice tries he gets Unauthorized
        self.changeUser('pmReviewer1')
        self.assertRaises(Unauthorized, item1.restrictedTraverse('@@delete_givenuid'), item1.meetingadvice.UID())
        # put the item back in a state where 'pmReviewer2' can remove the advice
        self.changeUser('pmManager')
        self.backToState(item1, self.WF_STATE_NAME_MAPPINGS['proposed'])
        self.changeUser('pmReviewer2')
        # remove the advice
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        self.assertEquals(item1.getAdvicesGroupsInfosForUser(), ([('vendors', u'Vendors')], []))
        # remove the fact that we asked the advice
        self.changeUser('pmManager')
        item1.setOptionalAdvisers([])
        item1.at_post_edit_script()
        self.changeUser('pmReviewer2')
        self.assertEquals(item1.getAdvicesGroupsInfosForUser(), ([], []))

    def test_subproduct_call_MayTriggerGiveAdviceWhenItemIsBackToANotViewableState(self):
        """test"""
        mcta.test_pm_MayTriggerGiveAdviceWhenItemIsBackToANotViewableState(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAdvices, prefix='test_subproduct_'))
    return suite
