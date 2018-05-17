# -*- coding: utf-8 -*-

from plone import api
from Products.PloneMeeting.utils import forceHTMLContentTypeForEmptyRichFields


def onItemDuplicated(original, event):
    '''After item's cloning, we removed decision annexe.
    '''
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
