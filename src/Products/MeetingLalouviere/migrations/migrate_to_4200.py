# -*- coding: utf-8 -*-
from datetime import datetime

from DateTime import DateTime
from plone import api
from Products.MeetingCommunes.migrations.migrate_to_4200 import Migrate_To_4200 as MCMigrate_To_4200
from Products.MeetingLalouviere.config import LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS, LLO_APPLYED_COUNCIL_WFA, \
    LLO_APPLYED_COLLEGE_WFA
from Products.MeetingLalouviere.config import LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS
from Products.PloneMeeting.config import NO_COMMITTEE
import logging

from plone.app.textfield import RichTextValue

logger = logging.getLogger('MeetingLalouviere')

# ids of commissions used as categories for MeetingItemCouncil
# before 2013, commission ids were :
COUNCIL_COMMISSION_IDS = (
    "commission-travaux",
    "commission-enseignement",
    "commission-cadre-de-vie-et-logement",
    "commission-ag",
    "commission-finances-et-patrimoine",
    "commission-police",
    "commission-speciale",
)
# until 2013, commission ids are :
# changes are about 'commission-enseignement', 'commission-cadre-de-vie-et-logement' and
# 'commission-finances-et-patrimoine' that are splitted in smaller commissions
COUNCIL_COMMISSION_IDS_2013 = (
    "commission-ag",
    "commission-finances",
    "commission-enseignement",
    "commission-culture",
    "commission-sport",
    "commission-sante",
    "commission-police",
    "commission-cadre-de-vie",
    "commission-patrimoine",
    "commission-travaux",
    "commission-speciale",
)
# commissions taken into account on the Meeting
# since 2013, some commissions are made of several categories...
COUNCIL_MEETING_COMMISSION_IDS_2013 = (
    "commission-travaux",
    (
        "commission-ag",
        "commission-finances",
        "commission-enseignement",
        "commission-culture",
        "commission-sport",
        "commission-sante",
    ),
    ("commission-cadre-de-vie", "commission-patrimoine",),
    "commission-police",
    "commission-speciale",
)

# commissions taken into account on the Meeting
# since 2019, travaux and finance are merge. ag and enseignement are merged
COUNCIL_MEETING_COMMISSION_IDS_2019 = (
    ("commission-travaux", "commission-finances"),
    (
        "commission-ag",
        "commission-enseignement",
        "commission-culture",
        "commission-sport",
        "commission-sante",
    ),
    ("commission-cadre-de-vie", "commission-patrimoine",),
    "commission-police",
    "commission-speciale",
)

# commissions taken into account on the Meeting
# since 2020, patrimoine is moved with travaux and finance
COUNCIL_MEETING_COMMISSION_IDS_2020 = (
    ("commission-travaux", "commission-finances", "commission-patrimoine"),
    (
        "commission-ag",
        "commission-enseignement",
        "commission-culture",
        "commission-sport",
        "commission-sante",
    ),
    "commission-cadre-de-vie",
    "commission-police",
    "commission-speciale",
)

Travaux_Finances_Patrimoine = "committee_2020-01-01.2501162132"
AG_Enseignement_Culture_Sport_Sante = "committee_2019-01-01.2501153343"
Cadre_Vie = "committee_2013-01-01.2501163335"
Police = "committee_2012-01-01.9920407131"
Speciale = "committee_2012-01-01.5810485069"
Travaux = 'committee_old_2012.5267121837'
Enseignement = 'committee_old_2012.5810478389'
Cadre_Vie_Logement = 'committee_old_2012.5810479936'
AG = 'committee_old_2012.5810473741'
Finances_Patrimoine = 'committee_old_2012.9920391524'
AG_Finances_Enseignement_Culture_Sport_Sante = 'committee_old_2013.2501155949'
Travaux_Finances = 'committee_old_2019.2501156983'
Cadre_Vie_Patrimoine = 'committee_old_2013.2501159941'
Conseillers2 = 'points-conseillers-2eme-supplement'
Conseillers3 = 'points-conseillers-3eme-supplement'

