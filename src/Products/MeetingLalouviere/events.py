# -*- coding: utf-8 -*-

from plone import api
from Products.PloneMeeting.utils import forceHTMLContentTypeForEmptyRichFields

from Products.MeetingLalouviere.config import COMMISSION_EDITORS_SUFFIX
from Products.MeetingLalouviere.config import COUNCIL_COMMISSION_IDS
from Products.MeetingLalouviere.config import COUNCIL_COMMISSION_IDS_2013
from collective.contact.plonegroup.utils import get_organization
from Products.PloneMeeting.utils import org_id_to_uid


def onItemDuplicated(original, event):
    '''After item's cloning, we removed decision annexe.'''
    newItem = event.newItem
    # only apply if we are actually creating a MeetingItemCouncil from another MeetingConfig
    if not (newItem.portal_type == 'MeetingItemCouncil' and original.portal_type != 'MeetingItemCouncil'):
        return
    existingMotivation = newItem.getMotivation()
    defaultCouncilMotivation = newItem.Schema()['motivation'].getDefault(newItem)
    if defaultCouncilMotivation:
        newItem.setMotivation(defaultCouncilMotivation + '<p>&nbsp;</p><p>&nbsp;</p>' + existingMotivation)
    # Make sure we have 'text/html' for every Rich fields
    forceHTMLContentTypeForEmptyRichFields(newItem)


def onItemAfterTransition(item, event):
    '''Called after the transition event called by default in PloneMeeting.
       Here, we are sure that code done in the onItemTransition event is finished.'''

    # if it is an item Council in state 'presented' (for which last transition was 'present'),
    # do item state correspond to meeting state
    if item.portal_type == 'MeetingItemCouncil' and event.transition.id == 'present':
        meeting = item.getMeeting()
        meetingState = meeting.queryState()
        if meetingState in ('in_committee', 'in_council'):
            wTool = api.portal.get_tool('portal_workflow')
            wTool.doActionFor(item, 'setItemInCommittee')
            if meetingState in ('in_council', ):
                wTool.doActionFor(item, 'setItemInCouncil')


def _removeTypistNote(field):
    ''' Remove typist's note find with highlight-purple class'''
    import re
    return re.sub('<span class="highlight-purple">.*?</span>', '', field)


def onItemLocalRolesUpdated(item, event):
    """Depending on the selected Council commission (category),
       give the 'MeetingCommissionEditor' role to the relevant Plone group"""
    # if the current category id startswith a given Plone group, this is the correspondance
    # for example, category 'commission-travaux' correspond to Plone
    # group 'commission-travaux_COMMISSION_EDITORS_SUFFIX'
    # category 'commission-travaux-1er-supplement' correspond to Plone
    # group 'commission-travaux_COMMISSION_EDITORS_SUFFIX'
    # first, remove previously set local roles for the Plone group commission
    # this is only done for MeetingItemCouncil

    if not item.portal_type == 'MeetingItemCouncil' \
            or not item.queryState() in ('item_in_committee', 'item_in_council'):
        return
    # existing commission Plone groups
    commissionEditorsGroupIds = set(COUNCIL_COMMISSION_IDS).union(set(COUNCIL_COMMISSION_IDS_2013))
    # now add the new local roles
    for groupId in commissionEditorsGroupIds:
        if item.getCategory().startswith(groupId):
            # we found the relevant group
            org_uid = org_id_to_uid(groupId)
            org = get_organization(org_uid)
            if org:
                group_id = "{}_{}".format(org.UID(), COMMISSION_EDITORS_SUFFIX)
                item.manage_addLocalRoles(group_id, ('MeetingCommissionEditor',))
                return
