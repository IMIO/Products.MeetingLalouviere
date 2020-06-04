from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.PloneMeeting.utils import org_id_to_uid

from plone import api


class IsLoggedInForDEFView(BrowserView):
    """
      This view check if the user is logged in and
      if he is able to add an item for the DEF
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.itemProposingGroup = org_id_to_uid('def-gestion-administrative-personnel')
        self.plone_group = '{}_creators'.format(self.itemProposingGroup)
        self.tool = api.portal.get_tool('portal_plonemeeting')

    def isConnectedOrNotJSONResponse(self):
        """
          This will return a JSON chunk of data depending on the fact that the
          user can create an item for the DEF (connected and DEF creator) or not
        """
        context = aq_inner(self.context)
        # we return JSON data
        context.REQUEST.RESPONSE.setHeader('Content-Type', 'text/javascript')
        mtool = getToolByName(context, 'portal_membership')
        if mtool.isAnonymousUser():
            return 'value_to_show({"value":"#mylogin"});'
        else:
            # even if the user is logged in, we must check that he can add items
            # for the def-gestion-administrative-personnel group
            if self.plone_group not in self.tool.get_plone_groups_for_user(org_uid=self.itemProposingGroup):
                return 'value_to_show({"value":"#mylogin"});'
            return 'value_to_show({"value":"#mysubmit"});'
