import pytest
import time
from flask import url_for



def test_badreq(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="unset", t1='2019-06-10T11:27:45',t2='2019-06-10T11:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 400
    
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="any", t1='A019-06-10T11:27:45',t2='2019-06-10T11:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 400
    
def test_caching(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)
    

    t0=time.time()
    print("repeating request")
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)

    assert (time.time() - t0)<1
    
def test_anysource(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)
    

    t0=time.time()
    print("repeating request")
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)

    assert (time.time() - t0)<1
    
def test_nrt(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="nrt", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print("response", r)
    assert r.status_code == 200
    print(r.json)
    

    t0=time.time()
    print("repeating request")
    r=client.get(url_for('scwlist', readiness="nrt", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)

    assert (time.time() - t0)<1

def test_cons(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="cons", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)
    

    t0=time.time()
    print("repeating request")
    r=client.get(url_for('scwlist', readiness="cons", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)

    assert (time.time() - t0)<1

def test_any(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)
    

    t0=time.time()
    print("repeating request")
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45'), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)
    assert isinstance(r.json, list)

    assert (time.time() - t0)<1
    
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-10T14:27:45', return_index_version="yes"), follow_redirects=True)
    print(r)
    assert 'index_version' in r.json

def test_any_radius(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-09-10T14:27:45'), query_string=dict(ra=83, dec=22, radius=10), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)
    

def test_good_isgri(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-09-10T14:27:45'), query_string=dict(min_good_isgri=1000), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)
    
def test_index_version(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="cons", t1='2019-06-10T11:27:45',t2='2019-09-10T14:27:45'), query_string=dict(return_index_version="yes", min_good_isgri=1000), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)

    index_version = r.json['index_version']

    assert index_version

    r=client.get(url_for('scwlist', readiness="cons", t1='2019-06-10T11:27:45',t2='2019-09-10T14:27:45'), query_string=dict(index_version=index_version, min_good_isgri=1000), follow_redirects=True)

    assert r.status_code == 200
    print(r.json)
    
    
    
def test_bad_index_version(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="cons", t1='2019-06-10T11:27:45',t2='2019-09-10T14:27:45'), query_string=dict(index_version="bad_version", min_good_isgri=1000), follow_redirects=True)
    print(r)
    assert r.status_code == 400
    print(r.json)


def test_return_columns(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-11T14:27:45'), query_string=dict(return_columns="SWID,RA_SCX,DEC_SCX,RA_SCZ"), follow_redirects=True)
    print(r)
    assert r.status_code == 200
    print(r.json)
    
    assert len(r.json['DEC_SCX']) == len(r.json['SWID'])
    
    r0=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-11T14:27:45'), follow_redirects=True)

    print(r0.json)

    assert len(r0.json) == len(r.json['SWID'])

def test_return_columns_badname(client):
    t0=time.time()
    r=client.get(url_for('scwlist', readiness="any", t1='2019-06-10T11:27:45',t2='2019-06-11T14:27:45'), query_string=dict(return_columns="SWID,RA_SCX,DEC_SCX,RA_SCA"), follow_redirects=True)
    print(r)
    assert r.status_code == 400
    print(r.json)
    
