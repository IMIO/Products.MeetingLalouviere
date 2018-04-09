from imio.actionspanel.utils import unrestrictedRemoveGivenObject
from Products.PloneMeeting.interfaces import IAnnexable
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


def _removeTypistNote(field):
    ''' Remove typist's note find with highlight-purple class'''
    import re
    return re.sub('<span class="highlight-purple">.*?</span>', '', field)
