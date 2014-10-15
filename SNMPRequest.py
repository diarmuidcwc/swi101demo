#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      DCollins
#
# Created:     17/09/2014
# Copyright:   (c) DCollins 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------


class SNMPRequest():
    '''Class to handle the raw SNMP Request'''

    C_OID_AllowedToGoToRoot = "1.3.6.1.2.1.17.5.1.1.3"
    C_OID_Interface_Description = "1.3.6.1.2.1.2.2.1.2"
    C_OID_TimeMode = "1.3.6.1.4.1.33698.13.6"
    C_OID_PtpVersion = "1.3.6.1.4.1.33698.13.10"
    C_OID_TimeReliable = "1.3.6.1.4.1.33698.13.5"
    C_OID_PTPSyncError = "1.3.6.1.4.1.33698.13.4"

    def __init__(self,ipaddress):
        self.ipaddress = ipaddress


    def core_snmp_get(self,oid):
        '''The core snmp get method'''
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        from pysnmp.proto import rfc1902

        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd( \
        cmdgen.CommunityData('public', mpModel=0),\
        cmdgen.UdpTransportTarget((self.ipaddress, 161),timeout=0.5,retries=0), \
        oid )
        if errorIndication:
            raise RuntimeError()
        else:
            if errorStatus:
                raise RuntimeError(errorStatus.prettyPrint())
            else:
                for name, val in varBinds:
                    return val


    def set_snmp_routing(self,port,value):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        from pysnmp.proto import rfc1902

        oid = "{}.{}".format(SNMPRequest.C_OID_AllowedToGoToRoot,port)

        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd( \
        cmdgen.CommunityData('public', mpModel=0),\
        cmdgen.UdpTransportTarget((self.ipaddress, 161)), \
        (oid, rfc1902.Integer(value)) )

        if errorIndication:
            raise RuntimeError()
        else:
            if errorStatus:
                raise RuntimeError(errorStatus.prettyPrint())
            else:
                return True

    # Wrappers around the snmp get

    def get_snmp_routing(self,port):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oid = "{}.{}".format(SNMPRequest.C_OID_AllowedToGoToRoot,port)

        try:
            val = self.core_snmp_get(oid)
        except:
            raise RuntimeError
        return val

    def get_port_status(self,port):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oid = "{}.{}".format(SNMPRequest.C_OID_Interface_Description,port)

        try:
            val = self.core_snmp_get(oid)
        except:
            raise RuntimeError
        return val


    def get_time_mode(self):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oid = "{}.{}".format(SNMPRequest.C_OID_TimeMode,0)

        try:
            val = self.core_snmp_get(oid)
        except:
            raise RuntimeError
        return val

    def get_ptp_version(self):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oid = "{}.{}".format(SNMPRequest.C_OID_PtpVersion,0)

        try:
            val = self.core_snmp_get(oid)
        except:
            raise RuntimeError
        return val

    def get_time_reliable(self):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oid = "{}.{}".format(SNMPRequest.C_OID_TimeReliable,0)

        try:
            val = self.core_snmp_get(oid)
        except:
            raise RuntimeError
        return val

    def get_ptp_error(self):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oid = "{}.{}".format(SNMPRequest.C_OID_PTPSyncError,0)

        try:
            val = self.core_snmp_get(oid)
        except:
            raise RuntimeError
        return val