COMMITTEES_TO_APPLY = ({'acronym': 'Trav',
                        'default_assembly': 'Monsieur J-C WARGNIE, Président,\r\nMadame L. ANCIAUX, Vice-présidente,\r\nMessieurs F. ROMEO, J. CHRISTIAENS, G. CALUCCI, Madame M. MULA, Messieurs M. PRIVITERA,\r\nS. ARNONE, Madame L. RUSSO, Monsieur C. BAISE, Madame P. TREMERIE,\r\nMessieurs A. HERMANT, M. PUDDU, X. PAPIER, Conseillers communaux',
                        'enabled': '1', 'default_signatures': '', 'label': 'Travaux/Finances/Patrimoine',
                        'auto_from': [], 'supplements': '1', 'enable_editors': '1',
                        'using_groups': ['843301b27d114daebc35905474ec156a', '0809c5964f50408aa801e091b6f3b23f',
                                         '893c88f7c43840388c8e1948782a770b', '3c52600f35f5482db0e53da9b6082a01',
                                         'ff6d050d17af43e7a422743426b9aafd', 'f2c8d805287341acb9a0925f4c5dcbb1',
                                         '7757427ce7d84b0b94b7503f69a51cce', '508ec1d5d0784e21bdd974cb32f82e05',
                                         '5b40654fea9d4676babfac34606ef403', '2dbe052d05f249dca5aa24912bc2ec21',
                                         '50bb634c3e9e4587ae285bab61f8cacb', 'da8551f7a47d4c0bb8d58b891ee960ce',
                                         '570118a8dcd84a3dae0bcee18dfbc438', 'ba9890fd253f4417bea2bbe5ed257d90',
                                         '8dd4df88aae54a51bf43cbda571895e9', 'ef1b31ae129844b7b098fe2a0995bd85',
                                         '5fa4384ca4194ab2a5a28a978202769e', 'd3c317ef1b144bebb031237d056dc2b4',
                                         '500d2bfec87a451c8e325f98309e6302', '4d92df8b012b45d7b170f6cd2cb279bc',
                                         '2a7766da63a747a2899392073dc937bd', '981203fe9739463a9a52a77b07c25dfd',
                                         'e9e67ad2ac6b4b08928e0682eaa75d3a', 'b9360e44854d4a8c87ae819a487e14d8',
                                         'f32d4ddfe0c5439ba771f7fda0433f27', 'c03242739b4e419ea8b2711d17a3ad8d',
                                         '542bd43a923c45c2a2f71761f2c73170', '30e293281da64c94bbfa489f11e2f8a3',
                                         '70669cb6d46543b9934c5eda6f6f974d', 'a703656d46c6405ab61e411943362cbe',
                                         'a32057437cab49239ab418f813ee1065', '164c003feb2b4b5da3268f66b5f406f4',
                                         'c36574b37e9c4ca79daec4649224a2aa', '8ca452441675410199cd68f9907c38ef',
                                         '5fa1d9cf3d0f4e328b6d292de1b664f8', 'd7e864f55c8d40cab54320bac3bb39e7',
                                         'a3bb631571b24ed1b2d9e84d27155f49', '2b08cf70eacf48e8ac1bf67c67bf17fd',
                                         '18123057e35a49ba8e9b6bef96097d20', '886a99faf1354422a895e2b9a400e353',
                                         '916091c475384010b3bba08b403dbd4d', '8556663bd1404016ba7775c1f824e028',
                                         'b72c3c9dd2e243a399544826ec0b4ce7', '389d6396406c4c0f9731633803f83e63',
                                         '5714e6b160c843e0b5cbd8dccdc73106', '5cb2e0db83fc401e8589c3c94969555b',
                                         '5e0e122407894b44ba9c126b342c7a34', '84e1ec45691f4a029e3bbf80773f2e6b',
                                         '2d8baba0c9884800931f59ab0e9eedcc'], 'default_signatories': [],
                        'row_id': 'committee_2020-01-01.2501162132', 'default_attendees': [],
                        'default_place': 'Salle du Conseil, 1er étage'}, {'acronym': 'AG',
                                                                          'default_assembly': 'Madame M. SPANO, Présidente,\r\nMonsieur A. AYCIK, Vice-président,\r\nMonsieur J-C WARGNIE, Madame D. STAQUET, Monsieur M. BURY, Madame M. MULA, Monsieur M. DI MATTIA,\r\nMesdames \xc3\x96. KAZANCI, L. LEONI, Monsieur M. SIASSIA-BULA,\r\nMesdames A. LECOCQ, L. LUMIA, Messieurs O. DESTREBECQ, O. LAMAND, Conseillers communaux',
                                                                          'enabled': '1',
                                                                          'default_signatures': '',
                                                                          'label': 'AG/Enseignement/Culture/Sport/Santé',
                                                                          'auto_from': [], 'supplements': '1',
                                                                          'enable_editors': '1',
                                                                          'using_groups': [
                                                                              'f063efbad17c48c3b7698dc7bfa21874',
                                                                              '0b1dc26e0156499aa3f8f9d3bfabe2c0',
                                                                              '7595cef78cfa4d74a28f65ac77f29303',
                                                                              '843301b27d114daebc35905474ec156a',
                                                                              'fe6f6d6e268248e784d85db9cd026133',
                                                                              '12d8cc8f4eba4052a7feb4bce6e2e638',
                                                                              'd699e77993674270aff42514dfdea023',
                                                                              '66e3a85f3f2a4cc8a7de8f24f94bd9d0',
                                                                              'e52602fab08c4a6ea35468188c1010a9',
                                                                              '3ad5eceedfb44df3a56f17b401c69538',
                                                                              'd1f710dec5964a2ebec6d38bc675def5',
                                                                              '0809c5964f50408aa801e091b6f3b23f',
                                                                              '893c88f7c43840388c8e1948782a770b',
                                                                              'cfadf496cc524f22a601a684ba78ff2f',
                                                                              '819c8dff530049328016e5f4d6d40d66',
                                                                              '6ef1b91b3fe94e559fee8f44c13a957f',
                                                                              'fffda58df66c48a3baaa8c76d22e0c8c',
                                                                              '23a2d1e9570e483bb64c211f769d96c2',
                                                                              '3c52600f35f5482db0e53da9b6082a01',
                                                                              'ff6d050d17af43e7a422743426b9aafd',
                                                                              'f2c8d805287341acb9a0925f4c5dcbb1',
                                                                              '7757427ce7d84b0b94b7503f69a51cce',
                                                                              '508ec1d5d0784e21bdd974cb32f82e05',
                                                                              '5b40654fea9d4676babfac34606ef403',
                                                                              '2dbe052d05f249dca5aa24912bc2ec21',
                                                                              '50bb634c3e9e4587ae285bab61f8cacb',
                                                                              'da8551f7a47d4c0bb8d58b891ee960ce',
                                                                              '570118a8dcd84a3dae0bcee18dfbc438',
                                                                              'ba9890fd253f4417bea2bbe5ed257d90',
                                                                              '8dd4df88aae54a51bf43cbda571895e9',
                                                                              'ef1b31ae129844b7b098fe2a0995bd85',
                                                                              '5fa4384ca4194ab2a5a28a978202769e',
                                                                              'd3c317ef1b144bebb031237d056dc2b4',
                                                                              '66eb0d5a256e414284720a155a304f84',
                                                                              'f7e5bab37ab34cc685806ddc55dff392',
                                                                              'b2401156e95c488ba5076dd58bde0c6d',
                                                                              '3451b2f241124a0497d8cb62945a9549',
                                                                              'c3b40b10927a481a8c02e992072da6af',
                                                                              '4971d56a17334da08f3780e3e5713d77',
                                                                              '99f2f3b4545f4b3790037f7e28825549',
                                                                              '21ae631cbfee4fce8b9ecdd36b18a8e9',
                                                                              'bdbc47c1e99746ee950b3ac4359f2873',
                                                                              '0c1e1980a2f04c85b82fada3d193002a',
                                                                              '500d2bfec87a451c8e325f98309e6302',
                                                                              '4d92df8b012b45d7b170f6cd2cb279bc',
                                                                              '2a7766da63a747a2899392073dc937bd',
                                                                              '981203fe9739463a9a52a77b07c25dfd',
                                                                              'e9e67ad2ac6b4b08928e0682eaa75d3a',
                                                                              'b9360e44854d4a8c87ae819a487e14d8',
                                                                              'f32d4ddfe0c5439ba771f7fda0433f27',
                                                                              '7a80b52446b9474fba85bd0a6bdb03b5',
                                                                              'a13f8295a5d04f198e59a0bd5c961762',
                                                                              '8add429a5a8e445db0e24f95987c6e89',
                                                                              '4586abeab2f042eab439d2cc58fe347b',
                                                                              '2ddf3f273c6341049cb080bbff105944',
                                                                              '164c003feb2b4b5da3268f66b5f406f4',
                                                                              'c36574b37e9c4ca79daec4649224a2aa',
                                                                              '8ca452441675410199cd68f9907c38ef',
                                                                              '2b08cf70eacf48e8ac1bf67c67bf17fd',
                                                                              'c9dd9894ae0240ca8dec6ffbdf04ee8b',
                                                                              '18123057e35a49ba8e9b6bef96097d20',
                                                                              'c526a73e7a4c4db99257fb3b18d19a96',
                                                                              '8d6ddf3276cc413e995f3b9405a0f581',
                                                                              '886a99faf1354422a895e2b9a400e353',
                                                                              '61d65007ad424236996308809eff4835',
                                                                              'c73927442a954caf9c86e6162731e2cc',
                                                                              '31ee37015bb4472ea280b019718d48dc',
                                                                              'a9acb79e3acf4950b6291a1bc21b3367',
                                                                              '60107d506624436dbd75c88208437687',
                                                                              '916091c475384010b3bba08b403dbd4d',
                                                                              '8cdc1ec4207546ffb91adc2e64d0e00f',
                                                                              '1b367da6d6434d75b75f7d048223c0e6',
                                                                              'b862c4b580bb49d8895da3ac397c8bca',
                                                                              '8556663bd1404016ba7775c1f824e028',
                                                                              'dc11fd4ecf5944b2ad917e4cd3135c5d',
                                                                              '7074868b5e36419a854706d12273a912',
                                                                              'b72c3c9dd2e243a399544826ec0b4ce7',
                                                                              'fc6d4d3307184b53a6ea6317ebb7a7d2'],
                                                                          'default_signatories': [],
                                                                          'row_id': 'committee_2019-01-01.2501153343',
                                                                          'default_attendees': [],
                                                                          'default_place': 'Salle du Collège, 2ème étage'},
                       {'acronym': 'Vie',
                        'default_assembly': 'Madame L. RUSSO, Présidente,\r\nMonsieur M. DI MATTIA, Vice-président,\r\nMadame O. ZRIHEN, Monsieur A. AYCIK, Mesdames M. SPANO, \xc3\x96. KAZANCI,\r\nMessieurs S. ARNONE, J. CHRISTIAENS, M. BURY, O. DESTREBECQ,\r\nMessieurs M. SIASSIA-BULA, A. CLEMENT,\r\nMadame A. SOMMEREYNS, Monsieur L. RESINELLI, Conseillers communaux',
                        'enabled': '1', 'default_signatures': '', 'label': 'Cadre de Vie', 'auto_from': [],
                        'supplements': '1', 'enable_editors': '1',
                        'using_groups': ['843301b27d114daebc35905474ec156a', '0809c5964f50408aa801e091b6f3b23f',
                                         '893c88f7c43840388c8e1948782a770b', '04f6ac4a441d46f3b5c4f10935e01a05',
                                         '0468c2e8f60444d4914655221daba722', '55409a7b622b482694b556bc02bd7331',
                                         '6176bf4fc16446e6a8333bf716bbd027', '7c262f1e29ec419d92e552785442907d',
                                         '8653bd8209eb4a768d24806f02b2fdc9', '22031a4b3d9e4cbb9b116dfd9d65e8b8',
                                         'f5a7bee0553a4702ad716336cc4131bf', 'f4b415a83ad2493d865e40924582578d',
                                         '1a72c41e55914a67b83a75dc59ff487b', '88d0276c5367406e8a39715f4303bb5d',
                                         '92f46176f7f446d5b92c7cc4a365b84c', 'fa33e8c11bf6456ab231063d36e27712',
                                         '3c52600f35f5482db0e53da9b6082a01', 'ff6d050d17af43e7a422743426b9aafd',
                                         'f2c8d805287341acb9a0925f4c5dcbb1', '7757427ce7d84b0b94b7503f69a51cce',
                                         '508ec1d5d0784e21bdd974cb32f82e05', '5b40654fea9d4676babfac34606ef403',
                                         '2dbe052d05f249dca5aa24912bc2ec21', '50bb634c3e9e4587ae285bab61f8cacb',
                                         'da8551f7a47d4c0bb8d58b891ee960ce', '570118a8dcd84a3dae0bcee18dfbc438',
                                         'ba9890fd253f4417bea2bbe5ed257d90', '8dd4df88aae54a51bf43cbda571895e9',
                                         'ef1b31ae129844b7b098fe2a0995bd85', '5fa4384ca4194ab2a5a28a978202769e',
                                         'd3c317ef1b144bebb031237d056dc2b4', '500d2bfec87a451c8e325f98309e6302',
                                         '4d92df8b012b45d7b170f6cd2cb279bc', '2a7766da63a747a2899392073dc937bd',
                                         '981203fe9739463a9a52a77b07c25dfd', 'e9e67ad2ac6b4b08928e0682eaa75d3a',
                                         'b9360e44854d4a8c87ae819a487e14d8', '164c003feb2b4b5da3268f66b5f406f4',
                                         'c36574b37e9c4ca79daec4649224a2aa', '8ca452441675410199cd68f9907c38ef',
                                         '2b08cf70eacf48e8ac1bf67c67bf17fd', '18123057e35a49ba8e9b6bef96097d20',
                                         '886a99faf1354422a895e2b9a400e353', '916091c475384010b3bba08b403dbd4d',
                                         '8556663bd1404016ba7775c1f824e028', 'b72c3c9dd2e243a399544826ec0b4ce7'],
                        'default_signatories': [], 'row_id': 'committee_2013-01-01.2501163335', 'default_attendees': [],
                        'default_place': 'Salle du Conseil,1er étage'}, {'acronym': 'Police',
                                                                         'default_assembly': 'Madame D. STAQUET, Présidente,\r\nMadame D. STAQUET, Vice-présidente,\r\nMessieurs F. ROMEO, M. PRIVITERA, Mesdames \xc3\x96. KAZANCI, L. ANCIAUX, M. SPANO,\r\nMessieurs J. CHRISTIAENS, M. BURY, M. BAISE, Madame P. TREMERIE,\r\nMonsieur A. CLEMENT, Madame A. SOMMEREYNS, Monsieur M. VAN HOOLAND,\r\nConseillers communaux',
                                                                         'enabled': '1',
                                                                         'default_signatures': '',
                                                                         'label': 'Police', 'auto_from': [],
                                                                         'supplements': '1',
                                                                         'enable_editors': '1', 'using_groups': [
        '843301b27d114daebc35905474ec156a', '0809c5964f50408aa801e091b6f3b23f', '893c88f7c43840388c8e1948782a770b',
        '3c52600f35f5482db0e53da9b6082a01', 'ff6d050d17af43e7a422743426b9aafd', 'f2c8d805287341acb9a0925f4c5dcbb1',
        '7757427ce7d84b0b94b7503f69a51cce', '508ec1d5d0784e21bdd974cb32f82e05', '5b40654fea9d4676babfac34606ef403',
        '2dbe052d05f249dca5aa24912bc2ec21', '50bb634c3e9e4587ae285bab61f8cacb', 'da8551f7a47d4c0bb8d58b891ee960ce',
        '570118a8dcd84a3dae0bcee18dfbc438', 'ba9890fd253f4417bea2bbe5ed257d90', '8dd4df88aae54a51bf43cbda571895e9',
        'ef1b31ae129844b7b098fe2a0995bd85', '5fa4384ca4194ab2a5a28a978202769e', 'd3c317ef1b144bebb031237d056dc2b4',
        '500d2bfec87a451c8e325f98309e6302', '4d92df8b012b45d7b170f6cd2cb279bc', '2a7766da63a747a2899392073dc937bd',
        '981203fe9739463a9a52a77b07c25dfd', 'e9e67ad2ac6b4b08928e0682eaa75d3a', 'b9360e44854d4a8c87ae819a487e14d8',
        'a32057437cab49239ab418f813ee1065', '164c003feb2b4b5da3268f66b5f406f4', 'c36574b37e9c4ca79daec4649224a2aa',
        '8ca452441675410199cd68f9907c38ef', '2b08cf70eacf48e8ac1bf67c67bf17fd', '18123057e35a49ba8e9b6bef96097d20',
        '886a99faf1354422a895e2b9a400e353', '8f4d21e5a9d94896bcad70783b556b29', '1bd03e0f7faa498dbb374e99f253236c',
        '1e0e69a272cd4fad9bce6bf8c5bd74d0', 'ae1e9bb3158b4d48a48a9580e0f73d1d', '44fb1ae0aa5a44989e21c38e65ea72b4',
        '1b367da6d6434d75b75f7d048223c0e6', '8556663bd1404016ba7775c1f824e028', 'b72c3c9dd2e243a399544826ec0b4ce7'],
                                                                         'default_signatories': [],
                                                                         'row_id': 'committee_2012-01-01.9920407131',
                                                                         'default_attendees': [],
                                                                         'default_place': 'Salle du Collège, 2ème étage'},
                       {'acronym': 'Spe', 'default_assembly': '', 'enabled': '1', 'default_signatures': '',
                        'label': 'Spéciale', 'auto_from': [], 'supplements': '1', 'enable_editors': '1',
                        'using_groups': ['843301b27d114daebc35905474ec156a', '0809c5964f50408aa801e091b6f3b23f',
                                         '893c88f7c43840388c8e1948782a770b', '3c52600f35f5482db0e53da9b6082a01',
                                         'ff6d050d17af43e7a422743426b9aafd', 'f2c8d805287341acb9a0925f4c5dcbb1',
                                         '7757427ce7d84b0b94b7503f69a51cce', '508ec1d5d0784e21bdd974cb32f82e05',
                                         '5b40654fea9d4676babfac34606ef403', '2dbe052d05f249dca5aa24912bc2ec21',
                                         '50bb634c3e9e4587ae285bab61f8cacb', 'da8551f7a47d4c0bb8d58b891ee960ce',
                                         '570118a8dcd84a3dae0bcee18dfbc438', 'ba9890fd253f4417bea2bbe5ed257d90',
                                         '8dd4df88aae54a51bf43cbda571895e9', 'ef1b31ae129844b7b098fe2a0995bd85',
                                         '5fa4384ca4194ab2a5a28a978202769e', 'd3c317ef1b144bebb031237d056dc2b4',
                                         '500d2bfec87a451c8e325f98309e6302', '4d92df8b012b45d7b170f6cd2cb279bc',
                                         '2a7766da63a747a2899392073dc937bd', '981203fe9739463a9a52a77b07c25dfd',
                                         'e9e67ad2ac6b4b08928e0682eaa75d3a', 'b9360e44854d4a8c87ae819a487e14d8',
                                         '164c003feb2b4b5da3268f66b5f406f4', 'c36574b37e9c4ca79daec4649224a2aa',
                                         '8ca452441675410199cd68f9907c38ef', '2b08cf70eacf48e8ac1bf67c67bf17fd',
                                         '18123057e35a49ba8e9b6bef96097d20', '886a99faf1354422a895e2b9a400e353',
                                         '916091c475384010b3bba08b403dbd4d', '8556663bd1404016ba7775c1f824e028',
                                         'b72c3c9dd2e243a399544826ec0b4ce7'], 'default_signatories': [],
                        'row_id': 'committee_2012-01-01.5810485069', 'default_attendees': [], 'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': '0', 'default_signatures': '',
                        'label': 'Travaux', 'auto_from': [], 'supplements': '1', 'enable_editors': '0',
                        'using_groups': [], 'default_signatories': [], 'row_id': 'committee_old_2012.5267121837',
                        'default_attendees': [], 'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': '0', 'default_signatures': '',
                        'label': 'Enseignement', 'auto_from': [], 'supplements': '1', 'enable_editors': '0',
                        'using_groups': [], 'default_signatories': [], 'row_id': 'committee_old_2012.5810478389',
                        'default_attendees': [], 'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': '0', 'default_signatures': '',
                        'label': 'Cadre de Vie et Logement', 'auto_from': [], 'supplements': '1', 'enable_editors': '0',
                        'using_groups': [], 'default_signatories': [], 'row_id': 'committee_old_2012.5810479936',
                        'default_attendees': [], 'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': '0', 'default_signatures': '', 'label': 'AG',
                        'auto_from': [], 'supplements': '1', 'enable_editors': '0', 'using_groups': [],
                        'default_signatories': [], 'row_id': 'committee_old_2012.5810473741', 'default_attendees': [],
                        'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': '0', 'default_signatures': '',
                        'label': 'Finances et Patrimoine', 'auto_from': [], 'supplements': '1', 'enable_editors': '0',
                        'using_groups': [], 'default_signatories': [], 'row_id': 'committee_old_2012.9920391524',
                        'default_attendees': [], 'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': '0', 'default_signatures': '',
                        'label': 'AG/Finances/Enseignement/Culture/Sport/Santé', 'auto_from': [],
                        'supplements': '1', 'enable_editors': '0', 'using_groups': [], 'default_signatories': [],
                        'row_id': 'committee_old_2013.2501155949', 'default_attendees': [], 'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': '0', 'default_signatures': '',
                        'label': 'Cadre de Vie/Patrimoine', 'auto_from': [], 'supplements': '1', 'enable_editors': '0',
                        'using_groups': [], 'default_signatories': [], 'row_id': 'committee_old_2013.2501159941',
                        'default_attendees': [], 'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': '0', 'default_signatures': '',
                        'label': 'Travaux/Finances', 'auto_from': [], 'supplements': '1', 'enable_editors': '0',
                        'using_groups': [], 'default_signatories': [], 'row_id': 'committee_old_2019.2501156983',
                        'default_attendees': [], 'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': 'item_only', 'default_signatures': '',
                        'label': 'Points conseillers (2ème supplément)', 'auto_from': [],
                        'supplements': '0', 'enable_editors': '0',
                        'using_groups': ['500d2bfec87a451c8e325f98309e6302', '4d92df8b012b45d7b170f6cd2cb279bc',
                                         '2a7766da63a747a2899392073dc937bd', '981203fe9739463a9a52a77b07c25dfd',
                                         'e9e67ad2ac6b4b08928e0682eaa75d3a', 'b9360e44854d4a8c87ae819a487e14d8',
                                         'b72c3c9dd2e243a399544826ec0b4ce7'], 'default_signatories': [],
                        'row_id': 'points-conseillers-2eme-supplement', 'default_attendees': [], 'default_place': ''},
                       {'acronym': '', 'default_assembly': '', 'enabled': 'item_only', 'default_signatures': '',
                        'label': 'Points conseillers (3ème supplément)', 'auto_from': [],
                        'supplements': '0', 'enable_editors': '0',
                        'using_groups': ['500d2bfec87a451c8e325f98309e6302', '4d92df8b012b45d7b170f6cd2cb279bc',
                                         '2a7766da63a747a2899392073dc937bd', '981203fe9739463a9a52a77b07c25dfd',
                                         'e9e67ad2ac6b4b08928e0682eaa75d3a', 'b9360e44854d4a8c87ae819a487e14d8',
                                         'b72c3c9dd2e243a399544826ec0b4ce7'], 'default_signatories': [],
                        'row_id': 'points-conseillers-3eme-supplement', 'default_attendees': [], 'default_place': ''})

