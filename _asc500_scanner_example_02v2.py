# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 08:28:42 2021

@author: grundch
"""

import numpy as np
from matplotlib import pyplot as plt
import asc500_base as asc
import time
import os
import ctypes as ct

chNo = 0
average = 0
sampTime = 0
bufSize = 1024


# Some Constants ----------------------------------------------------------------
columns         = 100                                           # Scanrange number of columns
lines           = 150                                           # Scanrange number of lines
pxSize       = 50                                          # Width of a column/line [10pm]
sampTime      = 1                                           # Scanner sample time [2.5us]
frameSize       = columns*lines*2                               # Amount of data in a frame
DYB_EVT_DATA_00 = chNo                                             # from daisydata.h
DYB_EVT_CUSTOM  = 0x8000                                        # from daisydata.h

def pollDataFull():
    event   = 0                                                 # Returncode of waitForEvent
    #frameNo = ct.c_int32( 0 )                                      # Return param of getDataBuffer
    #index   = ct.c_int32( 0 )                                      # Return param of getDataBuffer
    #dSize   = ct.c_int32( frameSize )                              # In- and output of getDataBuffer
    #frame   = (ct.c_int32 * frameSize)()                           # Array to receive data
    #meta    = (ct.c_int32 * 13)()                                  # Metadata, should be a struct...

    # Wait for full buffer on channel 0 and show progress
    while ( event == 0 ):
        event = asc500.waitForEvent( 500, asc500.getConst('DYB_EVT_DATA_00'), 0 );
        pos = asc500.getScannerXYPos()
        print( "Scanner at ", pos[0], " , ", pos[1], " um" )

    # Read and print data frame, forward and backward scan in separate files
    print( "Reading frame; bufSize=", frameSize, ", frameSize=",
           asc500.getFrameSize( chNo ) );
    out = asc500.getDataBuffer( chNo, 1, frameSize)
    data = out[3][:]
    index = out[1]
    dSize = out[2]
    frame = out[0]
    meta = out[4]
    print(type(meta))
    if ( dSize.value > 0 ):
        counts = out[3][:]
        asc500.writeBufferToFile( 'scan_once', 'ADC0', 0, 1, index, dSize, frame, meta )
        # asc500.writeBuffer( 'scan_fwd', 'ADC2', 0, 1, index, dSize, frame, meta )
        # asc500.writeBuffer( 'scan_bwd', 'ADC2', 0, 0, index, dSize, frame, meta )
        return out
    else:
        raise( "No data have been received!" )


binPath = "Installer\\ASC500CL-V2.7.6\\"
dllPath = "64bit_lib\\ASC500CL-LIB-WIN64-V2.7.6\\daisybase\\lib\\"
asc500 = asc.ASC500Base(binPath, dllPath)
asc500.startServer()
asc500.sendProfile('Installer\\ASC500CL-V2.7.6\\afm.ngp')
asc500.setDataEnable(1)
asc500.configureChannel(chNo,
                        asc500.getConst('CHANCONN_SCANNER'),
                        0,
                        average,
                        sampTime)
print(asc500.getChannelConfig(chNo))

asc500.configureDataBuffering(chNo, bufSize)

#asc500.setCounterExposureTime(expTime)
#print("Exposure time ", asc500.getCounterExposureTime())



#config Scanner
asc500.setParameter( asc500.getConst('ID_SCAN_X_EQ_Y'),   0, 0 )        # Switch off annoying automatics ..
asc500.setParameter( asc500.getConst('ID_SCAN_GEOMODE'),  0, 0 )        # that are useful only for GUI users
asc500.setParameter( asc500.getConst('ID_SCAN_PIXEL'),    pxSize, 0 ) # Adjust scanner parameters
asc500.setParameter( asc500.getConst('ID_SCAN_COLUMNS'),  columns, 0 )
asc500.setParameter( asc500.getConst('ID_SCAN_LINES'),   lines, 0 )
asc500.setParameter( asc500.getConst('ID_SCAN_OFFSET_X'), 75 * pxSize, 0 )
asc500.setParameter( asc500.getConst('ID_SCAN_OFFSET_Y'), 75 * pxSize, 0 )
asc500.setParameter( asc500.getConst('ID_SCAN_MSPPX'),    sampTime, 0 )
asc500.setParameter( asc500.getConst('ID_SCAN_ONCE'), 1)

# Enable Outputs and wait for success (enable outputs takes some time)
outActive = 0
asc500.setParameter( asc500.getConst('ID_OUTPUT_ACTIVATE'), 1, 0  )
while ( outActive == 0 ):
    outActive = asc500.getParameter( asc500.getConst('ID_OUTPUT_STATUS'), 0 )
    print( "Output Status: ", outActive )
    time.sleep( .05 )

out = []
#start scanning
asc500.sendScannerCommand( asc500.getConst('SCANRUN_ON') )                      # Start scanner
out.append(pollDataFull())                                              # Wait for data
asc500.sendScannerCommand( asc500.getConst('SCANRUN_OFF') )                     # Stop scanner

# Disable Outputs and wait until finished.
# We use wait for event instead of polling for demonstration.
asc500.setParameter( asc500.getConst('ID_OUTPUT_ACTIVATE'), 0, 0  )
asc500.waitForEvent( 5000, DYB_EVT_CUSTOM, asc500.getConst('ID_OUTPUT_STATUS') )
outActive = asc500.getParameter( asc500.getConst('ID_OUTPUT_STATUS'), 0 )
if ( outActive != 0 ):
    print( "Outputs are not deactivated!" )

asc500.stopServer()