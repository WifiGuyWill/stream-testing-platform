# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import Email, DataRequired, IPAddress, MacAddress

# login and registration


class LoginForm(FlaskForm):
    username = TextField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    serial = TextField('Serial',
                             id='serial_create',
                             validators=[DataRequired()])
    mac = TextField('Mac',
                             id='mac_create',
                             validators=[DataRequired()])
    hostname = TextField('Hostname',
                             id='hostname_create',
                             validators=[DataRequired()])
    

class UpdateAccountForm(FlaskForm):
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    serial = TextField('Serial',
                             id='serial_create',
                             validators=[DataRequired()])
    mac = TextField('Mac',
                             id='mac_create',
                             validators=[DataRequired(), MacAddress()])
    hostname = TextField('Hostname',
                             id='hostname_create',
                             validators=[DataRequired()])
    ip = TextField('IP',
                             id='ip_create',
                             validators=[DataRequired(), IPAddress()])