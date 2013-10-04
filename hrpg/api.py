#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phil Adams http://philadams.net

Python wrapper around the Habit RPG (http://habitrpg.com) API
http://github.com/philadams/hrpg
"""


import json
import os
import cmd
from pprint import pprint

import requests

API_URI_BASE = 'https://habitrpg.com/api/v1'
API_CONTENT_TYPE = 'application/json'


class HRPG(object):
    """
    A minimalist Habit RPG API class.
    """

    def __init__(self, auth=None, resource=None, aspect=None):
        self.auth = auth
        self.resource = resource
        self.aspect = aspect
        self.headers = auth if auth else {}
        self.headers.update({'content-type': API_CONTENT_TYPE})

    def __getattr__(self, m):
        try:
            return object.__getattr__(self, m)
        except AttributeError as e:
            if not self.resource:
                return HRPG(auth=self.auth, resource=m)
            else:
                return HRPG(auth=self.auth, resource=self.resource,
                            aspect=m)

    def __call__(self, **kwargs):
        if self.aspect:
            aspect_id = kwargs.pop('id', None)
            if aspect_id is not None:
                uri = '%s/%s/%s/%s' % (API_URI_BASE,
                                       self.resource,
                                       self.aspect,
                                       str(aspect_id))
            else:
                uri = '%s/%s/%s' % (API_URI_BASE,
                                    self.resource,
                                    self.aspect)
        else:
            uri = '%s/%s' % (API_URI_BASE,
                             self.resource)

        req = requests.get(uri, headers=self.headers, params=kwargs)
        #print(req.url)  # debug...
        if req.status_code == 200:
            return req.json()
        else:
            print('Unhandled HTTP status code')
            raise NotImplementedError
