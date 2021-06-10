# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 08:28:42 2021

@author: grundch
"""

import asc500_base as asc
import time

def getScannerXYPos():
    xOrigin   = asc500.getParameter(asc500.getConst('ID_SCAN_COORD_ZERO_X'), sync=True)
    yOrigin   = asc500.getParameter(asc500.getConst('ID_SCAN_COORD_ZERO_Y'), sync=True)
    xRelative = asc500.getParameter(asc500.getConst('ID_SCAN_CURR_X'), sync=True)
    yRelative = asc500.getParameter(asc500.getConst('ID_SCAN_CURR_Y'), sync=True)
    x = (xOrigin + xRelative) / 1e5  # 10pm -> um
    y = (yOrigin + yRelative) / 1e5
    return [x,y]

def pollDataFull():
    event = 0 # Returncode of waitForEvent

    # Wait for full buffer on channel 0 and show progress
    while ( event == 0 ):
        event = asc500.waitForEvent( 500, asc500.getConst('DYB_EVT_DATA_00'), 0 )
        pos = getScannerXYPos()
        print( "Scanner at ", pos[0], " , ", pos[1], " um" )

    # Read and print data frame, forward and backward scan in separate files
    print( "Reading frame; bufSize=", frameSize, ", frameSize=", asc500.getFrameSize(chNo))
    frame, index, dSize, data, meta = asc500.getDataBuffer(chNo, 1, frameSize)
    print(type(meta))
    if ( dSize.value > 0 ):
        asc500.writeBufferToFile( 'scan_once', 'ADC0', 0, 1, index, dSize, frame, meta )
        return
    else:
        raise( "No data have been received!" )

def sendScannerCommand(command):
    if (command == asc500.getConst('SCANRUN_ON') ):
        # Scan start requires two commands; the first one to move to the start position,
        # (which can take a long time), the second one to actually run the scan.
        # A rather simple approach: send command cyclically until the scanner is running
        state = 0
        while ( (state & asc500.getConst('SCANSTATE_SCAN')) == 0 ):
            asc500.setParameter(asc500.getConst('ID_SCAN_COMMAND'), command)
            time.sleep( .1 )
            state = asc500.getParameter(asc500.getConst('ID_SCAN_STATUS'), 0, sync=True)
            print( "Scanner State: ", end='' )
            if ( state & asc500.getConst('SCANSTATE_PAUSE')  ): print( "Pause ", end='' )
            if ( state & asc500.getConst('SCANSTATE_MOVING') ): print( "Move ",  end='' )
            if ( state & asc500.getConst('SCANSTATE_SCAN')   ): print( "Scan ",  end='' )
            if ( state & asc500.getConst('SCANSTATE_IDLE')   ): print( "Idle ",  end='' )
            if ( state & asc500.getConst('SCANSTATE_LOOP')   ): print( "Loop ",  end='' )
            print( "" )
    else:
        # Stop and pause only require one command
        asc500.setParameter(asc500.getConst('ID_SCAN_COMMAND'), command)

# Some Constants ----------------------------------------------------------------
chNo = 0
average = 0
sampTime = 0
bufSize = 1024
columns = 100 # Scanrange number of columns
lines = 150 # Scanrange number of lines
pxSize = 1000 # Width of a column/line [10pm]
sampTime = 100 # Scanner sample time [2.5us]
frameSize = columns * lines * 2 # Amount of data in a frame

binPath = 'Installer\\ASC500CL-V2.7.7\\'
dllPath = '64bit_lib\\ASC500CL-LIB-WIN64-V2.7.7\\daisybase\\lib\\'

asc500 = asc.ASC500Base(binPath, dllPath)
asc500.startServer('FindSim')
asc500.sendProfile('Installer\\ASC500CL-V2.7.7\\afm.ngp')
asc500.configureChannel(chNo,
                        asc500.getConst('CHANCONN_SCANNER'),
                        asc500.getConst('CHANADC_ADC_MIN') + 1,
                        average,
                        sampTime)
print(asc500.getChannelConfig(chNo))

asc500.configureDataBuffering(chNo, bufSize)

#config Scanner
asc500.setParameter(asc500.getConst('ID_SCAN_X_EQ_Y'), 0) # Switch off annoying automatics ..
asc500.setParameter(asc500.getConst('ID_SCAN_GEOMODE'), 0)        # that are useful only for GUI users
asc500.setParameter(asc500.getConst('ID_SCAN_PIXEL'), pxSize) # Adjust scanner parameters
asc500.setParameter(asc500.getConst('ID_SCAN_COLUMNS'), columns)
asc500.setParameter(asc500.getConst('ID_SCAN_LINES'), lines)
asc500.setParameter(asc500.getConst('ID_SCAN_OFFSET_X'), int(columns/2 *pxSize))
asc500.setParameter(asc500.getConst('ID_SCAN_OFFSET_Y'), int(lines/2 *pxSize))
asc500.setParameter(asc500.getConst('ID_SCAN_MSPPX'), sampTime)
# asc500.setParameter(asc500.getConst('ID_SCAN_ONCE'), 1)

# Enable Outputs and wait for success (enable outputs takes some time)
outActive = 0
asc500.setParameter(asc500.getConst('ID_OUTPUT_ACTIVATE'), 1)
while(outActive == 0):
    outActive = asc500.getParameter(asc500.getConst('ID_OUTPUT_STATUS'), 0, sync=True)
    print( "Output Status: ", outActive )
    time.sleep( .05 )

#start scanning
sendScannerCommand( asc500.getConst('SCANRUN_ON') ) # Start scanner
pollDataFull() # Wait for data
sendScannerCommand( asc500.getConst('SCANRUN_OFF') ) # Stop scanner


asc500.stopServer()
