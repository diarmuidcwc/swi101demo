#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      DCollins
#
# Created:     12/09/2014
# Copyright:   (c) DCollins 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import SWI101
import time

# SWI #1
C_BCU142 = 1
C_PC = 2
C_SECONDSWI = 3
C_MEINBERG = 4
C_INDOOR_CAMERA = 5
C_OUTDOOR_CAMERA = 6
C_WIFI = 7

#SWI #2
C_BCU145 = 6
C_FIRSTSWI = 8


C_SWI_ADDRESS_1 = "192.168.28.101"
C_SWI_ADDRESS_2 = "192.168.28.102"

def show_outdoor_camera(myswi):
    myswi.remove_forward_port_to_port(C_INDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_OUTDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_PC,C_OUTDOOR_CAMERA)

def show_indoor_camera(myswi):
    myswi.remove_forward_port_to_port(C_OUTDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_INDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_PC,C_INDOOR_CAMERA)

def show_both_cameras(myswi):
    myswi.forward_port_to_port(C_INDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_PC,C_INDOOR_CAMERA)
    myswi.forward_port_to_port(C_OUTDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_PC,C_OUTDOOR_CAMERA)

def show_no_camera(myswi):
    myswi.remove_forward_port_to_port(C_INDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_PC,C_INDOOR_CAMERA)
    myswi.remove_forward_port_to_port(C_OUTDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_PC,C_OUTDOOR_CAMERA)

def main():

    my_swi101 = SWI101.SWI101()
    my_swi101.ipaddress = C_SWI_ADDRESS_1


    print "-------------FIRST SWI -------------"
    try:
        my_swi101.get_current_routing()

        # Clear the Routing in the xbar
        my_swi101.all_to_none()
        my_swi101.forward_port_to_port(C_WIFI,C_PC)
        my_swi101.forward_port_to_port(C_PC,C_WIFI)
        my_swi101.forward_port_to_port(C_BCU142,C_PC)
        my_swi101.forward_port_to_port(C_PC,C_BCU142)
        my_swi101.forward_port_to_port(C_PC,C_SECONDSWI)
        my_swi101.forward_port_to_port(C_SECONDSWI,C_PC)

        show_outdoor_camera(my_swi101)

        print my_swi101.prettyprint_routing()

    except:
        print "SWI 1 down"

    print "-------------SECOND SWI -------------"
    second_swi = SWI101.SWI101()
    second_swi.ipaddress = C_SWI_ADDRESS_2
    try:
        second_swi.get_current_routing()
        second_swi.all_to_none()
        second_swi.forward_port_to_port(C_BCU145,C_FIRSTSWI)
        second_swi.forward_port_to_port(C_FIRSTSWI,C_BCU145)
        print second_swi.prettyprint_routing()
    except:
        print "SWI 2 down"

if __name__ == '__main__':
    main()
