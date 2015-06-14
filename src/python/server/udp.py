from utils import get_settings
import SocketServer
import argparse

parser = argparse.ArgumentParser(description='Run an FTP server')
parser.add_argument('--settings', '-s', action='store',
                    help='Provide a json file config')

args = parser.parse_args()


class SimpleUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        self.receive(data, socket, self.client_address)
        print data

    def send(self, data):
        self.request[1].sendto(data, self.client_address)

    def receive(self, socket, data, client):
        ''' data from inbound '''
        pass


def main(path=None):
    config = get_settings(path or args.settings)
    HOST, PORT = "localhost", config.udp_port
    server = SocketServer.UDPServer((HOST, PORT), SimpleUDPHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
