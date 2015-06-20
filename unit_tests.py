#!/usr/bin/python3
"""Collection of Unit Tests for Application """
# __author__ = 'sfblackl'

import unittest

from flask import json

from flaskApp import application


################################################################################
# SetUp Logging
################################################################################
import logging
import logging.handlers
LOGGER = logging.getLogger('tradlabs')
LOGGER.setLevel(logging.INFO)

# File Handler
H_FILE = logging.handlers.TimedRotatingFileHandler('C:\\TEMP\\api.log',
                                                   when='midnight', backupCount=5)
H_CONSOLE = logging.StreamHandler()

FORMATTER = logging.Formatter('%(asctime)s - %(lineno)3d:%(module)-10s-'
                              ' %(levelname)-8s- %(message)s')
H_FILE.setFormatter(FORMATTER)
H_CONSOLE.setFormatter(FORMATTER)

LOGGER.addHandler(H_FILE)
LOGGER.addHandler(H_CONSOLE)


class OtherItems(unittest.TestCase):
    """Universal Unit Tests for REST Service"""

    def test_health_app_pool(self):
        """Happy Path test of healthcheck, app pool"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/health')
            self.assertEqual(response.status_code, 200)

    def test_403(self):
        """Ensure un trapped error correctly reports out status and code"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/403')
            self.assertEqual(response.status_code, 403)
            self.assertEqual(json.loads(response.data)['code'], 'TLA-40301')

    def test_404(self):
        """Ensure un trapped error correctly reports out status and code"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/404')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(json.loads(response.data)['code'], 'TLA-40401')

    def test_500_prod(self):
        """Ensure un trapped error correctly reports out status and code"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/500')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(json.loads(response.data)['code'], 'TLA-50001')


# Allows to file to be run directly
if __name__ == '__main__':
    unittest.main()
