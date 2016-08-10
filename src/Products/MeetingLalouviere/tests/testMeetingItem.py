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

from DateTime import DateTime

from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.MeetingCommunes.tests.testMeetingItem import testMeetingItem as mctmi
from Products.MeetingLalouviere.config import FINANCE_GROUP_ID
from Products.PloneMeeting.config import POWEROBSERVERS_GROUP_SUFFIX
from Products.PloneMeeting.utils import ON_TRANSITION_TRANSFORM_TAL_EXPR_ERROR
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.permissions import View
from plone import api
from plone.app.textfield.value import RichTextValue


class testMeetingItem(MeetingLalouviereTestCase, mctmi):
    """
        Tests the MeetingItem class methods.
    """

    def test_subproduct_call_PowerObserversLocalRoles(self):
        '''Check that powerobservers local roles are set correctly...
           Test alternatively item or meeting that is accessible to and not...'''
        # we will check that (restricted) power observers local roles are set correctly.
        # - powerobservers may access itemcreated, validated and presented items (and created meetings),
        #   not restricted power observers;
        # - frozen items/meetings are accessible by both;
        # - only restricted power observers may access 'refused' items.
        self.meetingConfig.setItemPowerObserversStates(('itemcreated', 'validated', 'presented',
                                                       'itemfrozen', 'accepted', 'delayed'))
        self.meetingConfig.setMeetingPowerObserversStates(('created', 'frozen', 'decided', 'closed'))
        self.meetingConfig.setItemRestrictedPowerObserversStates(('itemfrozen', 'accepted', 'refused'))
        self.meetingConfig.setMeetingRestrictedPowerObserversStates(('frozen', 'decided', 'closed'))
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        item.setDecision("<p>Decision</p>")
        # itemcreated item is accessible by powerob, not restrictedpowerob
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        # propose the item, it is no more visible to any powerob
        self.proposeItem(item)
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.changeUser('powerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        # validate the item, only accessible to powerob
        self.validateItem(item)
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        # present the item, only viewable to powerob, including created meeting
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date='2015/01/01')
        self.presentItem(item)
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.assertFalse(self.hasPermission(View, meeting))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        # frozen items/meetings are accessible by both powerobs
        self.freezeMeeting(meeting)
        self.assertTrue(item.queryState() == 'itemfrozen')
        self.changeUser('restrictedpowerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        # decide the meeting and refuse the item, meeting accessible to both
        # but refused item only accessible to restricted powerob
        self.decideMeeting(meeting)
        self.changeUser('admin')  # only admin can refuse item
        self.do(item, 'refuse')
        self.changeUser('restrictedpowerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        self.changeUser('powerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))

    def test_subproduct_call_OnTransitionFieldTransforms(self):
        '''On transition triggered, some transforms can be applied to item or meeting
           rich text field depending on what is defined in MeetingConfig.onTransitionFieldTransforms.
           This is used for example to adapt the text of the decision when an item is delayed or refused.
           '''
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems()
        self.decideMeeting(meeting)
        # we will adapt item decision when the item is delayed
        item1 = meeting.getItems()[0]
        originalDecision = '<p>Current item decision.</p>'
        item1.setDecision(originalDecision)
        # for now, as nothing is defined, nothing happens when item is delayed
        self.changeUser('admin')  # for ll, only real manager can delay an item
        self.do(item1, 'delay')
        self.assertTrue(item1.getDecision(keepWithNext=False) == originalDecision)
        # configure onTransitionFieldTransforms and delay another item
        delayedItemDecision = '<p>This item has been delayed.</p>'
        self.meetingConfig.setOnTransitionFieldTransforms(
            ({'transition': 'delay',
              'field_name': 'MeetingItem.decision',
              'tal_expression': 'string:%s' % delayedItemDecision},))
        item2 = meeting.getItems()[1]
        item2.setDecision(originalDecision)
        self.do(item2, 'delay')
        self.assertTrue(item2.getDecision(keepWithNext=False) == delayedItemDecision)
        # if the item was duplicated (often the case when delaying an item), the duplicated
        # item keep the original decision
        duplicatedItem = item2.getBRefs('ItemPredecessor')[0]
        # right duplicated item
        self.assertTrue(duplicatedItem.getPredecessor() == item2)
        self.assertTrue(duplicatedItem.getDecision(keepWithNext=False) == originalDecision)
        # this work also when triggering any other item or meeting transition with every rich fields
        item3 = meeting.getItems()[2]
        self.meetingConfig.setOnTransitionFieldTransforms(
            ({'transition': 'accept',
              'field_name': 'MeetingItem.description',
              'tal_expression': 'string:<p>My new description.</p>'},))
        item3.setDescription('<p>My original description.</p>')
        self.do(item3, 'accept')
        self.assertTrue(item3.Description() == '<p>My new description.</p>')
        # if ever an error occurs with the TAL expression, the transition
        # is made but the rich text is not changed and a portal_message is displayed
        self.meetingConfig.setOnTransitionFieldTransforms(
            ({'transition': 'accept',
              'field_name': 'MeetingItem.decision',
              'tal_expression': 'some_wrong_tal_expression'},))
        item4 = meeting.getItems()[3]
        item4.setDecision('<p>My decision that will not be touched.</p>')
        self.do(item4, 'accept')
        # transition was triggered
        self.assertTrue(item4.queryState() == 'accepted')
        # original decision was not touched
        self.assertTrue(item4.getDecision(keepWithNext=False) == '<p>My decision that will not be touched.</p>')
        # a portal_message is displayed to the user that triggered the transition
        messages = IStatusMessage(self.request).show()
        self.assertTrue(messages[0].message == ON_TRANSITION_TRANSFORM_TAL_EXPR_ERROR % ('decision',
                                                                                         "'some_wrong_tal_expression'"))

    def test_subproduct_call_IsPrivacyViewable(self):
        '''
          Original test, see doc string in PloneMeeting.
          Here, as soon as a user can access an item, the item isPrivacyViewable.
          See adapters.isPrivacyViewable overrided method.
        '''
        self.setMeetingConfig(self.meetingConfig2.getId())
        # we will use the copyGroups to check who can fully access item and who can not
        self.meetingConfig.setItemCopyGroupsStates(('presented', ))
        # make powerobserver1 a PowerObserver
        self.portal.portal_groups.addPrincipalToGroup('powerobserver1', '%s_%s' %
                                                      (self.meetingConfig.getId(), POWEROBSERVERS_GROUP_SUFFIX))
        # create a 'public' and a 'secret' item
        self.changeUser('pmManager')
        # add copyGroups that check that 'external' viewers can access the item but not isPrivacyViewable
        publicItem = self.create('MeetingItem')
        publicItem.setCategory('development')
        publicItem.setCopyGroups('vendors_reviewers')
        publicItem.reindexObject()
        secretItem = self.create('MeetingItem')
        secretItem.setPrivacy('secret')
        secretItem.setCategory('development')
        secretItem.setCopyGroups('vendors_reviewers')
        secretItem.reindexObject()
        self.create('Meeting', date=DateTime('2013/06/01 08:00:00'))
        self.presentItem(publicItem)
        self.presentItem(secretItem)
        # log in as a user that is in copyGroups
        self.changeUser('pmReviewer2')
        member = self.portal.portal_membership.getAuthenticatedMember()
        # the user can see the item because he is in the copyGroups
        # not because he is in the same proposing group
        secretItemPloneGroupsOfProposingGroup = getattr(self.tool,
                                                        secretItem.getProposingGroup()).getPloneGroups(idsOnly=True)
        self.failIf(set(secretItemPloneGroupsOfProposingGroup).intersection
                    (set(self.portal.portal_groups.getGroupsForPrincipal(member))))
        # pmReviewer2 can access the item and isPrivacyViewable
        self.failUnless(self.hasPermission('View', secretItem))
        self.failUnless(self.hasPermission('View', publicItem))
        # XXX Begin change for MeetingLalouviere
        self.failUnless(secretItem.isPrivacyViewable())
        # XXX End change for MeetingLalouviere
        self.failUnless(publicItem.isPrivacyViewable())
        # a user in the same proposingGroup can fully access the secret item
        self.changeUser('pmCreator1')
        self.failUnless(secretItem.isPrivacyViewable())
        self.failUnless(publicItem.isPrivacyViewable())
        # MeetingManager
        self.changeUser('pmManager')
        self.failUnless(secretItem.isPrivacyViewable())
        self.failUnless(publicItem.isPrivacyViewable())
        # PowerObserver
        self.changeUser('powerobserver1')
        self.failUnless(secretItem.isPrivacyViewable())
        self.failUnless(publicItem.isPrivacyViewable())

    def test_subproduct_call_GetDeliberation(self):
        '''Test the custom getDeliberation from MeetingLalouviere.'''
        self.changeUser('admin')
        cfg = self.meetingConfig
        self._configureFinancesAdvice(cfg)
        groupsTool = api.portal.get_tool('portal_groups')
        groupsTool.addPrincipalToGroup('pmReviewer2', '%s_advisers' % FINANCE_GROUP_ID)
        finances = getattr(self.tool, FINANCE_GROUP_ID)
        finances.setItemAdviceStates(("%s__state__%s" % (cfg.getId(),
                                                         self.WF_STATE_NAME_MAPPINGS['proposed'])))
        finances.setItemAdviceEditStates(("%s__state__%s" % (cfg.getId(),
                                                             self.WF_STATE_NAME_MAPPINGS['proposed'])))
        finances.setItemAdviceViewStates(("%s__state__%s" % (cfg.getId(),
                                                             self.WF_STATE_NAME_MAPPINGS['proposed'])))

        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        item.setMotivation('<p>My motivation</p>')
        item.setDecision('<p>My decision</p>')
        self.assertTrue(item.getDeliberation() == item.getMotivation() + item.getDecision())
        # if p_withFinanceAdvice is True, we add some legal bullshit + the advice's comment.
        item.at_post_edit_script()
        self.changeUser('pmReviewer2')
        item.setOptionalAdvisers((FINANCE_GROUP_ID,))
        item.at_post_edit_script()
        self.proposeItem(item)
        form = item.restrictedTraverse('++add++meetingadvice').form_instance
        form.update()
        form.request.set('form.widgets.advice_type', u'positive')
        form.request.set('form.widgets.advice_group', FINANCE_GROUP_ID)
        form.request.form['advice_group'] = FINANCE_GROUP_ID
        form.request.form['advice_comment'] = RichTextValue('<p>My comment</p>')
        form.createAndAdd(form.request.form)
        expected = item.getMotivation() +\
            "<p>Vu l'avis du Directeur financier repris ci-dessous ainsi qu'en annexe :</p><p>My comment</p>" +\
            item.getDecision()
        self.assertEqual(expected, item.getDeliberation(withFinanceAdvice=True))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_subproduct_'))
    return suite
