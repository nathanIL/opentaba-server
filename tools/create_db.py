#!/usr/bin/python

from conn import *
from gushim import GUSHIM
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--force", dest="force", default=False, action="store_true", help="delete existing dbs")

(options, args) = parser.parse_args()

if not options.force:
    print ("This script will delete the gushim and plans collection. "
           "To make sure this isn't running by mistake, run this with --force")
    exit()

# print "Deleting db.gushim and db.plans"
db.gushim.drop()
db.plans.drop()
# delete blacklist in case it still exists. we don't use it anymore
db.blacklist.drop()

db.gushim.create_index([('gush_id', 1)], unique=True)

for g in GUSHIM:
    db.gushim.insert({'gush_id': g,
                      'json_hash': '',
                      'last_checked_at': ''})

db.plans.create_index([('plan_id', pymongo.DESCENDING)], unique=True)
db.plans.create_index([('gushim', pymongo.ASCENDING),
                       ('year', pymongo.DESCENDING),
                       ('month', pymongo.DESCENDING),
                       ('day', pymongo.DESCENDING),
                       ('number', pymongo.ASCENDING),
                       ('essence', pymongo.ASCENDING)],
                      unique=True)  # , drop_dups = True)
