# -*- coding: utf-8 -*-

from Products.MeetingLalouviere.config import COMMISSION_EDITORS_SUFFIX
from Products.MeetingLalouviere.config import COUNCIL_COMMISSION_IDS
from Products.MeetingLalouviere.config import COUNCIL_COMMISSION_IDS_2013

from plone import api


def onItemAfterTransition(item, event):
    '''Called after the transition event called by default in PloneMeeting.
       Here, we are sure that code done in the onItemTransition event is finished.'''

    # if it is an item Council in state 'presented' (for which last transition was 'present'),
    # do item state correspond to meeting state
    if item.portal_type == 'MeetingItemCouncil' and event.transition.id == 'present':
        meeting = item.getMeeting()
        meetingState = meeting.query_state()
        if meetingState in ('in_committee', 'in_council'):
            wTool = api.portal.get_tool('portal_workflow')
            wTool.doActionFor(item, 'setItemInCommittee')
            if meetingState in ('in_council', ):
                wTool.doActionFor(item, 'setItemInCouncil')


def onItemLocalRolesUpdated(item, event):
    """
    Add MeetingFollowUpWriter localrole?
    Depending on the selected Council commission (category),
    give the 'MeetingCommissionEditor' role to the relevant Plone group
       """
    tool = api.portal.get_tool('portal_plonemeeting')
    cfg = tool.getMeetingConfig(item)
    if item.query_state() in cfg.getItemDecidedStates():
        group_id = "{}_followupwriters".format(item.getProposingGroup(theObject=False))
        item.manage_addLocalRoles(group_id, ('MeetingFollowUpWriter',))
    elif item.portal_type == 'MeetingItemCouncil' and item.query_state() in ('itemfrozen', 'itempublished'):
        # if the current category id startswith a given Plone group, this is the correspondance
        # for example, category 'commission-travaux' correspond to Plone
        # group 'commission-travaux_COMMISSION_EDITORS_SUFFIX'
        # category 'commission-travaux-1er-supplement' correspond to Plone
        # group 'commission-travaux_COMMISSION_EDITORS_SUFFIX'
        # first, remove previously set local roles for the Plone group commission
        # this is only done for MeetingItemCouncil
        # existing commission Plone groups
        plone_group_ids = set(COUNCIL_COMMISSION_IDS).union(set(COUNCIL_COMMISSION_IDS_2013))
        # now add the new local roles
        for group_id in plone_group_ids:
            if item.getClassifier().startswith(group_id):
                # we found the relevant group
                group_id = "{}_{}".format(group_id, COMMISSION_EDITORS_SUFFIX)
                item.manage_addLocalRoles(group_id, ('MeetingCommissionEditor',))
                return
