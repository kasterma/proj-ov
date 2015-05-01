## convert data to csv selecting the bits I need

import xml.etree.ElementTree as ET
import csv
import datetime

def xml_message(message):
    return ET.fromstring(message)

def getparsedlines(filename):
    """Read in the file and parse every line to xml.element"""
    infile = open(filename)
    lines = infile.readlines()
    infile.close()
    xmls = [xml_message(line) for line in lines]
    return xmls

def elts2arrs(elt):
    """Given ArrayOfTreinLocation xml.element create array of relevant data"""
    trainloc_elts = elt.getchildren()
    trainloc_arrs = [trainloc2arr(it) for it in trainloc_elts]
    return [trainloc for trainloc in trainloc_arrs if trainloc[3] != "MISSING"]

def trainloc2arr(tl):
    """Given a TrainLocation element, extract the interesting data"""
    treinnummer = int(tl[0].text)
    lat = float(tl[1].find('{http://schemas.datacontract.org/2004/07/Cognos.Infrastructure.Models}Latitude').text)
    lon = float(tl[1].find('{http://schemas.datacontract.org/2004/07/Cognos.Infrastructure.Models}Longitude').text)
    try:
        tijd = datetime.datetime.strptime(tl[1].find('{http://schemas.datacontract.org/2004/07/Cognos.Infrastructure.Models}GpsDatumTijd').text, "%Y-%m-%dT%H:%M:%S")
        hour = tijd.hour
        minute = tijd.minute
    except:
        hour = "MISSING"
        minute = "MISSING"
    return [treinnummer, lat, lon, hour, minute]

def flatten(xs):
    """Probably exists as standard python function, but easier to write than to find"""
    y = []
    for x in xs:
        y.extend(x)
    return y

def writecsv(csvdat, filename):
    outfile = open(filename, "w")
    wr = csv.writer(outfile)
    wr.writerows(csvdat)
    outfile.close()

def dat2csv(infilename, csvfilename):
    """Convert the output from the api to a csv file"""
    dat = getparsedlines(infilename)
    csvdat = [elts2arrs(its) for its in dat]  ## since an infile contains a list of outputs from the apit iterate over the list
    writecsv(flatten(csvdat), csvfilename)

ovdatFiles = ["2015-04-24-11-13fridayrun",
              "2015-04-24-15-14fridayrun",
              "2015-04-24-11-43fridayrun",
              "2015-04-24-15-44fridayrun",
              "2015-04-24-12-13fridayrun",
              "2015-04-24-16-14fridayrun",
              "2015-04-24-12-43fridayrun",
              "2015-04-24-16-44fridayrun",
              "2015-04-24-13-13fridayrun",
              "2015-04-24-17-14fridayrun",
              "2015-04-24-13-43fridayrun",
              "2015-04-24-17-44fridayrun",
              "2015-04-24-14-14fridayrun",
              "2015-04-24-18-15fridayrun",
              "2015-04-24-14-44fridayrun"]

def main():
    for name in ovdatFiles:
        print(name)
        dat2csv("rawdata/" + name + ".ovdat", name + ".csv")

#if __name__ == '__main__':
#    main()


