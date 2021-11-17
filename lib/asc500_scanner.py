# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 13:40:13 2021

@author: grundch
"""
import re
import time
import numpy as np
import enum
from lib.asc500_base import ASC500Base


class ScannerState(enum.Enum):
        PAUSE = 1
        MOVING = 2
        SCAN4 = 4
        SCAN6 = 6    # This differs from documentation (which says SCAN=4), but seems to work like this!
        IDLE = 8
        LOOP = 10

class ASC500Scanner(ASC500Base):
    
    def getScannerState(self):
        state = self.getParameter(self.getConst('ID_SCAN_STATUS'))
        if state == ScannerState.MOVING \
               or state == ScannerState.SCAN4 \
               or state == ScannerState.SCAN6 :
            return 1
        else:
            return 0
        return ScannerState(state)
    
    @staticmethod
    def unitConversion(type, value, reverse=False):
        """Takes care of unit conversion from SI-unit to scanner unit (and vice-versa).
           type [str]: distinguishes the type of the input number
           value [float]: number that is to be converted
           reverse [bool]: if true, conversion is scanner-unit to SI-unit"""
        convFactor = 1
        if type == 'Voltage':
            # scanner unit is 350 uV: V -> 350uV
            convFactor = 1/305.2*1e6
        elif type == 'Position':
            # position unit is 10pm: m -> 10pm
            convFactor = 1e11
        elif type == 'Temperature':
            # scanner unit is mK: K -> mK
            convFactor = 1e3
        elif type == 'Velocity':
            # scanner unit is nm/s: m?s -> nm/s
            convFactor = 1e9
        elif type == 'Frequency':
            # ASC unit is mHz: Hz -> mHz
            convFactor = 1e3
        elif type == 'Proportional':
            # Proportional part of PI, in units of 1e-6: 1 -> 1e-6
            convFactor = 1e6
        elif type == 'TF Phase':
            # scanner unit is 83.82 ndeg: 1 deg -> 83.82 ndeg
            convFactor = 1/83.82*1e9
        elif type == 'TF Time':
            # scanner unit is 20ns: 1 s -> 20ns
            convFactor = 1/20*1e9
        elif type == 'TF exc Voltage':
            # scanner unit is 19.074 uV: 1 V -> 19.074 uV 
            convFactor = 1/19.074*1e6
        elif type == 'TF det Voltage':
            # scanner unit is 305.2 uV: 1 V -> 305.2 uV
            convFactor = 1/305.2*1e6
        elif type == 'AAP Speed':
            # scanner unit is 976.6 uV/s: 1 V -> 976.6 uV
            convFactor = 1/976.6*1e6
        if reverse:
            return value/convFactor
        return int(value*convFactor)
    
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
    
    def getGeoMode(self):
        """
        Retrieves if the aspect ratio of the scan is set fixed.

        Parameters
        ----------
        None.

        Returns
        -------
        fixed : int
            [0, 1] fixed X and Y [off, on]
        """
        fixed = self.getParameter( self.getConst('ID_SCAN_X_EQ_Y'))
        return fixed

    def setGeoMode(self, fixed):
        """
        Sets the aspect ratio of the scan as fixed.

        Parameters
        ----------
        fixed : int
            [0, 1] fixed X and Y [off, on]

        Returns
        -------
        None.
        """
        self.setParameter( self.getConst('ID_SCAN_X_EQ_Y'), fixed)

    def getXEqualY(self):
        """
        Retrieves if the size of lines and columns of the scanner are set as equal.

        Parameters
        ----------
        None.

        Returns
        -------
        equal : int
            [0, 1] equal X and Y [off, on]
        """
        equal = self.getParameter( self.getConst('ID_SCAN_X_EQ_Y'))
        return equal

    def setXEqualY(self, equal):
        """
        Sets the size of lines and columns of the scanner as equal.

        Parameters
        ----------
        equal : int
            [0, 1] equal X and Y [off, on]

        Returns
        -------
        None.
        """
        self.setParameter( self.getConst('ID_SCAN_X_EQ_Y'), equal)

    def getSamplingTime(self):
        """
        Retrieves the sampling time of the scanner.

        Parameters
        ----------
        None.

        Returns
        -------
        samplingtime : float
            Sampling time in [s]
        """
        samplingtime = self.getParameter( self.getConst('ID_SCAN_MSPPX'))*2.5*1e-6
        return samplingtime

    def setSamplingTime(self, samplingtime):
        """
        Retrieves the sampling time of the scanner.

        Parameters
        ----------
        samplingtime : float
            Sampling time in [s]

        Returns
        -------
        None.
        """
        self.setParameter( self.getConst('ID_SCAN_MSPPX'), samplingtime/2.5*1e6)
    
    def resetScannerCoordSystem(self):
        """
        Resets the coordinate system of the scanner.

        Parameters
        ----------
        None.

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
    
    def setOutputsActive(self):
        """
        Activates the output of the scanner.

        Parameters
        ----------
        None.
        
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

    def getPositionsXYRel(self):
        """
        Get the scanner x and y position relative to the voltage origin as list.

        Parameters
        ----------
        None.

        Returns
        -------
        positions : list
            [xPos, yPos] relative position in m.

        """
        xPos = self.getParameter(self.getConst('ID_SCAN_CURR_X'), 0)*1e-11
        yPos = self.getParameter(self.getConst('ID_SCAN_CURR_Y'), 0)*1e-11
        positions = [xPos, yPos]
        return positions
    
    def setPositionsXYRel(self, positions):
        """
        Sets the scanners x and y position relative to the voltage origin as list.

        Parameters
        ----------
        positions : list
            [xPos, yPos] relative positions in m.

        Returns
        -------
        None.

        """
        # try:
        #     self._checkPositioningLimits(x=positions[0], y=positions[1])
        # except self.outOfLimitsError:
        #     raise
            
        currPos = self.getPositionsXYRel()
        # the following checks whether the starting and target positions are the same. This is needed
        # to avoid triggering the start of a scan
        if not (abs(positions[0] - currPos[0]) < 2e-9 and abs(positions[1] - currPos[1]) < 2e-9):
            self.setParameter(self.getConst('ID_POSI_TARGET_X'), positions[0]*1e11) #asc takes inputs in 10pm
            self.setParameter(self.getConst('ID_POSI_TARGET_Y'), positions[1]*1e11) 
            self.setParameter(self.getConst('ID_POSI_GOTO'), 0)

    def getPositionsXYZRel(self):
        """
        Get the scanner x, y and z positions relative to the voltage origin.

        Parameters
        ----------
        None.

        Returns
        -------
        positions : list
            [xPos, yPos, zPos] relative positions in m.

        """
        xPos = self.getParameter(self.getConst('ID_SCAN_CURR_X'), 0)*1e-11
        yPos = self.getParameter(self.getConst('ID_SCAN_CURR_Y'), 0)*1e-11
        zPos = self.getParameter(self.getConst('ID_REG_GET_Z_M'), 0)*1e-12
        positions = [xPos, yPos, zPos]
        return positions
    
    def setPositionsXYZRel(self, positions):
        """
        Sets the scanner x, y and z positions relative to the voltage origin.

        Parameters
        ----------
        position : list
            [xPos, yPos, zPos] relative positions in m.

        Returns
        -------
        None.

        """
        currPos = self.getPositionsXYRel()
        # try:
        #     self._checkPositioningLimits(x=position[0], y=position[1])
        # except self.outOfLimitsError:
        #     raise
        if not (abs(positions[0] - currPos[0]) < 2e-9 and abs(positions[1] - currPos[1]) < 2e-9):
            self.setParameter(self.getConst('ID_POSI_TARGET_X'), positions[0]*1e11) #asc takes inputs in 10pm
            self.setParameter(self.getConst('ID_POSI_TARGET_Y'), positions[1]*1e11) 
            self.setParameter(self.getConst('ID_POSI_GOTO'), 0)
            self.setParameter(self.getConst('ID_REG_SET_Z_M'), positions[2]*1e12)

    def startScanner(self):
        """
        Starts the scanner.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        self.sendScannerCommand(self.getConst('SCANRUN_ON'))

    def stopScanner(self):
        """
        Stops the scanner.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        state = self.getScannerState()
        if state == 1:
            self.sendScannerCommand(self.getConst('SCANRUN_OFF'))
            time.sleep(0.1)
        while self.getScannerState() == 1:
            self.sendScannerCommand(self.getConst('SCANRUN_OFF'))
            time.sleep(0.1)
        if self.getParameter(self.getConst('ID_EXTTRG_STATUS')):
            self.setParameter(self.getConst('ID_SPEC_PATHCTRL'), 0)  # stop path ctrl in case it's running
            time.sleep(0.05)

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
    
    def triggeredScan(self, deltaX, deltaY, duration, absolute=False):
        """
        Starts a scan relative to the current position (unless absolute=True, delX and delY will be interpreted as
        absolute positions instead!). Duration determines the scanner speed. The scan start is triggered externally
        
        Parameters
        ----------
        deltaX : float
            Width of the scan in [m].
        deltaY : float
            Height of the scan in [m].

        duration : float
            Duration of the scan in [s].

        Returns
        -------
        None.
        """
        # This was never tested in house...

        # make sure that Scanner and PATH-Mode are off
        self.stopScanner()

        # determine target position
        currPos = self.positionXYZRel
        if not absolute:
            targetPos = [currPos[0] + delX, currPos[1] + delY]
        else:
            targetPos = [delX, delY]

        targetPos = [round(p, 9) for p in targetPos]    # 1nm precision

        # try:
        #     self._checkPositioningLimits(x=targetPos[0], y=targetPos[1])
        # except self.outOfLimitsError:
        #     raise

        # set scan origin to target position, for later fall-back when PathCtrl is turned off
        self.setRelativeOrigin(targetPos)

        # calculate and set scanner velocity
        scanLength = np.sqrt(np.sum((np.array(currPos) - np.array(targetPos))**2))
        scanSpeed = scanLength/duration
        self.velocity = scanSpeed

        # set pathmode settings:
        # the current position is shifted by 0.25nm to avoid scanning issues.
        currPos = [((cP*1e11) + 0.25e-9) for cP in currPos]
        targetPos = [((tP*1e11) - 0.25e-9) for tP in targetPos]
        self.setParameter(self.getConst('ID_PATH_GUI_X'), currPos[0], index=0)  # start point is current position
        self.setParameter(self.getConst('ID_PATH_GUI_X'), targetPos[0], index=1)    # target point

        self.setParameter(self.getConst('ID_PATH_GUI_Y'), currPos[1], index=0)  # start point is current position
        self.setParameter(self.getConst('ID_PATH_GUI_Y'), targetPos[1], index=1)  # target point

        # set trigger action
        self.setParameter(self.getConst('ID_EXTTRG_HS'), 1)        # enables the external trigger
        self.setParameter(self.getConst('ID_PATH_ACTION'), 1, index=0)   # defines single action
        self.setParameter(self.getConst('ID_PATH_ACTION'), 4, index=1)   # defines this action to be an external trigger
        self.setParameter(self.getConst('ID_EXTTRG_EDGE'), 0)      # set trigger edge to rising

        # start path control
        self.setParameter(self.getConst('ID_SPEC_PATHCTRL'), 2)  # start Path mode with two coordinates (start, target)
        time.sleep(0.05)
    
    def setRelativeOrigin(self, position):
        """
        This sets the scanner origin relative to the voltage origin.
        
        Parameters
        ----------
        position : list
            [xPos, yPos] Positions of relative origin in [m].
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_OFFSET_X'), pos[0]*1e11)
        self.setParameter(self.getConst('ID_SCAN_OFFSET_Y'), pos[1]*1e11)
    
    def getPositioningSpeed(self):
        """
        This function retrieves the positioning speed of the XY scanner in [m/s]
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        speed : float
            Positioning speed in [m/s]
        """
        speed = self.getParameter(self.getConst('ID_SCAN_PSPEED'))*1e-9
        return speed

    def setPositioningSpeed(self, speed):
        """
        This function sets the positioning speed of the XY scanner in [m/s]
        
        Parameters
        ----------
        speed : float
            Positioning speed in [m/s]

        Returns
        -------
        """
        self.setParameter(self.getConst('ID_SCAN_PSPEED'), speed*1e9)

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
        counts : array
            Array of data
        meta : array
            related meta data (to convert into physical values).

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

        Parameters
        ----------
        None.

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
    

    def getPixelSize(self):
        """
        This function retrieves the currently set pixel size of a scan in [m]

        Parameters
        ----------
        None.

        Returns
        -------
        pixelsize : float
            Scanning pixel size in [m]

        """
        pixelsize = self.getParameter(self.getConst('ID_SCAN_PIXEL')) *1e-11
        return pixelsize

    def setPixelSize(self, pixelsize):
        """
        This function sets the pixel size of a scan in [m]

        Parameters
        ----------
        pixelsize : float
            Scanning pixel size in [m]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_PIXEL'), pixelsize*1e11)


    def getNumberOfColumns(self):
        """
        This function retrieves the currently set number of columns of a scan

        Parameters
        ----------
        None.

        Returns
        -------
        columns : int
            Scanning number of columns
        """
        columns = self.getParameter(self.getConst('ID_SCAN_COLUMNS'))
        return columns

    def setNumberOfColumns(self, columns):
        """
        This function sets the number of columns of a scan

        Parameters
        ----------
        columns : int
            Scanning number of columns

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_COLUMNS'), columns)

    def getNumberOfLines(self):
        """
        This function retrieves the currently set number of lines of a scan

        Parameters
        ----------
        None.

        Returns
        -------
        lines : int
            Scanning number of lines
        """
        lines = self.getParameter(self.getConst('ID_SCAN_LINES'))
        return lines

    def setNumberOfLines(self, lines):
        """
        This function sets the number of lines of a scan

        Parameters
        ----------
        lines : int
            Scanning number of lines

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_LINES'), lines)
        
    
    # def _checkPositioningLimits(self, x=None, y=None):
    #     """Checks whether x/y are within the current travel limits, raises exception if not"""
    #     # print(f"x={x}, self.xActualTravelLimit={self.xActualTravelLimit}")
        
    #     if x is not None:
    #         if not 0 <= x <= self.xActualTravelLimit:
    #             raise self.outOfLimitsError(1)

    #     if y is not None:
    #         if not 0 <= y <= self.yActualTravelLimit:
    #             raise self.outOfLimitsError(2)
    
    # class outOfLimitsError(Exception):
    #         """Error Handling for xyStage, e.g. if positioning limits are reached"""
    
    #         def __init__(self, errorCode):
    #             messages = {
    #                 1: "xyStage Error: X stage position out of limits",
    #                 2: "xyStage Error: Y stage position out of limits",
    #             }
    #             super().__init__(messages[errorCode])
    #             self.errorCode = errorCode

