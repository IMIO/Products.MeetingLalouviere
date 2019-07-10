# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2016 by Imio.be
#
# GNU General Public License (GPL)
#

from Products.MeetingLalouviere.config import FINANCE_GROUP_ID
from Products.PloneMeeting.browser.views import FolderDocumentGenerationHelperView, ItemDocumentGenerationHelperView, \
    MeetingDocumentGenerationHelperView
from Products.PloneMeeting.config import NOT_GIVEN_ADVICE_VALUE
from Products.PloneMeeting.utils import get_annexes, getLastEvent

from Products.CMFPlone.utils import safe_unicode
from plone import api


def formatedAssembly(assembly, focus):
    is_finish = False
    absentFind = False
    excuseFind = False
    res = []
    res.append('<p class="mltAssembly">')
    for ass in assembly:
        if is_finish:
            break
        lines = ass.split(',')
        cpt = 1
        my_line = ''
        for line in lines:
            if((line.find('Excus') >= 0 or line.find('Absent') >= 0) and focus == 'present') or \
                    (line.find('Absent') >= 0 and focus == 'excuse'):
                is_finish = True
                break
            if line.find('Excus') >= 0:
                excuseFind = True
                continue
            if line.find('Absent') >= 0:
                absentFind = True
                continue
            if (focus == 'absent' and not absentFind) or (focus == 'excuse' and not excuseFind):
                continue
            if cpt == len(lines):
                my_line = "%s%s<br />" % (my_line, line)
                res.append(my_line)
            else:
                my_line = "%s%s," % (my_line, line)
            cpt = cpt + 1
    if len(res) > 1:
        res[-1] = res[-1].replace('<br />', '')
    else:
        return ''
    res.append('</p>')
    return ('\n'.join(res))


