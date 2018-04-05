# encoding: utf-8

from zope.i18n import translate
from zope.interface import implements
from zope.globalrequest import getRequest
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ItemFollowUpVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ """
        request = getRequest()
        d = 'PloneMeeting'
        res = [SimpleTerm("follow_up_no",
                          "follow_up_no",
                          translate('follow_up_no',
                                    domain=d,
                                    context=request)),
               SimpleTerm("follow_up_yes",
                          "follow_up_yes",
                          translate('follow_up_yes',
                                    domain=d,
                                    context=request)),
               SimpleTerm("follow_up_provided",
                          "follow_up_provided",
                          translate('follow_up_provided',
                                    domain=d,
                                    context=request)),
               SimpleTerm("follow_up_provided_not_printed",
                          "follow_up_provided_not_printed",
                          translate('follow_up_provided_not_printed',
                                    domain=d,
                                    context=request))]
        return SimpleVocabulary(res)


ItemFollowUpVocabularyFactory = ItemFollowUpVocabulary()
