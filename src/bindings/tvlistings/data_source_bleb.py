import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests as requests
import time
import cfg as cfg
from log.log import log_error


def get(channel_id):
    #
    str_listing = getlisting(channel_id, 0)
    xml_listing = ET.fromstring(str_listing)
    #
    if check_enabled(xml_listing):
        return convert_to_dict(xml_listing)
    else:
        return {}


def convert_to_dict(data):
    json_channel = {}
    #
    lastitem = 'am'
    nextday_start = 0
    nextday_end = 0
    for programme in data:
        json_programme = {}
        #
        d = datetime.strptime(data.attrib['date'], '%d/%m/%Y').date()
        #
        t_start = datetime.strptime(programme.find('start').text, '%H%M').time()
        if lastitem == 'pm' and t_start.hour < 12:
            nextday_start = 1
        lastitem = 'am' if t_start.hour < 12 else 'pm'
        d_start = d + timedelta(days=nextday_start)
        start = datetime.combine(d_start, t_start)
        #
        t_end = datetime.strptime(programme.find('end').text, '%H%M').time()
        if nextday_start == 1 or t_end.hour < t_start.hour:
            nextday_end = 1
        d_end = d + timedelta(days=nextday_end)
        end = datetime.combine(d_end, t_end)
        #
        if start > datetime.now() or end > datetime.now():
            json_programme['start'] = start.isoformat(' ')
            json_programme['end'] = end.isoformat(' ')
            json_programme['title'] = programme.find('title').text
            try:
                json_programme['subtitle'] = programme.find('subtitle').text
            except:
                json_programme['subtitle'] = ''
            json_programme['desc'] = programme.find('desc').text
            #
            id = json_programme['start']
            json_channel[id] = json_programme
        #
    return json_channel


def check_enabled(data):
    if data.attrib['source'] == 'Disabled':
        return False
    else:
        return True


def getlisting(channel_id, day):
    #
    # Use of bleb.org data requires API calls to be 2 seconds apart
    time.sleep(2)
    #
    headers = {'User-Agent': 'TV::Fetch::XML, {app_name} - {email}'.format(app_name=cfg.app_name,
                                                                           email=cfg.developer_email),
               'Connection': 'close',
               'content-type': 'text/xml; charset=utf-8'}
    #
    r = requests.get('http://www.bleb.org/tv/data/listings/{day}/{channel_id}.xml'.format(day=day,
                                                                                          channel_id=channel_id),
                     headers=headers)
    #
    if r.status_code == requests.codes.ok:
        return r.content
    else:
        log_error('Request to bleb.org failed - {status}'.format(status=r.status_code))
        return None