# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from imp import reload
import os, sys
from urllib import response
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from apps.home import blueprint
from flask import render_template, request, flash, redirect
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.authentication.models import Users, Devices
from apps.authentication.forms import LoginForm, CreateAccountForm
import creds as creds
from pycentral.base import ArubaCentralBase
from apps import db, login_manager
import flask

central_info = creds.central_info

ssl_verify = True
central = ArubaCentralBase(central_info=central_info,
                           ssl_verify=ssl_verify)

@blueprint.route('/index')
@login_required
def index():
#    return render_template('home/ui-vpn.html', segment='vpn', devices = Devices.query.all())
    return redirect("/ui-vpn.html", code = 302)

@blueprint.route('/ui-vpn.html', methods=['GET', 'POST'])
@login_required
def vpn_info():
    if request.method == 'POST':
        serial = request.form.get("serial")
        mac = request.form.get("mac")
        AP_INNER_IP = request.form.get("ip")
        hostname = request.form.get("hostname")
        PBR_1 = request.form.get("PBR_1")
        PBR_2 = request.form.get("PBR_2")
        PBR_3 = request.form.get("PBR_3")
        PBR_4 = request.form.get("PBR_4")
        PBR_WIRED_1 = request.form.get("PBR_WIRED_1")
        PBR_WIRED_2 = request.form.get("PBR_WIRED_2")
        PBR_WIRED_3 = request.form.get("PBR_WIRED_3")
        PBR_WIRED_4 = request.form.get("PBR_WIRED_4")
        apiPath = "/configuration/v1/devices/" + serial + "/template_variables"
        apiMethod = "PATCH"
        apiData = {
        "variables": {
            "_sys_lan_mac": mac,
            "_sys_serial": serial,
            "hostname": hostname,
            "AP_INNER_IP": AP_INNER_IP,
            "PBR_1": PBR_1,
            "PBR_2": PBR_2,
            "PBR_3": PBR_3,
            "PBR_4": PBR_4,
            "PBR_WIRED_1": PBR_WIRED_1,
            "PBR_WIRED_2": PBR_WIRED_2,
            "PBR_WIRED_3": PBR_WIRED_3,
            "PBR_WIRED_4": PBR_WIRED_4
                    }
                }
        central.command(apiMethod=apiMethod, apiPath=apiPath, apiData=apiData)
#        flash('AP Provisioning Complete')
#        flash(mac + serial)
#        return render_template("home/ui-vpn.html", message="Success", segment='vpn', devices = Devices.query.all())
#        return redirect("/ui-vpn.html")
        return ('', 204)

#    elif request.method == 'GET':
    else:
#        print(current_user.serial)
        serial = current_user.serial
        results = central.command(apiMethod="GET", apiPath="/configuration/v1/devices/" + serial + "/template_variables")
        PBR_1_CURRENT = results['data']['variables']['PBR_1']
        PBR_2_CURRENT = results['data']['variables']['PBR_2']
        PBR_3_CURRENT = results['data']['variables']['PBR_3']
        PBR_4_CURRENT = results['data']['variables']['PBR_4']
        PBR_WIRED_1_CURRENT = results['data']['variables']['PBR_WIRED_1']
        PBR_WIRED_2_CURRENT = results['data']['variables']['PBR_WIRED_2']
        PBR_WIRED_3_CURRENT = results['data']['variables']['PBR_WIRED_3']
        PBR_WIRED_4_CURRENT = results['data']['variables']['PBR_WIRED_4']
        PBR_1 = Devices.query.filter_by(ipsec=PBR_1_CURRENT).first()
        PBR_2 = Devices.query.filter_by(ipsec=PBR_2_CURRENT).first()
        PBR_3 = Devices.query.filter_by(ipsec=PBR_3_CURRENT).first()
        PBR_4 = Devices.query.filter_by(ipsec=PBR_4_CURRENT).first()
        PBR_WIRED_1 = Devices.query.filter_by(ipsec=PBR_WIRED_1_CURRENT).first()
        PBR_WIRED_2 = Devices.query.filter_by(ipsec=PBR_WIRED_2_CURRENT).first()
        PBR_WIRED_3 = Devices.query.filter_by(ipsec=PBR_WIRED_3_CURRENT).first()
        PBR_WIRED_4 = Devices.query.filter_by(ipsec=PBR_WIRED_4_CURRENT).first()
        return render_template("home/ui-vpn.html", segment='vpn', 
        PBR_1_CURRENT=PBR_1_CURRENT,
        PBR_2_CURRENT=PBR_2_CURRENT,
        PBR_3_CURRENT=PBR_3_CURRENT,
        PBR_4_CURRENT=PBR_4_CURRENT,
        PBR_1=PBR_1, 
        PBR_2=PBR_2,
        PBR_3=PBR_3,
        PBR_4=PBR_4,
        PBR_WIRED_1_CURRENT=PBR_WIRED_1_CURRENT,
        PBR_WIRED_2_CURRENT=PBR_WIRED_2_CURRENT,
        PBR_WIRED_3_CURRENT=PBR_WIRED_3_CURRENT,
        PBR_WIRED_4_CURRENT=PBR_WIRED_4_CURRENT,
        PBR_WIRED_1=PBR_WIRED_1,
        PBR_WIRED_2=PBR_WIRED_2,
        PBR_WIRED_3=PBR_WIRED_3,
        PBR_WIRED_4=PBR_WIRED_4,
        devices = Devices.query.all())

@blueprint.route('/ui-inventory.html', methods=['GET', 'POST'])
@login_required
def inventory_info():
    create_account_form = CreateAccountForm(request.form)

    if 'user-submit' in request.form:
        
        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('home/ui-inventory.html', users = Users.query.all(), devices = Devices.query.all(),
                                   msg='Username already registered',
                                   segment = 'inventory',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('home/ui-inventory.html', users = Users.query.all(), devices = Devices.query.all(),
                                   msg='Email already registered',
                                   segment = 'inventory', 
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('home/ui-inventory.html', users = Users.query.all(), devices = Devices.query.all(),
                               msg='User Added',
                               segment = 'inventory', 
                               success=True,
                               form=create_account_form)
            
    if 'user-delete' in request.form:
        deleteUser = request.form.get('id')
        Users.query.filter_by(id=deleteUser).delete()
        db.session.commit()

        return render_template('home/ui-inventory.html', users = Users.query.all(), devices = Devices.query.all(),
                               msg='User Deleted',
                               segment = 'inventory', 
                               success=True,
                               form=create_account_form)

    if 'gateway-submit' in request.form:

        # else we can create the user
        devices = Devices(**request.form)
        db.session.add(devices)
        db.session.commit()

        return render_template('home/ui-inventory.html', users = Users.query.all(), devices = Devices.query.all(),
                               gwmsg='Gateway Added',
                               segment = 'inventory', 
                               success=True)

    if 'gateway-delete' in request.form:
        deleteGateway = request.form.get('device_id')
        Devices.query.filter_by(id=deleteGateway).delete()
        db.session.commit()

        return render_template('home/ui-inventory.html', users = Users.query.all(), devices = Devices.query.all(),
                               gwmsg='Gateway Deleted', 
                               segment = 'inventory',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('home/ui-inventory.html', users = Users.query.all(), devices = Devices.query.all(),
                                segment = 'inventory', 
                                form=create_account_form)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            pass

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, users = Users.query.all(), devices = Devices.query.all())

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
