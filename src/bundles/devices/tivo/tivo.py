import datetime
import telnetlib
import threading
import time
import xml.etree.ElementTree as ET

import requests as requests
from requests.auth import HTTPDigestAuth

from src.bundles.devices.device import Device
from src.config.devices.config_devices import get_cfg_device_detail, get_cfg_device_detail_public
from src.lists.channels.list_channels import get_channel_logo_from_devicekey, get_channel_name_from_devicekey
from src.log.console_messages import print_command, print_error, print_msg


class device_tivo(Device):

    def __init__(self, room_id, device_id, q_dvc, queues):
        #
        Device.__init__(self, "tivo", room_id, device_id, q_dvc, queues)
        #
        self.recordings = False
        t = threading.Thread(target=self.get_recordings, args=())
        t.daemon = True
        t.start()
        #
        self.run()

    def get_recordings(self):
        while self._active:
            # Reset value
            self.recordings = False
            #
            try:
                recordings_timestamp = datetime.datetime.now()
                #
                ############
                #
                folders = self._retrieve_recordings('No').replace(' xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/"', '')
                folders = ET.fromstring(folders)
                xml_folders = []
                for item in folders.iter('Item'):
                    xml_folders.append(item.find('Details'))
                #
                ############
                #
                retrieve_items = 50
                #
                files_repeat = True
                loop_count = 0
                itemCount = '&ItemCount={retrieve_items}'.format(retrieve_items=retrieve_items)
                xml_files = []
                #
                while files_repeat:
                    files_count = 0
                    files = self._retrieve_recordings('Yes', itemCount=itemCount).replace(' xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/"','')
                    files = ET.fromstring(files)
                    # Run through individual items
                    for item in files.iter('Item'):
                        xml_files.append(item.find('Details'))
                        files_count += 1
                    #
                    if files_count<50:
                        files_repeat = False
                    else:
                        loop_count += 1
                        itemCount = '&ItemCount={retrieve_items}&AnchorOffset={AnchorOffset}'.format(retrieve_items=retrieve_items,
                                                                                                     AnchorOffset=(retrieve_items*loop_count))
                #
                ############
                #
                self.recordings = self._create_recordings_json(recordings_timestamp, xml_folders, xml_files)
                #
                ############
                #
                print_msg('TV recording information retrieved: {type}'.format(type=self._type), dvc_or_acc_id=self.dvc_or_acc_id())
            except:
                self.recordings_timestamp = 0
                self.recordings = False
            #
            time.sleep(600) # 600 = 10 minutes


    def _accesskey(self):
        return get_cfg_device_detail(self._room_id, self._device_id, "mak")

    def _package(self):
        return get_cfg_device_detail_public(self._room_id, self._device_id, "package")

    def _getChan(self):
        response = self._send_telnet(self._ipaddress(), self._port(), response=True)
        #
        if not bool(response):
            return False
        #
        nums = [int(s) for s in response.split() if s.isdigit()]
        #
        if len(nums) > 0:
            chan_no = nums[0]
            if bool(chan_no):
                #
                chan_name = get_channel_name_from_devicekey(self._type, chan_no)
                #
                chan_logo = get_channel_logo_from_devicekey(self._type, chan_no)
                chan_logo = chan_logo if not chan_logo == '-' else 'ic_blank.png'
                #
                json_channel = {}
                json_channel['channel'] = {}
                json_channel['channel']['number'] = str(chan_no)
                json_channel['channel']['name'] = chan_name
                json_channel['channel']['logo'] = chan_logo
                #
                return json_channel
        return False

    def sendCmd(self, request):
        #
        try:
            code = False
            response = False
            #
            if request['command'] == 'channel':
                response = self._send_telnet(ipaddress=self._ipaddress(),
                                             port=self._port(),
                                             data=("SETCH {}\r").format(request['chan']),
                                             response=True)
                if response.startswith('CH_FAILED'):
                    print_command('channel',
                                  self.dvc_or_acc_id(),
                                  self._type,
                                  self._ipaddress(),
                                  response)
                    return False
            elif request['command'] == 'command':
                code = self.commands[request['code']]
                try:
                    response = self._send_telnet(self._ipaddress(), self._port(), data=code)
                except:
                    response = False
            #
            x = request['code'] if code else request['command']
            print_command (x,
                           self.dvc_or_acc_id(),
                           self._type,
                           self._ipaddress(),
                           response)
            return response
        except:
            print_command(request['command'],
                          self.dvc_or_acc_id(),
                          self._type,
                          self._ipaddress(),
                          'ERROR')
            return False

    def getData(self, request):
        try:
            if request['data'] == 'recordings':
                return self.recordings
            elif request['data'] == 'channel':
                return self._getChan()
        except Exception as e:
            print_error('Failed to return requested data {request} - {error}'.format(request=request['data'],
                                                                                     error=e))
            return False

    def _create_recordings_json(self, _timestamp, _folders, _files):
        #
        json_recordings = {}
        json_recordings["recordings"] = {}
        json_recordings["timestamp"] = _timestamp.strftime('%d/%m/%Y %H:%M:%S')

        #
        if len(_folders)==0 or len(_files) == 0:
            return False
        #
        try:
            #
            folderCount = 0
            for itemFolder in _folders:
                if itemFolder.find('Title').text != 'Suggestions' and itemFolder.find('Title').text != 'HD Recordings':
                    json_recordings['recordings'][str(folderCount)] = {}
                    json_recordings['recordings'][str(folderCount)]['folderName'] = itemFolder.find('Title').text
                    json_recordings['recordings'][str(folderCount)]['type'] = '-'
                    #
                    json_recordings['recordings'][str(folderCount)]['items'] = {}
                    #
                    # Run through individual items
                    itemCount = 0
                    for itemFile in _files:
                        #
                        if itemFile.find('Title').text == itemFolder.find('Title').text:
                            #
                            json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)] = {}
                            #
                            try:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['episodeTitle'] = itemFile.find('EpisodeTitle').text
                            except Exception as e:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['episodeTitle'] = ''
                            #
                            json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['channel'] = {}
                            #
                            try:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['channel']['image'] = get_channel_logo_from_devicekey(self._type, int(itemFile.find('SourceChannel').text))
                            except Exception as e:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['channel']['image'] = '-'
                                #
                            try:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['channel']['name'] = get_channel_name_from_devicekey(self._type, int(itemFile.find('SourceChannel').text))
                            except Exception as e:
                                print (int(itemFile.find('SourceChannel').text))
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['channel']['name'] = '-'

                                #
                            try:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['description'] = itemFile.find('Description').text
                            except Exception as e:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['description'] = ''
                            #
                            try:
                                date = int(itemFile.find('CaptureDate').text, 0)
                                date = datetime.datetime.fromtimestamp(date)
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['recordingDate'] = date.strftime('%d-%m-%Y')
                            except Exception as e:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['recordingDate'] = '-'
                            #
                            json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['episodeNumber'] = {}
                            #
                            try:
                                episodenumber = itemFile.find('EpisodeNumber').text
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['episodeNumber']['series'] = episodenumber[:-2]
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['episodeNumber']['episode'] = episodenumber[-2:]
                            except:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['episodeNumber']['series'] = ''
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['episodeNumber']['episode'] = ''
                            #
                            try:
                                if itemFile.find('ProgramId').text.startswith('EP'):
                                    json_recordings['recordings'][str(folderCount)]['type'] = 'tv'
                                    json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['mpaaRating'] = ''
                                elif itemFile.find('ProgramId').text.startswith('MV'):
                                    json_recordings['recordings'][str(folderCount)]['type'] = 'movie'
                                    json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['mpaaRating'] = itemFile.find('MpaaRating').text
                            except:
                                json_recordings['recordings'][str(folderCount)]['items'][str(itemCount)]['mpaaRating'] = ''
                                #
                            itemCount += 1
                #
                folderCount += 1
            #
            return json_recordings
            #
        except Exception as e:
            print_error('Attempted to create recordings json - {error}'.format(error=e))
            return False

    def _retrieve_recordings(self, recurse, itemCount=''):
        try:
            r = requests.get('https://{ipaddress}/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse={recurse}{itemCount}'.format(ipaddress=self._ipaddress(), recurse=recurse, itemCount=itemCount),
                             auth=HTTPDigestAuth('tivo', self._accesskey()),
                             verify=False)
            print_command('retrieve listings (recurse={recurse})'.format(recurse=recurse),
                          self.dvc_or_acc_id(),
                          self._type,
                          self._ipaddress(),
                          r.status_code)
            if r.status_code == requests.codes.ok:
                return r.content
            else:
                return False
        except Exception as e:
            return False

    def _send_telnet(self, ipaddress, port, data='', response=False):
        try:
            tn = telnetlib.Telnet(ipaddress, port)
            time.sleep(0.1)
            output = tn.read_eager() if response else None
            if data:
                tn.write(str(data)+"\n")
                time.sleep(0.1)
                op = tn.read_eager()
                if op=='':
                    output = True
                else:
                    output = op if (response and not bool(op)) else True
            tn.close()
            return output
        except:
            return False

    commands = {"power": "IRCODE STANDBY\r",
                "1": "IRCODE NUM1\r",
                "2": "IRCODE NUM2\r",
                "3": "IRCODE NUM3\r",
                "4": "IRCODE NUM4\r",
                "5": "IRCODE NUM5\r",
                "6": "IRCODE NUM6\r",
                "7": "IRCODE NUM7\r",
                "8": "IRCODE NUM8\r",
                "9": "IRCODE NUM9\r",
                "0": "IRCODE NUM0\r",
                "home": "IRCODE TIVO\r",
                "livetv": "IRCODE LIVETV\r",
                "myshows": "IRCODE NOWSHOWING\r",
                "info": "IRCODE INFO\r",
                "zoom": "IRCODE ZOOM\r",
                "guide": "IRCODE GUIDE\r",
                "subtitles": "IRCODE CC_ON\r",
                "up": "IRCODE UP\r",
                "down": "IRCODE DOWN\r",
                "left": "IRCODE LEFT\r",
                "right": "IRCODE RIGHT\r",
                "select": "IRCODE SELECT\r",
                "channelup": "IRCODE CHANNELUP\r",
                "channeldown": "IRCODE CHANNELDOWN\r",
                "thumbsup": "IRCODE THUMBSUP\r",
                "thumbsdown": "IRCODE THUMBSDOWN\r",
                "record": "IRCODE RECORD\r",
                "play": "IRCODE PLAY\r",
                "pause": "IRCODE PAUSE\r",
                "stop": "IRCODE STOP\r",
                "reverse": "IRCODE REVERSE\r",
                "forward": "IRCODE FORWARD\r",
                "slow": "IRCODE SLOW\r",
                "back": "IRCODE REPLAY\r",
                "next": "IRCODE ADVANCE\r",
                "actiona": "IRCODE ACTION_A\r",
                "actionb": "IRCODE ACTION_B\r",
                "actionc": "IRCODE ACTION_C\r",
                "actiond": "IRCODE ACTION_D\r",
                "clear": "IRCODE CLEAR\r",
                "enter": "IRCODE ENTER\r"}
