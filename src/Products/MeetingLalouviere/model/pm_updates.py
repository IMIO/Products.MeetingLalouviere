# -*- coding: utf-8 -*-

# Classes have already been registered, but we register them again here
# because we have potentially applied some schema adaptations (see above).
# Class registering includes generation of accessors and mutators, for
# example, so this is why we need to do it again now.
from Products.PloneMeeting.config import registerClasses
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.MeetingItem import MeetingItem


def update_meeting_schema(base_schema):
    base_schema["observations"].widget.label_method = "getLabelObservations"
    return base_schema


Meeting.schema = update_meeting_schema(Meeting.schema)


def update_item_schema(base_schema):

    # Don't forget the label override in skins/meetinglalouviere_templates/meetingitem_view.pt
    base_schema["description"].widget.label_method = "getLabelDescription"
    base_schema["privacy"].widget.condition = "python: here.showMeetingManagerReservedField('privacy')"
    return base_schema


MeetingItem.schema = update_item_schema(MeetingItem.schema)


registerClasses()
