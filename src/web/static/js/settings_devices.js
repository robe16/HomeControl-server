function addGroup(num) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET', '/web/settings?gethtml=group&num=' + num, false);
    xmlHttp.send(null);
    if (xmlHttp.status==200) {
        var z = document.createElement('div');
        z.innerHTML = xmlHttp.responseText;
        document.getElementById('settings-groups').appendChild(z);
        document.getElementById('btn_addgroup').setAttribute('onclick', 'addGroup(' + (num + 1) + ')');
        return
        }
    else {return}
}


function addDevice(grpnum) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET', '/web/settings?gethtml=selection&grpnum=' + grpnum, false);
    xmlHttp.send(null);
    if (xmlHttp.status==200) {
        document.getElementById('msg_title').innerHTML = 'Select device:';
        document.getElementById('msg_txt').innerHTML = xmlHttp.responseText;
        document.getElementById('msg_btn').innerHTML = 'Cancel';
        document.getElementById('message_popup').className = 'message viewport_centre visible';
        return
        }
    else {return}
    //
    return
}


function addDeviceHTML(grpnum, device) {
    hidePopup();
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET', '/web/settings?gethtml=device&device='+ device, false);
    xmlHttp.send(null);
    if (xmlHttp.status==200) {
        var z = document.createElement('div');
        z.innerHTML = xmlHttp.responseText;
        document.getElementById('devicegroup_' + grpnum).appendChild(z);
        }
    else {return}
    //
    return
}


function sendDevices() {
    //
    if (!checkInputs()) {
        //
        document.getElementById('msg_txt').innerHTML = 'Errors prohibited the settings being saved. Please check entry fields and try again.';
        document.getElementById('msg_title').innerHTML = 'Error';
        document.getElementById('msg_btn').innerHTML = 'Ok'
        document.getElementById('message_popup').className = 'message viewport_centre visible';
        //
    } else {
        json = buildJson();
        if (json) {
            if (listChans && sendHttp('/settings/devices', json, 'POST', 2, false)) {
                document.getElementById('msg_title').innerHTML = 'Success';
                document.getElementById('msg_txt').innerHTML = 'Device settings have been successfully sent to the server.';
                document.getElementById('message_popup').className = 'message viewport_centre visible';
            } else {
                document.getElementById('msg_title').innerHTML = 'Error';
                document.getElementById('msg_txt').innerHTML = 'An error has been encountered.';
                document.getElementById('message_popup').className = 'message viewport_centre visible';
            }
        }
    }
}


function checkInputs() {
    //
    var result = true;
    //
    // Check all input elements and highlight if blank
    var elementsInputs = document.getElementsByTagName('input');
    //
    for (var i = 0; i < elementsInputs.length; i++) {
        //
        if (elementsInputs[i].value == '') {
            elementError(elementsInputs[i]);
            result = false;
        } else {
            elementNoError(elementsInputs[i]);
        }
        //
    }
    //
    // Check ipaddress inputs and highlight if input does not meet validation function
    var elementsIP = document.getElementsByName('ipaddress');
    //
    for (var i = 0; i < elementsIP.length; i++) {
        //
        if (!validateIpaddress(elementsIP[i].value)) {
            elementError(elementsIP[i]);
            result = false;
        } else {
            elementNoError(elementsIP[i]);
        }
        //
    }
    //
    return result;
    //
}


function elementError (element) {
    element.setAttribute("style", "outline: none; border-color: #ff0000; box-shadow: 0 0 5px #ff0000;");
}
function elementNoError (element) {
    element.setAttribute("style", "");
}


function validateIpaddress(ipaddress) {
    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress))
        {return (true)}
    else
        {return (false)}
}


function buildJson() {
    //
    var json = '[';
    //
    var grps = document.getElementsByName('group');
    //
    for (var g = 0; g < grps.length; g++) {
        //
        var grp_name = grps[g].getElementsByTagName('input');
        for (var e = 0; e < grp_name.length; e++) {
            if (grp_name[e].Name = 'groupname') {
                grp_name = grp_name[e].value;
                break;
            }
        }
        //
        if (g>0) {json += ',';}
        //
        json += '{"group": "' + grp_name + '",';
        json += '"devices": [';
        //
        var grp_dvcs = grps[g].getElementsByClassName('settings_box device');
        //
        for (var d = 0; d < grp_dvcs.length; d++) {
            //
            if (d>0) {json += ',';}
            //
            json += '{"device": "' + grp_dvcs[d].getAttribute("name") + '",';
            json += '"details": {';
            //
            var dvc_inputs = grp_dvcs[d].getElementsByTagName('input');
            //
            for (var i = 0; i < dvc_inputs.length; i++) {
                //
                if (i>0) {json += ',';}
                //
                json += '"' + dvc_inputs[i].name + '": "' + dvc_inputs[i].value + '"';
                //
            }
            //
            json += '}}';
            //
        }
        //
        json += ']}';
        //
    }
    //
    json += ']'
    //
    return json
    //
}