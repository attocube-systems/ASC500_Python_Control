# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 13:40:13 2021

@author: grundch
"""
import re
import time
import numpy as np
import enum
from .asc500_base import ASC500Base


class ScannerState(enum.Enum):
        PAUSE = 1
        MOVING = 2
        SCAN4 = 4
        SCAN6 = 6    # This differs from documentation (which says SCAN=4), but seems to work like this!
        IDLE = 8
        LOOP = 10

class ASC500Scanner(ASC500Base):
    
    def getScannerStateMoving(self):
        """
        This function retrieves if the scanner is in a moving or scanning state.
        
        Parameters
        ----------
        None.

        Returns
        -------
        moving : int
            [0, 1] scanner is [not moving, moving]
        """
        state = self.getParameter(self.getConst('ID_SCAN_STATUS'))
        if state == ScannerState.MOVING \
               or state == ScannerState.SCAN4 \
               or state == ScannerState.SCAN6 :
            moving = 1
        else:
            moving = 0
        return moving
    
    def getScannerState(self):
        """
        This function retrieves the scanner state.

        Parameters
        ----------
        None.

        Returns
        -------
        ScannerState : enum
            The state the scanner is currently in, see ScanerState class
        """
        state = self.getParameter(self.getConst('ID_SCAN_STATUS'))
        return ScannerState(state)
    
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
    
    def getScanOnce(self):
        """
        This function retrieves the scanners single scan property = if the scanner stops after the first run.

        Parameters
        ----------
        None.

        Returns
        -------
        once : int
            [0, 1] single scan [off, on]
        """
        once = self.getParameter(self.getConst('ID_SCAN_ONCE'))
        return once

    def setScanOnce(self, once):
        """
        This function sets the scanners single scan property.
        If set, the scanner stops after the first run.

        Parameters
        ----------
        once : int
            [0, 1] single scan [off, on]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_ONCE'), once)

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
        fixed = self.getParameter( self.getConst('ID_SCAN_GEOMODE'))
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
        self.setParameter( self.getConst('ID_SCAN_GEOMODE'), fixed)

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
    
    def getScannerCoordSystemZero(self):
        """
        Retrieves the currently set zero-position of the scanners coordinate system as list [coordX0, coordY0].

        Parameters
        ----------
        None.
        
        Returns
        -------
        coord0 : list
            [coordX0, coordY0] scanner coordinate system zero-position

        """
        coordX0 = self.getParameter(self.getConst('ID_SCAN_COORD_ZERO_X'))
        coordY0 = self.getParameter(self.getConst('ID_SCAN_COORD_ZERO_Y'))
        coord0 = [coordX0, coordY0]
        return coord0
    
    def getScannerAbsolutCoordSystem(self):
        """
        Retrieves the currently set origin of the scanners absolute coordinate system in [m].

        Parameters
        ----------
        None.
        
        Returns
        -------
        coordAbs : list
            [coordAbsX, coordAbsY] scanners new absolute coordinate system origin in [m].
        """
        coordAbsX = self.getParameter(self.getConst('ID_SCAN_COORD_MOVE_X'))*1e-11
        coordAbsY = self.setParameter(self.getConst('ID_SCAN_COORD_MOVE_Y'))*1e-11
        coordAbs = [coordAbsX, coordAbsY]
        return coordAbs

    def setScannerAbsolutCoordSystem(self, coordAbs):
        """
        Sets the new origin of the scanners absolute coordinate system as list in [m].

        Parameters
        ----------
        coordAbs : list
            [coordAbsX, coordAbsY] scanners new absolute coordinate system origin in [m].
        
        Returns
        -------
        None.
        """
        coordAbsX = coordAbs[0]
        coordAbsY = coordAbs[0]
        self.setParameter(self.getConst('ID_SCAN_COORD_MOVE_X'), coordAbsX *1e11)
        self.setParameter(self.getConst('ID_SCAN_COORD_MOVE_Y'), coordAbsY *1e11)
        self.sendScannerCommand(self.getConst('ID_SCAN_COORD_MOVE'))

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
    
    def pauseScanner(self):
        """
        Pauses the scanner.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        self.sendScannerCommand(self.getConst('SCANRUN_PAUSE'))

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
        state = self.getScannerStateMoving()
        if state == 1:
            self.sendScannerCommand(self.getConst('SCANRUN_OFF'))
            time.sleep(0.1)
        while self.getScannerStateMoving() == 1:
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
        Starts a scan relative to the current position (unless absolute=True, deltaX and deltaY will be interpreted as
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
            targetPos = [currPos[0] + deltaX, currPos[1] + deltaY]
        else:
            targetPos = [deltaX, deltaY]

        targetPos = [round(p, 9) for p in targetPos]    # 1nm precision

        # try:
        #     self._checkPositioningLimits(x=targetPos[0], y=targetPos[1])
        # except self.outOfLimitsError:
        #     raise

        # set scan origin to target position, for later fall-back when PathCtrl is turned off
        self.setScanFieldCentre(targetPos)

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
    
    def getScanFieldCentre(self):
        """
        This retrieves the scan field centre relative to the voltage origin in [m].
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        position : list
            [xPos, yPos] Positions of scan field centre in [m].
        """
        xPos = self.getParameter(self.getConst('ID_SCAN_OFFSET_X'))*1e-11
        yPos = self.getParameter(self.getConst('ID_SCAN_OFFSET_Y'))*1e-11
        return position

    def setScanFieldCentre(self, position):
        """
        This sets the scan field centre relative to the voltage origin in [m].
        
        Parameters
        ----------
        position : list
            [xPos, yPos] Positions of scan field centre in [m].
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_OFFSET_X'), position[0]*1e11)
        self.setParameter(self.getConst('ID_SCAN_OFFSET_Y'), position[1]*1e11)
    
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

    def getAccelerationMax(self):
        """
        This function retrieves the currently set maximum acceleration of the XY scanner in [m/s^2]
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        acceleration : float
            Acceleration in [m/s^2]
        """
        acceleration = self.getParameter(self.getConst('ID_SCAN_ACCEL'))*1e-6
        return acceleration

    def setAccelerationMax(self, acceleration):
        """
        This function sets the maximum acceleration of the XY scanner in [m/s^2]
        
        Parameters
        ----------
        acceleration : float
            Maximum acceleration in [m/s^2]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_ACCEL'), acceleration*1e6)

    def getAccelerationShare(self):
        """
        This function retrieves the currently set Scanner share of accel distance outside scanrange [%]
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        accelShare : float
            Scanner share of accel distance outside scanrange [%]
        """
        accelShare = self.getParameter(self.getConst('ID_SCAN_ACCEL_PRC'))
        return accelShare

    def setAccelerationShare(self, accelShare):
        """
        This function sets the Scanner share of accel distance outside scanrange [%]
        
        Parameters
        ----------
        accelShare : float
            Scanner share of accel distance outside scanrange [%]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_ACCEL_PRC'), accelShare)

    def getCLUseSensorPosition(self):
        """
        This function retrieves if the use of sensor position for closed loop is set.
        
        Parameters
        ----------
        None.

        Returns
        -------
        use : int
            [0, 1] use sensor position [off/on]
        """
        use = self.getParameter(self.getConst('ID_CL_USESENPOS'))
        return use

    def setCLUseSensorPosition(self, use):
        """
        This function sets the use of sensor position for closed loop.
        
        Parameters
        ----------
        use : int
            [0, 1] use sensor position [off/on]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_CL_USESENPOS'), use)
    
    def clearSaturationError(self):
        """
        This function clears the closed loop saturation error.
        
        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        self.sendScannerCommand(self.getConst('ID_CL_RESTORE'))
    
    def getCLSaturationStatus(self):
        """
        This function retrievs the closed loop saturation status.
        
        Parameters
        ----------
        None.

        Returns
        -------
        status : int
            Scanner saturation; 1=left, 2=right, 4=top, 8=bottom
        """
        status = self.getParameter(self.getConst('ID_CL_SATSTATUS'))
        return status
    
    def getDualLineON(self):
        """
        This function retrieves [0,1], if the dual line mode is set [off/on].
        
        Parameters
        ----------
        None.

        Returns
        -------
        state : int
            [0, 1] dual line mode [off/on]
        """
        state = self.getParameter(self.getConst('ID_SCAN_DUALLINE'))
        return state
    
    def setDualLineON(self, state):
        """
        This function sets the dual line mode [off/on].
        
        Parameters
        ----------
        state : int
            [0, 1] dual line mode [off/on]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_DUALLINE'), state)
    
    def getDualLineFeedback(self):
        """
        This function retrieves [0,1], the type of feedback for the dual line mode [feedback/1st line profile].
        
        Parameters
        ----------
        None.

        Returns
        -------
        feedback : int
            [0, 1] dual line mode feedback [feedback/1st line profile]
        """
        feedback = self.getParameter(self.getConst('ID_REG_MFM_EN'))
        return feedback
    
    def setDualLineFeedback(self, feedback):
        """
        This function sets the dual line mode feedback type [feedback/1st line profile].
        
        Parameters
        ----------
        feedback : int
            [0, 1] dual line mode feedback [feedback/1st line profile]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_MFM_EN'), feedback)

    def getDualLineLiftOffset(self):
        """
        This function retrieves the lift offset set for the dual line mode in [m].
        
        Parameters
        ----------
        None.

        Returns
        -------
        offset : float
            Dual line mode lift offset in [m]
        """
        offset = self.getParameter(self.getConst('ID_REG_MFM_OFF_M'))*1e-11
        return offset
    
    def setDualLineLiftOffset(self, offset):
        """
        This function sets the lift offset for the dual line mode in [m].
        
        Parameters
        ----------
        offset : float
            Dual line mode lift offset in [m]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_MFM_OFF_M'), offset*1e11)
    
    def getDualLineLiftSlewRate(self):
        """
        This function retrieves the lift slew rate set for the dual line mode in [m/s].
        
        Parameters
        ----------
        None.

        Returns
        -------
        slewrate : float
            Dual line mode lift slew rate in [m/s]
        """
        slewrate = self.getParameter(self.getConst('ID_REG_MFM_SLEW_M'))*1e-12
        return slewrate
    
    def setDualLineLiftSlewRate(self, slewrate):
        """
        This function sets the lift slew rate for the dual line mode in [m/s].
        
        Parameters
        ----------
        slewrate : float
            Dual line mode lift slew rate in [m/s]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_MFM_SLEW_M'), slewrate*1e12)
    
    def getDualLineWaitTime(self):
        """
        This function retrieves the wait time set for the dual line mode in [s].
        
        Parameters
        ----------
        None.

        Returns
        -------
        waittime : float
            Dual line mode wait time in [s]
        """
        waittime = self.getParameter(self.getConst('ID_DUALLINE_WAIT'))*1e-3
        return waittime
    
    def setDualLineWaitTime(self, waittime):
        """
        This function sets the wait time for the dual line mode in [s].
        
        Parameters
        ----------
        waittime : float
            Dual line mode wait time in [s]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_DUALLINE_WAIT'), waittime*1e3)
    
    def getDualLineAlternativeSetPointEnable(self):
        """
        This function retrieves if an alternative setpoint for the dual line mode is enabled.
        
        Parameters
        ----------
        None.

        Returns
        -------
        enabled : int
            [0, 1] Alternative setpoint [disabled/enabled]
        """
        enabled = self.getParameter(self.getConst('ID_DUALLINE_SP_EN'))
        return enabled

    def setDualLineAlternativeSetPointEnable(self, enable):
        """
        This function [disabled/enabled] the alternative setpoint for the dual line mode.
        
        Parameters
        ----------
        enable : int
            [0, 1] Alternative setpoint [disabled/enabled]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_DUALLINE_SP_EN'), enable)
    
    def getDualLineAlternativeSetPointValue(self):
        """
        This function retrieves the currently set alternative setpoint for the dual line mode.
        
        Parameters
        ----------
        None.

        Returns
        -------
        setpoint : int
            Alternative setpoint
        """
        setpoint = self.getParameter(self.getConst('ID_DUALLINE_SP_DISP'))
        return setpoint
    
    def getDualLineAlternativeSetPointValue(self, setpoint):
        """
        This function sets the alternative setpoint for the dual line mode.
        
        Parameters
        ----------
        setpoint : int
            Alternative setpoint

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_DUALLINE_SP_DISP'), setpoint)
    
    def getDualLineDACEnabled(self, DACOutput):
        """
        This function retrieves if an alternative DAC output for the dual line mode is enabled.
        
        Parameters
        ----------
        DACOutput : int
            DAC Output number

        Returns
        -------
        enabled : int
            [0, 1] Alternative DAC output [disabled/enabled]
        """
        enabled = self.getParameter(self.getConst('ID_DUALLINE_DAC_EN'), DACOutput)
        return enabled
    
    def setDualLineDACEnabled(self, DACOutput, enable):
        """
        This function [disabled/enabled] the alternative DAC output for the dual line mode.
        
        Parameters
        ----------
        DACOutput : int
            DAC Output number
        enable : int
            [0, 1] Alternative DAC output [disabled/enabled]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_DUALLINE_DAC_EN'), enable, DACOutput)
    
    def getDualLineDACValue(self, DACOutput):
        """
        This function retrieves the value of the alternative DAC output for the dual line.
        
        Parameters
        ----------
        DACOutput : int
            DAC Output number

        Returns
        -------
        output : float
            alternative DAC output value in [V]
        """
        output = self.getParameter(self.getConst('ID_DUALLINE_DAC'), DACOutput)*305.2*1e-6
        return output
    
    def setDualLineDACValue(self, DACOutput, output):
        """
        This function sets the value of the alternative DAC output for the dual line.
        
        Parameters
        ----------
        DACOutput : int
            DAC Output number
        output : float
            alternative DAC output value in [V]

        Returns
        -------
        """
        self.setParameter(self.getConst('ID_DUALLINE_DAC'), output/305.2*1e6, DACOutput)





    def getDualLineFrequencyEnabled(self):
        """
        This function retrieves if an alternative excitation frequency for the dual line mode is enabled.
        
        Parameters
        ----------
        None.

        Returns
        -------
        enabled : int
            [0, 1] Alternative excitation frequency [disabled/enabled]
        """
        enabled = self.getParameter(self.getConst('ID_DUALLINE_FEXC_EN'))
        return enabled
    
    def setDualLineFrequency(self, enable):
        """
        This function [disabled/enabled] the alternative excitation frequency for the dual line mode.
        
        Parameters
        ----------
        enable : int
            [0, 1] Alternative excitation frequency [disabled/enabled]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_DUALLINE_FEXC_EN'), enable)
    
    def getDualLineFrequency(self):
        """
        This function retrieves the value of the alternative excitation frequency for the dual line.
        
        Parameters
        ----------
        None.

        Returns
        -------
        frequency : float
            alternative excitation frequency value in [Hz]
        """
        frequency = self.getParameter(self.getConst('ID_DUALLINE_FEXC'))*1e-3
        return frequency
    
    def setDualLineFrequency(self, frequency):
        """
        This function sets the value of the alternative excitation frequency for the dual line.
        
        Parameters
        ----------
        frequency : float
            alternative excitation frequency value in [Hz]

        Returns
        -------
        """
        self.setParameter(self.getConst('ID_DUALLINE_FEXC'), frequency*1e3)







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

    def getScanFieldRotation(self):
        """
        This function retrieves the currently set rotation of the scan field in [deg]

        Parameters
        ----------
        None.

        Returns
        -------
        rotation : float
            Currently set scan field rotation in [deg]
        """
        rotation = self.getParameter(self.getConst('ID_SCAN_ROTATION')) *65536/360
        return rotation
    
    def setScanFieldRotation(self, rotation):
        """
        This function sets the rotation of the scan field in [deg]

        Parameters
        ----------
        rotation : float
            Scan field rotation in [deg]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SCAN_ROTATION'), rotation*360/65536)
        

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

