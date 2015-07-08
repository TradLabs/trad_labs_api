#!/usr/bin/python3
"""Collection of Unit Tests for Application """
__author__ = 'sfblackl'

import unittest

import flask.json

from flaskApp import application
import log_setup

log_setup.start_log()


class OtherItems(unittest.TestCase):
    """Universal Unit Tests for REST Service"""

    def test_health_app_pool(self):
        """Happy Path test of health check, app pool"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/health')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(flask.json.loads(response.data)['currentSetting'], 'ci')
            self.assertEqual(flask.json.loads(response.data)['detail'], 'app_pool')

    def test_health_bad_detail(self):
        """Validation that bad detail_level handled correctly"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/health?detail_level=blah')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(flask.json.loads(response.data)['detail'], 'app_pool')

    def test_health_sla(self):
        """Happy Path test of health check sla"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/health?detail_level=sla')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(flask.json.loads(response.data)['detail'], 'sla')

    def test_403(self):
        """Ensure un trapped error correctly reports out status and code"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/403')
            self.assertEqual(response.status_code, 403)
            self.assertEqual(flask.json.loads(response.data)['code'], '403')

    def test_404(self):
        """Ensure un trapped error correctly reports out status and code"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/404')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(flask.json.loads(response.data)['code'], '404')

    def test_500_prod(self):
        """Ensure un trapped error correctly reports out status and code"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/500')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(flask.json.loads(response.data)['code'], '500_01')


class Random(unittest.TestCase):
    """
        Test the DB to hell.  Ok, limited amounts
    """

    def test_db_query(self):
        """Basic Test of db"""
        with application.test_client(self) as tc1:
            response = tc1.get('/tradlabs/v1/test/db')
            self.assertEqual(response.status_code, 200)

# Allows to file to be run directly
if __name__ == '__main__':
    unittest.main()
