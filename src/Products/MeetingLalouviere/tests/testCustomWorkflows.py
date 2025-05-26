# -*- coding: utf-8 -*-
#
# File: testWorkflows.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testCustomWorkflows import testCustomWorkflows as mctcw
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.MeetingLalouviere.utils import intref_group_uid


class testCustomWorkflows(mctcw, MeetingLalouviereTestCase):
    """Tests the default workflows implemented in PloneMeeting."""

    def test_IntegrityReferentWorkflow(self):
        """For the "referent-integrite" group, there is only 3 validation levels:
           - "itemcreated";
           - "proposed_to_director";
           - "validated".
           We especially do not have the "proposed_to_dg" WF state.
        """
        self._activate_wfas(('item_validation_shortcuts', ))
        self.changeUser('pmCreator2')
        item = self.create('MeetingItem', proposingGroup=intref_group_uid())
        self.assertEqual(self.transitions(item), ['proposeToDirector'])
        self.do(item, 'proposeToDirector')
        self.assertEqual(item.query_state(), 'proposed_to_director')
        self.assertEqual(self.transitions(item), [])
        self.changeUser('pmDirector2')
        self.assertEqual(self.transitions(item), ['backToItemCreated', 'validate'])
        self.do(item, 'validate')
        self.assertEqual(item.query_state(), 'validated')
        self.changeUser('pmManager')
        self.assertEqual(self.transitions(item), ['backToItemCreated', 'backToProposedToDirector'])


def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testCustomWorkflows, prefix="test_"))
    return suite
