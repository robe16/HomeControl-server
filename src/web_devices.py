from urllib import urlopen
from web_tvlistings import html_listings_user_and_all


def _create_device_page(user, tvlistings, device, group_name, device_name):
    #
    if not device:
        return ''
    #
    html_body = device.getHtml()
    # Get whether device requires TV guide displaying on page
    try:
        bool_tvguideuse = device.getTvguide_use()
    except:
        bool_tvguideuse = False
    # Create tv guide html if required
    if bool_tvguideuse:
        #
        html_tv = refresh_tvguide(tvlistings,
                                  device=device,
                                  group_name=group_name,
                                  device_name=device_name,
                                  user=user)
        #
        html_body += '</div>'
        html_body += '<br>'
        html_body += '<div class="row">'
        html_body += urlopen('web/html_tvguide/tvguide.html').read().encode('utf-8').format(listings=html_tv)
    #
    return html_body


def refresh_tvguide(tvlistings, device=None, group_name=False, device_name=False, user=False):
    # Attempt getting current channel from device
    try:
        chan_current = device.getChan()
    except:
        chan_current = False
    #
    return html_listings_user_and_all(tvlistings, device=device, group_name=group_name, device_name=device_name, chan_current=chan_current, user=user)