#!/usr/bin/python3
"""Google Identity Functions"""
__author__ = 'sfblackl'

import traceback
import sys
import os
import logging

from flask import redirect, request, url_for
from oauth2client import client
import requests

import flaskApp.config
import flaskApp.custom_errors



# Create Logger
LOGGER = logging.getLogger('tradlabs.api.routes')
LOGGER.setLevel(flaskApp.config.LOG_LEVEL_GOOGLE)


def google_flow():
    """Get values so they can be logged under debug before constructing"""
    file_name = os.getcwd() + '/client.json'
    redirect_uri = url_for('google_callback', _external=True)
    LOGGER.debug('secret file path: %s; redirect_uri: %s', file_name, redirect_uri)

    # Create the flow
    flow = client.flow_from_clientsecrets(file_name,
                                          scope='https://www.googleapis.com/auth/userinfo.profile '
                                                'https://www.googleapis.com/auth/userinfo.email',
                                          redirect_uri=redirect_uri)

    return flow


def google_fetch_user_info(access_token):
    # Call Google to get credentials
    url = 'https://www.googleapis.com/userinfo/v2/me'
    headers = {'Authorization': 'Bearer ' + access_token}
    try:
        response = requests.get(url, headers=headers)

    except Exception:
        LOGGER.error("Exception getting user info: %s",
                     traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        return flaskApp.custom_errors.error_formatter(code='500_02', display_format='html',
                                                      details=traceback.format_exception_only(sys.exc_info()[0],
                                                                                              sys.exc_info()[1]))

    return response.text


################################################################################
def google_login():
    """Handle Initial Login"""
    flow = google_flow()

    # Using Flow get the auth URI
    auth_uri = flow.step1_get_authorize_url()
    LOGGER.debug('auth_uri: %s', str(auth_uri))

    return redirect(auth_uri)


def google_callback():
    """Handle the redirect request from consumers browser containing information from identity provider"""

    # I. Get Inputs and Handle Error returned
    error_message = request.args.get('error')
    auth_code = request.args.get('code', '')
    LOGGER.debug('Google Return Error: %s, Code: %s', str(error_message), auth_code)

    # If Error, throw error message
    if error_message is not None:
        return flaskApp.custom_errors.error_formatter(code='403_opt_out', display_format='html', details=error_message)

    # II. Call Google to get credentials
    # If no success return error message
    try:
        flow = google_flow()
        credentials = flow.step2_exchange(auth_code)
        LOGGER.debug('credentials: %s', str(credentials.access_token))
    except Exception:
        LOGGER.error("Exception getting credentials: %s",
                     traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        return flaskApp.custom_errors.error_formatter(code='500_02', display_format='html',
                                                      details=traceback.format_exception_only(sys.exc_info()[0],
                                                                                              sys.exc_info()[1]))

    # III. Use credentials to get information
    return google_fetch_user_info(str(credentials.access_token))
