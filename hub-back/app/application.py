#!/usr/bin/env python

"""Copyright and License Information.

For license and copyright information please see the LICENSE.md (the "License")
document packaged with this software. This file and all other files included in
this packaged software may not be used in any manner except in compliance with
the License. Software distributed under this License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTY, OR CONDITIONS OF ANY KIND, either express or
implied.

See the License for the specific language governing permission and limitations
under the License.
"""


import io
import json


from datetime import datetime


from flask import jsonify
from flask import request


from . import flask
from . import logger
from . import os
from . import imp



CORE_MODULES = [
    'core'
]

class Application(object):
    """Create Flask Application via a Class."""

    def __init__(self, environment, name, app=None, extensions={}):
        """Application Constructor.

        Setup our base Flask application, retaining it as our application
        object for use throughout the application

        :param (class) self
            The representation of the instantiated Class Instance
        :param (str) name
            The name of the application
        :param (str) environment
            The name of the enviornment in which to load the application
        :param (class) app
            The Flask class for the application that was created
        """
        logger.info('Application Started at %s', datetime.utcnow())

        self.name = name
        self.environment = environment
        self.extensions = extensions

        """Create our base Flask application
        """
        self.app = flask.Flask(__name__)
        logger.info('Starting application named `%s`' % __name__)

        """Import all custom app configurations
        """
        _config = ('config/%s.config') % (environment)

        """Read the JSON configuration file content.
        """
        self.app.config.from_json(_config)
        self.app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

        logger.info('Application loading configuration from %s', _config)

        """Setup Cross Site Origin header rules
        """
        self.app.after_request(self.setup_cors)

        logger.info('Application setup complete')

        @self.app.route('/')
        def hello_world():
            return {"status":"okay"}

        from .modules import convert
        self.app.register_blueprint(convert.module)

    def setup_cors(self, response):
        """Define global Cross Origin Resource Sharing rules.

        Setup our headers so that the respond correctly and securely

        :param (object) self
            the current class (i.e., Application)

        @return (object) response
            the fully qualified response object
        """
        logger.info('Application Cross Origin Resource Sharing')

        """Access-Control-Allow-Origin
        """
        _origin = None

        if flask.request.headers.get('Origin', '') in \
                self.app.config['ACCESS_CONTROL_ALLOW_ORIGIN']:
            _origin = request.headers.get('Origin', '')

        """Access-Control-Allow-Methods
        """
        _methods = self.app.config['ACCESS_CONTROL_ALLOW_METHODS']

        """Access-Control-Allow-Headers
        """
        _headers = self.app.config['ACCESS_CONTROL_ALLOW_HEADERS']

        """Access-Control-Allow-Credentials
        """
        _credentials = self.app.config['ACCESS_CONTROL_ALLOW_CREDENTIALS']

        """Setup Access Control headers for the application

        Using the user defined enviornment, setup access control headers
        """
        response.headers['Access-Control-Allow-Origin'] = _origin
        response.headers['Access-Control-Allow-Methods'] = _methods
        response.headers['Access-Control-Allow-Headers'] = _headers
        response.headers['Access-Control-Allow-Credentials'] = _credentials

        return response

    


    
