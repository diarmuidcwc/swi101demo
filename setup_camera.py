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

import Kappa
import KappaConfigs
import os,tempfile
import SWI101
import time


C_INDOOR_CAMERA = 5
C_OUTDOOR_CAMERA = 6
C_PC = 2
C_SWI_ADDRESS = "192.168.28.101"

C_INDOOR_IP_ADDRESS = "192.168.28.202"
C_OUTDOOR_IP_ADDRESS = "192.168.28.201"
# just a few commonly use ip address Really should be converted but I'm too lazy
C_IP_TO_MAC = { "235.0.0.1" : "01:00:5e:00:00:01","235.0.0.2" : "01:00:5e:00:00:02",\
                "235.0.0.3" : "01:00:5e:00:00:03","235.0.0.4" : "01:00:5e:00:00:04"}

def main():

    # Configure the Swtich so that I can program both devices
    my_swi101 = SWI101.SWI101()
    my_swi101.ipaddress = C_SWI_ADDRESS
    my_swi101.get_current_routing()
    my_swi101.forward_port_to_port(C_INDOOR_CAMERA,C_PC)
    my_swi101.forward_port_to_port(C_PC,C_INDOOR_CAMERA)
    my_swi101.forward_port_to_port(C_OUTDOOR_CAMERA,C_PC)
    my_swi101.forward_port_to_port(C_PC,C_OUTDOOR_CAMERA)

    #-------------------------
    # Indoor camera
    #-------------------------

    # Setup the indoor camera
    indoorcamera = Kappa.Kappa()
    indoorcamera.SetAsIndoor()
    indoorcamera.ipaddress = C_INDOOR_IP_ADDRESS

    # Change to single stream
    indoorcamera.config['Streaming'] = KappaConfigs.KappaConfigs.C_STREAMING_ONE_1
    #indoorcamera.SetIFrameRate(5)
    indoorcamera.SetPTPV2Mode()

    # Write and program the cameras
    mytmpconfigfile = "config_indoor_{}.txt".format(os.getpid())
    indoorcamera.WriteConfigToFile(mytmpconfigfile)
    program_errors = indoorcamera.ProgramAndVerify(mytmpconfigfile)
    if len(program_errors) != 0:
        print "ERROR: Programming failure of indoor camera with {} error".format(' '.join(program_errors))
        #exit()
    else:
        os.remove(mytmpconfigfile)

    #----------------------
    # Outdoor Camera
    #----------------------
    outdoorcamera = Kappa.Kappa()
    outdoorcamera.SetAsOutdoor()
    outdoorcamera.ipaddress = C_OUTDOOR_IP_ADDRESS

    # Change to single stream
    outdoorcamera.config['Streaming'] = KappaConfigs.KappaConfigs.C_STREAMING_ONE_1
    #outdoorcamera.SetIFrameRate(5)
    outdoorcamera.SetPTPV2Mode()
    #outdoorcamera.SetExposure(100000)

    # Write and program the cameras
    mytmpconfigfile = "config_outdoor_{}.txt".format(os.getpid())
    outdoorcamera.WriteConfigToFile(mytmpconfigfile)
    program_errors = outdoorcamera.ProgramAndVerify(mytmpconfigfile)
    if len(program_errors) != 0:
        print "ERROR: Programming failure of outdoor camera with {} error".format(' '.join(program_errors))
        exit()
    else:
        os.remove(mytmpconfigfile)


    print "Done programming\n"
if __name__ == '__main__':
    main()
