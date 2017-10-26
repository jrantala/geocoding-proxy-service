#!/usr/bin/env python

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
import latlon_fetch
import settings

PORT = settings.PORT

if __name__ == "__main__":
    try:
        import argparse

        parser = argparse.ArgumentParser(description='tiny server that implements GET')
        parser.add_argument('-p', '--port', type=int, dest="PORT",
                           help='the port the server will run on - defaults to 8003')

        args = parser.parse_args()

        if args.PORT:
            PORT = args.PORT

    except Exception:
        # argparse error: use default port of 8003
        pass


class JSONRequestHandler (BaseHTTPRequestHandler):

    def do_GET(self):

        # /foo/address?addr=16886+fenton+48219
        # ignore ...addr=
        raw_addr = self.path
        mark_1 = raw_addr.find('addr=') 
        mark_2 = mark_1 + len('addr=')
        addr = raw_addr[mark_2:]

        if mark_1 == -1:
            # address parsing error
            self.send_response(500)
            # send headers:
            self.send_header("Content-type", "application/json")
            # send a blank line to end headers:
            self.wfile.write("\r\n")

            json_500 = {"errors":[
                {
                    "status": "500",
                    "title": "Address parsing error",
                    "detail": "missing addr parameter"
                }]}

            self.wfile.write(json.dumps(json_500))

        else: # address parsed successfully
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.wfile.write("\r\n")
            
            llf = latlon_fetch.LatLonFetch()

            # test failover
            # llf.force_error('GOOGLE')

            latlon = llf.fetch_with_backup(addr)

            latlon_json = '{"data":[{"coordinates": ' + str(latlon) + '}]}'
            latlon_json = latlon_json.replace("'", '"').replace('u"', '"')

            self.wfile.write(latlon_json)


server = HTTPServer(("localhost", PORT), JSONRequestHandler)
server.serve_forever()
