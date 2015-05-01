## base copied from internets
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import zmq
import zlib
import xml.etree.ElementTree as ET
import time
import csv

frameleft = 4.6725475
frameright = 5.1844415
frametop = 52.4917905
framebottom = 52.274690500000005

url = "tcp://vid.openov.nl:6701"
subscribe_string = "/TreinLocatieService/AllTreinLocaties"

infofile = open("info.csv")
ff = [it for it in csv.reader(infofile)]
infofile.close()

def getinfo(number):
    print(number)
    r = [[t,d] for [n,t,d] in ff if n == str(number)]
    if len(r) == 0:
        return "unknown"
    else:
        return r[0][0] + ":" + r[0][1]

def str_message(message):
    return zlib.decompress(message, zlib.MAX_WBITS|16)

def xml_message(message):
    return ET.fromstring(message)

def trainloc2arr(tl):
    """Given a TrainLocation element, extract the interesting data"""
    treinnummer = int(tl[0].text)
    lat = float(tl[1].find('{http://schemas.datacontract.org/2004/07/Cognos.Infrastructure.Models}Latitude').text)
    lon = float(tl[1].find('{http://schemas.datacontract.org/2004/07/Cognos.Infrastructure.Models}Longitude').text)
    return [getinfo(treinnummer), lat, lon]

def getCurrentDat():
    """Quick adjustment of get_messages_while from getdata"""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(url)
    socket.setsockopt(zmq.SUBSCRIBE, subscribe_string)

    messages = []
    while len(messages) == 0:
        m = socket.recv()
        if m != subscribe_string:
            messages.append(str_message(m) + "\n")

    socket.close()

    message = xml_message(messages[0])

    return [trainloc2arr(it) for it in message.getchildren()]

def filterCurrentDat(dat):
    return [it for it in dat if it[1] < frametop and it[1] > framebottom and it[2] > frameleft and it[2] < frameright]

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type',	'text/html')
        self.end_headers()
        headfile = open("mappagehead.html")
        footfile = open("mappagefoot.html")

        for line in headfile.readlines():
            self.wfile.write(line)

        dat = [[b, c, a] for [a,b,c] in filterCurrentDat(getCurrentDat())]
        s = "<script> var locdata = " + str(dat[1:10]) + ";</script>"
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