class MCItemDocumentGenerationHelperView(ItemDocumentGenerationHelperView):
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
        signature_event = advice_id and getLastEvent(getattr(self.context, advice_id), 'signFinancialAdvice') or ''
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

    def printAllAnnexes(self, portal_types=['annex']):
        ''' Printing Method use in templates :
            return all viewable annexes for item '''
        res = []
        annexes = get_annexes(self.context, portal_types=portal_types)
        for annex in annexes:
            url = annex.absolute_url()
            title = annex.Title().replace('&', '&amp;')
            res.append(u'<p><a href="{0}">{1}</a></p>'.format(
                url, safe_unicode(title)))
        return (u'\n'.join(res))

    def printFormatedAdvice(self):
        ''' Printing Method use in templates :
            return formated advice'''
        res = []
        keys = self.context.getAdvicesByType().keys()
        for key in keys:
            for advice in self.context.getAdvicesByType()[key]:
                if advice['type'] == 'not_given':
                    continue

                comment = ''
                type = key

                if 'hidden_during_redaction' in advice and advice['hidden_during_redaction']:
                    type = 'hidden_during_redaction'
                elif advice['comment']:
                    comment = advice['comment']

                res.append({'type': self.translate(msgid=type, domain='PloneMeeting').encode('utf-8'),
                            'name': advice['name'].encode('utf-8'),
                            'comment': comment})
        return res

    def printFormatedItemAssembly(self, focus=''):
        ''' Printing Method use in templates :
            return formated assembly with 'absent', 'excused', ... '''
        if focus not in ('present', 'excuse', 'absent'):
            return ''
        # ie: Pierre Helson, Bourgmestre, Président
        # focus is present, excuse or absent
        assembly = self.context.getItemAssembly().replace('<p>', '').replace('</p>', '').split('<br />')
        return formatedAssembly(assembly, focus)

    def printFinanceAdvice(self, cases, show_hidden=False):
        """
        :param cases: collection containing either 'initiative', 'legal', 'simple' or 'not_given'
               cases can also be a string in case a single case should be returned and for backward compatibility.
        :return: an array of dictionaries same as MeetingItem.getAdviceDataFor
        or empty if no advice matching the given case.
        """

        """
        case 'simple' means the financial advice was requested but without any delay.
        case 'legal' means the financial advice was requested with a delay. It's a legal financial advice.
        case 'initiative' means the financial advice was given without being requested at the first place.
        case 'legal_not_given' means the financial advice was requested with delay. But was ignored by the finance director.
        case 'simple_not_given' means the financial advice was requested without delay. But was ignored by the finance
         director.
        """

        def check_given_or_not_cases(advice, case_to_check, case_given, case_not_given):
            if advice['advice_given_on']:
                return case_to_check == case_given
            else:
                return case_to_check == case_not_given

        if isinstance(cases, str):
            cases = [cases]

        result = []
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        finance_advice_ids = cfg.adapted().getUsedFinanceGroupIds()

        if finance_advice_ids:
            advices = self.context.getAdviceDataFor(self.context.context)

            for case in cases:
                if case in ['initiative', 'legal', 'simple', 'simple_not_given', 'legal_not_given']:
                    for finance_advice_id in finance_advice_ids:

                        if finance_advice_id in advices:
                            advice = advices[finance_advice_id]
                        else:
                            continue

                        # Change data if advice is hidden
                        if 'hidden_during_redaction' in advice and advice['hidden_during_redaction'] and not show_hidden:
                            message = self.translate('hidden_during_redaction', domain='PloneMeeting')
                            advice['type_translated'] = message
                            advice['type'] = 'hidden_during_redaction'
                            advice['comment'] = message

                        # check if advice was given on self initiative by the adviser
                        if advice['not_asked']:
                            if case == 'initiative' and advice['advice_given_on']:
                                result.append(advice)
                        else:
                            # set transmission date to adviser because advice was asked by the agent
                            advice['item_transmitted_on'] = self.getItemFinanceAdviceTransmissionDate(finance_advice_id)
                            if advice['item_transmitted_on']:
                                advice['item_transmitted_on_localized'] = self.display_date(
                                    date=advice['item_transmitted_on'])
                            else:
                                advice['item_transmitted_on_localized'] = ''

                            # If there is a delay then it is a legal advice. If not, it's a simple advice
                            if advice['delay']:
                                if check_given_or_not_cases(advice, case, 'legal', 'legal_not_given'):
                                    result.append(advice)
                            elif check_given_or_not_cases(advice, case, 'simple', 'simple_not_given'):
                                result.append(advice)
        return result

    def getItemFinanceDelayLimitDate(self):
        finance_id = self.context.adapted().getFinanceAdviceId()
        if finance_id:
            data = self.real_context.getAdviceDataFor(self.real_context, finance_id)
            return ('delay_infos' in data and 'limit_date_localized' in data['delay_infos']
                    and data['delay_infos']['limit_date_localized']) or None

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
            event = getLastEvent(self.context, item_transition)
            if event and 'review_state' in event and event['review_state'] in item_advice_states:
                return event['time']

        return None

    def print_item_state(self):
        return self.translate(self.real_context.queryState())

    def print_creator_name(self):
        return (self.real_context.portal_membership.getMemberInfo(str(self.real_context.Creator())) \
               and self.real_context.portal_membership.getMemberInfo(str(self.real_context.Creator()))['fullname']) \
               or str(self.real_context.Creator())

    def getDeliberation(self, withFinanceAdvice=True, **kwargs):
        """Override getDeliberation to be able to specify that we want to print the finance advice."""
        deliberation = self.getMotivation(**kwargs)
        # insert finance advice if necessary
        if withFinanceAdvice:
            if FINANCE_GROUP_ID in self.adviceIndex and \
                    self.adviceIndex[FINANCE_GROUP_ID]['type'] != NOT_GIVEN_ADVICE_VALUE:
                financeAdviceData = self.getAdviceDataFor(self.getSelf(), FINANCE_GROUP_ID)
                if financeAdviceData['comment'] and financeAdviceData['comment'].strip():
                    comment = "<p>Vu l'avis du Directeur financier repris ci-dessous ainsi qu'en annexe :</p>"
                    comment = comment + financeAdviceData['comment'].strip()
                    deliberation = deliberation + comment
        deliberation = deliberation + self.getDecision(**kwargs)
        return deliberation


