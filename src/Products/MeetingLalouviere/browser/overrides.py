# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2016 by Imio.be
#
# GNU General Public License (GPL)
#
from Products.MeetingCommunes.browser.overrides import MCItemDocumentGenerationHelperView
from Products.MeetingCommunes.browser.overrides import MCMeetingDocumentGenerationHelperView

import cgi


class MLLItemDocumentGenerationHelperView(MCItemDocumentGenerationHelperView):
    """Specific printing methods used for item."""

    def print_link_and_title(self):
        return '<a href="%s">%s</a>' % (self.real_context.absolute_url(), cgi.escape(self.real_context.Title()))


class MLLMeetingDocumentGenerationHelperView(MCMeetingDocumentGenerationHelperView):

    def get_all_committees_items(self, supplement, privacy='public', list_types=['normal'], include_no_committee=False):
        """
        Returns all items of all committees respecting the order of committees on the meeting.
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
                                         list_types=list_types,
                                         additional_catalog_query={"privacy": privacy,
                                                                   "committees_index": [u'no_committee']})

        for committee in self.context.get_committees():
            res += self.context.get_committee_items(committee,
                                                    int(supplement),
                                                    additional_catalog_query={"privacy": privacy},
                                                    list_types=list_types)
        return res
