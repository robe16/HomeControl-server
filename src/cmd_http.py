import urllib
import urllib2
import httplib


def sendHTTP(ipaddress, path, connection, data=False, port=False):
    '''Send data via http to IP address over network conection'''
    if not ipaddress.startswith("http"):
        ipaddress = "http://" + ipaddress
    if port!=False:
        url = ipaddress+":"+port
    else:
        url = ipaddress
    if data:
        #data = urllib.quote_plus(data)
        #data = urllib2.urlencode(data)
        req = urllib2.Request(url+path, data=data)
    else:
        req = urllib2.Request(url+path)
    req.add_header("content-type","text/xml; charset=utf-8")
    req.add_header("Connection", connection)
    req.add_header("User-Agent","Linux/2.6.18 UDAP/2.0 CentOS/5.8")
    try:
        x = urllib2.urlopen(req)
        if not str(x.getcode()).startswith("2"):
            return False
        else:
            return x
    except urllib2.HTTPError as e:
        return False
    except urllib2.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        return False