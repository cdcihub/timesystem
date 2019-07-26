#!flask/bin/python
from flask import Flask, url_for, jsonify, send_file, request

import requests

import sys
import pilton
import re

import socket

def dlog(*a, **aa):
    pass

consul=False

context=socket.gethostname()

app = Flask(__name__)

@app.route('/api/v1.0/converttime/<string:informat>/<string:intime>/<string:outformat>', methods=['GET'])
def converttime(informat,intime,outformat):
    if outformat=="ANY":
        outformat=""

    if informat=="SCWID":
        datamirror.ensure_data(scw=intime)

    ct=pilton.heatool("converttime")
    ct['informat']=informat
    ct['intime']=intime
    ct['outformat']=outformat

    try:
        ct.run()
    except Exception as e:
        print("problem:",e)
        r=jsonify({'error from converttime':repr(e),'output':ct.output if hasattr(ct,'output') else None})

        if outformat=="SCWID":
            try:
                return isdcclient.getscw(intime)
            except Exception as ei:
                r=jsonify({'error from converttime':repr(e),'output':ct.output,'error from ISDC':repr(ei),'ISDC response':c})
        
        if outformat=="":
            try:
                r=dict(re.findall("Log_1  : Input Time\(.*?\): .*? Output Time\((.*?)\): (.*?)\n",ct.output,re.S))
                print(r)
                c=isdcclient.getscw(intime)
                r['SCWID']=c
                r=jsonify(r)
            except Exception as ei:
                raise
                print(ei)
                r=jsonify({'error from converttime':repr(e),'output':ct.output,'error from ISDC':repr(ei),'ISDC response':c})

        r.status_code=500
        dlog(logging.ERROR,"error in converttime "+repr(e))
        return r

    r=dict(re.findall("Log_1  : Input Time\(.*?\): .*? Output Time\((.*?)\): (.*?)\n",ct.output,re.S))

    print(r)

    if outformat=="":
        return jsonify(r)
    else:
        return r[outformat]

@app.route('/poke', methods=['GET'])
def poke():
    return ""

if __name__ == '__main__':

    if consul:
        import os
        from export_service import export_service,pick_port
        os.environ['EXPORT_SERVICE_PORT']="%i"%pick_port("")
        port=export_service("integral-timesystem","/poke",interval=0.1,timeout=0.2)

        host=os.environ['EXPORT_SERVICE_HOST'] if 'EXPORT_SERVICE_HOST' in os.environ else '127.0.0.1'
    else:
        host="0.0.0.0"
        port=5000
        
    ##
    app.run(debug=False,port=port,host=host)
