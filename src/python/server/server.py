from pyftpdlib.handlers import FTPHandler
from udp import SimpleUDPHandler


class AppUDPHandler(SimpleUDPHandler):

    def receive(self, socket, data, client):
        pass


class AppFTPHandler(FTPHandler):

    def on_connect(self):
        print "%s:%s connected" % (self.remote_ip, self.remote_port)
        
    def on_disconnect(self):
        # do something when client disconnects
        print 'on_disconnect'

    def on_login(self, username):
        # do something when user login
        print 'on_login', username

    def on_logout(self, username):
        # do something when user logs out
        print 'on_logout', username

    def on_file_sent(self, file):
        # do something when a file has been sent
        print 'on_file_sent', file

    def on_file_received(self, file):
        # do something when a file has been received
        print 'on_file_received', file

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        print 'on_incomplete_file_sent', file

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        import os
        os.remove(file)
