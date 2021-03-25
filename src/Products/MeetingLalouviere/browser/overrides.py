# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2016 by Imio.be
#
# GNU General Public License (GPL)
#

from Products.PloneMeeting.config import NOT_GIVEN_ADVICE_VALUE
from imio.history.utils import getLastWFAction

from Products.CMFPlone.utils import safe_unicode
from plone import api

from Products.MeetingCommunes.browser.overrides import MCItemDocumentGenerationHelperView, \
    MCMeetingDocumentGenerationHelperView, MCFolderDocumentGenerationHelperView


class MLLItemDocumentGenerationHelperView(MCItemDocumentGenerationHelperView):
    """Specific printing methods used for item."""
    def _financialAdviceDetails(self):
        '''Get the financial advice signature date, advice type and comment'''
        res = {}
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        financialAdvice = cfg.adapted().getUsedFinanceGroupIds()[0]
        adviceData = self.context.getAdviceDataFor(self.context.context, financialAdvice)
        res['comment'] = 'comment' in adviceData\
            and adviceData['comment'] or ''
        advice_id = 'advice_id' in adviceData\
            and adviceData['advice_id'] or ''
        signature_event = advice_id and getLastWFAction(getattr(self.context, advice_id), 'signFinancialAdvice') or ''
        res['out_of_financial_dpt'] = 'time' in signature_event and signature_event['time'] or ''
        res['out_of_financial_dpt_localized'] = res['out_of_financial_dpt']\
            and res['out_of_financial_dpt'].strftime('%d/%m/%Y') or ''
        # "positive_with_remarks_finance" will be printed "positive_finance"
        if adviceData['type'] == 'positive_with_remarks_finance':
            type_translated = self.translate(msgid='positive_finance',
                                             domain='PloneMeeting').encode('utf-8')
        else:
            type_translated = adviceData['type_translated'].encode('utf-8')
        res['advice_type'] = '<p><u>Type d\'avis:</u>  %s</p>' % type_translated
        res['delay_started_on_localized'] = 'delay_started_on_localized' in adviceData['delay_infos']\
            and adviceData['delay_infos']['delay_started_on_localized'] or ''
        res['delay_started_on'] = 'delay_started_on' in adviceData\
            and adviceData['delay_started_on'] or ''
        return res

    def getItemFinanceDelayLimitDate(self):
        finance_id = self.context.adapted().getFinanceAdviceId()
        if finance_id:
            data = self.real_context.getAdviceDataFor(self.real_context, finance_id)
            return ('delay_infos' in data and 'limit_date_localized' in data['delay_infos'] and
                    data['delay_infos']['limit_date_localized']) or None

        return None

    def getItemFinanceAdviceDelayDays(self):
        finance_id = self.context.adapted().getFinanceAdviceId()
        if finance_id:
            data = self.real_context.getAdviceDataFor(self.real_context, finance_id)
            return ('delay' in data and data['delay']) or None

        return None

    def getItemFinanceAdviceTransmissionDate(self, finance_id=None):
        """
        :return: The date as a string when the finance service received the advice request.
                 No matter if a legal delay applies on it or not.
        """
        if not finance_id:
            finance_id = self.context.adapted().getFinanceAdviceId()
            # may return None anyway

        if finance_id:
            data = self.real_context.getAdviceDataFor(self.real_context, finance_id)
            if 'delay_infos' in data and 'delay_started_on' in data['delay_infos'] \
                    and data['delay_infos']['delay_started_on']:
                return data['delay_infos']['delay_started_on']
            else:
                return self.getWorkFlowAdviceTransmissionStep()
        return None

    def getWorkFlowAdviceTransmissionStep(self):

        """
        :return: The date as a string when the finance service received the advice request if no legal delay applies.
        """

        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)

        wf_present_transition = list(cfg.getTransitionsForPresentingAnItem())
        item_advice_states = cfg.itemAdviceStates

        if 'itemfrozen' in item_advice_states and 'itemfreeze' not in wf_present_transition:
            wf_present_transition.append('itemfreeze')

        for item_transition in wf_present_transition:
            event = getLastWFAction(self.context, item_transition)
            if event and 'review_state' in event and event['review_state'] in item_advice_states:
                return event['time']

        return None

    def getDeliberation(self, withFinanceAdvice=True, **kwargs):
        """Override getDeliberation to be able to specify that we want to print the finance advice."""
        deliberation = self.getMotivation(**kwargs)
        # insert finance advice if necessary
        if withFinanceAdvice:
            # respect order of priority
            advice = self.printFinanceAdvice(self, ['legal'])
            if not advice:
                advice = self.printFinanceAdvice(self, ['simple'])
            if not advice:
                advice = self.printFinanceAdvice(self, ['initiative'])

            if advice and advice['comment'] and advice['comment'].strip():
                comment = "<p>Vu l'avis du Directeur financier repris ci-dessous ainsi qu'en annexe :</p>{}".format(advice['comment'].strip())
                deliberation = "{}{}".format(deliberation, comment)
        deliberation = "{}{}".format(deliberation, self.getDecision(**kwargs))
        return deliberation


