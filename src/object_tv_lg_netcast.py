from send_cmds import sendHTTP
from list_remotes_retriever import read_list_remotes


class object_tv_lg_netcast:
    '''LG TV object'''

    STRtv_PATHpair = "/udap/api/pairing"
    STRtv_PATHcommand = "/udap/api/command"
    STRtv_PATHevent = "/udap/api/event"
    STRtv_PATHquery = "/udap/api/data"

    def __init__ (self, STRname, STRipaddress, INTport, STRpairingkey=None):
        self._STRipaddress = STRipaddress
        self._INTport = INTport
        self._STRpairingkey = STRpairingkey
        self._type = "lgtv"
        if self._STRpairingkey!=None:
            self._pairDevice()
        self._name = STRname
        self._html = "object_lgtv.html"
        self._img = "logo_lg.png"
        self._tvguide = True

    def getIP(self):
        return self._STRipaddress

    def getPort(self):
        return self._INTport

    def getPairingkey(self):
        return self._STRpairingkey

    def setPairingkey(self, STRpairingkey):
        self._STRpairingkey = STRpairingkey
        self._pairDevice()

    def getTvguide_use(self):
        return self._tvguide

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def getHtml(self):
        return self._html

    def getLogo(self):
        return self._img

    def isPaired(self):
        return self._BOOLpaired

    def _pairDevice(self):
        STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"pairing\"><name>hello</name><value>{}</value><port>{}</port></api></envelope>".format(self._STRpairingkey, str(self._INTport))
        x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHpair), "close", data=STRxml)
        self._BOOLpaired = bool(x)
        return self._BOOLpaired

    def showPairingkey(self):
        STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"pairing\"><name>showKey</name></api></envelope>"
        x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHpair), "close", data=STRxml)
        return str(x.getcode()).startswith("2") if bool(x) else False

    def getChan(self):
        # sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHquery)+"?target=cur_channel", "close")
        return False

    def sendCmd(self, STRcommand):
        data = read_list_remotes(self._type, STRcommand)
        if data:
            if not self._BOOLpaired:
                if not self._repair_device():
                    return False
            STRxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?><envelope><api type=\"command\"><name>HandleKeyInput</name><value>{}</value></api></envelope>".format(data)
            x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHcommand), "close", data=STRxml)
            if bool(x) and not str(x.getcode()).startswith("2"):
                if not self._repair_device():
                    return False
                x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+str(self.STRtv_PATHcommand), "close", data=STRxml)
            return str(x.getcode()).startswith("2") if bool(x) else False
        else:
            return False


    def _repair_device(self):
        count = 0
        while count < 5:
            self._pairDevice()
            if self._BOOLpaired:
                break
            count+=1
        if count==5 and not self._BOOLpaired:
            return False
        return True


    def getApplist(self, APPtype=3, APPindex=0, APPnumber=0):
        # Note - If both index and number are 0, the list of all apps in the category specified by type is fetched.
        # 'APPtype' specifies the category for obtaining the list of apps. The following three values are available.
        #           1: List of all apps
        #           2: List of apps in the Premium category
        #           3: List of apps in the My Apps category
        # 'APPindex' specifies the starting index of the apps list. The value range is from 1 to 1024.
        # 'APPnumber' specifies the number of apps to be obtained from the starting index.
        #             This value has to be greater than or equal to the index value. The value can be from 1 to 1024.
        STRurl = "/udap/api/data?target=applist_get&type={}&index={}&number={}".format(str(APPtype), str(APPindex), str(APPnumber))
        x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+STRurl, "keep-alive")
        if bool(x):
            return x.read() if str(x.getcode()).startswith("2") else False
        else:
            return False

    def getAppicon (self, auid, name):
        # auid = This is the unique ID of the app, expressed as an 8-byte-long hexadecimal string.
        # name = App name
        STRurl = "/udap/api/data?target=appicon_get&auid={}&appname={}".format(auid, name)
        x = sendHTTP(self._STRipaddress+":"+str(self._INTport)+STRurl, "keep-alive")
        if bool(x):
            return x.read() if str(x.getcode()).startswith("2") else False
        else:
            return False