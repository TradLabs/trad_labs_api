#!/usr/bin/python3
"""Allows for default errors to be formatted correctly according to our specification"""
__author__ = 'sfblackl'

from flask import jsonify, request

from . import application


################################################################################
# ERROR MESSAGES
################################################################################
ERROR_MESSAGES = {40001: 'Invalid request: unspecified item.',
                  40401: 'Not Found: The resource (%s) you requested could not be found.',
                  50001: 'Internal server error(1)',    # General
                  50002: 'Internal server error(2)',    # Service
                  50003: 'Internal server error(3)'}    # DB

def error_formatter(code, request_id=None, details=None, parm1=None, parm2=None):
    """Takes Error Code and various parms to build JSON error structure"""
    if request_id:
        request_id = str(request_id)

    if details is not None:
        details = str(details)

    # Determine Status Code based on error
    status_code = int(code / 100)

    # Build Message based on parameters
    if parm2 is not None:
        message = str(ERROR_MESSAGES[code] % (parm1, parm2))
    elif parm1 is not None:
        message = str(ERROR_MESSAGES[code] % parm1)
    else:
        message = str(ERROR_MESSAGES[code])

    # Build JSON - Include Detail if exists
    if details is None:
        json_message = jsonify(code='TLA-' + str(code),
                               message=message,
                               request_id=request_id)
    else:
        json_message = jsonify(code='TLA-' + str(code),
                               message=message,
                               request_id=request_id,
                               details=details)
    # Return message and HTTP status code
    return json_message, status_code

################################################################################
# ERROR ROUTES
################################################################################
@application.errorhandler(404)
def page_not_found(err):
    """Error Handler for Page Not Found"""
    return error_formatter(code=40401, request_id='', parm1=request.path, details=err)

@application.errorhandler(500)
def internal_server_error(err):
    """Error Handler for Internal Server Error"""
    return error_formatter(code=50001, details=err)
