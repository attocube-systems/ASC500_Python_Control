# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 13:40:13 2021

@author: grundch
"""
import time
import numpy as np

class ascScannerFunctions:
    
    def configureScanner(self, xOffset, yOffset, pxSize, columns, lines, sampTime):
        """
        Configures the scanner to perform a scan according to the parameters

        Parameters
        ----------
        xOffset : float
            Offset of the scan area in x direction (in m)
        yOffset : float
            Offset of the scan area in y direction (in m)
        pxSize : int
            Pixelsize / Size of a column/line.
        columns : int
            Scanrange number of columns.
        lines : int
            Scanrange number of lines.
        sampT : float
            Scanner sampling Time.

        Returns
        -------
        None.

        """
        maxSampTime = self.minExpTime * 2**16
        if sampTime < self.minExpTime:
            sampTime = self.minExpTime
        elif sampTime > maxSampTime:
            sampTime = maxSampTime

        sampTimeInt = int(sampTime / self.minExpTime) - 1
        
        self.setParameter( self.getConst('ID_SCAN_X_EQ_Y'),   0, 0 )        # Switch off annoying automatics ..
        self.setParameter( self.getConst('ID_SCAN_GEOMODE'),  0, 0 )        # that are useful only for GUI users
        self.resetScannerCoordSystem()
        self.setParameter( self.getConst('ID_SCAN_PIXEL'),    pxSize, 0 ) # Adjust scanner parameters
        self.setParameter( self.getConst('ID_SCAN_COLUMNS'),  columns, 0 )
        self.setParameter( self.getConst('ID_SCAN_LINES'),   lines, 0 )
        self.setParameter( self.getConst('ID_SCAN_OFFSET_X'), int(xOffset*1e11), 0 )
        self.setParameter( self.getConst('ID_SCAN_OFFSET_Y'), int(yOffset*1e11), 0 )
        self.setParameter( self.getConst('ID_SCAN_MSPPX'),    sampTimeInt, 0 )
        self.setParameter( self.getConst('ID_SCAN_ONCE'), 1)
    
    def resetScannerCoordSystem(self):
        """
        Resets the coordinate system of the scanner.

        Returns
        -------
        None.

        """
        currX = self.getParameter(self.getConst('ID_SCAN_COORD_ZERO_X'))
        currY = self.getParameter(self.getConst('ID_SCAN_COORD_ZERO_Y'))
        if (currX != 0) or (currY != 0):
            self.setParameter(self.getConst('ID_SCAN_COORD_MOVE_X'), currX)
            self.setParameter(self.getConst('ID_SCAN_COORD_MOVE_Y'), currY)
            self.setParameter(self.getConst('ID_SCAN_COORD_MOVE'), 1)
            self.setParameter(self.getConst('ID_SCAN_COORD_MOVE_X'), 0)
            self.setParameter(self.getConst('ID_SCAN_COORD_MOVE_Y'), 0)
    
    def activateScanner(self):
        """
        Activates the output of the scanner.

        Returns
        -------
        None.

        """
        # check if scanner output is already active?
        outActive = self.getParameter(self.getConst('ID_OUTPUT_STATUS'), 0 )
        
        if outActive == 0:
        # Enable Outputs and wait for success (enable outputs takes some time)
            self.setParameter(self.getConst('ID_OUTPUT_ACTIVATE'), 1)
            while(outActive == 0):
                outActive = self.getParameter(self.getConst('ID_OUTPUT_STATUS'), 0 )
                print( "Output Status: ", outActive )
                time.sleep( .01 )

    
    def getScannerXYZRelPos(self):
        """
        Get the scanner x and y position relative to the voltage origin.

        Returns
        -------
        [x, y] : list
            [x,y] relative position in m.

        """
        x = self.getParameter(self.getConst('ID_SCAN_CURR_X'), 0) *1e-11
        y = self.getParameter(self.getConst('ID_SCAN_CURR_Y'), 0) *1e-11
        z = self.getParameter(self.getConst('ID_REG_SET_Z_M'), 0) *1e-12
        a = 0
        return [x, y, z, a]

    def setScannerXYZRelPos(self, pos):
        """
        Sets the scanner origin relative to the voltage origin.

        Parameters
        ----------
        pos : list
            [x,y] relative positions in microns.

        Returns
        -------
        None.

        """
        pos = [i *1e9 for i in pos] # Convert input to nm
        self.setParameter(self.getConst('ID_POSI_TARGET_X'), int(pos[0]*100)) #asc takes inputs in 10pm
        self.setParameter(self.getConst('ID_POSI_TARGET_Y'), int(pos[1]*100)) #therefore conv factor 100
        self.setParameter(self.getConst('ID_POSI_GOTO'), 0)
        self.setParameter(self.getConst('ID_REG_SET_Z_M'), int(pos[2]*1000))

    def startScanner(self):
        """
        Starts the scanner.

        Returns
        -------
        None.

        """
        self.sendScannerCommand(self.getConst('SCANRUN_ON'))

    def stopScanner(self):
        """
        Stops the scanner.

        Returns
        -------
        None.

        """
        self.sendScannerCommand(self.getConst('SCANRUN_OFF'))

    def sendScannerCommand(self, command):
        """
        Starting the scanner is a little bit more complicated as it requires two commands
        with handshake. The function encapsulates the processing of all scanner commands.

        Parameters
        ----------
        command : str
            Constant name.

        Returns
        -------
        None.

        """
        outActive_was = self.getParameter( self.getConst('ID_OUTPUT_STATUS'), 0 )
        
        if (outActive_was == 0):
            self.setParameter( self.getConst('ID_OUTPUT_ACTIVATE'), 1, 0  )
            activeChecker = 0
            while ( activeChecker == 0 ):
                activeChecker = self.getParameter( self.getConst('ID_OUTPUT_STATUS'), 0 )
                print( "Output Status: ", activeChecker )
                time.sleep( .05 )
                
        if (command == self.getConst('SCANRUN_ON')):
            # Scan start requires two commands; the first one to move to the start position,
            # (which can take a long time), the second one to actually run the scan.
            # A rather simple approach: send command cyclically until the scanner is running
            state = 0
            while ( (state & self.getConst('SCANSTATE_SCAN')) == 0 ):
                self.setParameter( self.getConst('ID_SCAN_COMMAND'), command, 0 )
                time.sleep( .001 )
                state = self.getParameter( self.getConst('ID_SCAN_STATUS'), 0 )
                print( "Scanner State: ", end='' )
                if ( state & self.getConst('SCANSTATE_PAUSE')  ): print( "Pause ", end='' )
                if ( state & self.getConst('SCANSTATE_MOVING') ): print( "Move ",  end='' )
                if ( state & self.getConst('SCANSTATE_SCAN')   ): print( "Scan ",  end='' )
                if ( state & self.getConst('SCANSTATE_IDLE')   ): print( "Idle ",  end='' )
                if ( state & self.getConst('SCANSTATE_LOOP')   ): print( "Loop ",  end='' )
                print( "" )
        else:
            # Stop and pause only require one command
            self.setParameter( self.getConst('ID_SCAN_COMMAND'), command, 0 )
    
    def pollDataFull(self, frameSize, chn):
        """
        Polls the data while scanner is performing a scan.

        Parameters
        ----------
        frameSize : int
            framesize of data.
        chn : int
            Internal channel connected to scanner.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        event   = 0                                                 # Returncode of waitForEvent
                
        # Wait for full buffer on channel 0 and show progress
        while ( event == 0 ):
            event = self.waitForEvent(5, self.getConst('DYB_EVT_DATA_00'), 0 ) # TODO: Keep eye on this when changing channel
            pos = self.getScannerXYZRelPos()
            print( "Scanner at ", pos[0], " , ", pos[1], " nm" )
    
        # Read and print data frame, forward and backward scan in separate files
        print( "Reading frame; bufSize=", frameSize, ", frameSize=",
               self.getFrameSize( chn ) )
        out = self.getDataBuffer( chn, 1, frameSize)
        counts = out[3][:]
        meta = out[4]
        if ( frameSize > 0 ):
            return np.asarray(counts), meta
        return 0
    
    def closeScanner(self):
        """
        Deactivates scanner outputs.

        Returns
        -------
        None.

        """
        self.setParameter( self.getConst('ID_OUTPUT_ACTIVATE'), 0, 0  )
        self.waitForEvent( 5000, self.getConst('DYB_EVT_CUSTOM') , self.getConst('ID_OUTPUT_STATUS') )
        outActive = self.getParameter( self.getConst('ID_OUTPUT_STATUS'), 0 )
        if ( outActive != 0 ):
            print( "Outputs are not deactivated!" )
        else:
            print('Outputs deactivated')

