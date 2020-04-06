import base64
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.MeetingLalouviere.config import DEFURL


class LogUserFromDEFView(BrowserView):
    """
      This way a user can log in to PloneMeeting and be sended back to the DEF intranet
      By default such came_from outside Plone is not allowed to avoid fishing
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        # we NEED a defurl and we check that we are correctly redirected to the DEF
        # to avoid this view being used for fishing
        defurl = self.request.get('defurl', None)
        self.defurl = None
        if defurl:
            try:
                self.defurl = base64.b64decode(defurl)
                if not self.defurl.startswith(DEFURL):
                    raise Unauthorized
            except:
                raise Unauthorized
        else:
            raise Unauthorized

    def logUserOrRedirect(self):
        """
          Either we propose the user to log him in or the user is already logged in
          and we return to the DEF
        """
        context = aq_inner(self.context)
        mtool = getToolByName(context, 'portal_membership')
        if mtool.isAnonymousUser():
            # raise an unauthorized so the login page is shown to the user
            raise Unauthorized
        else:
            request = aq_inner(self.request)
            # to avoid args mismatches in the url, the def back url is passed in base64
            request.RESPONSE.redirect(self.defurl)
