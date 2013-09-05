#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from app import app
from nose.tools import eq_, assert_true
from nose import with_setup
import json

testapp = app.test_client()

def setup():
    app.config['TESTING'] = True

def teardown():
    app.config['TESTING'] = False

@with_setup(setup, teardown)
def test_root_working():
    response = testapp.get('/')
    eq_(response.status_code,200)
    msg = "reached the server side"
    assert_true(msg in response.data)

@with_setup(setup, teardown)
def test_api_gushim():
    response = testapp.get('/gushim')
    print(dir(response))
    j = json.loads(response.data)
    eq_(len(j), 644) #the correct number
    eq_(response.status_code,200)
    eq_(response.mimetype, 'application/json')

@with_setup(setup, teardown)
def test_api_get_gush():
    response = testapp.get('/gush/30035')
    j = json.loads(response.data)
    eq_(j.keys(), ['_id','gush_id', 'last_checked_at', 'html_hash'])


#    def test_get_block(self):
#        response = self.client.get("/gush/30540/plans")
#        data = response.json  # maybe should be without the () to be a method
#        print(len(data))
#        eq_(len(data),3)
#        d1 = data[0]
#        eq_(len(d1['tasrit_link']),2)
#        eq_(d1['tasrit_link'][0],'http://mmi.gov.il//IturTabotData/tabot/jerus/1011879_K.pdf')
#        eq_(d1['gush_id'],"30540")
#        eq_(d1['area'],u"ירושלים")
#        eq_(d1['takanon_link'][0],'http://mmi.gov.il//IturTabotData/takanonim/jerus/1011879.pdf')
#
#
#
