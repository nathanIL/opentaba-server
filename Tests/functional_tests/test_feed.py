#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from app import app
from nose.tools import eq_, assert_true
from nose import with_setup
from lxml import etree

testapp = app.test_client()


def setup():
    app.config['TESTING'] = True


def teardown():
    app.config['TESTING'] = False


@with_setup(setup, teardown)
def test_basic_feed_sane():
    response = testapp.get('/plans.atom')
    eq_(response.status_code, 200)

    # Check that the XML tree is parsable and is an ATOM feed
    tree = etree.fromstring(response.data)
    eq_("{http://www.w3.org/2005/Atom}feed", tree.tag)
    
    # And check that it has at least one entry
    assert_true(tree.xpath('count(//*[local-name() = "entry"])') > 0)

@with_setup(setup, teardown)
def test_gush_feed_sane_single():
    response = testapp.get('/gush/30649/plans.atom')
    eq_(response.status_code, 200)

    # Check that the XML tree is parsable and is an ATOM feed
    tree = etree.fromstring(response.data)
    eq_("{http://www.w3.org/2005/Atom}feed", tree.tag)
    
    # And check that it has at least one entry
    assert_true(tree.xpath('count(//*[local-name() = "entry"])') > 0)

@with_setup(setup, teardown)
def test_gush_feed_sane_multi():
    response = testapp.get('/gush/30649,28107/plans.atom')
    eq_(response.status_code, 200)

    # Check that the XML tree is parsable and is an ATOM feed
    tree = etree.fromstring(response.data)
    eq_("{http://www.w3.org/2005/Atom}feed", tree.tag)
    
    # And check that it has at least one entry
    assert_true(tree.xpath('count(//*[local-name() = "entry"])') > 0)

@with_setup(setup, teardown)
def test_city_plan_feed():
    response = testapp.get('/jerusalem/plans.atom')
    eq_(response.status_code, 200)

    # Check that the XML tree is parsable and is an ATOM feed
    tree = etree.fromstring(response.data)
    eq_("{http://www.w3.org/2005/Atom}feed", tree.tag)
    
    # And check that it has at least one entry
    assert_true(tree.xpath('count(//*[local-name() = "entry"])') > 0)

@with_setup(setup, teardown)
def test_invalid_city_plan_feed():
    response = testapp.get('/idonotexist/plans.atom')
    eq_(response.status_code, 404)
