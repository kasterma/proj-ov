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

def line2arr(xmlline):
    """Given a PutReisInformatieBoodschapIn xml.element generate array of the relevant data

    Clearly needs to be unhacked."""
    try:
        tijd = datetime.datetime.strptime(xmlline.getchildren()[0].getchildren()[0].getchildren()[2].text, "%Y-%m-%dT%H:%M:%SZ")
        hour = tijd.hour
        minute = tijd.minute
        assert xmlline.getchildren()[0].getchildren()[1].getchildren()[3].getchildren()[0].tag == "{urn:ndov:cdm:trein:reisinformatie:data:2}TreinNummer"
        treinnummer = int(xmlline.getchildren()[0].getchildren()[1].getchildren()[3].getchildren()[0].text)
        assert xmlline.getchildren()[0].getchildren()[1].getchildren()[3].getchildren()[1].tag == "{urn:ndov:cdm:trein:reisinformatie:data:2}TreinSoort"
        treinsoort = xmlline.getchildren()[0].getchildren()[1].getchildren()[3].getchildren()[1].text
        assert xmlline.getchildren()[0].getchildren()[1].getchildren()[3].getchildren()[12].getchildren()[4].tag == "{urn:ndov:cdm:trein:reisinformatie:data:2}LangeNaam"
        eindbestemming = xmlline.getchildren()[0].getchildren()[1].getchildren()[3].getchildren()[12].getchildren()[4].text
        return [treinnummer, treinsoort, eindbestemming.encode('iso-8859-1'), hour, minute]
    except:
        return ["MISFORMED"]

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

def infodat2csv(infilename, csvfilename):
    """Convert the output from the informatoin api to a csv file"""
    dat = getparsedlines(infilename)
    csvdat = [line2arr(its) for its in dat]
    writecsv([it for it in csvdat if it != "MISFORMED"], csvfilename)

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

infoFiles = ["2015-04-24-12-28fridayrun",
             "2015-04-24-15-58fridayrun",
             "2015-04-24-12-58fridayrun",
             "2015-04-24-16-28fridayrun",
             "2015-04-24-13-28fridayrun",
             "2015-04-24-16-58fridayrun",
             "2015-04-24-13-58fridayrun",
             "2015-04-24-17-28fridayrun",
             "2015-04-24-14-28fridayrun",
             "2015-04-24-17-58fridayrun",
             "2015-04-24-14-58fridayrun",
             "2015-04-24-18-28fridayrun",
             "2015-04-24-15-28fridayrun"]

def convertdat():
    for name in ovdatFiles:
        print(name)
        dat2csv("rawdata/" + name + ".ovdat", name + ".csv")

def convertinfo():
    for name in infoFiles:
        print(name)
        infodat2csv("rawdata/" + name + ".ovinfo", name + "-info.csv")

