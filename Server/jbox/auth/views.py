import sys, os
import requests
from flask import json, jsonify, render_template, redirect, request, url_for, flash, session, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from wtforms import Form
from . import auth
from ..models import Developer, Integration
from ..main.forms import FakeUserForm
from ..api_1_0.developers import get_channels, modificate_integration

UPLOAD_FOLDER = '/users/admin/Desktop/temp/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return render_template('index.html')


@auth.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    integrations = Developer.query.filter_by(dev_key=current_user.dev_key).first().integrations
    return render_template('auth/manage.html', integrations=integrations)


@auth.route('/manage/create_integration/<string:integration_id>/<string:token>/<string:channel>', methods=['GET', 'POST'])
@login_required
def create_integration(integration_id, token, channel):
    channels = get_channel_list()
    dev_key = current_user.dev_key
    return render_template('auth/create.html', **locals())


@auth.route('/manage/edit_integration', methods=['GET'])
@login_required
def edit_integration():
    if request.json['name'] is not None:
        name = request.json['name']
        description = request.json['description']
        channel = request.json['channel']
        icon = request.json['icon']
    return render_template('auth/create.html', **locals())


@auth.route('/new/postTochannels', methods=['GET'])
@login_required
def post_to_channel():
    dev_key = current_user.dev_key
    return render_template('auth/new/postToChannels.html', dev_key=dev_key, channels=get_channel_list())


@auth.route('/new/channel', methods=['GET'])
@login_required
def new_channel():
    return render_template('auth/new/channel.html', dev_key=current_user.dev_key)


@auth.route('/qrcode', methods=['GET'])
@login_required
def qrcode():
    return render_template('auth/qrcode.html', dev_key=current_user.dev_key)


@auth.route('/uploadajax', methods=['POST'])
def upldfile():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            file_size = os.path.getsize(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify(name=filename, size=file_size)


# @auth.route('/edit_integration/<string:integration_id>', methods=['GET', 'POST'])
# @login_required
# def edit_integration(integration_id):
#     dev_key = current_user.dev_key
#     file = form.icon.data
#     if file and allowed_file(file.filename):
#         filename = file.filename
#         file.save(os.path.join(UPLOAD_FOLDER, filename))
#         name = form.integration_name.data
#         description = form.description.data
#         channel = form.input.data
#         print("name: " + name + " description: " + description + " channel: " + channel)
#
#         r = modificate_integration(dev_key, integration_id)
#         print(dir(r))
#         return redirect(url_for('/manage'))
#     else:
#         flash('file is not null or not allowed')
#     return render_template('auth/create.html', **locals())

def get_channel_list():
    channel_list = []
    developer = Developer.query.filter_by(dev_key=current_user.dev_key).first()
    if developer is not None:
        channels = developer.channels
        for channel in channels:
            channel_list.append(channel.channel)
        return channel_list
