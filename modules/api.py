from http.server import SimpleHTTPRequestHandler, HTTPServer
from json import dumps, loads


class RestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        response = { 'description': 'REST API for Bot War' }
        if self.path == '/start':
            post_data_dict = loads(post_data)
            response = {
                'description': 'Starting bot war game...',
                'players': len(post_data_dict['players']),
            }
            
            
        self.create_response(response)
        
        
    def create_response(self, response):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(dumps(response))))
        self.end_headers()
        self.wfile.write(str(response).encode('utf-8'))


def run(settings):
    server_settings = (
        settings['host'],
        int(settings['port']),
    )
    http_daemon = HTTPServer(server_settings, RestHandler)
    print(f'Starting server daemon on {server_settings[0]}:{server_settings[1]}...')
    http_daemon.serve_forever()