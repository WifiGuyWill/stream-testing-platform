# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from typing import Match
from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    serial = db.Column(db.String(64), unique=True)
    hostname = db.Column(db.String(64), unique=True)
    mac = db.Column(db.String(64), unique=True)
    ip = db.Column(db.String(64), unique=True)
    

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

class Devices(db.Model):

    __tablename__ = 'Devices'

    id = db.Column(db.Integer, primary_key=True)
    vgwname = db.Column(db.String(64), nullable=False)
    region = db.Column(db.String(64), nullable=False)
    ipsec = db.Column(db.String(128), nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.vgwname)
#    def __init__(self, id, vgwname, region, ipsec):
#        self.id = id
#        self.vgwname = vgwname
#        self.region = region
#       self.ipsec = ipsec
#@login_manager.devices_loader
#def device_loader(id):
#    return Devices.query.all()

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
