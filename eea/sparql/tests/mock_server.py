""" Mock http server for testing sparql"""

import BaseHTTPServer
import sys
import os

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ Mock http request handler"""
    
    def do_POST(self):
        """ On post return the contents of sparql.xml file"""
        self.send_response(200)
        self.send_header("Content-type", "application/sparql-results+json")
        self.end_headers()
        stdout = sys.stdout
        sys.stdout = self.wfile
        json_file = os.path.join(os.path.dirname(__file__),"sparql.xml")
        f = open(json_file, 'r')
        json_str = f.read()
        f.close()
        print json_str
        sys.stdout = stdout


if __name__ == "__main__":
    PORT = 8888
    httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
    httpd.serve_forever()
