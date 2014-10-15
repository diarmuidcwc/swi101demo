#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      DCollins
#
# Created:     16/09/2014
# Copyright:   (c) DCollins 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import bottle
import SWI101,BCU
import re
import TrafficGenerator


C_INDOOR_CAMERA = 5
C_OUTDOOR_CAMERA = 6
C_PC = 2
C_WIFI = 4
C_SWI_ADDRESS = "192.168.28.101"
C_TRAFFIC_GENERATOR = {"1":2212, "2":2122}

# Handy functions to switch cameras
def show_outdoor_camera(myswi):
    myswi.remove_forward_port_to_port(C_INDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_OUTDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_PC,C_OUTDOOR_CAMERA)

def show_indoor_camera(myswi):
    myswi.remove_forward_port_to_port(C_OUTDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_INDOOR_CAMERA,C_PC)
    myswi.forward_port_to_port(C_PC,C_INDOOR_CAMERA)


# The root index page. All the magic happens in the templated
@bottle.route('/')
def swistatus():
    return bottle.template('swi')


# This is to route all the javascript and css static paths
@bottle.route('/static/:path#.+#', name='static')
def static(path):
    return bottle.static_file(path, root='static')


# All the following are AJAX requests with either value or JSON
# replies.



# Get the link status of all the ports of a SWI
@bottle.route('/linkstatus/<ipaddress>')
def linkstatus(ipaddress):
    my_swi101 = SWI101.SWI101()
    my_swi101.ipaddress = ipaddress
    try:
        my_swi101.get_interface_status()
        return my_swi101.link_status
    except:
        return {"swidown":"swidown"}


# Route one of the cameras to the PC in effect selecting it
@bottle.route('/selectcamera/<cameratype>')
def selectcamera(cameratype):
    my_swi101 = SWI101.SWI101()
    my_swi101.ipaddress = C_SWI_ADDRESS
    try:
        my_swi101.get_current_routing()
    except:
        return "outdoor"

    if "outdoor" in cameratype:
        show_outdoor_camera(my_swi101)
        return "outdoor"
    elif "indoor" in cameratype :
        show_indoor_camera(my_swi101)
        return "indoor"
    else:
        return "@{}@".format(cameratype)



# JSON Response with the time information for one particular swi
@bottle.route('/timeinfo/<ipaddress>')
def timeinfo(ipaddress):
    my_swi101 = SWI101.SWI101()
    my_swi101.ipaddress = ipaddress
    try:
        my_swi101.get_time_info()
        return my_swi101.timemode
    except:
        return {"Link Status":"Down"}

# JSON Response with the time information for the BCUs
@bottle.route('/bcutimeinfo/<ipaddress>')
def timeinfo(ipaddress):
    mybcu = BCU.BCU()
    mybcu.ipaddress = ipaddress
    try:
        mybcu.get_time_info()
        return mybcu.timemode
    except:
        return {"Link Status": "Down"}



# Set the traffic rate for one particular generator
@bottle.route('/trafficrate')
@bottle.route('/trafficrate/<generator>/<rate>')
def trafficrate(generator=0,rate=0):
    if generator == 0:
        return C_TRAFFIC_GENERATOR
    else:
        #print("generator={} type={}".format(generator,type(generator)))
        udpsetrate = TrafficGenerator.TrafficGenerator()
        udpsetrate.port = C_TRAFFIC_GENERATOR[generator]
        rate_int = int(rate)
        #print "Rate={} Type={}".format(rate_int,type(rate_int))
        for count in range(5):
            udpsetrate.SendBitRate(rate_int)


@bottle.route('/routing/<ipaddress>/<port>')
def routing(ipaddress,port):
    my_swi101 = SWI101.SWI101()
    my_swi101.ipaddress = ipaddress
    try:
        return my_swi101.get_port_routing(port)
    except:
        return {"Link Status":"Down"}

@bottle.route('/toggleport/<ipaddress>/<srcport>/<dstport>')
def toggleport(ipaddress,srcport,dstport):
    my_swi101 = SWI101.SWI101()
    my_swi101.ipaddress = ipaddress
    try:
        print "ipaddress={}:srcport={}:dstport={}".format(ipaddress,srcport,dstport)
        return my_swi101.toggle_port_routing(int(srcport),int(dstport))
    except:
        return {"Link Status":"Down"}

@bottle.route('/resetrouting')
def resetrouting():

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
        # - meingberg
        my_swi101.forward_port_to_port(C_BCU142,C_MEINBERG)
        my_swi101.forward_port_to_port(C_MEINBERG,C_BCU142)
        my_swi101.forward_port_to_port(C_SECONDSWI,C_MEINBERG)
        my_swi101.forward_port_to_port(C_MEINBERG,C_SECONDSWI)

        my_swi101.remove_forward_port_to_port(C_INDOOR_CAMERA,C_PC)
        my_swi101.forward_port_to_port(C_OUTDOOR_CAMERA,C_PC)
        my_swi101.forward_port_to_port(C_PC,C_OUTDOOR_CAMERA)
        print second_swi.prettyprint_routing()


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

    return


bottle.run(host='192.168.28.110', port=80, debug=True, reload=True)
