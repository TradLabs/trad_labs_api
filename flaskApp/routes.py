#!/usr/bin/python3
# pylint: disable=unused-import

"""Maps all incoming paths to correct functions to handle"""
from flaskApp import application


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
