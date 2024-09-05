from pymongo import MongoClient
from datetime import datetime
import pymongo
from pprint import pprint
from mongoengine import connect                                                                             


client = MongoClient('mongodb://10.10.30.12:30017')
# client = MongoClient('mongodb://10.10.30.12:30017')
# client = MongoClient('mongodb://mongo-cdat:30017')


class CDAT():
    def __init__(self):
        self.db = client['CDAT']
        self.cellidchart = self.db['cdat_cellidchart']
        self.cellidchart_jio = self.db['cellid_jio']
        self.cdrdata = self.db['cdat_cdr']
        self.ipdrdata = self.db['raw_data']
        self.ipdr = self.db['raw_data']
        self.imeicdrdata = self.db['cdat_imeicdr']
        self.towercdrdata = self.db['cdat_tower']
        self.sdrdata = self.db['cdat_sdr']
        self.voip = self.db['voip_calls']
        self.matchedcall = self.db['matchedcalls']
        self.rhdata = self.db['cdat_rhdata']
        self.poadata = self.db['poadata']
        self.gprs = self.db['gprsdata']
        self.suspect = self.db['cdat_suspect']
        self.phonearea = self.db['cdat_phonearea']
        self.indcase = self.db['ind_cases']
        self.indcaseentries = self.db['ind_case_entries']
        self.redflag = self.db['redflags']
        self.notification = self.db['notifications']
        self.existingdata = self.db['cdat_existing_row']
        self.imeiexistingdata = self.db['imeicdr_existing_row']
        self.towerexistingdata = self.db['towercdr_existing_row']
        self.gprsexistingdata = self.db['gprs_existing_row']
        self.mapdata = self.db['map_data']
        self.caffiles = self.db['caf_data']
        self.rhdata = self.db['rh']

        return None


class thunderbolt():
    def __init__(self):
        self.db = client['THUNDERBOLT']
        self.users = self.db['users']
        self.tickets = self.db['tickets']
        self.number_anaysis = self.db['number_analysis']
        self.userlogs = self.db['userlogs']
        self.casedata = self.db['casedata']
        self.list_collectons = self.db.list_collection_names()


class Database():
    def __init__(self):
        db = client['FILESTAT']
        self.filemanage = db['file_manager']
        self.emailmanage = db['email_manager']
        self.direct_up = db['direct_files']
        return None


class NEXUS():
    def __init__(self):
        self.db = client['NexusData']

class VIGOR():
    def __init__(self):
        self.db = client['VIGOR']
        self.cri_meta = self.db['CRI_Meta']
