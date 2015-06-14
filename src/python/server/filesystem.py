from pyftpdlib._compat import PY3, u, unicode, property
from pyftpdlib.filesystems import AbstractedFS
import os

class UserFS(AbstractedFS):
    def __init__(self, root, cmd_channel):
        """
         - (str) root: the user "real" home directory (e.g. '/home/user')
         - (instance) cmd_channel: the FTPHandler class instance
        """
        assert isinstance(root, unicode)
        # Set initial current working directory.
        # By default initial cwd is set to "/" to emulate a chroot jail.
        # If a different behavior is desired (e.g. initial cwd = root,
        # to reflect the real filesystem) users overriding this class
        # are responsible to set _cwd attribute as necessary.
        print 'File System mounted'
        self._cwd = u('/')
        self._root = self.set_jail(root, cmd_channel)
        self.cmd_channel = cmd_channel

    def set_jail(self, root, cmd_channel):
        username = cmd_channel.username
        jpath = os.path.join(root, username)
        if os.path.exists(jpath) is not True:
            os.makedirs(jpath)
        return jpath

    @property
    def cwd(self):
        """The user current working directory."""
        return self._cwd

    @cwd.setter
    def cwd(self, path):
        print 'Current Working DIR'
        assert isinstance(path, unicode), path
        self._cwd = path
