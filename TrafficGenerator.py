#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      DCollins
#
# Created:     18/09/2014
# Copyright:   (c) DCollins 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import socket
import struct

class TrafficGenerator():



    def __init__(self):
        self.dstip = "235.0.0.1"
        self.port = 2212

    def SendBitRate(self,mbits):
        if mbits > 1000:
            mbits = 1000

        counter = int((1352*8)/(32e-3*mbits))
        if counter < 1:
            counter = 1
        elif counter > 0xffff:
            counter = 0xffff

        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(struct.pack('>H',counter), (self.dstip, self.port))



mypacket = TrafficGenerator()
mypacket.SendBitRate(50)