#!/usr/bin/env python

"""Transpose module.


For license and copyright information please see the LICENSE document (the
"License") included with this software package. This file may not be used
in any manner except in compliance with the License unless required by
applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
"""


from flask import Blueprint


module = Blueprint(**{
    'name': __name__,
    'import_name': __name__,
    'static_folder': None,
    'static_url_path': None,
    'template_folder': 'templates',
    'url_prefix': None,
    'subdomain': None,
    'url_defaults': None
})

if module:
    """Verify module Blueprint is instantiated."""
    from . import views