class MLLMeetingDocumentGenerationHelperView(MCMeetingDocumentGenerationHelperView):
    """Specific printing methods used for meeting."""
    def get_classifiers_for_commission(self, commission_num):
        commission_classifier_ids = self.real_context.adapted().get_commission_classifiers_ids()
        classifier = commission_classifier_ids[commission_num - 1]
        if isinstance(classifier, tuple):
            return list(classifier)
        else:
            # single classifier as a string
            return [classifier]

    def get_commission_items(self, itemUids, commission_num, type='normal'):
        """
        Get the items of the commission
        :param commission_num: number of the commission
        :param supplement: supplement items
        :param type: must be 'normal', 'supplement' or '*'
        :return: list of meetingItem
        """
        classifiers = self.get_classifiers_for_commission(commission_num)
        if type == 'supplement':
            # If we want the supplements items only
            # append supplement suffix to the classifiers
            classifiers = [classifier + '-1er-supplement' for classifier in classifiers]
        elif type == '*':
            # If we want all items
            classifiers = classifiers + [classifier + '-1er-supplement' for classifier in classifiers]

        items = self.context.getItems(uids=itemUids,
                                      ordered=True,
                                      additional_catalog_query={"getRawClassifier": classifiers})
        return items

    def format_commission_pre_meeting_date(self, commission_num):
        """
        format pre-meeting date like this : (Lundi 20 mai 2019 (18H30), Salle du Conseil communal)
        :param commission_num: number of the commission
        :return: formatted pre-meeting date string
        """
        meeting = self.context
        if commission_num > 1:
            pre_meeting_date = getattr(meeting, "getPreMeetingDate_" + str(commission_num))()
            pre_meeting_place = getattr(meeting, "getPreMeetingPlace_" + str(commission_num))()
        else:
            pre_meeting_date = meeting.getPreMeetingDate()
            pre_meeting_place = meeting.getPreMeetingPlace()

        weekday = meeting.translate("weekday_%s" % pre_meeting_date.aDay().lower(), domain="plonelocales")
        day = pre_meeting_date.strftime('%d')
        month = meeting.translate('month_%s' % pre_meeting_date.strftime('%b').lower(),
                                  domain='plonelocales').lower()
        year = pre_meeting_date.strftime('%Y')
        time = pre_meeting_date.strftime('%HH%M')

        return u"({weekday} {day} {month} {year} ({time}), {place})".format(
            weekday=safe_unicode(weekday),
            day=safe_unicode(day),
            month=safe_unicode(month),
            year=safe_unicode(year),
            time=safe_unicode(time),
            place=safe_unicode(pre_meeting_place)
        )

    def has_commission_pre_meeting_date(self, commission_num):
        """
        Has the commission [com_num] a pre-meeting date ?
        :return: True if it has one, False otherwise
        """
        meeting = self.context
        if commission_num > 1:
            pre_meeting_date = getattr(meeting, "getPreMeetingDate_" + str(commission_num))()
        else:
            pre_meeting_date = meeting.getPreMeetingDate()
        return pre_meeting_date is not None

    def get_commission_assembly(self, commission_num):
        """
        get the commission pre-meeting assembly based on the commission number.
        :param commission_num: number of the commission
        :return: preMeetingAssembly
        """
        meeting = self.context
        if commission_num > 1:
            return getattr(meeting, "getPreMeetingAssembly_" + str(commission_num))()
        else:
            return meeting.getPreMeetingAssembly()


class MLLFolderDocumentGenerationHelperView(MCFolderDocumentGenerationHelperView):
    """"""
