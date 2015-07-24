import dataholder
from config import read_config
import create_objects
from object_tv_lg import object_LGTV
from object_tivo import object_TIVO
import os, time, threading
from tvlisting import getall_listings, getall_xmllistings
from bottle import route, request, run, static_file, HTTPResponse
from multiprocessing import Process


def start_bottle():
    run(host='localhost', port=8080, debug=True)

def server_start():
    tvlistings_startprocess()
    p2.start()

def server_end():
    p1.terminate()
    p2.terminate()

def tvlistings_startprocess():
    p1.start()

def tvlistings_process():
    # 604800 secs = 7 days
    while True:
        tvlistings()
        time.sleep(604800)

def tvlistings():
    x = getall_listings()
    dataholder.TVlistings = x[0]
    dataholder.TVlistings_timestamp = x[1]


@route('/device/<room>/<device>/<command>')
def send_command(room="-", device="-", command="-"):
    #TODO
    BOOLsuccess = False
    if room=="lounge" and device=="lgtv" and command=="appslist":
        APPtype = request.query.type or 3
        APPindex = request.query.index or 0
        APPnumber = request.query.number or 0
        x = dataholder.OBJloungetv.getApplist(APPtype=APPtype, APPindex=APPindex, APPnumber=APPnumber)
        return HTTPResponse(data=x, status=200) if bool(x) else HTTPResponse(status=400)
    elif room=="lounge" and device=="lgtv":
        BOOLsuccess = dataholder.OBJloungetv.sendCmd(command)
    elif room=="lounge" and device=="tivo":
        BOOLsuccess = dataholder.OBJloungetivo.sendCmd(command)
    return HTTPResponse(status=200) if BOOLsuccess else HTTPResponse(status=400)

@route('/tvlistings')
def get_tvlistings():
    x = getall_xmllistings(dataholder.TVlistings)
    return HTTPResponse(data=x, status=200) if bool(x) else HTTPResponse(status=400)

@route('/img/<category>/<filename:re:.*\.png>')
def get_image(category, filename):
    root = os.path.join(os.path.dirname(__file__), '..', 'img/%s' % category)
    return static_file(filename, root=root, mimetype='image/png')


# Get configuration
read_config()
# Create objects
dataholder.OBJloungetv = create_objects.create_lgtv(dataholder.STRloungetv_lgtv_ipaddress,dataholder.STRloungetv_lgtv_pairkey)
dataholder.OBJloungetivo = create_objects.create_tivo(dataholder.STRloungetv_tivo_ipaddress, dataholder.STRloungetv_tivo_mak)
# GCreate processes for TV Listing code and code to start bottle server
p1 = Process(target=tvlistings_process)
p2 = Process(target=start_bottle)
# Start server
server_start()