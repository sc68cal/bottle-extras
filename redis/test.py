import unittest
import os
import bottle
from bottle.ext import redis as redis_plugin
import redis

class RedisTest(unittest.TestCase):
    def setUp(self):
        self.app = bottle.Bottle(catchall=False)

    def test_with_keyword(self):
        self.plugin = self.app.install(redis_plugin.Plugin())

        @self.app.get('/')
        def test(rdb):
            self.assertEqual(type(rdb), type(redis.client.Redis()))
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

    def test_without_keyword(self):
        self.plugin = self.app.install(redis_plugin.Plugin())

        @self.app.get('/')
        def test():
            pass
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

        @self.app.get('/2')
        def test(**kw):
            self.assertFalse('rdb' in kw)
        self.app({'PATH_INFO':'/2', 'REQUEST_METHOD':'GET'}, lambda x, y: None)
        
if __name__ == '__main__':
    unittest.main()
