from server.ftp import get_settings, make_server, make_handler, \
    make_authorizer, make_throttle, make_filesystem, setup_handler, \
    make_basedir, force_config, create_ftp, get_address, ThreadFTP

from server.filesystem import UserFS
from server.server import AppFTPHandler

from pyftpdlib._compat import getcwdu
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import ThrottledDTPHandler
from pyftpdlib.servers import FTPServer

import unittest
import collections
import os
import shutil

compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

TEST_ROOT = './_test_root'

class TestFTPMethods(unittest.TestCase):

    def setUp(self):
        self.config = get_settings('config.json')
        self.config.basedir = getcwdu()
        h = make_handler(self.config)
        address = (self.config.listen_ip, self.config.listen_port)
        self.server = make_server(address, h, self.config)

    def tearDown(self):
        self.server.close_all()

    def test_make_server(self):
        '''
        make_server created a ready server passing correct address
        '''
        c = self.config
        server = self.server
        address = (c.listen_ip, c.listen_port)
        self.assertIsInstance(server, FTPServer)
        self.assertEqual(server.address, address)
        server.close()
        server.close_all()

    def test_make_authorizer(self):
        '''
        make_authorizer returns a ready Authroizer class.
        '''
        c = self.config
        a = make_authorizer(c)
        for user in c.users:
            self.assertTrue(a.has_user(user))
        self.assertIsInstance(a, DummyAuthorizer)

    def test_make_trottle(self):
        '''
        make_throttle returns a ThrottledDTPHandler class
        '''
        c = self.config
        t = make_throttle(c)
        self.assertEqual(t.write_limit, c.write_throttle)
        self.assertEqual(t.read_limit, c.read_throttle)
        self.assertEqual(t, ThrottledDTPHandler)

    def test_make_filsystem(self):
        '''
        make_filesystem returns a UserFS class
        '''
        c = self.config
        fs = make_filesystem(c)
        self.assertEqual(fs, UserFS)

    def test_make_basedir(self):
        '''
        make_basedir methods should create a folder for the incoming files
        '''
        c = self.config
        bp = c.basedir
        # change to test
        c.basedir = './_test_dir'
        made = make_basedir(c)
        self.assertTrue(made)
        self.assertTrue(os.path.exists(c.basedir))
        if made:
            # cleanup
            shutil.rmtree(c.basedir)
        # reset
        c.basedir = bp

    def test_make_handler(self):
        '''
        make_handler returns a AppFTPHandler class
        '''
        c = self.config
        h = make_handler(c)

        self.assertEqual(h, AppFTPHandler)

    def test_get_settings(self):
        '''
        check the config file is loaded through get_settings function
        inherited from utils
        '''
        c = self.config
        self.assertIsNotNone(c)
        self.assertEqual(c.version, "0.1")

    def test_force_config(self):
        '''
        get config or exit
        '''
        with self.assertRaises(SystemExit) as cm:
            force_config('badname.json')

        self.assertEqual(cm.exception.code, 1)

    def test_set_config_users(self):
        '''
        Check users are added to FTP handler correctly from config.json
        '''
        c = self.config
        h = setup_handler(c)
        cusers = [x for x in c.users]
        hnames = [x for x in h.authorizer.user_table]
        print cusers, hnames
        self.assertTrue(compare(cusers, hnames))

    def test_get_address(self):
        self.config.listen_ip = 'localhost'
        self.config.listen_port = 0
        addr = get_address(self.config)
        self.assertEqual(addr[0], self.config.listen_ip)
        self.assertEqual(addr[1], self.config.listen_port)

    def test_create_ftp(self):
        self.server.close_all()
        server = create_ftp('config.json')
        self.assertEqual(server.addr[0], self.config.listen_ip)
        self.assertEqual(server.addr[1], self.config.listen_port)
        server.close_all()
        self.setUp()


class TestThreadFTP(unittest.TestCase):

    def setUp(self):
        self.config = get_settings('config.json')
        self.config.basedir = getcwdu()

        self.ftp = ThreadFTP('config.json')

    def tearDown(self):
        self.ftp.close()
        if self.ftp.running is True:
            self.ftp.stop()

        # delete test folder
        if os.path.exists(TEST_ROOT):
            shutil.rmtree(TEST_ROOT)

    def test_ftp_config(self):
        '''
        ThreadFTP should accept string or object config
        '''
        self.ftp.server.close_all()
        self.ftp = ThreadFTP('config.json')
        self.assertEqual(self.ftp.config.version, '0.1')

        self.ftp.server.close_all()
        self.ftp = ThreadFTP(self.config)
        self.assertEqual(self.ftp.config.version,'0.1')

    def test_create_config(self):
        '''
        Create a new ready instance of a thread FTP
        '''
        t = self.ftp
        c = self.config
        self.assertEqual(t.host, c.listen_ip)
        self.assertEqual(t.port, c.listen_port)

    def test_running(self):
        '''
        running value should flag False and True from stop() start() routine
        '''
        t = self.ftp
        self.assertEqual(t.running, False)
        t.start()

        # from nose.tools import set_trace; set_trace()
        self.assertEqual(t.running, True)
        t.stop()
        self.assertEqual(t.running, False)

    def test_make_root(self):
        '''
        ThreadFTP will make a root in the basedir location
        '''
        bp = self.config.basedir
        self.config.basedir = TEST_ROOT
        self.ftp.close()
        self.ftp = ThreadFTP(self.config)
        if self.ftp.running is False:
            self.ftp.start()
        self.assertTrue(os.path.exists(self.config.basedir))



if __name__ == '__main__':
    unittest.main()
