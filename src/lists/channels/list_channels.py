import json
import os


def read_list_channels():
    with open(os.path.join('lists', 'list_channels.json'), 'r') as data_file:
        data = json.load(data_file)
        data_file.close()
    if isinstance(data, dict):
        return data
    else:
        return False


def get_channel_categories():
    data = read_list_channels()
    try:
        return data['categories']
    except:
        return False


def get_channel_cat_list(category):
    data = read_list_channels()
    try:
        return data['channels'][category]
    except:
        return False


def get_channel_cat_item(category, channel):
    try:
        list = get_channel_cat_list(category)
        if bool(list):
            for item in list:
                if item['name'] == channel:
                    return item
        return False
    except:
        return False


def get_channel_item_detail(category, channel, detail):
    try:
        item = get_channel_cat_item(category, channel)
        if bool(item):
            return item[detail]
        return False
    except:
        return False


def get_channel_item_type(category, channel):
    try:
        item = get_channel_cat_item(category, channel)
        if bool(item):
            return item['type']
        return False
    except:
        return False


def get_channel_item_listingsrc(category, channel, src):
    try:
        item = get_channel_cat_item(category, channel)
        if bool(item):
            return item['listingsrc'][src]
        return False
    except:
        return False


def get_channel_item_res_detail(category, channel, res, detail):
    try:
        item = get_channel_cat_item(category, channel)
        if bool(item):
            return item[res][detail]
        return False
    except:
        return False


def get_channel_item_res_logo(category, channel, res):
    try:
        item = get_channel_cat_item(category, channel)
        if bool(item):
            return item[res]['logo']
        return False
    except:
        return False


def get_channel_item_res_devicekey(category, channel, res, device_type):
    try:
        item = get_channel_cat_item(category, channel)
        if bool(item):
            return item[res]['devicekeys'][device_type]
        return False
    except:
        return False


def get_channel_item_res_freeview(category, channel, res):
    try:
        item = get_channel_cat_item(category, channel)
        if bool(item):
            return item[res]['freeview']
        return False
    except:
        return False


def get_channel_item_res_package(category, channel, res, package_name):
    try:
        item = get_channel_cat_item(category, channel)
        if bool(item):
            return item[res][package_name]
        return False
    except:
        return False


def get_channel_item_image_from_devicekey(device_type, device_key):
    try:
        qual_list = ['sd', 'hd']
        cat_list = get_channel_categories()
        for cat in cat_list:
            chan_list = get_channel_cat_list(cat)
            for chan in chan_list:
                for qual in qual_list:
                    try:
                        if chan[qual]['devicekeys'][device_type] == device_key:
                            return chan[qual]['logo']
                    except:
                        # dummy code just to allow use of try/except
                        x = False
        return False
    except:
        return False


def get_channel_name_from_devicekey(device_type, channo):
    try:
        #
        categories = get_channel_categories()
        #
        data = read_list_channels()
        cat_chans = data['channels']
        #
        for cat in categories:
            chans = cat_chans[cat]
            #
            for chan in chans:
                try:
                    if chan['sd']['devicekeys'][device_type] == channo:
                        return chan['name']
                except:
                    True
                try:
                    if chan['hd']['devicekeys'][device_type] == channo:
                        return chan['name']
                except:
                    True
            #
        return '-'
    except:
        return 'error'


def get_channel_logo_from_devicekey(device_type, channo):
    try:
        #
        categories = get_channel_categories()
        #
        data = read_list_channels()
        cat_chans = data['channels']
        #
        for cat in categories:
            chans = cat_chans[cat]
            #
            for chan in chans:
                try:
                    if chan['sd']['devicekeys'][device_type] == channo:
                        return chan['sd']['logo']
                except:
                    True
                try:
                    if chan['hd']['devicekeys'][device_type] == channo:
                        return chan['hd']['logo']
                except:
                    True
            #
        return '-'
    except:
        return 'error'