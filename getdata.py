## connect to sockets and save data and info
##
## data: location data of trains
## info: enrichment of this location data

import zmq
import zlib
import xml.etree.ElementTree as ET
import time

url_dat = "tcp://vid.openov.nl:6701"
subscribe_string_dat = "/TreinLocatieService/AllTreinLocaties"
outfilename_dat = "fridayrun.ovdat"

url_info = "tcp://do.u0d.de:7660"
subscribe_string_info = "/RIG/InfoPlusDVSInterface"
outfilename_info = "fridayrun.ovinfo"

def str_message(message):
    return zlib.decompress(message, zlib.MAX_WBITS|16)

def xml_message(message):
    return ET.fromstring(str_message(message))

def get_messages_while(while_pred, url, subscribe_string):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(url)
    socket.setsockopt(zmq.SUBSCRIBE, subscribe_string)

    messages = []
    while while_pred():
        m = socket.recv()
        if m != subscribe_string:
            messages.append(str_message(m) + "\n")
            print("message")

    socket.close()

    return messages

def make_while_pred(mins):
    time_now = time.time()
    time_until = time_now + 60 * mins

    def pred():
        return time.time() < time_until

    return pred

def get_messages(mins, basefilename, url, subscribe_string):
    messages = get_messages_while(make_while_pred(mins), url, subscribe_string)
    outfile = open(time.strftime("%Y-%m-%d-%H-%M", time.gmtime(time.time())) + basefilename, "w")
    outfile.writelines(messages)
    outfile.close()

def get_dat():
    while True:
        print(time.strftime("%Y-%m-%d-%H-%M", time.gmtime(time.time())))
        get_messages(30, outfilename_dat, url_dat, subscribe_string_dat)

def get_info():
    while True:
        print(time.strftime("%Y-%m-%d-%H-%M", time.gmtime(time.time())))
        get_messages(30, outfilename_info, url_info, subscribe_string_info)



# <TreinLocation xmlns:ns0="http://schemas.datacontract.org/2004/07/Cognos.Infrastructure.Models">
#   <ns0:TreinNummer>6324</ns0:TreinNummer>
#   <ns0:TreinMaterieelDelen>
#     <ns0:MaterieelDeelNummer>2412</ns0:MaterieelDeelNummer>
#     <ns0:Materieelvolgnummer>1</ns0:Materieelvolgnummer>
#     <ns0:GeneratieTijd>1429864812</ns0:GeneratieTijd>
#     <ns0:GpsDatumTijd>2015-04-24T08:40:12</ns0:GpsDatumTijd>
#     <ns0:Orientatie>0</ns0:Orientatie>
#     <ns0:BronId>3159</ns0:BronId>
#     <ns0:Bron>2</ns0:Bron>
#     <ns0:Fix>1</ns0:Fix>
#     <ns0:Berichttype>1</ns0:Berichttype>
#     <ns0:Longitude>4.4565733304741</ns0:Longitude>
#     <ns0:Latitude>52.147186465672</ns0:Latitude>
#     <ns0:Snelheid>0</ns0:Snelheid>
#     <ns0:Richting>0</ns0:Richting>
#     <ns0:Rijrichting>0</ns0:Rijrichting>
#     <ns0:Hdop>1.2</ns0:Hdop>
#     <ns0:AantalSatelieten>0</ns0:AantalSatelieten>
#   </ns0:TreinMaterieelDelen>
# </TreinLocation>
