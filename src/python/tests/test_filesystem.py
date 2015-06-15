from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib._compat import getcwdu
from pyftpdlib.handlers import (FTPHandler, DTPHandler, ThrottledDTPHandler,
                                SUPPORTS_HYBRID_IPV6)

from server.ftp import get_settings, make_server, make_handler, \
    make_authorizer, make_throttle, make_filesystem, setup_handler, \
    make_basedir, force_config, create_ftp, get_address, ThreadFTP

from ftplib import FTP
from server.filesystem import UserFS
from server.server import AppFTPHandler

import socket
import unittest
import collections
import os
import shutil

# Attempt to use IP rather than hostname (test suite will run a lot faster)
try:
    HOST = socket.gethostbyname('localhost')
except socket.error:
    HOST = 'localhost'

USER = 'user'
PASSWD = 'pass'
HOME = getcwdu()
TESTFN = 'tmp-pyftpdlib'
TESTFN_UNICODE = TESTFN + '-unicode-' + '\xe2\x98\x83'
TESTFN_UNICODE_2 = TESTFN_UNICODE + '-2'
TIMEOUT = 2
BUFSIZE = 1024
INTERRUPTED_TRANSF_SIZE = 32768
NO_RETRIES = 5


compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

TEST_ROOT = './_test_root'


class TestFilesystem(unittest.TestCase):

    def setUp(self):
        self.config = get_settings('config.json')
        self.config.basedir = './_test_root'
        self.ftp = ThreadFTP(self.config)
        self.ftp.start()
        self.client = FTP()
        self.client.connect(self.config.listen_ip, self.config.listen_port)
        self.client.sock.settimeout(TIMEOUT)
        self.client.login(USER, PASSWD)

        if self.ftp.running is False:
            self.ftp.start()

    def tearDown(self):
        self.ftp.close()
        self.client.close()

        if self.ftp.running is True:
            self.ftp.stop()

        # delete test folder
        if os.path.exists(TEST_ROOT):
            shutil.rmtree(TEST_ROOT)

    def test_make_root(self):
        '''
        ThreadFTP will make a root in the basedir location
        '''
        self.assertTrue(os.path.exists(self.config.basedir))

    def test_send_file(self):
        '''
        can upload file through natural FTP
        '''
        filename = 'config.json'
        tfile = open(filename, 'r')
        self.client.storlines("STOR " + filename, tfile)
        tfile.close()
        up = os.path.join(self.config.basedir, USER, filename)
        self.assertTrue(os.path.exists(up))

if __name__ == '__main__':
    unittest.main()
