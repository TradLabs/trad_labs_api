#!/usr/bin/python3

"""Maps all incoming paths to correct functions to handle"""
from flaskApp import application, custom_errors


@application.route('/tradlabs/v1/health')
def health():
    """Health Check Function used by ELB and SLA Monitoring"""
    return "OK"

################################################################################
# TESTING
################################################################################
@application.route('/tradlabs/v1/500', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test_500():
    """Forces error to validate error message is correct"""
    print(1/0)

@application.route('/tradlabs/v1/403', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test_403():
    """Generates 403 Error.  ToDo: Replace this with valid test"""
    return custom_errors.error_formatter(code=40301)
