# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2016 by Imio.be
#
# GNU General Public License (GPL)
#

from imio.history.utils import getLastWFAction

from Products.CMFPlone.utils import safe_unicode
from plone import api

from Products.MeetingCommunes.browser.overrides import MCItemDocumentGenerationHelperView, \
    MCMeetingDocumentGenerationHelperView


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

    def get_all_commission_items(self, supplement, privacy, include_no_committee=False):
        """
        Returns every items of all committees respecting the order of committees on the meeting.
        For p_supplement:
        - -1 means only include normal, no supplement;
        - 0 means normal + every supplements;
        - 1, 2, 3, ... only items of supplement 1, 2, 3, ...
        - 99 means every supplements only.
        This is calling get_committee_items under so every parameters of get_items may be given in kwargs.
        For p_privacy:
        - 'public' means filter on public items
        - 'secret' means filter on secret items
        For p_include_no_committee:
        - True insert 'no_committee' items before others
        """
        res = []
        if include_no_committee:
            res = self.context.get_items(ordered=True,
                                         additional_catalog_query={"privacy": privacy,
                                                                   "committees_index": [u'no_committee']})

        for committee in self.context.get_committees():
            res += self.context.get_committee_items(committee,
                                                    int(supplement),
                                                    additional_catalog_query={"privacy": privacy}, )
        return res
