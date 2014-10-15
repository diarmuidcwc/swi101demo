#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      DCollins
#
# Created:     15/09/2014
# Copyright:   (c) DCollins 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import tftpy
import KappaConfigs
import os
import xml.dom.minidom
import time


class Kappa():
    '''Class to control the programming of the Kappa cameras'''
    C_OUTDOOR_TYPE = 0xb24
    C_INDOOR_TYPE = 0xb20
    C_TFTP_PORT = 69

    def __init__(self):
        self.ipaddress = None
        self.outdoor_camera = None # Indoor or outdoor
        self.camera_type = Kappa.C_OUTDOOR_TYPE
        self.DefaultConfiguration()

    def SetAsOutdoor(self):
        '''Configure the camera as an outdoor camera'''
        self.outdoor_camera = True
        self.camera_type = Kappa.C_OUTDOOR_TYPE

    def SetAsIndoor(self):
        '''Configure the camera as an outdoor camera'''
        self.outdoor_camera = False
        self.camera_type = Kappa.C_INDOOR_TYPE

    def DefaultConfiguration(self):
        '''Create the default configuration'''
        self.config = {
            'SignalGeneration' : {
                'Exposure' : 33333,
                'Gain' : 0,
                'SensorFrameRate' : 30,
                'ExposureMode' : 1
            },
            'ColorProcessing' : {
                'ColorBalanceR' : 64,
                'ColorBalanceG' : 64,
                'ColorBalanceB' : 64
            },
            'ControlLoops' : {
                'AET' : 0,
                'ACG' : 0,
                'ExposureLevel' : 128,
                'AWB' : 0
            },
            'Streaming' : KappaConfigs.KappaConfigs.C_STREAMING_TWO_1

        }

    def WriteConfigToFile(self,filename):
        '''Write a configuration file to a local file'''
        fobject = file(filename,'w')
        for section,stanza in sorted(self.config.iteritems()):
            fobject.write("[{}]\n".format(section))
            for setting,value in sorted(stanza.iteritems()):
                fobject.write("{}={}\n".format(setting,value))
            fobject.write("\n")
        fobject.close()


    def GetConfigXML(self,localfile):
        '''Download the xml configuration file'''
        client = tftpy.TftpClient(self.ipaddress,Kappa.C_TFTP_PORT)
        try:
            client.download("0/config.xml",localfile)
        except:
            raise Exception("TFTP Download Failed")

        return True

    def WriteCRC(self,localfile):
        '''Download the xml configuration file'''
        client = tftpy.TftpClient(self.ipaddress,Kappa.C_TFTP_PORT)
        try:
            client.upload("0/crcreq.xml",localfile)
        except:
            raise Exception("TFTP Download Failed")

        return True

    def PutConfigFile(self,localfile):
        '''TFTP the local configuration file to the correct location on the camera'''
        client = tftpy.TftpClient(self.ipaddress,Kappa.C_TFTP_PORT)
        dst_fname = "0/01{:04X}/1A0000.bin".format(self.camera_type)
        try:
            client.upload(dst_fname,localfile)
        except:
            raise Exception("TFTP Upload Failed")

        return True

    def GetConfigFile(self,localfile):
        '''Do no use'''
        client = tftpy.TftpClient(self.ipaddress,Kappa.C_TFTP_PORT)
        dst_fname = "0/01{:04X}/1A0000.bin".format(self.camera_type)
        try:
            client.download(dst_fname,localfile)
        except:
            raise Exception("TFTP Download Failed")

        return True

    def ProgramAndVerify(self,localfile):
        mytmpxml = "tmp_cfg_{}.xml".format(os.getpid())

        try:
            self.GetConfigXML(mytmpxml)
        except:
            raise RuntimeError

        try:
            self.PutConfigFile(localfile)
        except:
            raise RuntimeError

        # Now trigger the crc
        try:
            self.WriteCRC(mytmpxml)
        except:
            raise RuntimeError

        # delete the tmp file
        os.remove(mytmpxml)
        # Get The config Again
        mytmpxml = "tmp_cfg2_{}.xml".format(os.getpid())
        try:
            self.GetConfigXML(mytmpxml)
        except:
            raise RuntimeError

        # Now parse the xml for an error
        dom = xml.dom.minidom.parse(mytmpxml)
        sector = dom.getElementsByTagName("Sector")
        errors_found = []
        for element in sector:
            if element.getAttribute("Error"):
                errors_found.append(element.getAttribute("Error"))
        # keep the file if errors are returned
        if len(errors_found) == 0:
            os.remove(mytmpxml)

        return errors_found

    # Some methods help set common configus

    def SetDstIPAddr(self,stream,dstaddr):
        '''Set the Destination IP address for a stream'''
        if (stream != 0) and (stream != 1):
            raise ValueError("Stream should be 1 or 0")
        config_key = "DestinationIPAddress{}".format(stream)
        self.config['Streaming'][config_key] = dstaddr

    def SetDstMACAddr(self,stream,macaddr):
        '''Set the destination MAC address for a stream'''
        if (stream != 0 and stream != 1):
            raise ValueError
        config_key = "DestinationMACAddress{}".format(stream)
        self.config['Streaming'][config_key] = macaddr

    def SetDstPort(self,stream,port):
        '''Set the destination UDP port'''
        if (stream != 0 and stream != 1):
            raise ValueError
        config_key = "DestinationPort{}".format(stream)
        self.config['Streaming'][config_key] = port


    def SetPTPV1Mode(self):
        '''Set the camera to sync to PTPv1 mode'''
        self.config['Streaming']['PTPMode'] = KappaConfigs.KappaConfigs.C_PTPv1_SLAVE

    def SetPTPV2Mode(self):
        '''Set the camera to sync to PTPv2 mode'''
        self.config['Streaming']['PTPMode'] = KappaConfigs.KappaConfigs.C_PTPv2_SLAVE

    def DisablePTPMode(self):
        '''Disable PTP synchronisation'''
        self.config['Streaming']['PTPMode'] = KappaConfigs.KappaConfigs.C_NO_PTP

    def SetFrameRate(self,rate):
        '''Set the sensor frame rate'''
        if rate > 30 or rate < 1 or type(rate) is not int:
            raise ValueError("Frame Rate integer between 1 and 30")
        self.config['SignalGeneration']['SensorFrameRate'] = rate

    def SetExposure(self,time):
        '''Set the exposure of the camera'''
        if time > 2000000 or time < 0 or type(time) is not int:
            raise ValueError("Exposure Level is integer between 0 and 2000000")
        self.config['SignalGeneration']['Exposure'] = time

    def SetIFrameRate(self,rate):
        '''Set the I-Frame rate'''
        if rate > 30 or rate < 1 or type(rate) is not int:
            raise ValueError("I-Frame Rate integer between 1 and 30")
        self.config['Streaming']['I-FrameInterval'] = rate

    def SetAutoMode(self):
        self.config['ControlLoops']['AET'] = 1
        self.config['ControlLoops']['ACG'] = 1
        self.config['ControlLoops']['AWB'] = 1

    def DisableAutoMode(self):
        self.config['ControlLoops']['AET'] = 0
        self.config['ControlLoops']['ACG'] = 0
        self.config['ControlLoops']['AWB'] = 0