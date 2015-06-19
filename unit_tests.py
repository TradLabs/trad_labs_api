#!/usr/bin/python3
"""Collection of Unit Tests for Application """
# __author__ = 'sfblackl'

import unittest

from flask import json

from flaskApp import application


class OtherItems(unittest.TestCase):
    """Universal Unit Tests for REST Service"""

    def test_health_app_pool(self):
        """Happy Path test of healthcheck, app pool"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/health')
            self.assertEqual(response.status_code, 200)

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
