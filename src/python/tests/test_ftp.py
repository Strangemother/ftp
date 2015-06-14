from pyftpdlib.authorizers import DummyAuthorizer
import unittest
from server.ftp import get_settings, make_server, make_handler, \
    make_authorizer, make_throttle, make_filesystem

from server.filesystem import UserFS
from server.server import AppFTPHandler
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import collections


class TestFTPMethods(unittest.TestCase):

    def test_get_settings(self):
        '''
        check the config file is loaded through get_settings function
        inherited from utils
        '''
        c = get_settings('config.json')
        self.assertIsNotNone(c)
        self.assertEqual(c.version, "0.1")

    def test_make_server(self):
        '''
        make_server creared a ready server passing correct address
        '''
        c = get_settings('config.json')
        h = make_handler(c)
        address = (c.listen_ip, c.listen_port)
        server = make_server(address, h, c)
        self.assertIsInstance(server, FTPServer)
        self.assertEqual(server.address, address)

    def test_make_authorizer(self):
        '''
        make_authorizer returns a ready Authroizer class.
        '''
        c = get_settings('config.json')
        a = make_authorizer(c)
        for user in c.users:
            self.assertTrue(a.has_user(user))
        self.assertIsInstance(a, DummyAuthorizer)

    def test_make_filsystem(self):
        '''
        make_filesystem returns a UserFS class
        '''
        c = get_settings('config.json')
        fs = make_filesystem(c)
        self.assertEqual(fs, UserFS)

    def test_make_trottle(self):
        '''
        make_throttle returns a ThrottledDTPHandler class
        '''
        c = get_settings('config.json')
        t = make_throttle(c)
        self.assertEqual(t.write_limit, c.write_throttle)
        self.assertEqual(t.read_limit, c.read_throttle)
        self.assertEqual(t, ThrottledDTPHandler)

    def test_make_handler(self):
        '''
        make_handler returns a AppFTPHandler class
        '''
        c = get_settings('config.json')
        h = make_handler(c)

        self.assertEqual(h, AppFTPHandler)

    def test_set_config_users(self):
        '''
        Check users are added to FTP handler correctly from 
        config.json
        '''
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        c = get_settings('config.json')
        h = make_handler(c)
        cusers = [x for x in c.users]
        hnames = [x for x in h.authorizer.user_table]
        self.assertTrue( compare(cusers, hnames) )

if __name__ == '__main__':
    unittest.main()
