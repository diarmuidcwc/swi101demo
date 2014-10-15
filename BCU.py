#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      DCollins
#
# Created:     22/09/2014
# Copyright:   (c) DCollins 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import SNMPRequest

class BCU():
    C_PTPVERSION = ['None','PTPv1','PTPv2']

    C_TIMEMODE = [  'LocalFreeRunning', 'PTPSlave','LocalTimeNoPTP', 'LocalTimePTPGrandmaster',\
                    'Automatic', 'FreeRunningPTPGrandmaster','SNTPClient', 'SNTPServer','SNTPBoth',]
    C_TIMERELAIBLE = ["Not In Sync","In Sync"]

    def __init__(self):
        self.ipaddress = None
        self.timemode = {'Mode':None,'PTP':None, 'Reliable':None, 'PTP Error' : 0}
        self.insync = False
        self.ptpSyncError = 0

    def get_time_info(self):
        '''Get the current timemode'''
        snmp_get = SNMPRequest.SNMPRequest(self.ipaddress)
        self.timemode['Mode'] = BCU.C_TIMEMODE[snmp_get.get_time_mode()]
        self.timemode['PTP'] = BCU.C_PTPVERSION[snmp_get.get_ptp_version()]
        self.timemode['Reliable'] = BCU.C_TIMERELAIBLE[snmp_get.get_time_reliable()]
        self.timemode['PTP Error'] = abs(snmp_get.get_ptp_error())

