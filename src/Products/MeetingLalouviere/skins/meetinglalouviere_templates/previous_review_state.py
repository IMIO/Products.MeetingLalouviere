## Script (Python) "previous_review_state"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return the previous review_state.  Used for index "previous_review_state"
##

from AccessControl import Unauthorized

try:
    if not context.meta_type == 'MeetingItem':
        return ''
except Unauthorized:
    return ''

wh = context.getWorkflowHistory()
if not wh or not len(wh) > 1:
    return ''

last_action = wh[1]['review_state']
return last_action
