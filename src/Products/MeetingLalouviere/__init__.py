# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#

from config import product_globals
from Products.CMFCore import DirectoryView

import adapters  # noqa
import logging
import model.pm_updates  # noqa


logger = logging.getLogger("MeetingLalouviere")
logger.debug("Installing Product")


DirectoryView.registerDirectory("skins", product_globals)


def initialize(context):
    """initialize product (called by zope)"""
