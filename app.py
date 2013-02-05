import os
import datetime
import json
import pymongo
from bson import json_util
from urlparse import urlparse

from flask import Flask
from flask import abort, redirect, url_for, make_response


app = Flask(__name__)

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:	# on Heroku, get a connection
    m_conn = pymongo.Connection(MONGO_URL)   
    db = m_conn[urlparse(MONGO_URL).path[1:]]
    RUNNING_LOCAL = False
else:			# work locally
    m_conn = pymongo.Connection('localhost', 27017)
    db = m_conn['citymap']
    RUNNING_LOCAL = True
    app.debug = True # since we're local, keep debug on


#### Helpers ####

# convert dictionary to JSON. json_util.default adds automatic mongoDB result support
def _to_json(mongo_obj):
	return json.dumps(mongo_obj, ensure_ascii=False, default=json_util.default)


def _resp(data):
	r = make_response(_to_json(data))
	r.headers['Access-Control-Allow-Origin'] = "*"
	r.headers['Content-Type'] = "application/json"
	return r


#### ROUTES ####

# get gush_id metadata
@app.route('/gush/<gush_id>')
def get_gush(gush_id):
	gush = db.gushim.find_one({"gush_id" : gush_id})
	if gush is None:
		abort(404)
	return _resp(gush)


# get plans from gush_id
@app.route('/gush/<gush_id>/plans')
def get_plans(gush_id):
	if db.gushim.find_one({"gush_id" : gush_id}) is None:
		abort(404)

	plans = db.plans.find({"gush_id" : gush_id}).sort([("year", pymongo.DESCENDING), ("month", pymongo.DESCENDING), ("day", pymongo.DESCENDING)])
	
	# eliminate plans which appear in >99 blocks - cover for MMI's database bugs
	blacklist = db.blacklist.find_one()['blacklist']

	plans_clean = [p for p in list(plans) if p['number'] not in blacklist]

	return _resp(plans_clean)


# TODO add some text on the project
@app.route('/')
def hello():
	out = '''<html><body style="font-size: 3em; margin: 100px; text-align:center">
	<p>Hi. You\'ve reached the server side of <a href="http://opentaba.info">opentaba.info</a></p>
	<p><a href="https://github.com/niryariv/citymap-server">Source</a></p>
</body></html>'''

	return out


# wake up heroku dyno from idle. perhaps can if >1 dynos 
# used as endpoint for a "wakeup" request when the client inits
@app.route('/wakeup')
def wakeup():
	return _resp({'morning' : 'good'})


#### MAIN ####

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



