__author__ = 'sfblackl'

import unittest

from app import application


class OtherItems(unittest.TestCase):
    def test_health_app_pool(self):
        with application.test_client(self) as c:
            response = c.get('/tradlabs/v1/health')
            self.assertEqual(response.status_code, 200)


# Allows to file to be run directly
if __name__ == '__main__':
    unittest.main()
