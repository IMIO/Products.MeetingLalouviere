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

from plone import api


class MLLItemDocumentGenerationHelperView(MCItemDocumentGenerationHelperView):
    """Specific printing methods used for item."""

    def print_link_and_title(self):
        return '<a href="%s">%s</a>' % (self.real_context.absolute_url(), cgi.escape(self.real_context.Title()))


class MLLMeetingDocumentGenerationHelperView(MCMeetingDocumentGenerationHelperView):

    def get_all_committees_items(self, uids, supplement, privacy='public', list_types=['normal'], include_no_committee=False):
        """
        Returns all items of all committees respecting the order of committees on the meeting.
        For p_supplement:
        - -1 means only include normal, no supplement;
        - 0 means normal + every supplements;
        - 1, 2, 3, ... only items of supplement 1, 2, 3, ...
        - 99 means every supplements only.
        This is calling get_committee_items under so every parameter of get_items may be given in kwargs.
        For p_privacy:
        - 'public' means filter on public items
        - 'secret' means filter on secret items
        For p_include_no_committee:
        - True insert 'no_committee' items before others
        """
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self)
        additional_catalog_query = {"privacy": privacy, 'committees_index': []}

        if include_no_committee:
            additional_catalog_query['committees_index'].append(u'no_committee')
        # =========
        # ATTENTION
        # =========
        # Police committee items are the last of public part but the first of private part.
        # So it is important to respect item order as manually defined on the meeting.
        # Even if they are doing wrong weird shit and should separate police council from municipality council properly.
        for committee in self.context.get_committees():
            available_suppl_ids = cfg.get_supplements_for_committee(committee)
            if int(supplement) == -1:
                additional_catalog_query['committees_index'].append(committee)
            elif int(supplement) == 0:
                additional_catalog_query['committees_index'].append(committee)
                additional_catalog_query['committees_index'] += available_suppl_ids
            elif supplement == 2:
                additional_catalog_query['committees_index'].append("points-conseillers-2eme-supplement")
            elif supplement == 3:
                additional_catalog_query['committees_index'].append("points-conseillers-3eme-supplement")
            elif int(supplement) == 99:
                additional_catalog_query['committees_index'] = available_suppl_ids
            elif len(available_suppl_ids) >= int(supplement):
                additional_catalog_query['committees_index'].append(available_suppl_ids[int(supplement) - 1])

        return self.context.get_items(uids,
                                      ordered=True,
                                      additional_catalog_query=additional_catalog_query,
                                      list_types=list_types)
