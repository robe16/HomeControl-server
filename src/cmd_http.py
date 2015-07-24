import urllib2


def sendHTTP(ipaddress, connection, data=False):
    # Send data via http to IP address over network conection
    if not ipaddress.startswith("http"):
        ipaddress = "http://" + ipaddress
    if data:
        req = urllib2.Request(ipaddress, data=data)
    else:
        req = urllib2.Request(ipaddress)
    req.add_header("content-type","text/xml; charset=utf-8")
    req.add_header("Connection", connection)
    req.add_header("User-Agent","Linux/2.6.18 UDAP/2.0 CentOS/5.8")
    try:
        x = urllib2.urlopen(req, timeout=5)
        return False if not str(x.getcode()).startswith("2") else x
    except:
        return False