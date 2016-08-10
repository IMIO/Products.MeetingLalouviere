# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting
from Products.PloneMeeting.testing import PloneMeetingLayer
import Products.MeetingLalouviere
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE

MLL_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                           package=Products.MeetingLalouviere,
                           name='MLL_ZCML')

MLL_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MLL_ZCML),
                               name='MLL_Z2')

MLL_TESTING_PROFILE = PloneMeetingLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingLalouviere,
    additional_z2_products=('Products.MeetingLalouviere',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingLalouviere:testing',
    name="MLL_TESTING_PROFILE")

MLL_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MLL_TESTING_PROFILE,), name="MLL_TESTING_PROFILE_FUNCTIONAL")
