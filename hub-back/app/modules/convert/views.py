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

import wget
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

    _file = request.files['file']
    _type = None

    if len(os.path.splitext(_file.filename))>1:
        if os.path.splitext(_file.filename)[1] == '.csv':
            _type = 'csv'
        elif os.path.splitext(_file.filename)[1] == '.xlsx':
            _type = 'excel' 
        else:
            abort(make_response(jsonify(message="File type must be .csv or .xlsx"), 400))
    else:
        abort(make_response(jsonify(message="File type was not found"), 400))
    

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



    return jsonify(**utilities.get_column_headers(filepath, _type)), 200

@module.route('/v1/upload-file-url', methods=['POST'])
def file_url_upload_post(*args, **kwargs):

    data = json.loads(request.data)

    if data['file_path']:
        url = data['file_path']
        directory = os.getcwd() + '/app/static/usercontent/' + 'files/'
        filename = wget.download(url, out=directory)

    if len(os.path.splitext(filename))>1:
        if os.path.splitext(filename)[1] == '.csv':
            _type = 'csv'
        elif os.path.splitext(filename)[1] == '.xlsx':
            _type = 'excel' 
        else:
            abort(make_response(jsonify(message="File type must be .csv or .xlsx"), 400))
    else:
        abort(make_response(jsonify(message="File type was not found"), 400))

    return jsonify(**utilities.get_column_headers(filename, _type)), 200

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

    data = json.loads(request.data)
    result = {}

    if request.content_type is None:
        abort(make_response(jsonify(message="Must be in JSON format"), 400))

    if request.content_type is not None and (request.content_type == 'application/json' or 'application/json' in request.content_type):
        try:
            data = json.loads(request.data)
            print("Lets do it", "output" in data )
            result = utilities.process_data(data)
            # return jsonify(**result), 200
        except ValueError as e:
             abort(make_response(jsonify(message="This is not working out"), 400))


    # abort(make_response(jsonify(message="Must be in JSON format"), 400))
    return {
        "content-type":request.content_type,
        "result":result
        # "data":data
        }

@module.route('/v1/schedule', methods=['POST'])
def schedule_cron_post(*args, **kwargs):
    if request.content_type is None:
        abort(make_response(jsonify(message="Must be in JSON format"), 400))

    if request.content_type is not None and (request.content_type == 'application/json' or 'application/json' in request.content_type):
        try:
            data = json.loads(request.data)
        except ValueError as e:
             abort(make_response(jsonify(message="Must be in JSON format"), 400))
       
        return jsonify(**utilities.schedule_cron(data)), 200


    abort(make_response(jsonify(message="Must be in JSON format"), 400))

@module.route('/v1/run_job', methods=['POST'])
def run_job_post(*args, **kwargs):
    if request.content_type is None:
        abort(make_response(jsonify(message="Must be in JSON format"), 400))

    if request.content_type is not None and (request.content_type == 'application/json' or 'application/json' in request.content_type):
        try:
            data = json.loads(request.data)
        except ValueError as e:
             abort(make_response(jsonify(message="Must be in JSON format"), 400))
       
        return jsonify(**utilities.run_cron(data)), 200


    abort(make_response(jsonify(message="Must be in JSON format"), 400))



@module.route('/v1/cron', methods=['GET'])
def cron_get(*args, **kwargs):
    return jsonify(**utilities.get_cron()), 200

@module.route('/v1/cron', methods=['DELETE'])
def cron_delete_one(*args, **kwargs):
    return jsonify(**utilities.delete_job()), 200

@module.route('/v1/cron/delete-all', methods=['DELETE'])
def cron_delete_all(*args, **kwargs):
    return jsonify(**utilities.delete_all_jobs()), 200


@module.route('/v1/cron-log', methods=['GET'])
def cron_log_get(*args, **kwargs):
    return jsonify(**utilities.get_cron_log()), 200
