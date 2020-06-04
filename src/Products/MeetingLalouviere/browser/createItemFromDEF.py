import base64
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from plone import api


class CreateItemFromDEFView(BrowserView):
    """
      This way you can add an item from the DEF application
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.itemTitle = request.get('deftitle', '')
        self.itemDescription = request.get('defdescription', '')
        self.itemMotivation = request.get('defmotivation', '')
        self.itemDecision = request.get('defdecision', '')
        # every decisions coming out from the DEF intranet are about
        # def-gestion-administrative-personnel
        self.itemProposingGroup = '21ae631cbfee4fce8b9ecdd36b18a8e9'
        self.plone_group = '21ae631cbfee4fce8b9ecdd36b18a8e9_creators'

    def mayUserAddItem(self):
        """
          The user must be connected
        """
        # the user must be logged in
        context = aq_inner(self.context)
        mtool = getToolByName(context, 'portal_membership')
        # the user must be creator for "def-gestion-administrative-personnel"
        if mtool.isAnonymousUser():
            raise Unauthorized

        pmtool = api.portal.get_tool('portal_plonemeeting')
        if self.plone_group not in pmtool.get_plone_groups_for_user(org_uid=self.itemProposingGroup):
            raise Unauthorized
        return True

    def createItem(self):
        """
          Proceed with item creation
        """
        context = aq_inner(self.context)
        # raise Unauthorized if the user can not add an item for the DEF
        self.mayUserAddItem()

        member = context.restrictedTraverse('@@plone_portal_state').member()
        meetingFolder = getattr(member.getHomeFolder().mymeetings, 'meeting-config-college')
        data = {
            'title': self.getItemTitle(),
            'proposingGroup': self.itemProposingGroup,
        }
        newitemid = meetingFolder.invokeFactory('MeetingItemCollege',
                                                id=context.generateUniqueId('MeetingItemCollege'),
                                                **data)
        newitem = getattr(meetingFolder, newitemid)
        # special handling for text/html decision field
        newitem.setDescription(self.getItemDescription(), contenttype='text/html')
        newitem.setMotivation(self.getItemMotivation(), contenttype='text/html')
        newitem.setDecision(self.getItemDecision(), contenttype='text/html')
        newitem.processForm()
        newitem.reindexObject()
        aq_inner(self.request).RESPONSE.redirect(newitem.absolute_url() + '/edit')

    def getItemTitle(self):
        """
          Returns the item title
        """
        return base64.b64decode(self.itemTitle)

    def getItemMotivation(self):
        """
          Returns the item motivation
        """
        return base64.b64decode(self.itemMotivation)

    def getItemDecision(self):
        """
          Returns the item decision
        """
        return base64.b64decode(self.itemDecision)

    def getItemDescription(self):
        """
          Returns the item description
        """
        return base64.b64decode(self.itemDescription)
