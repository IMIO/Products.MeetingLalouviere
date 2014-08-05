# ------------------------------------------------------------------------------
import logging
logger = logging.getLogger('MeetingLalouviere')
from Products.PloneMeeting.migrations import Migrator


# The migration class ----------------------------------------------------------
class migrate_to_3_2_0_1(Migrator):

    def _updateTopics(self):
        '''Update topics :
           - remove useless topic 'searchreturnedtoserviceitems';
           - remove topic_search_script defined for 'searchcorrecteditems';
           - change condition of topic 'searchitemstocorrect'.
        '''
        logger.info("Updating topics...")
        topicCondition = 'python: here.portal_plonemeeting.userIsAmong("officemanagers") or ' \
                         'here.portal_plonemeeting.userIsAmong("creators")'
        for cfg in self.portal.portal_plonemeeting.objectValues('MeetingConfig'):
            if 'searchreturnedtoserviceitems' in cfg.topics.objectIds():
                cfg.topics.manage_delObjects(ids=['searchreturnedtoserviceitems', ])

            searchcorrecteditems = getattr(cfg.topics, 'searchcorrecteditems', None)
            if searchcorrecteditems and searchcorrecteditems.getProperty('topic_search_script'):
                searchcorrecteditems.manage_changeProperties(topic_search_script='')
                criteria = [criterion.field for criterion in searchcorrecteditems.listCriteria()]
                if not 'previous_review_state' in criteria:
                    criterion = searchcorrecteditems.addCriterion(field='previous_review_state',
                                                                  criterion_type='ATListCriterion')
                    criterion.setValue(('returned_to_proposing_group',))

            searchitemstocorrect = getattr(cfg.topics, 'searchitemstocorrect', None)
            if searchitemstocorrect and not searchitemstocorrect.getProperty('topic_tal_expression') == topicCondition:
                searchitemstocorrect.manage_changeProperties(topic_tal_expression=topicCondition)

    def run(self):
        logger.info('Migrating to MeetingLalouviere 3.2.0.1...')
        self._updateTopics()
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Update search items to correct topics.
    '''
    migrate_to_3_2_0_1(context).run()
# ------------------------------------------------------------------------------
