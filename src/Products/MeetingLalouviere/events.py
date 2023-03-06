# -*- coding: utf-8 -*-
from plone import api


def onItemLocalRolesUpdated(item, event):
    """
    Add MeetingFollowUpWriter localrole?
    Depending on the selected Council commission (category),
    give the 'MeetingFollowUpWriter' role to the relevant Plone group
       """
    tool = api.portal.get_tool('portal_plonemeeting')
    cfg = tool.getMeetingConfig(item)
    if item.query_state() in cfg.getItemDecidedStates():
        group_id = "{}_followupwriters".format(item.getProposingGroup(theObject=False))
        item.manage_addLocalRoles(group_id, ('MeetingFollowUpWriter',))