COMMITTEES_2020 = [Travaux_Finances_Patrimoine, AG_Enseignement_Culture_Sport_Sante, Cadre_Vie, Police, Speciale]
COMMITTEES_2019 = [Travaux_Finances, AG_Enseignement_Culture_Sport_Sante, Cadre_Vie_Patrimoine, Police, Speciale]
COMMITTEES_2013 = [Travaux, AG_Finances_Enseignement_Culture_Sport_Sante, Cadre_Vie_Patrimoine, Police, Speciale]
COMMITTEES_2012 = [Travaux, Enseignement, Cadre_Vie_Logement, AG, Finances_Patrimoine, Police, Speciale]


class Migrate_To_4200(MCMigrate_To_4200):

    def _replace_user_committee_editors(self):
        binding = {
            "commission-travaux_commissioneditors": Travaux_Finances_Patrimoine,
            "commission-sport_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
            "commission-speciale_commissioneditors": Speciale,
            "commission-sante_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
            "commission-police_commissioneditors": Police,
            "commission-patrimoine_commissioneditors": Travaux_Finances_Patrimoine,
            "commission-finances_commissioneditors": Travaux_Finances_Patrimoine,
            "commission-enseignement_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
            "commission-cadre-de-vie_commissioneditors": Cadre_Vie,
            "commission-ag_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
            "commission-culture_commissioneditors": AG_Enseignement_Culture_Sport_Sante,
        }
        group_tool = self.portal.portal_groups
        meetingmanagers = group_tool.getGroupById('meeting-config-council_meetingmanagers').getAllGroupMemberIds()
        for old_commission in binding:
            group = group_tool.getGroupById(old_commission)
            if group:
                members = group.getAllGroupMemberIds()
                new_group = group_tool.getGroupById("meeting-config-council_" + binding[old_commission])
                for member in members:
                    group.removeMember(member)
                    if new_group and member not in meetingmanagers:
                        new_group.addMember(member)
                group_tool.removeGroup(group.getId())

    def _applyMeetingConfig_fixtures(self):
        logger.info('applying meetingconfig fixtures...')
        self.updateTALConditions("year()", "year")
        self.updateTALConditions("month()", "month")
        self.cleanUsedItemAttributes(['classifier', 'commissionTranscript', 'neededFollowUp', 'decisionSuite'])
        self.cleanUsedMeetingAttributes(["preMeetingDate", "preMeetingPlace", "preMeetingAssembly",
                                         "preMeetingDate_2", "preMeetingPlace_2", "preMeetingAssembly_2",
                                         "preMeetingDate_3", "preMeetingPlace_3", "preMeetingAssembly_3",
                                         "preMeetingDate_4", "preMeetingPlace_4", "preMeetingAssembly_4",
                                         "preMeetingDate_5", "preMeetingPlace_5", "preMeetingAssembly_5",
                                         "preMeetingDate_6", "preMeetingPlace_6", "preMeetingAssembly_6",
                                         "preMeetingDate_7", "preMeetingPlace_7", "preMeetingAssembly_7",
                                         "first_item_number",
                                         ])
        logger.info("Adapting 'meetingWorkflow/meetingItemWorkflow' for every MeetingConfigs...")
        for cfg in self.tool.objectValues('MeetingConfig'):
            if 'council' in cfg.getId():
                cfg.setCommittees(COMMITTEES_TO_APPLY)
                cfg.createCommitteeEditorsGroups()
                self._replace_user_committee_editors()
                # Force init some fields
                cfg.setItemCommitteesStates(('presented', 'itemfrozen', 'itempublished'))
                cfg.setItemCommitteesViewStates(('presented', 'itemfrozen', 'itempublished', 'accepted',
                                                 'accepted_but_modified', 'pre_accepted', 'refused', 'delayed',
                                                 'removed',
                                                 'returned_to_proposing_group'))
                used_meeting_attr = list(cfg.getUsedMeetingAttributes())
                used_meeting_attr.append("committees")
                used_meeting_attr.append("committees_assembly")
                used_meeting_attr.append("committees_place")
                # meeting_number will be used in convocations in meeting reference field
                for attribute in ("pre_meeting_date", "pre_meeting_place"):
                    if attribute in used_meeting_attr:
                        used_meeting_attr.remove(attribute)
                cfg.setUsedMeetingAttributes(tuple(used_meeting_attr))
                used_item_attr = list(cfg.getUsedItemAttributes())
                used_item_attr.append("committeeTranscript")
                used_item_attr.append("votesResult")
                cfg.setUsedItemAttributes(tuple(used_item_attr))
                cfg.setWorkflowAdaptations(LLO_APPLYED_COUNCIL_WFA)
                cfg.setDashboardItemsListingsFilters(
                    self.replace_in_list("c24", "c31", cfg.getDashboardItemsListingsFilters()))
                cfg.setDashboardMeetingAvailableItemsFilters(
                    self.replace_in_list("c24", "c31", cfg.getDashboardMeetingAvailableItemsFilters()))
                cfg.setDashboardMeetingLinkedItemsFilters(
                    self.replace_in_list("c24", "c31", cfg.getDashboardMeetingLinkedItemsFilters()))
            else:
                cfg.setWorkflowAdaptations(LLO_APPLYED_COLLEGE_WFA)
            # replace action and review_state column by async actions
            self.updateColumns(to_replace={'actions': 'async_actions',
                                           'review_state': 'review_state_title',
                                           'getRawClassifier': 'committees_index'})
            # remove old attrs
            old_attrs = ('preMeetingAssembly_default', 'preMeetingAssembly_2_default', 'preMeetingAssembly_3_default',
                         'preMeetingAssembly_4_default', 'preMeetingAssembly_5_default', 'preMeetingAssembly_6_default',
                         'preMeetingAssembly_7_default')
            for field in old_attrs:
                if hasattr(cfg, field):
                    delattr(cfg, field)

            cfg.setItemBudgetInfosStates(self.replace_in_list(u'proposed_to_budgetimpact_reviewer',
                                                              u'proposed_to_budget_reviewer',
                                                              cfg.getItemBudgetInfosStates())
                                         )
            cfg.setItemAdviceStates(self.replace_in_list(u'proposed_to_budgetimpact_reviewer',
                                                         u'proposed_to_budget_reviewer',
                                                         cfg.getItemAdviceStates())
                                    )
            cfg.setItemAdviceViewStates(self.replace_in_list(u'proposed_to_budgetimpact_reviewer',
                                                             u'proposed_to_budget_reviewer',
                                                             cfg.getItemAdviceViewStates())
                                        )
            cfg.setItemAdviceEditStates(self.replace_in_list(u'proposed_to_budgetimpact_reviewer',
                                                             u'proposed_to_budget_reviewer',
                                                             cfg.getItemAdviceEditStates())
                                        )
            cfg.setUseVotes('council' in cfg.getId())
            cfg.setVotesResultTALExpr(
                "python: item.getPollType() == 'no_vote' and '' or '<p>&nbsp;</p>' + pm_utils.print_votes(item)")
            cfg.setEnabledAnnexesBatchActions(('delete', 'download-annexes'))

    def replace_in_list(self, to_replace, new_value, list):
        result = set()
        for value in list:
            if value == to_replace:
                result.add(new_value)
            else:
                result.add(value)
        return tuple(result)

    def _fixUsedMeetingWFs(self):
        # remap states and transitions
        for cfg in self.tool.objectValues('MeetingConfig'):
            # ensure attr exists
            cfg.getCommittees()
            cfg.getItemCommitteesStates()
            cfg.getItemCommitteesViewStates()
            cfg.getItemPreferredMeetingStates()
            cfg.getItemObserversStates()
            cfg.setMeetingWorkflow('meeting_workflow')
            cfg.setItemWorkflow('meetingitem_workflow')
            cfg.setItemConditionsInterface(
                'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions')
            cfg.setItemActionsInterface(
                'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions')
            cfg.setMeetingConditionsInterface(
                'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions')
            cfg.setMeetingActionsInterface(
                'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions')

        # delete old unused workflows
        wfs_to_delete = [wfId for wfId in self.wfTool.listWorkflows()
                         if any(x in wfId for x in (
                'meetingcollegelalouviere_workflow',
                'meetingcouncillalouviere_workflow',
                'meetingitemcollegelalouviere_workflow',
                'meetingitemcouncillalouviere_workflow'))]
        if wfs_to_delete:
            self.wfTool.manage_delObjects(wfs_to_delete)
        logger.info('Done.')

    def _get_wh_key(self, itemOrMeeting):
        """Get workflow_history key to use, in case there are several keys, we take the one
           having the last event."""
        keys = itemOrMeeting.workflow_history.keys()
        if len(keys) == 1:
            return keys[0]
        else:
            lastEventDate = DateTime('1950/01/01')
            keyToUse = None
            for key in keys:
                if itemOrMeeting.workflow_history[key][-1]['time'] > lastEventDate:
                    lastEventDate = itemOrMeeting.workflow_history[key][-1]['time']
                    keyToUse = key
            return keyToUse

    def _adaptWFHistoryForItemsAndMeetings(self):
        """We use PM default WFs, no more meeting(item)lalouviere_workflow..."""
        logger.info('Updating WF history items and meetings to use new WF id...')
        catalog = api.portal.get_tool('portal_catalog')
        for cfg in self.tool.objectValues('MeetingConfig'):
            # this will call especially part where we duplicate WF and apply WFAdaptations
            cfg.registerPortalTypes()
            for brain in catalog(portal_type=(cfg.getItemTypeName(), cfg.getMeetingTypeName())):
                itemOrMeeting = brain.getObject()
                itemOrMeetingWFId = self.wfTool.getWorkflowsFor(itemOrMeeting)[0].getId()
                if itemOrMeetingWFId not in itemOrMeeting.workflow_history:
                    wf_history_key = self._get_wh_key(itemOrMeeting)
                    itemOrMeeting.workflow_history[itemOrMeetingWFId] = \
                        tuple(itemOrMeeting.workflow_history[wf_history_key])
                    del itemOrMeeting.workflow_history[wf_history_key]
                    # do this so change is persisted
                    itemOrMeeting.workflow_history = itemOrMeeting.workflow_history
                else:
                    # already migrated
                    break
        logger.info('Done.')

    def _doConfigureItemWFValidationLevels(self, cfg):
        """Apply correct itemWFValidationLevels and fix WFAs."""
        cfg.setItemWFValidationLevels(cfg.getId() == 'meeting-config-council' and
                                      LLO_ITEM_COUNCIL_WF_VALIDATION_LEVELS or
                                      LLO_ITEM_COLLEGE_WF_VALIDATION_LEVELS)

        cfg.setWorkflowAdaptations(cfg.getId() == 'meeting-config-council' and
                                   LLO_APPLYED_COUNCIL_WFA or
                                   LLO_APPLYED_COLLEGE_WFA)

    def _hook_custom_meeting_to_dx(self, old, new):

        def get_committee(date, assembly, place, row_id):
            date._timezone_naive = True
            datetime = date.asdatetime()
            return {'assembly': RichTextValue(assembly.raw, 'text/plain', 'text/x-html-safe'),
                    'attendees': None,
                    'committee_observations': None,
                    'convocation_date': None,
                    'date': datetime,  # fill selected date in old
                    'place': place,  # fill place value in old
                    'row_id': row_id,  # fill row_id un cfg
                    'signatories': None,
                    'signatures': None}

        if new.portal_type == 'MeetingCouncil':
            committees = []
            if old.preMeetingDate:
                committees.append(get_committee(old.preMeetingDate, old.preMeetingAssembly,
                                                old.preMeetingPlace, self.find_committee_row_id(1, old.getDate())))
            if hasattr(old, 'preMeetingDate_2') and old.preMeetingDate_2:
                committees.append(get_committee(old.preMeetingDate_2, old.preMeetingAssembly_2,
                                                old.preMeetingPlace_2, self.find_committee_row_id(2, old.getDate())))
            if hasattr(old, 'preMeetingDate_3') and old.preMeetingDate_3:
                committees.append(get_committee(old.preMeetingDate_3, old.preMeetingAssembly_3,
                                                old.preMeetingPlace_3, self.find_committee_row_id(3, old.getDate())))
            if hasattr(old, 'preMeetingDate_4') and old.preMeetingDate_4:
                committees.append(get_committee(old.preMeetingDate_4, old.preMeetingAssembly_4,
                                                old.preMeetingPlace_4, self.find_committee_row_id(4, old.getDate())))
            if hasattr(old, 'preMeetingDate_5') and old.preMeetingDate_5:
                committees.append(get_committee(old.preMeetingDate_5, old.preMeetingAssembly_5,
                                                old.preMeetingPlace_5, self.find_committee_row_id(5, old.getDate())))
            if old.getDate().year() <= 2013 and old.getDate().month() < 6:
                if hasattr(old, 'preMeetingDate_6') and old.preMeetingDate_6:
                    committees.append(get_committee(old.preMeetingDate_6, old.preMeetingAssembly_6,
                                                    old.preMeetingPlace_6,
                                                    self.find_committee_row_id(6, old.getDate())))
                if hasattr(old, 'preMeetingDate_7') and old.preMeetingDate_7:
                    committees.append(get_committee(old.preMeetingDate_7, old.preMeetingAssembly_7,
                                                    old.preMeetingPlace_7,
                                                    self.find_committee_row_id(7, old.getDate())))
            new.committees = committees
        new.pre_meeting_date = None
        new.pre_meeting_place = None

    def _hook_after_meeting_to_dx(self):
        self._applyMeetingConfig_fixtures()
        self._adaptWFHistoryForItemsAndMeetings()
        self._adapt_council_items()
        self.update_wf_states_and_transitions()

    def update_wf_states_and_transitions(self):
        self.updateWFStatesAndTransitions(
            query={'portal_type': ('MeetingItemCouncil',)},
            review_state_mappings={
                'item_in_committee': 'itemfrozen',
                'item_in_council': 'itempublished',
            },
            transition_mappings={
                'setItemInCommittee': 'itemfreeze',
                'setItemInCouncil': 'itempublish',
            },
            # will be done by next step in migration
            update_local_roles=False)

        self.updateWFStatesAndTransitions(
            related_to="Meeting",
            query={'portal_type': ('MeetingCouncil',)},
            review_state_mappings={
                'in_committee': 'frozen',
                'in_council': 'decided',
            },
            transition_mappings={
                'setInCommittee': 'freeze',
                'setInCouncil': 'decide',
            },
            # will be done by next step in migration
            update_local_roles=False)

    def find_committee_row_id(self, number, date):
        if not date or date.year() > 2020 or (date.year() == 2020 and date.month() > 8):
            return COMMITTEES_2020[number - 1]
        elif date.year() >= 2019 and date.month() > 8:
            return COMMITTEES_2019[number - 1]
        elif date.year() >= 2013 and date.month() > 5:
            return COMMITTEES_2013[number - 1]
        else:
            return COMMITTEES_2012[number - 1]

    def find_item_committee_row_id(self, date, item_classifier):
        suffix = ""
        if "1er-supplement" in item_classifier:
            suffix = "__suppl__1"
            item_classifier = '-'.join(item_classifier.split('-')[:-2])
        if not date or date.year > 2020 or (date.year == 2020 and date.month > 8):
            binding = {
                "commission-travaux": Travaux_Finances_Patrimoine,
                "commission-sport": AG_Enseignement_Culture_Sport_Sante,
                "commission-speciale": Speciale,
                "commission-sante": AG_Enseignement_Culture_Sport_Sante,
                "commission-police": Police,
                "commission-patrimoine": Travaux_Finances_Patrimoine,
                "commission-finances": Travaux_Finances_Patrimoine,
                "commission-enseignement": AG_Enseignement_Culture_Sport_Sante,
                "commission-cadre-de-vie": Cadre_Vie,
                "commission-ag": AG_Enseignement_Culture_Sport_Sante,
                "commission-culture": AG_Enseignement_Culture_Sport_Sante,
                "points-conseillers-2eme-supplement": Conseillers2,
                "points-conseillers-3eme-supplement": Conseillers3
            }
        elif date.year > 2019 or (date.year == 2019 and date.month > 8):
            binding = {
                "commission-travaux": Travaux_Finances,
                "commission-sport": AG_Enseignement_Culture_Sport_Sante,
                "commission-speciale": Speciale,
                "commission-sante": AG_Enseignement_Culture_Sport_Sante,
                "commission-police": Police,
                "commission-patrimoine": Cadre_Vie_Patrimoine,
                "commission-finances": Travaux_Finances,
                "commission-enseignement": AG_Enseignement_Culture_Sport_Sante,
                "commission-cadre-de-vie": Cadre_Vie_Patrimoine,
                "commission-ag": AG_Enseignement_Culture_Sport_Sante,
                "commission-culture": AG_Enseignement_Culture_Sport_Sante,
                "points-conseillers-2eme-supplement": Conseillers2,
                "points-conseillers-3eme-supplement": Conseillers3
            }
        elif date.year > 2013 or (date.year == 2013 and date.month > 5):
            binding = {
                "commission-travaux": Travaux,
                "commission-sport": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-speciale": Speciale,
                "commission-sante": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-police": Police,
                "commission-patrimoine": Travaux_Finances_Patrimoine,
                "commission-finances": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-enseignement": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-cadre-de-vie": Cadre_Vie,
                "commission-ag": AG_Finances_Enseignement_Culture_Sport_Sante,
                "commission-culture": AG_Finances_Enseignement_Culture_Sport_Sante,
                "points-conseillers-2eme-supplement": Conseillers2,
                "points-conseillers-3eme-supplement": Conseillers3
            }
        else:
            binding = {
                "commission-travaux": Travaux,
                "commission-sport": AG,
                "commission-speciale": Speciale,
                "commission-sante": AG,
                "commission-police": Police,
                "commission-patrimoine": Finances_Patrimoine,
                "commission-finances": Finances_Patrimoine,
                "commission-enseignement": Enseignement,
                "commission-cadre-de-vie": Cadre_Vie_Logement,
                "commission-ag": AG,
                "commission-culture": AG,
                "commission-cadre-de-vie-et-logement": Cadre_Vie_Logement,
                "commission-finances-et-patrimoine": Finances_Patrimoine,
                "points-conseillers-2eme-supplement": Conseillers2,
                "points-conseillers-3eme-supplement": Conseillers3
            }
        committee = binding.get(item_classifier, None)
        if committee:
            return committee + suffix
        else:
            return NO_COMMITTEE

    def _adapt_council_items(self):
        logger.info('adapting council items...')
        brains = self.catalog(portal_type='MeetingItemCouncil')
        treshold_datetime = datetime(2000, 1, 1)
        substitute_datetime = datetime.now()
        for brain in brains:
            if brain.getRawClassifier:
                meeting_date = brain.meeting_date
                if meeting_date < treshold_datetime:
                    meeting_date = substitute_datetime
                committee_id = self.find_item_committee_row_id(meeting_date, brain.getRawClassifier)
                if committee_id == NO_COMMITTEE:
                    logger.warning("Committee not found for {} at {}, classifier = {} committee = {}".format(
                        brain.portal_type,
                        brain.getPath(),
                        brain.getRawClassifier,
                        committee_id))
                item = brain.getObject()
                item.setCommittees((committee_id,))

    def _remove_old_dashboardcollection(self):
        for cfg in self.tool.objectValues('MeetingConfig'):
            items = cfg.searches.searches_items
            meetings = cfg.searches.searches_items
            decided = cfg.searches.searches_items
            for folder in (items, meetings, decided):
                api.content.delete(objects=folder.listFolderContents())
            cfg.setToDoListSearches(())

    def post_migration_fixtures(self):
        logger.info("Adapting todo searches ...")
        for cfg in self.tool.objectValues('MeetingConfig'):
            cfg_dashboard_path = "portal_plonemeeting/{}/searches/searches_items/".format(cfg.getId())
            to_dashboard_ids = ["searchallitemstoadvice",
                                "searchallitemsincopy",
                                "searchitemstovalidate",
                                "searchitemstocorrect"]
            searches = [self.catalog.resolve_path(cfg_dashboard_path + id) for id in to_dashboard_ids]
            cfg.setToDoListSearches(tuple([search.UID() for search in searches if search is not None]))

    def run(self,
            profile_name=u'profile-Products.MeetingLalouviere:default',
            extra_omitted=[]):
        self._remove_old_dashboardcollection()
        super(Migrate_To_4200, self).run(extra_omitted=extra_omitted)
        self.post_migration_fixtures()
        logger.info('Done migrating to MeetingLalouviere 4200...')


# The migration function -------------------------------------------------------
def migrate(context):
    '''
    This migration function:
       1) Change MeetingConfig workflows to use meeting_workflow/meetingitem_workflow;
       2) Call PloneMeeting migration to 4200 and 4201;
       3) In _after_reinstall hook, adapt items and meetings workflow_history
          to reflect new defined workflow done in 1);
    '''
    migrator = Migrate_To_4200(context)
    migrator.run()
    migrator.finish()
