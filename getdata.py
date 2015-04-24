## connect to sockets and save data

import zmq
import zlib
import xml.etree.ElementTree as ET
import time

url = "tcp://vid.openov.nl:6701"
subscribe_string = "/TreinLocatieService/AllTreinLocaties"
outfilename = "fridayrun.ovdat"

def str_message(message):
    return zlib.decompress(message, zlib.MAX_WBITS|16)

def xml_message(message):
    return ET.fromstring(str_message(message))

def get_messages(while_pred):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(url)
    socket.setsockopt(zmq.SUBSCRIBE, subscribe_string)

    messages = []
    while while_pred():
        m = socket.recv()
        if m != '/TreinLocatieService/AllTreinLocaties':
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

def get_30min_messages(basefilename):
    messages = get_messages(make_while_pred(30))
    outfile = open(time.strftime("%Y-%m-%d-%H-%M", time.gmtime(time.time())) + basefilename, "w")
    outfile.writelines(messages)
    outfile.close()


def main():
    while True:
        print(time.strftime("%Y-%m-%d-%H-%M", time.gmtime(time.time())))
        get_30min_messages(outfilename)

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
