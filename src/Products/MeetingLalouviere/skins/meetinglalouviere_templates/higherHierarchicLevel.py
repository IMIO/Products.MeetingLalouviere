## Script (Python) "previous_review_state"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=member
##title=Return the previous review_state.  Used for index "previous_review_state"
##

#get the groups of the current user and check the highest hierarchic level
groups = context.portal_groups.getGroupsForPrincipal(member)

#du plus grand au plus petit, chefs de service, chefs de bureau, chefs de division, directeurs, echevins=validateurs
hierarchies = ('_reviewers', '_directors', '_divisionheads', '_officemanagers', '_serviceheads', )

groupsstr = str(groups)

for hierarchy in hierarchies:
    if hierarchy in groupsstr:
        return hierarchy
return ''
