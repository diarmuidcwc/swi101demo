#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      diarmuid
#
# Created:     12/09/2014
# Copyright:   (c) DCollins 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import SNMPRequest

def number_to_list(bitmap):
    '''Convert a boolean to a list of booleans'''
    list_return = [None] * 8
    for mybit in range(8):
        list_return[mybit] = bool((bitmap % pow(2,mybit+1) )/pow(2,mybit))

    return list_return

def number_to_dict(bitmap):
    '''Convert a boolean to a dict of booleans'''
    dict_return = {}
    for mybit in range(1,9):
        dict_return[mybit] = bool((bitmap % pow(2,mybit) )/pow(2,mybit-1))

    return dict_return

def list_to_number(connectivity_list):
    '''Convert the list of Booleans to a bit map'''
    bitmap = 0
    for index in range(8):
        if connectivity_list[index] == True:
            bitmap += pow(2,index)
    return bitmap


def dict_to_number(connectivity_dict):
    '''Convert the list of Booleans to a bit map'''
    bitmap = 0
    for port,val in connectivity_dict.iteritems():
        if val == True:
            bitmap += pow(2,port-1)
    return bitmap




class SWI101():
    '''Handle SWI101 xbar configurations'''
    # A few useful constants
    C_TO_ALL  = [True,True,True,True,True,True,True,True]
    C_TO_NONE = [False,False,False,False,False,False,False,False]
    C_LINKDOWN = 0
    C_LINK100  = 100
    C_LINK1000 = 1000
    C_LINKUNKNOWN = -1
    C_LINKSTRING = {C_LINKDOWN:"Link Down",C_LINK100:"100 Mbps",C_LINK1000:"1000 Mbps"}

    C_TIMEMODE = [  'LocalFreeRunning', 'PTPSlave','LocalTimeNoPTP', 'LocalTimePTPGrandmaster',\
                    'Automatic', 'FreeRunningPTPGrandmaster','SNTPClient', 'SNTPServer','SNTPBoth',]
    C_PTPVERSION = ['None','PTPv1','PTPv2']
    #
    # The constructor
    #
    def __init__(self):
        self.ipaddress = "192.168.28.101"
        self.routing_setup = [None] * 8 # This should contain all the routing
        self.pc_port = 2
        self.aggregator= SWI101.C_TO_NONE
        self.dau= SWI101.C_TO_NONE
        self.timemode = {'Mode':None,'PTP':None}

        self.link_status={ 1: SWI101.C_LINKDOWN, 2: SWI101.C_LINKDOWN, 3: SWI101.C_LINKDOWN, 4:SWI101.C_LINKDOWN,\
                           5: SWI101.C_LINKDOWN, 6: SWI101.C_LINKDOWN, 7: SWI101.C_LINKDOWN, 8:SWI101.C_LINKDOWN}

    #
    # Two core methods. One to read back all the xbar routing
    # and one to set the port routing for one port.
    # Most othe methods are based on this
    #
    def get_current_routing(self):
        '''populate the current snmp table'''
        snmp_get = SNMPRequest.SNMPRequest(self.ipaddress)
        for portnum in range(1,9):
            (routeval,) = snmp_get.get_snmp_routing(portnum).asNumbers()
            self.routing_setup[portnum-1] = number_to_list(routeval)

    def get_port_routing(self,portnum):
        '''Get the routing for one port as a dict of booleans'''
        snmp_get = SNMPRequest.SNMPRequest(self.ipaddress)
        (routeval,) = snmp_get.get_snmp_routing(portnum).asNumbers()
        return number_to_dict(routeval)

    def toggle_port_routing(self,srcport,dstport):
        snmp_get = SNMPRequest.SNMPRequest(self.ipaddress)
        (routeval,) = snmp_get.get_snmp_routing(srcport).asNumbers()
        current_routing = number_to_dict(routeval)

        current_routing[dstport] = not current_routing[dstport]

        newbitmap = dict_to_number(current_routing)
        snmp_get.set_snmp_routing(srcport,newbitmap)
        return current_routing


    def set_port_routing(self,portnum,connectivity_list=[]):
        '''Configure a port routing. Arugments are the port number and a list of booleans'''
        # Some data checking on the input
        if portnum < 1 or portnum > 8:
            raise ValueError("Port Numbers between 1 and 8")
        if len(connectivity_list) != 8:
            raise ValueError("Not enough values in the list")
        if connectivity_list.count(0) + connectivity_list.count(1) != 8:
            raise ValueError("Only Booleans allowed in connectivity list")

        # Sent the request
        bitmap =  list_to_number(connectivity_list)
        snmp_set = SNMPRequest.SNMPRequest(self.ipaddress)
        try:
            snmp_set.set_snmp_routing(portnum,bitmap)
        except:
            raise Exception("SNMP Request failed")
        else:
            # record the new routing
            self.routing_setup[portnum-1] = connectivity_list

    #
    # Some useful methods to use as short hand for commonly used
    # functions
    #
    def all_to_all(self):
        ''' connect all ports to all others'''
        for port in range(1,9):
            not_me_list = SWI101.C_TO_ALL
            not_me_list[port-1] = False
            self.set_port_routing(port,not_me_list)


    def all_to_none(self):
        '''Clear all the routing'''
        for port in range(1,9):
            self.set_port_routing(port,SWI101.C_TO_NONE)


    def act_as_aggregator(self,port):
        '''Define a port as an aggregator. This means all traffic goes here'''
        self.aggregator[port-1] = True

        not_me_list = SWI101.C_TO_ALL
        not_me_list[port-1] = False
        self.set_port_routing(port,not_me_list)
        # Need to check that all the dau
        for (dnum,dport) in enumerate(self.dau):
            if self.routing_setup[dnum][port-1] == False:
                new_route = self.routing_setup[dnum]
                new_route[port-1] = True
                self.set_port_routing(dnum+1,new_route)


    def forward_port_to_port(self,srcport,dstport):
        single_dst = list(self.routing_setup[srcport-1]) # Get a copy of what the current routing is on this port
        single_dst[dstport-1] = True # Change the dst port to tru
        self.set_port_routing(srcport,single_dst) # Execute it


    def remove_forward_port_to_port(self,srcport,dstport):
        single_dst = list(self.routing_setup[srcport-1]) # Get a copy of what the current routing is on this port
        single_dst[dstport-1] = False # Change the dst port to tru
        self.set_port_routing(srcport,single_dst) # Execute it


    def get_interface_status(self):
        '''Get the current status of the interfaces'''
        snmp_get = SNMPRequest.SNMPRequest(self.ipaddress)
        for portnum in range(1,9):
            linkstat = str(snmp_get.get_port_status(portnum))
            if "N/C" in linkstat:
                self.link_status[portnum] = SWI101.C_LINKDOWN
            elif "100Mbps" in linkstat:
                self.link_status[portnum] = SWI101.C_LINK100
            elif "1000Mbps" in linkstat:
                self.link_status[portnum] = SWI101.C_LINK1000
            else:
                self.link_status[portnum] = SWI101.C_LINKUNKNOWN

    def get_time_info(self):
        '''Get the current timemode'''
        snmp_get = SNMPRequest.SNMPRequest(self.ipaddress)
        self.timemode['Mode'] = SWI101.C_TIMEMODE[snmp_get.get_time_mode()]
        self.timemode['PTP'] = SWI101.C_PTPVERSION[snmp_get.get_ptp_version()]



    def act_as_dau(self,port):
        '''Setup a port as a dau. It transmits to other aggregrators'''
        if port < 1 or port > 8:
            raise ValueError("Port Numbers between 1 and 8")
        my_custom_list = [None] * 8
        for index in range(8): # loop through each agg
            my_custom_list[index] = self.aggregator[index]
        self.set_port_routing(port,my_custom_list)



    def prettyprint_routing(self):
        '''A method to make the connectivity printable'''
        pp_string = ""
        for (port,srcport) in enumerate(self.routing_setup):
            str_format = ""
            for (targport,connect) in enumerate(srcport):
                str_format += "{:2d}:{:7s}".format(targport+1,str(connect))
            pp_string += "Port {} = {}\n".format(port+1,str_format)

        return pp_string



    def prettyprint_link_status(self):
        '''A method to make the connectivity printable'''
        pp_string = ""
        for (port,value) in self.link_status.iteritems():
            pp_string += "Port {} = {}\n".format(port,SWI101.C_LINKSTRING[value])

        return pp_string