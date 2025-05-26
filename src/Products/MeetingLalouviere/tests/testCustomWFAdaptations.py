# -*- coding: utf-8 -*-

from Products.MeetingCommunes.tests.testCustomWFAdaptations import testCustomWFAdaptations as mctcwfa
from Products.MeetingLalouviere.tests.MeetingLalouviereTestCase import MeetingLalouviereTestCase
from Products.MeetingLalouviere.utils import intref_group_uid


class testCustomWFAdaptations(mctcwfa, MeetingLalouviereTestCase):
    """ """

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
    suite.addTest(makeSuite(testCustomWFAdaptations, prefix="test_"))
    return suite
