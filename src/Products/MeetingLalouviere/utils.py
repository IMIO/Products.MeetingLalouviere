# -*- coding: utf-8 -*-

from plone.memoize import forever
from Products.MeetingLalouviere.config import DG_GROUP_ID
from Products.MeetingLalouviere.config import FALLBACK_DG_GROUP_ID
from Products.MeetingLalouviere.config import INTREF_GROUP_ID
from Products.PloneMeeting.utils import org_id_to_uid


@forever.memoize
def dg_group_uid(raise_on_error=False):
    """ """
    return org_id_to_uid(DG_GROUP_ID, raise_on_error=raise_on_error) or org_id_to_uid(FALLBACK_DG_GROUP_ID)


@forever.memoize
def intref_group_uid(raise_on_error=False):
    """ """
    return org_id_to_uid(INTREF_GROUP_ID, raise_on_error=raise_on_error)
