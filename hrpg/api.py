#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phil Adams http://philadams.net

Python wrapper around the Habit RPG (http://habitrpg.com) API
http://github.com/philadams/hrpg
"""


import json

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
        except AttributeError:
            if not self.resource:
                return HRPG(auth=self.auth, resource=m)
            else:
                return HRPG(auth=self.auth, resource=self.resource, aspect=m)

    def __call__(self, **kwargs):
        method = kwargs.pop('_method', 'get')

        # build up URL... HRPG's api is the *teeniest* bit annoying
        # so either i need to find a cleaner way here, or i should
        # get involved in the API itself and... help it.
        if self.aspect:
            aspect_id = kwargs.pop('_id', None)
            direction = kwargs.pop('_direction', None)
            if aspect_id is not None:
                uri = '%s/%s/%s/%s' % (API_URI_BASE,
                                       self.resource,
                                       self.aspect,
                                       str(aspect_id))
            else:
                uri = '%s/%s/%s' % (API_URI_BASE, self.resource, self.aspect)
            if direction is not None:
                uri = '%s/%s' % (uri, direction)
        else:
            uri = '%s/%s' % (API_URI_BASE, self.resource)

        # actually make the request of the API
        if method in ['put', 'post']:
            res = getattr(requests, method)(uri, headers=self.headers,
                                            data=json.dumps(kwargs))
        else:
            res = getattr(requests, method)(uri, headers=self.headers,
                                            params=kwargs)

        print(res.url)  # debug...
        if res.status_code == requests.codes.ok:
            return res.json()
        else:
            res.raise_for_status()
