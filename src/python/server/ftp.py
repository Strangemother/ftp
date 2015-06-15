from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import ThrottledDTPHandler
from pyftpdlib.servers import FTPServer

from server import AppFTPHandler
from filesystem import UserFS
from utils import get_settings

import argparse
import os
import threading

parser = argparse.ArgumentParser(description='Run an FTP server')
parser.add_argument('--settings', '-s', action='store',
                    help='Provide a json file config')



def make_server(address, handler, config=None):
    '''
    build a server entity and pass config setup
    '''
    print 'Making Server', address
    server = FTPServer(address, handler)

    if config is not None:
        # set a limit for connections
        server.max_cons = config.max_connections
        server.max_cons_per_ip = config.max_user_connections

    return server


def make_authorizer(config):
    '''
    Returns an authorizer class and mounts user configs.
    '''
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    for user in config.users:
        authorizer.add_user(user, config.users[user], config.basedir,
                            perm='elradfmwM')
    # authorizer.add_anonymous(os.getcwd())
    return authorizer


def make_throttle(config):
    '''
    Returns a readied ThrottledDTPHandler class
    '''
    dtp = ThrottledDTPHandler
    dtp.read_limit = config.read_throttle
    dtp.write_limit = config.write_throttle
    return dtp


def make_filesystem(config):
    '''
    Returns a UserFS class
    '''
    UserFS.config = config
    return UserFS


def make_basedir(config):
    '''
    Make the basedir for the inbound FTP client files
    '''
    if os.path.exists(config.basedir) is not True:
        os.makedirs(config.basedir)
    return os.path.exists(config.basedir)


def make_handler(config):
    make_basedir(config)
    return AppFTPHandler


def setup_handler(config, handler=None):

    # Instantiate FTP handler class
    handler = handler or make_handler(config)
    handler.authorizer = make_authorizer(config)
    handler.dtp_handler = make_throttle(config)
    handler.abstracted_fs = make_filesystem(config)
    # Define a customized banner (string returned when client connects)
    handler.banner = config.banner
    return handler


def force_config(path):
    '''
    get a config file and result object or force exit the app
    '''
    if path is None:
        print '-s config file is required'
        exit(1)

    config = get_settings(path)
    if config is None:
        print 'bad config file "%s"' % (path,)
        exit(1)
    return config


def get_address(config):
    '''
    return a address, port tuple
    '''
    addr = (config.listen_ip, config.listen_port)
    return addr


def create_ftp(config_path):
    '''
    Create a server class based upon the config provided.
    The return server class should be run(server)
    '''

    config = force_config(config_path)
    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    # handler.masquerade_address = '151.25.42.11'
    # handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = get_address(config)
    handler = setup_handler(config)
    server = make_server(address, handler, config)
    # start ftp server
    return server


def main(path=None):
    server = create_ftp(path)
    run(server)


def run(server):
    try:
        server.serve_forever()
        shutdown(server)
    except (KeyboardInterrupt, SystemExit):
        shutdown(server)
        raise
    except:
        shutdown(server)


def shutdown(server):
    print 'Shutdown FTP'


class ThreadFTP(threading.Thread):
    """A threaded FTP server used for running tests.
    This is basically a modified version of the FTPServer class which
    wraps the polling loop into a thread.
    The instance returned can be used to start(), stop() and
    eventually re-start() the server.
    """
    handler = AppFTPHandler
    server_class = FTPServer

    def __init__(self, config=None):
        '''
        Start a threaded FTP server, with server classes already applied.
        pass address tuple (HOST,PORT,) and config util object.
        '''
        threading.Thread.__init__(self)
        self.__serving = False
        self.__stopped = False
        self.__lock = threading.Lock()
        self.__flag = threading.Event()
        if isinstance(config, (str, unicode,)):
            self.config = force_config(config)
        else:
            self.config = config

        addr = get_address(self.config)
        self.handler = setup_handler(self.config)
        # authorizer = DummyAuthorizer()
        # # full perms
        # authorizer.add_user(USER, PASSWD, HOME, perm='elradfmwM')
        # self.handler.authorizer = authorizer
        # lower buffer sizes = more "loops" while transfering data
        # = less false positives
        # self.handler.dtp_handler.ac_in_buffer_size = 4096
        # self.handler.dtp_handler.ac_out_buffer_size = 4096
        self.server = make_server(addr, self.handler, self.config)
        self.host, self.port = self.server.socket.getsockname()[:2]

    def __repr__(self):
        status = [self.__class__.__module__ + "." + self.__class__.__name__]
        if self.__serving:
            status.append('active')
        else:
            status.append('inactive')
        status.append('%s:%s' % self.server.socket.getsockname()[:2])
        return '<%s at %#x>' % (' '.join(status), id(self))

    def close(self):
        '''
        Close the server connection releasing the port
        '''
        self.server.close_all()

    @property
    def running(self):
        return self.__serving

    def start(self, timeout=0.001):
        """Start serving until an explicit stop() request.
        Polls for shutdown every 'timeout' seconds.
        """
        if self.__serving:
            raise RuntimeError("Server already started")
        if self.__stopped:
            # ensure the server can be started again
            ThreadFTP.__init__(self, self.server.socket.getsockname(),
                               self.handler)
        self.__timeout = timeout
        threading.Thread.start(self)
        self.__flag.wait()

    def run(self):
        self.__serving = True
        self.__flag.set()
        while self.__serving:
            self.__lock.acquire()
            self.server.serve_forever(timeout=self.__timeout, blocking=False)
            self.__lock.release()
        self.server.close_all()


    def stop(self):
        """Stop serving (also disconnecting all currently connected
        clients) by telling the serve_forever() loop to stop and
        waits until it does.
        """
        self.close()
        if not self.__serving:
            raise RuntimeError("Server not started yet")
        self.__serving = False
        self.__stopped = True
        self.join(timeout=3)
        shutdown(self.server)
        if threading.activeCount() > 1:
            print "test FTP server thread is still running"


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.settings)
