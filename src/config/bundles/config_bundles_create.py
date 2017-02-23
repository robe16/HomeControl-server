from bundles.devices.tv_lg_netcast.tv_lg_netcast import device_tv_lg_netcast
from bundles.devices.tivo.tivo import device_tivo
from bundles.devices.nest.nest import account_nest
from bundles.info_services.news.news import info_news
from bundles.info_services.weather.weather import info_metoffice
from bundles.info_services.tvlistings.tvlistings import info_tvlistings

from config.bundles.config_bundles import get_cfg_bundles_json
from config.bundles.config_bundles import get_cfg_device_type
from log.console_messages import print_msg


def create_bundles(_devices, _infoservices):
    #
    data = get_cfg_bundles_json()
    #
    for group_id in data['bundles']['devices']['groups']:
        #
        _devices[group_id] = {}
        group_devices = {}
        #
        for device_id in data['bundles']['devices']['groups'][group_id]['devices']:
            #
            group_devices[device_id] = _create_device(group_id, device_id)
            print_msg('Device object created: {type}: {group}:{device}'.format(type=get_cfg_device_type(group_id, device_id),
                                                                               group=group_id,
                                                                               device=device_id))
        _devices[group_id] = group_devices
    #
    _infoservices['weather'] = info_metoffice()
    print_msg('Infoservice object created: {type}'.format(type='weather'))
    #
    _infoservices['tvlistings'] = info_tvlistings()
    print_msg('Infoservice object created: {type}'.format(type='tvlistings'))
    #
    _infoservices['news'] = info_news()
    print_msg('Infoservice object created: {type}'.format(type='news'))
    #
    print_msg('All devices and infoservice instances created')


def _create_device(group_id, device_id):
    device_type = get_cfg_device_type(group_id, device_id)
    #
    if device_type=='tv_lg_netcast':
        return device_tv_lg_netcast(group_id=group_id, device_id=device_id)
    elif device_type=='tivo':
        return device_tivo(group_id=group_id, device_id=device_id)
    elif device_type=='nest_account':
        return account_nest(group_id=group_id, device_id=device_id)
    else:
        return False