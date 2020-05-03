# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:28:24 2020

@author: schaecl
"""

import time
import ctypes as ct
from enum import Enum
from asc500_base import ASC500Base
import numpy as np

class ASC500ScannerXY(ASC500Base):
    # Address definitions
    # Scanner coordinates
    _SCAN_CURR_X = 0x002A # Scanner position relative to voltage origin X [10pm]
    _SCAN_CURR_Y = 0x002B # Scanner position relative to voltage origin Y [10pm]
    # Scanner settings
    _SCAN_OFFSET_X = 0x0010 # Centre of the scanfield, relative to origin [10pm] in X
    _SCAN_OFFSET_Y = 0x0011 # Centre of the scanfield, relative to origin [10pm] in Y
    _SCAN_PIXEL = 0x1021 # Pixel size [10pm]
    _SCAN_PSPEED = 0x100B # Positioning speed [nm/s]
    # Scanner command
    _SCAN_COMMAND = 0x0100 # Scanner command (SCANRUN_ constants)
    # Scanner state
    _SCAN_STATUS = 0x0101 # Scanner running state
    # Path mode
    _PATH_CTRL = 0x0263 # Pathmode mode: -1=grid, >1=no of points of path
    _PATH_EXTTRIG_EDGE = 0x0272 # Pathmode edge of external trigger (0=rising, 1=falling)
    _PATH_XPOINT = 0x1302 # Position in [10pm]. Index corresponds to point number
    _PATH_YPOINT = 0x1303 # Position in [10pm]. Index corresponds to point number

    class ScannerState(Enum):
        PAUSE = 1
        MOVING = 2
        SCAN = 6 # This differs from documentation (which says SCAN=4), but seems to work like this!
        IDLE = 8
        LOOP = 10

    def getStatus(self):
        """
        Returns status of the scanner, as a ScannerState object.
        """
        state = self._getParameter(self._SCAN_STATUS)
        return self.ScannerState(state)

    @staticmethod
    def unitConversion(type_, value, reverse=False):
        """
        Takes care of unit conversion from SI-unit to scanner unit (and vice-versa).
        type [str]: distinguishes the type of the input number
        value [float]: number that is to be converted
        reverse [bool]: if true, conversion is scanner-unit to SI-unit
        """
        convFactor = 1
        if type_ == 'Position':
            # position unit is 10pm: m -> 10pm
            convFactor = 1e11
        elif type_ == 'Velocity':
            # scanner unit is nm/s: m/s -> nm/s
            convFactor = 1e9
        if reverse:
            return value / convFactor
        return np.round(value * convFactor)

    @property
    def position(self):
        """
        Returns current scanner position as a list [x, y] in [m]
        """
        xCurrent = self._getParameter(self._SCAN_CURR_X)
        yCurrent = self._getParameter(self._SCAN_CURR_Y)
        xPos = self.unitConversion('Position', xCurrent, reverse=True)
        yPos = self.unitConversion('Position', yCurrent, reverse=True)
        return [xPos, yPos]

    @position.setter
    def position(self, newPos):
        """
        Sets current scanner position. Input as a list [x, y] in [m]
        """
        currPos = self.position

        # the following checks whether the starting and target positions are
        # the same. This is needed to avoid triggering the start of a scan
        if not (abs(newPos[0] - currPos[0]) < 2e-9 and abs(newPos[1] - currPos[1]) < 2e-9):
            # set scan window to zero size (i.e. the scan origin corresponds to the position)
            self._setParameter(self._SCAN_PIXEL, 0)
            # set scan origin
            self.setRelativeOrigin(newPos)
            # move to new origin (will not actually start a scan!)
            self._setParameter(self._SCAN_COMMAND, 1)

    def stopStage(self):
        """
        Turns off current Scan and Path mode.
        """
        if self.getStatus() == self.ScannerState.SCAN:
            self._setParameter(self._SCAN_COMMAND, 0)
        while self.getStatus() == self.ScannerState.MOVING:
            time.sleep(0.1)

    def triggeredScan(self, delX, delY, duration, absolute=False):
        """
        Starts a scan relative to the current position (unless absolute=True,
        delX and delY will be interpreted as absolute positions instead!).
        Duration determines the scanner speed. The scan start is triggered
        externally
        """
        # determine target position
        currPos = self.position
        if not absolute:
            targetPos = [currPos[0] + delX, currPos[1] + delY]
        else:
            targetPos = [delX, delY]

        # set scan origin to target position, for later fall-back when PathCtrl is turned off
        self.setRelativeOrigin(targetPos)

        # calculate and set scanner velocity
        scanLength = np.sqrt(np.sum((np.array(currPos) - np.array(targetPos))**2))
        scanSpeed = scanLength/duration
        self.velocity = scanSpeed

        # set pathmode settings:
        currPos = [self.unitConversion('Position', cP) for cP in currPos]
        targetPos = [self.unitConversion('Position', tP) for tP in targetPos]

        self._setParameter(self._PATH_XPOINT, currPos[0], index=0) # start point is current position
        self._setParameter(self._PATH_XPOINT, targetPos[0], index=1) # target point

        self._setParameter(self._PATH_YPOINT, currPos[1], index=0) # start point is current position
        self._setParameter(self._PATH_YPOINT, targetPos[1], index=1) # target point

        # set trigger action
        self._setParameter(self._PATH_EXTTRIG_EDGE, 1) # set trigger edge to falling

        # start path control
        # start Path mode with two coordinates (start, target)
        self._setParameter(self._PATH_CTRL, 2)

    def setRelativeOrigin(self, pos):
        """
        This sets the scanner origin relative to the voltage origin. We use it
        to move around within the coordinate system defined by the voltage
        origin. Input is the position as a list [x, y] in [m].
        """
        self._setParameter(self._SCAN_OFFSET_X, self.unitConversion('Position', pos[0]))
        self._setParameter(self._SCAN_OFFSET_Y, self.unitConversion('Position', pos[1]))

    @property
    def velocity(self):
        """
        Returns positioning speed in [m/s]
        """
        v = self._getParameter(self._SCAN_PSPEED)
        return self.unitConversion('Velocity', v, reverse=True)

    @velocity.setter
    def velocity(self, v):
        """
        Sets positioning speed, input as a float in [m/s]
        """
        v = self.unitConversion('Velocity', v)
        self._setParameter(self._SCAN_PSPEED, v)

if __name__ == "__main__":

    server_loc = '01 ASC500 Installer and Data\\ASC500CL-18_11_13'
    dll_loc_64 = '04 ASC500 64bit libraries\\ASC500CL-LIB-WIN64-18_11_13\\daisybase\\lib\\'
    dll_loc_32 = '01 ASC500 Installer and Data\\ASC500CL-18_11_13\\daisybase\\lib\\'

    xystage = ASC500ScannerXY(server_loc,
                              7000,
                              dll_loc_64)

    xystage.startServer()
    time.sleep(2)
    xystage.velocity = 3e-6
    xystage._setParameter(xystage._SCAN_PIXEL, 0)
    xystage.output = 1
    time.sleep(2)

    workingPosition = [2.000005e-05, 2.262754e-05]
    notWorkingPosition = [2.000005e-05, 2.256741e-05]

    print('Line 257')

    xystage.position = notWorkingPosition
#    xystage.position = workingPosition
    time.sleep(2)

    print('Line 262')

    while xystage.getStatus() == xystage.ScannerState.MOVING:
        time.sleep(0.1)

    print('Line 267')

    # make sure that Scanner and PATH-Mode are off
    xystage.stopStage()
    xystage.triggeredScan(10e-6, 0, 5)

    print('We are out')