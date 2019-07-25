from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
      lookup: 
        author: Chris Mills <chris@discreet-its.co.uk>
        version_added: 2.9
        short_description: query elements from Netbox
        description:
            - This lookup returns elements from Netbox via it's API.
        options:
          _terms:
            description: path(s) of files to read
            required: True
        notes:
          - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from pprint import pformat

import pynetbox

display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

	netbox_api_token = kwargs.get('token')
        netbox_api_endpoint = kwargs.get('api_endpoint')

        netbox = pynetbox.api(netbox_api_endpoint,
            token=netbox_api_token)

        ret = {}
        for term in terms:

            # Don't use print or your own logging, the display class
            # takes care of it in a unified way.
            display.vvvv(u"Netbox lookup for %s to %s using token %s" % (term, netbox_api_endpoint, netbox_api_token))
            display.vvvv(u"kwargs is: %s" % kwargs)

            for object in netbox.tenancy.tenants.all():
                o = dict(object)
                display.vvvv(pformat(o))
                ret[o['name']] = o

        return [ret]
