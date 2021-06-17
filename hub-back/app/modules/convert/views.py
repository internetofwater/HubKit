#!/usr/bin/env python

"""Transpose module views.

For license and copyright information please see the LICENSE document (the
"License") included with this software package. This file may not be used
in any manner except in compliance with the License unless required by
applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
"""


from flask import abort
from flask import json
from flask import jsonify
from flask import request
from flask import make_response
from flask import render_template
from flask import current_app

from . import module
from . import utilities

import json
import os
import os.path

from uuid import uuid4


@module.route('/v1/convert', methods=['OPTIONS'])
def convert_options():
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/upload-file', methods=['POST'])
def file_upload_post(*args, **kwargs):

    # data = json.loads(request)

    _file = request.files['excel']

    # Save  File

    basepath = current_app.config['MEDIA_BASE_PATH'] + 'files/'
    directory = os.getcwd() + '/app/static/usercontent/' + 'files/'

    """
    Prepare the file for processing
    # """

    filepath = os.path.join(directory, _file.filename)
    fileurl = os.path.join(basepath, _file.filename)

    try:
        _file.save(filepath)
    except:
        raise



    return jsonify(**utilities.get_column_headers(filepath)), 200

@module.route('/v1/upload-config', methods=['POST'])
def file_upload_json_post(*args, **kwargs):


    if request and request.files and 'json' in request.files:
        _file = request.files['json']

    result = {"status":"okay"}

    basepath = current_app.config['MEDIA_BASE_PATH'] + 'files/'
    directory = os.getcwd() + '/app/static/usercontent/' + 'files/'

    """
    Prepare the file for processing
    # """

    filepath = os.path.join(directory, _file.filename)
    fileurl = os.path.join(basepath, _file.filename)

    try:
        _file.save(filepath)
    except:
        raise

    # Opening JSON file
    f = open(filepath,)
    
    # returns JSON object as 
    # a dictionary
    result = json.load(f)
    
    # Closing file
    f.close()


    return jsonify(**result), 200


@module.route('/v1/convert', methods=['POST'])
def convert_post(*args, **kwargs):

    data = json.loads(request.data)
    source = None
    config = None

    if 'source' in data and data['source']:
        source = data['source']
    else:
        abort(make_response(jsonify(message="A source is required"), 400))

    if 'config' in data and data['config']:
        config = data['config']
    else:
        abort(make_response(jsonify(message="A configuration is required"), 400))


    return jsonify(**utilities.convert_data(source, config)), 200


@module.route('/v1/config', methods=['OPTIONS'])
def config_options():
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/config', methods=['POST'])

def config_post(*args, **kwargs):
    if request.content_type is None:
        abort(make_response(jsonify(message="Must be in JSON format"), 400))

    if request.content_type is not None and (request.content_type == 'application/json' or 'application/json' in request.content_type):
        try:
            data = json.loads(request.data)
        except ValueError as e:
             abort(make_response(jsonify(message="Must be in JSON format"), 400))
       
        return jsonify(**utilities.create_config(data)), 200


    abort(make_response(jsonify(message="Must be in JSON format"), 400))

@module.route('/v1/process', methods=['OPTIONS'])
def process_options():
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/process', methods=['POST'])

def process_post(*args, **kwargs):
    if request.content_type is None:
        abort(make_response(jsonify(message="Must be in JSON format"), 400))

    if request.content_type is not None and (request.content_type == 'application/json' or 'application/json' in request.content_type):
        try:
            data = json.loads(request.data)
        except ValueError as e:
             abort(make_response(jsonify(message="Must be in JSON format"), 400))
       
        return jsonify(**utilities.process_data(data)), 200


    abort(make_response(jsonify(message="Must be in JSON format"), 400))

        
@module.route('/v1/form', methods=['GET'])
def form_get(*args, **kwargs):

    return render_template("index.html")