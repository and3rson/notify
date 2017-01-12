#!/usr/bin/env python2

import settings
from gevent import monkey, spawn, joinall
monkey.patch_all()
from ircclient import IRCClient
from handlers import MailPoller, APIServer


class NotifierClient(IRCClient):
    def on_connect(self):
        print 'Connected!'
        self.join(settings.CHAN)
        self.privmsg('general', 'I\'m here @andrew!')

    def on_message(self, message):
        print 'Got message:', message


def main():
    notifier = NotifierClient(settings.HOST, settings.PORT, settings.USER, settings.PASS)
    mail_poller = MailPoller(notifier)
    api_server = APIServer(notifier)
    try:
        joinall([
            spawn(notifier.start),
            spawn(mail_poller.start),
            spawn(api_server.start)
        ])
    except KeyboardInterrupt:
        notifier.stop()
        mail_poller.stop()
        api_server.stop()


if __name__ == '__main__':
    main()
