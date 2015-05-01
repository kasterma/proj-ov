## base copied from internets
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type',	'text/html')
        self.end_headers()
        headfile = open("mappagehead.html")
        footfile = open("mappagefoot.html")

        for line in headfile.readlines():
            self.wfile.write(line)

        s = "<script> var locdata = [[52.395380, 4.844216, \"label1\"], [52.461260, 5.053292, \"hi\"]];</script>"
        self.wfile.write(s)

        for line in footfile.readlines():
            self.wfile.write(line)

        headfile.close()
        footfile.close()
        return

def main():
    try:
        server = HTTPServer(('', 8080), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

