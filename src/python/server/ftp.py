from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer

from server import AppFTPHandler
from filesystem import UserFS
from utils import get_settings

import os
import argparse

parser = argparse.ArgumentParser(description='Run an FTP server')
parser.add_argument('--settings', '-s', action='store',
                    help='Provide a json file config')

args = parser.parse_args()

def make_server(address, handler, config=None):
    server = FTPServer(address, handler)

    if config is not None:
        # set a limit for connections
        server.max_cons = config.max_connections
        server.max_cons_per_ip = config.max_user_connections

    return server


def make_authorizer(config):
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    for user in config.users:
        authorizer.add_user(user, config.users[user], '.', perm='elradfmwM')
    # authorizer.add_anonymous(os.getcwd())
    return authorizer


def make_throttle(config):
    dtp = ThrottledDTPHandler
    dtp.read_limit = config.read_throttle
    dtp.write_limit = config.write_throttle
    return dtp


def make_filesystem(config):
    return UserFS


def make_handler(config):
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


def main(path=None):
    config_path = path or args.settings
    if config_path is None:
        print '-s config file is required'
        exit()
    
    config = get_settings(config_path)
    if config is None:
        print 'bad config file "%s"' % (config_path,)
        exit()
    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    # handler.masquerade_address = '151.25.42.11'
    # handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = (config.listen_ip, config.listen_port)
    handler = setup_handler(config)
    server = make_server(address, handler)
    # start ftp server
    run(server)


def run(server):
    try:
        server.serve_forever()
        shutdown()
    except (KeyboardInterrupt, SystemExit):
        shutdown()
        raise
    except:
        shutdown()


def shutdown():
    print 'Shutdown FTP'

if __name__ == '__main__':
    main()
