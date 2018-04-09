from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class MessagesViewlet(ViewletBase):
    '''This viewlet displays some warning messages if needed.'''

    def update(self):
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')

    def getCurrentMeetingConfig(self):
        '''Returns the current meetingConfig.'''
        portal_plonemeeting = getToolByName(self.context, 'portal_plonemeeting')
        return portal_plonemeeting.getMeetingConfig(self.context)

    def getPloneMeetingTool(self):
        '''.Returns portal_plonemeeting.'''
        return getToolByName(self.context, 'portal_plonemeeting')

    def getCurrentObject(self):
        '''Returns the current object.'''
        return self.context

    def available(self):
        '''Is the viewlet available?'''
        if not self.getMessages():
            return False
        return True

    @memoize
    def getMessages(self):
        '''Returns the messages to display.'''
        res = []
        if not self.getCurrentMeetingConfig().id == 'meeting-config-council':
            return res
        if self.context.getItemInitiator() and \
           not self.context.getCategory() == 'points-conseillers-2eme-supplement' and \
           self.context.queryState() in ['itemcreated', 'proposed_to_officemanager', ]:
            res.append({
                'type': 'warning',
                'msg': 'check_intitiator_and_category',
            })
        if not self.context.getCategory():
            res.append({
                'type': 'warning',
                'msg': 'check_category',
            })
        return res

    def getPortalUrl(self):
        return getToolByName(self.context, 'portal_url').getPortalPath()

    index = ViewPageTemplateFile("messages.pt")
