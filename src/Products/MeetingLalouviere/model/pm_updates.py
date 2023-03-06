from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.MeetingItem import MeetingItem

from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import TextField
from Products.CMFCore.permissions import ModifyPortalContent


def update_meeting_schema(baseSchema):
    baseSchema['observations'].widget.label_method = "getLabelObservations"
    return baseSchema


Meeting.schema = update_meeting_schema(Meeting.schema)


def update_item_schema(baseSchema):

    specificSchema = Schema((
        # specific field for council added for MeetingManagers to transcribe interventions
        TextField(
            name='interventions',
            widget=RichWidget(
                rows=15,
                condition="python: here.portal_type == 'MeetingItemCouncil' "
                          "and here.showMeetingManagerReservedField('privacy')",
                label='Interventions',
                label_msgid='MeetingLalouviere_label_interventions',
                description='Transcription of interventions',
                description_msgid='MeetingLalouviere_descr_interventions',
                i18n_domain='PloneMeeting',
            ),
            optional=True,
            default_content_type="text/html",
            searchable=True,
            allowable_content_types=('text/html',),
            default_output_type="text/html",
        ),
        # here above are 3 specific fields for managing item follow-up
        StringField(
            name='followUp',
            default="follow_up_no",
            widget=SelectionWidget(
                condition="python: not here.isDefinedInTool() "
                          "and here.attribute_is_used('neededFollowUp') and here.adapted().showFollowUp()",
                description="A follow up is needed : no, yes, provided?",
                description_msgid="MeetingLalouviere_descr_followUp",
                label='FollowUp',
                label_msgid='MeetingLalouviere_label_followUp',
                i18n_domain='PloneMeeting',
            ),
            vocabulary_factory='Products.MeetingLalouviere.vocabularies.listFollowUps',
            write_permission="MeetingLalouviere: Write followUp",
        ),
        TextField(
            name='neededFollowUp',
            optional=True,
            widget=RichWidget(
                rows=15,
                condition="python: not here.isDefinedInTool() "
                          "and here.attribute_is_used('neededFollowUp') and here.adapted().showFollowUp()",
                label='NeededFollowUp',
                label_msgid='MeetingLalouviere_label_neededFollowUp',
                description='Follow-up needed for this item',
                description_msgid='MeetingLalouviere_descr_neededFollowUp',
                i18n_domain='PloneMeeting',
            ),
            default_content_type="text/html",
            searchable=True,
            allowable_content_types=('text/html',),
            default_output_type="text/html",
            write_permission="MeetingLalouviere: Write neededFollowUp",
        ),
        TextField(
            name='providedFollowUp',
            optional=True,
            widget=RichWidget(
                rows=15,
                condition="python: not here.isDefinedInTool() "
                          "and here.attribute_is_used('providedFollowUp') and here.adapted().showFollowUp()",
                label='ProvidedFollowUp',
                label_msgid='MeetingLalouviere_label_providedFollowUp',
                description='Follow-up provided for this item',
                description_msgid='MeetingLalouviere_descr_providedFollowUp',
                i18n_domain='PloneMeeting',
            ),
            default_content_type="text/html",
            default="<p>N&eacute;ant</p>",
            searchable=True,
            allowable_content_types=('text/html',),
            default_output_type="text/html",
            write_permission="MeetingLalouviere: Write providedFollowUp",
        ),
    ),)

    # Don't forget the label override in skins/meetinglalouviere_templates/meetingitem_view.pt
    baseSchema['description'].widget.label_method = "getLabelDescription"

    baseSchema['privacy'].widget.condition = "python: here.showMeetingManagerReservedField('privacy')"

    baseSchema['observations'].write_permission = ModifyPortalContent

    completeItemSchema = baseSchema + specificSchema.copy()
    return completeItemSchema


MeetingItem.schema = update_item_schema(MeetingItem.schema)


# Classes have already been registered, but we register them again here
# because we have potentially applied some schema adaptations (see above).
# Class registering includes generation of accessors and mutators, for
# example, so this is why we need to do it again now.
from Products.PloneMeeting.config import registerClasses
registerClasses()
