'''
Created on May 15, 2013

@author: thiagorramos
'''

from django.http.response import HttpResponse
import json


def jsonify(function=None):
    if function:
        def wrapped(*args, **kwargs):
            try:
                return HttpResponse(json.dumps(function(*args, **kwargs)),
                                    mimetype="application/json")
            except Exception, e:
                raise e
                return HttpResponse(json.dumps({"ok": False}),
                                    mimetype="application/json")
        return wrapped
    return jsonify
