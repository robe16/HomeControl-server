from send_cmds import sendSOCKET
from enum_remoteTIVO import LSTremote_tivo

class object_TIVO:
    '''TiVo object'''

    def __init__ (self, STRname, STRipaddress, INTport, STRaccesskey="", BOOLtvguide_use=False, STRgroup=None):
        self._STRipaddress = STRipaddress
        self._INTport = INTport
        self._STRaccesskey = STRaccesskey
        self._tvguide_use = BOOLtvguide_use
        self._group = STRgroup
        self._device = "tivo"
        self._chan_array_no = 0
        self._name = STRname
        self._html = "object-tivo.html"
        self._img = "logo_virgin.png"


    def getIP(self):
        return self._STRipaddress

    def getPort(self):
        return self._INTport

    def getAccesskey(self):
        return self._STRaccesskey

    def setAccesskey(self, STRaccesskey):
        self._STRaccesskey = STRaccesskey

    def getChan_array_no(self):
        return self._chan_array_no

    def getTvguide_use(self):
        return self._tvguide_use

    def getGroup(self):
        return self._group

    def getDevice(self):
        return self._device

    def getName(self):
        return self._name

    def getHtml(self):
        return self._html

    def getLogo(self):
        return self._img


    def sendCmd(self, STRcommand):
        if STRcommand.startswith("FORCECH"):
            return sendSOCKET(self._STRipaddress, self._INTport, STRcommand)
        else:
            comms = LSTremote_tivo
            for x in range(len(comms)):
                if comms[x][0]==STRcommand:
                    return sendSOCKET(self._STRipaddress, self._INTport, comms[x][1])
            return False