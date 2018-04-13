#!/bin/sh
/srv/archgenxml/bin/archgenxml --cfg generate.conf MeetingLalouviere.zargo -o tmp

# only keep workflows
cp -rf tmp/profiles/default/workflows/meetingcollegelalouviere_workflow ../profiles/default/workflows
cp -rf tmp/profiles/default/workflows/meetingitemcollegelalouviere_workflow ../profiles/default/workflows
cp -rf tmp/profiles/default/workflows/meetingcouncillalouviere_workflow ../profiles/default/workflows
cp -rf tmp/profiles/default/workflows/meetingitemcouncillalouviere_workflow ../profiles/default/workflows
rm -rf tmp