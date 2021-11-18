#!/usr/bin/python3
#(c) 2021 Will Smith

from pycentral.base import ArubaCentralBase
import json
import creds as creds
import requests
from flask import Flask, render_template, request, flash
import flask

central_info = creds.central_info

ssl_verify = True
central = ArubaCentralBase(central_info=central_info,
                           ssl_verify=ssl_verify)

app = Flask(__name__)

@app.route("/")
def starting_url():
    return flask.redirect("/vpn.html")

@app.route("/index.html")
def dashboard():
    wlan_total_up = central.command(apiMethod="GET",
                            apiPath="/monitoring/v2/clients?calculate_total=true&limit=1&timerange=3H&client_type=WIRELESS&client_status=CONNECTED")
    wired_total_up = central.command(apiMethod="GET",
                            apiPath="/monitoring/v2/clients?calculate_total=true&limit=1&timerange=3H&client_type=WIRED&client_status=CONNECTED")
    ap_total_up = central.command(apiMethod="GET",
                            apiPath="/monitoring/v2/aps?status=Up&calculate_total=true")
    gateway_total_up = central.command(apiMethod="GET",
                            apiPath="/monitoring/v1/gateways?status=Up&calculate_total=true")
    apprf_top = central.command(apiMethod="GET",
                            apiPath="/apprf/datapoints/v2/topn_stats")
    audit_events = central.command(apiMethod="GET",
                            apiPath="/auditlogs/v1/events?limit=5")                         
    return render_template("index.html", wlan_total_up = wlan_total_up, wired_total_up = wired_total_up, ap_total_up = ap_total_up, gateway_total_up = gateway_total_up, apprf_top = apprf_top, audit_events = audit_events)
   
@app.route("/wlan_clients.html")
def wlan_client_info():
    clients = central.command(apiMethod="GET",
                            apiPath="/monitoring/v2/clients?timerange=3H&client_type=WIRELESS&client_status=CONNECTED")
    return render_template("wlan_clients.html", clients = clients)

@app.route("/wired_clients.html")
def wired_client_info():
    clients = central.command(apiMethod="GET",
                            apiPath="/monitoring/v2/clients?timerange=3H&client_type=WIRED&client_status=CONNECTED")
    return render_template("wired_clients.html", clients = clients)

@app.route("/devices.html")
def device_info():
    aps = central.command(apiMethod="GET",
                            apiPath="/monitoring/v2/aps")
    gateways = central.command(apiMethod="GET",
                            apiPath="/monitoring/v1/gateways")
    return render_template("devices.html", aps = aps, gateways = gateways)

@app.route("/vpn.html", methods = ['POST', 'GET'])
def rap_info():
    if request.method == 'POST':
        serial = request.form.get("serial")
        vpn = request.form.get("vpn")
        apiPath = "/configuration/v1/devices/" + serial + "/template_variables"
        apiMethod = "PATCH"
        apiData = {
        "variables": {
        "vpn_primary": vpn,
        "vpn_tunnel_ip": "10.254.254.254"
                    }
                }
        central.command(apiMethod=apiMethod, apiPath=apiPath, apiData=apiData)
        flash('AP Provisioning Complete')
        return render_template("vpn.html", message="Success")

    elif request.method == 'GET':
        return render_template("vpn.html")

@app.route('/manual.html', methods = ['POST', 'GET'])
def main():
        if request.method == 'POST':
            api = request.form.get("api")
            serial = request.form.get("serial")
            mac = request.form.get("mac")
            vpn = request.form.get("vpn")
            url = "https://apigw-prod2.central.arubanetworks.com/configuration/v1/devices/" + serial + "/template_variables"
            headers = {
            'Authorization': 'Bearer ' + api,
            'Content-Type': 'application/json'
            }
            payload = json.dumps({
            "variables": {
                "vpn_primary": vpn,
                "vpn_tunnel_ip": vpn
                }
            })
            response = requests.request("PATCH", url, headers=headers, data=payload)
            return 'AP Provisioning Complete'

        elif request.method == 'GET':
            return render_template("manual.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')