class MCMeetingDocumentGenerationHelperView(MeetingDocumentGenerationHelperView):
    """Specific printing methods used for meeting."""

    def printFormatedMeetingAssembly(self, focus=''):
        ''' Printing Method use in templates :
            return formated assembly with 'absent', 'excused', ... '''
        if focus not in ('present', 'excuse', 'absent'):
            return ''
        # ie: Pierre Helson, Bourgmestre, PrÃ©sident
        # focus is present, excuse or absent
        assembly = self.context.getAssembly().replace('<p>', '').replace('</p>', '').split('<br />')
        return formatedAssembly(assembly, focus)

    def get_categories_for_commission(self, commission_num):
        commissionCategoryIds = self.real_context.adapted().getCommissionCategoriesIds()
        cat = commissionCategoryIds[commission_num-1]
        if isinstance(cat, tuple):
            return list(cat)
        else:
            # single category as a string
            return [cat]

    def get_commission_items(self, itemUids, commission_num, type='normal'):
        """
        Get the items of the commission
        :param commission_num: number of the commission we want ([1-6])
        :param supplement: supplement items
        :return: list of meetingItem
        """
        cats = self.get_categories_for_commission(commission_num)
        print cats
        if type == 'supplement':  # If we want the supplements items
            cats = [cat + '-1er-supplement' for cat in cats]  # append supplement suffix to the categories
        elif type == '*':
            cats = [cat + '-1er-supplement' for cat in cats] + cats
        return self.real_context.adapted().getPrintableItems(itemUids, categories=cats)

    def get_commission_premeetingdate(self, commission_num):
        """
        format pre-meeting date like this : (Lundi 20 mai 2019 (18H30), Salle du Conseil communal)
        :return: formatted pre-meeting date string
        """
        meeting = self.context
        premeetingdate = getattr(meeting, "getPreMeetingDate_" + str(commission_num))()
        return u"({weekday} {day} {month} {year} ({time}), {place})".format(
            weekday=meeting.utranslate("weekday_%s" % premeetingdate.aDay().lower(), domain="plonelocales"),
            day=premeetingdate.strftime('%d'),
            month=meeting.translate('month_%s' % premeetingdate.strftime('%b').lower(), domain='plonelocales').lower(),
            year=premeetingdate.strftime('%Y'),
            time=premeetingdate.strftime('%HH%M'),
            place=getattr(meeting, "getPreMeetingPlace_" + str(commission_num))()
        )

    def get_commission_assembly(self, commission_num):
        meeting = self.context
        return getattr(meeting, "getPreMeetingAssembly_" + str(commission_num))()


class MCFolderDocumentGenerationHelperView(FolderDocumentGenerationHelperView):

    def get_all_items_dghv_with_finance_advice(self, brains):
        """
        :param brains: the brains collection representing @Product.PloneMeeting.MeetingItem
        :return: an array of dictionary with onnly the items linked to a finance advics which contains 2 keys
                 itemView : the documentgenerator helper view of a MeetingItem.
                 advice   : the data from a single advice linked to this MeetingItem as extracted with getAdviceDataFor.
        """
        res = []

        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        finance_advice_ids = cfg.adapted().getUsedFinanceGroupIds()

        for brain in brains:
            item = brain.getObject()
            advices = item.getAdviceDataFor(item)
            if advices:
                for advice in advices:
                    if advice in finance_advice_ids:
                        res.append({'itemView': self.getDGHV(item), 'advice': advices[advice]})

        return res
