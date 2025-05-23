from http.server import SimpleHTTPRequestHandler, HTTPServer


class RestHandler(SimpleHTTPRequestHandler):
    pass


def run(settings):
    server_settings = (
        settings['host'],
        int(settings['port']),
    )
    http_daemon = HTTPServer(server_settings, RestHandler)
    print(f'Starting server daemon on {server_settings[0]}:{server_settings[1]}...')
    http_daemon.serve_forever()