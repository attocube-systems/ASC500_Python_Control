import time
import ctypes as ct
import os
from enum import Enum
import asc500_const
import numpy as np

#%%

class ASC500Base:
    """
    Base class for ASC500, consisting of error handling, wrapping of the DBY
    parameter set and get functions and server communication functionality.
    """

    _OUTPUT_ACTIVATE = getConst('ID_OUTPUT_ACTIVATE')
    _OUTPUT_STATUS = getConst('ID_OUTPUT_STATUS')

    def ASC_errcheck(self, code, func, args):
        """
        Checks and interprets the return value of daisybase calls.

        Parameters
        ----------
        code : int
            Return value from the function
        func : function
            Function that is called
        args : list
            Parameters passed to the function
        """
        # daisybase returns defined in "daisybase.h"
        DYB_Rc = {
            0 : "No error",
            1 : "Unknown / other error",
            2 : "Communication timeout",
            3 : "No contact to controller via USB",
            4 : "Error when calling USB driver",
            5 : "Controller boot image not found",
            6 : "Server executable not found",
            7 : "No contact to the server",
            8 : "Invalid parameter in function call",
            9 : "Call in invalid thread context",
            10 : "Invalid format of profile file",
            11 : "Can't open specified file"}

        if code != DYB_Rc[0]:
            RuntimeError('Error: {:}'.format(DYB_Rc[code]) +
                         str(func.__name__) +
                         ' with parameters: ' + str(args))
        return code

    def getConst(self, symbol):
        """
        Gets string and returns constant defined in ASC500 headers.

        Parameters
        ----------
        symbol : str
            Constant name.

        Returns
        -------
        int
            Integer of constant.
        """
        return int(asc500_const.cc.get(symbol), base=16)

    def __init__(self, serverPath, portNr, dllPath):
        """
        Initialises the class.

        Parameters
        ----------
        serverPath : str
            The folder where daisysrv.exe is found
        portNr : int
            Port number of the device
        """
        dll_loc = dllPath + 'daisybase.dll'
        assert os.path.isfile(dll_loc)
        assert os.path.isdir(serverPath)
        API = ct.cdll.LoadLibrary(dll_loc)
        self.serverPath = serverPath
        self.portNr = portNr

        # Aliases for the functions from the dll. For handling return
        # values: '.errcheck' is an attribute from ctypes.
        # Taken from daisybase.h,v 1.13 2016/10/24 17:55:23
        self._DataCallback = API.DYB_DataCallback
        self._DataCallback.errcheck = self.ASC_errcheck
        self._EventCallback = API.DYB_EventCallback
        self._EventCallback.errcheck = self.ASC_errcheck

        self._init = API.DYB_init
        self._init.errcheck = self.ASC_errcheck
        self._run = API.DYB_run
        self._run.errcheck = self.ASC_errcheck
        self._stop = API.DYB_stop
        self._stop.errcheck = self.ASC_errcheck
        self._reset = API.DYB_reset
        self._reset.errcheck = self.ASC_errcheck

        self._setDataCallback = API.DYB_setDataCallback
        self._setDataCallback.errcheck = self.ASC_errcheck
        self._setEventCallback = API.DYB_setEventCallback
        self._setEventCallback.errcheck = self.ASC_errcheck

        self._setParameterASync = API.DYB_setParameterAsync
        self._setParameterASync.errcheck = self.ASC_errcheck
        self._setParameterSync = API.DYB_setParameterSync
        self._setParameterSync.errcheck = self.ASC_errcheck

        self._getParameterASync = API.DYB_getParameterAsync
        self._getParameterASync.errcheck = self.ASC_errcheck
        self._getParameterSync = API.DYB_getParameterSync
        self._getParameterSync.errcheck = self.ASC_errcheck

        self._sendProfile = API.DYB_sendProfile
        self._sendProfile.errcheck = self.ASC_errcheck

        # Aliases for the functions from the dll. For handling return
        # values: '.errcheck' is an attribute from ctypes.
        # Taken from daisydata.h,v 1.4 2016/12/01 18:02:32
        self._printRc = API.DYB_printRc
        self._printRc.errcheck = self.ASC_errcheck
        self._printUnit = API.DYB_printUnit
        self._printUnit.errcheck = self.ASC_errcheck
        self._configureChannel = API.DYB_configureChannel
        self._configureChannel.errcheck = self.ASC_errcheck
        self._getChannelConfig = API.DYB_getChannelConfig
        self._getChannelConfig.errcheck = self.ASC_errcheck
        self._configureDataBuffering = API.DYB_configureDataBuffering
        self._configureDataBuffering.errcheck = self.ASC_errcheck
        self._getFrameSize = API.DYB_getFrameSize
        self._getFrameSize.errcheck = self.ASC_errcheck
        self._getDataBuffer = API.DYB_getDataBuffer
        self._getDataBuffer.errcheck = self.ASC_errcheck
        self._writeBuffer = API.DYB_writeBuffer
        self._writeBuffer.errcheck = self.ASC_errcheck
        self._waitForEvent = API.DYB_waitForEvent
        self._waitForEvent.errcheck = self.ASC_errcheck

        # Aliases for the functions from the dll. For handling return
        # values: '.errcheck' is an attribute from ctypes.
        # Taken from metadata.h,v 1.12.8.1 2018/10/11 08:50:55
        self._getOrder = API.DYB_getOrder
        self._getOrder.errcheck = self.ASC_errcheck
        self._getPointsX = API.DYB_getPointsX
        self._getPointsX.errcheck = self.ASC_errcheck
        self._getPointsY = API.DYB_getPointsY
        self._getPointsY.errcheck = self.ASC_errcheck
        self._getUnitXY= API.DYB_getUnitXY
        self._getUnitXY.errcheck = self.ASC_errcheck
        self._getUnitVal = API.DYB_getUnitVal
        self._getUnitVal.errcheck = self.ASC_errcheck
        self._getRotation = API.DYB_getRotation
        self._getRotation.errcheck = self.ASC_errcheck
        self._getPhysRangeX = API.DYB_getPhysRangeX
        self._getPhysRangeX.errcheck = self.ASC_errcheck
        self._getPhysRangeY = API.DYB_getPhysRangeY
        self._getPhysRangeY.errcheck = self.ASC_errcheck
        self._convIndex2Pixel = API.DYB_convIndex2Pixel
        self._convIndex2Pixel.errcheck = self.ASC_errcheck
        self._convIndex2Direction = API.DYB_convIndex2Direction
        self._convIndex2Direction.errcheck = self.ASC_errcheck
        self._convIndex2Phys1 = API.DYB_convIndex2Phys1
        self._convIndex2Phys1.errcheck = self.ASC_errcheck
        self._convIndex2Phys2 = API.DYB_convIndex2Phys2
        self._convIndex2Phys2.errcheck = self.ASC_errcheck
        self._convValue2Phys = API.DYB_convValue2Phys
        self._convValue2Phys.errcheck = self.ASC_errcheck
        self._convPhys2Print = API.DYB_convPhys2Print
        self._convPhys2Print.errcheck = self.ASC_errcheck

    def _getParameter(self, address, index=0, async_=False):
        """
        A/Synchronous inquiry about a parameter.
        The function sends an inquiry about a single parameter value to the
        server and waits for the answer. This may take a few ms at most.
        The function must not be called in the context of a data or event
        callback.

        Parameters
        ----------
        address : int
            Identification of the parameter
        index : int
            If defined for the parameter: subaddress, 0 otherwise
        async_ : bool
            Enable for ASYNC call

        Returns
        -------
        data.value : int
            The return of the SYNC call. In case of ASYNC, returns 0.
        """
        data = ct.c_int32(0)
        if not async_:
            self._getParameterSync(address, index, ct.byref(data))
        else:
            self._getParameterASync(address, index)
        return data.value

    def _setParameter(self, address, value, index=0, async_=False):
        """
        Generic function that sends a single parameter value to the server and
        waits for the acknowledgement. The acknowledged value is returned.
        The semantics depends on the address and the index (if applicable).
        The function must not be called in the context of a data or event
        callback.

        Parameters
        ----------
        address : int
            Identification of the parameter
        index : int
            If defined for the parameter: subaddress, 0 otherwise
        async_ : bool
            Enable for ASYNC call

        Returns
        -------
        ret.value : int
            The return of the SYNC call. In case of ASYNC, returns 0.
        """
        value = ct.c_int32(int(value))
        ret = ct.c_int32(0)
        if not async_:
            self._setParameterSync(address, index, value, ct.byref(ret))
        else:
            self._setParameterASync(address, index, value)
        return ret.value

    @property
    def output(self):
        """
        Returns output status (*all* outputs) as a boolean: 0: off, 1: on.
        """
        return self._getParameter(self._OUTPUT_STATUS)

    @output.setter
    def output(self, enable):
        """
        Activates or deactivates all outputs of the ASC500.

        Parameters
        ----------
        enable : int
            0: disable, 1: enable
        """
        self._setParameter(self._OUTPUT_ACTIVATE, enable)

    def startServer(self):
        """
        Configures connection to daisybase and starts server.
        """
        binPath = self.serverPath.encode('utf-8')
        assert os.path.isdir(binPath)
        self._init(0, binPath, 0, self.portNr)
        # Run daisybase (without GUI)
        self._run()

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
