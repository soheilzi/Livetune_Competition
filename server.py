from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import argparse

target_port = 0

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Default file if request is root
        if self.path == '/':
            self.path = '/index.html'
        
        try:
            # Extract file extension
            _, ext = os.path.splitext(self.path)

            # Determine content type
            if ext in [".html", ".htm"]:
                content_type = "text/html"
            elif ext == ".css":
                content_type = "text/css"
            else:
                content_type = "text/plain"  # default

            # Open and serve the file
            with open(self.path[1:], 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)

        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')

    def do_POST(self):
        # Get the size of data
        content_length = int(self.headers['Content-Length'])
        # Read the data
        post_data = self.rfile.read(content_length)
        # Parse the data
        fields = urllib.parse.parse_qs(post_data.decode())
        print(f"Received port: {target_port}, tag: {fields.get('tag', [''])[0]}, value: {fields.get('value', [''])[0]}")
        os.system(f"tune -p {target_port} -t {fields.get('tag', [''])[0]} -v {fields.get('value', [''])[0]}")
        # Redirect back to form
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on http://localhost:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LiveTune server')
    parser.add_argument('--port', type=int, default=8000, help='port for liveTune server (default: 8000)')
    parser.add_argument('--port-target', type=int, default=8001, help='port for target server (default: 8001)')
    args = parser.parse_args()
    target_port = args.port_target
    run(port=args.port)
