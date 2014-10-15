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

class KappaConfigs():
    C_PTPv1_SLAVE = 3
    C_PTPv2_SLAVE = 1
    C_NO_PTP = 0
    C_ALL_IFRAMES = 1

    C_STREAMING_TWO_1 ={
                'StreamProtocol' : 6,
                'StreamID1' : '0x000000dc',
                'StreamID0' : '0x00000002',
                'EncoderStreamBitrate0' : '8000000',
                'EncoderStreamBitrate1' : '1000000',
                'DestinationIPAddress0' : '235.0.0.1',
                'DestinationMACAddress0' : '01:00:5e:00:00:01',
                'DestinationPort0' : 8010,
                'DestinationIPAddress1' : '235.0.0.1',
                'DestinationMACAddress1' : '01:00:5e:00:00:01',
                'DestinationPort1' : 8011,
                'PTPMode' : C_PTPv1_SLAVE,
                'I-FrameInterval' : 20
            }

    C_STREAMING_TWO_2 ={
                'StreamProtocol' : 6,
                'StreamID1' : '0x000000dc',
                'StreamID0' : '0x00000002',
                'EncoderStreamBitrate0' : '8000000',
                'EncoderStreamBitrate1' : '1000000',
                'DestinationIPAddress0' : '235.0.0.2',
                'DestinationMACAddress0' : '01:00:5e:00:00:02',
                'DestinationPort0' : 8020,
                'DestinationIPAddress1' : '235.0.0.3',
                'DestinationMACAddress1' : '01:00:5e:00:00:03',
                'DestinationPort1' : 8023,
                'PTPMode' : C_PTPv1_SLAVE,
                'I-FrameInterval' : 20
            }

    C_STREAMING_ONE_1 ={
                'StreamProtocol' : 6,
                'StreamID1' : '0x000000dc',
                'StreamID0' : '0x00000002',
                'EncoderStreamBitrate0' : '8000000',
                'EncoderStreamBitrate1' : '1000000',
                'DestinationIPAddress0' : '235.0.0.1',
                'DestinationMACAddress0' : '01:00:5e:00:00:01',
                'DestinationPort0' : 8030,
                'DestinationIPAddress1' : '0.0.0.0',
                'DestinationMACAddress1' : 'FF:FF:FF:FF:FF:FF',
                'DestinationPort1' : 0,
                'PTPMode' : C_PTPv1_SLAVE,
                'I-FrameInterval' : 20
            }

    C_STREAMING_ONE_2 ={
                'StreamProtocol' : 6,
                'StreamID1' : '0x000000dc',
                'StreamID0' : '0x00000002',
                'EncoderStreamBitrate0' : '8000000',
                'EncoderStreamBitrate1' : '1000000',
                'DestinationIPAddress0' : '235.0.0.2',
                'DestinationMACAddress0' : '01:00:5e:00:00:02',
                'DestinationPort0' : 8030,
                'DestinationIPAddress1' : '0.0.0.0',
                'DestinationMACAddress1' : 'FF:FF:FF:FF:FF:FF',
                'DestinationPort1' : 0,
                'PTPMode' : C_PTPv1_SLAVE,
                'I-FrameInterval' : 20
            }