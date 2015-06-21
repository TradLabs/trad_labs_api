#!/usr/bin/python3
# pylint: disable=broad-except
"""Change Messages to be sent"""
__author__ = 'sfblackl'

import logging
import logging.handlers
import socket

from flask import g, request
from requests_futures.sessions import FuturesSession

SESSION = FuturesSession()


def bg_cb(sess, resp):
    """ Don't do anything with the response """
    pass

# def get_full_message(record):
#     """ Unused """
#     if record.exc_info:
#         return '\n'.join(traceback.format_exception(*record.exc_info))
#     else:
#         return record.getMessage()

def generate_header():
    """ Creates custom tags to go over header """
    env = getattr(g, 'env', 'unknown')
    return {'X-LOGGLY-TAG': env}

class HTTPSHandler(logging.Handler):
    """ Stolen from Loggy's default class """
    def __init__(self, url, fqdn=False, localname=None, facility=None):
        """ Initialize """
        logging.Handler.__init__(self)
        self.url = url
        self.fqdn = fqdn
        self.localname = localname
        self.facility = facility

    def to_loggly(self, record):
        """ Generates Message """
        if self.fqdn:
            host = socket.getfqdn()
        elif self.localname:
            host = self.localname
        else:
            host = socket.gethostname()

        env = getattr(g, 'env', 'unknown')
        location = '%d:%s' % (record.lineno, record.module)
        operation = '%s %s' % (request.method, request.path)
        request_id = getattr(g, 'request_id', '')

        source_ip = request.remote_addr
        xff = request.headers.get('HTTP_X_FORWARDED_FOR', None)
        if xff is None:
            xff = request.headers.get('X_FORWARDED_FOR', None)
        if xff is not None:
            source_ip = xff + ',' + source_ip

        return {
            'deployment': env,
            'host': host,
            'program': 'api',
            'operation': operation,
            'level': logging.getLevelName(record.levelno),
            'location': location,
            'message': record.getMessage(),
            'request_id': request_id,
            'timestamp': record.created,
            'source_ip': source_ip,
            # 'full_message': self.get_full_message(record), # Removed for performance
        }

    def emit(self, record):
        """ Called by all requests to log """
        try:
            payload = self.to_loggly(record)
            headers = generate_header()
            SESSION.post(self.url, data=payload, background_callback=bg_cb, headers=headers)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
