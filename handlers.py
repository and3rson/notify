import settings
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class MailPoller(object):
    def __init__(self, notifier):
        self.notifier = notifier

    def start(self):
        pass

    def stop(self):
        pass


class APIServer(object):
    def make_request_handler(self, ref):
        class APIRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                path, _, query = self.path.partition('?')
                if path.strip('/') == 'api/notify':
                    body = self.rfile.read().strip()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write('{"success": true}')
                    ref.notifier.privmsg(settings.CHAN, '{}: {}'.format(settings.MENTION, body))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write('{"success": false, "message": "Not found"}')
        return APIRequestHandler

    def __init__(self, notifier):
        self.notifier = notifier
        self.alive = True

    def start(self):
        self.server = HTTPServer(('', 11022), self.make_request_handler(self))
        self.server.serve_forever(1)

    def stop(self):
        self.server.shutdown()
