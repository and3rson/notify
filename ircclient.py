import socket
from select import select
from time import sleep


class IRCClient(object):
    def __init__(self, server, port, username, password):
        # super(Client, self).__init__()

        self.server = server
        self.port = port
        self.username = username
        self.password = password

        self.alive = False

    def send(self, message):
        self.conn.send(message + '\r\n')

    def start(self):
        self.alive = True
        while self.alive:
            while not self.connect():
                pass
            self.process()

    def process(self):
        while self.alive:
            i, o, e = select([self.conn], [], [], 1)
            if self.conn in i:
                data = filter(None, self.conn.recv(1024).split('\r\n'))
                if not len(data):
                    return
                for line in data:
                    self.on_recv(line)

    def connect(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.server, self.port))

            self.send('NICK {}'.format(self.username))
            self.send('PASS {}'.format(self.password))
            self.send('USER {u} {u} {u} NotifyClient {u}'.format(u=self.username))

            self.alive = True
        except:
            sleep(1)
            return False
        return True

    def on_recv(self, line):
        parts = line.split(' ')
        if parts[0].lower() == 'ping':
            self.send('PONG {}'.format(parts[1]))
        elif parts[1] == '001':
            self.on_connect()
        else:
            self.on_message(line)

    def on_message(self, line):
        raise NotImplementedError()

    def join(self, channel):
        self.send('JOIN #{}'.format(channel))

    def privmsg(self, channel, message):
        self.send('PRIVMSG #{} {}'.format(channel, message))

    def stop(self):
        self.alive = False
        print 'See ya!'
        self.send('QUIT')
