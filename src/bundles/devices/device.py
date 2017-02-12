from config.bundles.config_bundles import get_cfg_device_detail
from lists.bundles.list_bundles import get_bundle_detail, get_bundle_name, get_bundle_logo


class Device:

    def __init__(self, type, group_id, device_id):
        self._group_id = group_id
        self._device_id = device_id
        self._type = type

    def dvc_id(self):
        return self._group_id + ':' + self._device_id

    def _ipaddress(self):
        return get_cfg_device_detail(self._group_id, self._device_id, 'ipaddress')

    def _port(self):
        return get_bundle_detail(self._type, 'port')

    def _logo(self):
        return get_bundle_logo(self._type)

    def _dvc_name(self):
        return get_cfg_device_detail(self._group_id, self._device_id, 'name')

    def _type_name(self):
        return get_bundle_name(self._type)

    def sendCmd(self, request):
        # Mastered in each of the device specific classes
        pass

    def getData(self, request):
        # Mastered in each of the device specific classes
        pass
