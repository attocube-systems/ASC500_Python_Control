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

    def ASC_errcheck(self, ret_code, func, args):
        """
        Checks and interprets the return value of daisybase calls.

        Parameters
        ----------
        ret_code : int
            Return value from the function
        func : function
            Function that is called
        args : list
            Parameters passed to the function

        Returns
        -------
        str
            String of the return code
        """
        # daisybase returns defined in "daisybase.h"
        DYB_RC = {
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

        if ret_code != 0:
            RuntimeError('Error: {:} '.format(DYB_RC[ret_code]) +
                         str(func.__name__) +
                         ' with parameters: ' + str(args))
        return DYB_RC[ret_code]

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
            The folder where daisysrv.exe is found.
        portNr : int
            Port number of the device.
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
            Identification of the parameter.
        index : int
            If defined for the parameter: subaddress, 0 otherwise.
        async_ : bool
            Enable for ASYNC call.

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
            Identification of the parameter.
        index : int
            If defined for the parameter: subaddress, 0 otherwise.
        async_ : bool
            Enable for ASYNC call. If enabled, you have to catch data via an
            event.

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

    def getOutputStatus(self):
        """
        Returns output status (*all* outputs) as a boolean: 0: off, 1: on.

        Returns
        -------
        list
            Output status of outputs.
        """
        return self._getParameter(self.getConst('ID_OUTPUT_STATUS'))

    def setOutputs(self, enable):
        """
        Activates or deactivates all outputs of the ASC500.

        Parameters
        ----------
        enable : int
            0: disable, 1: enable.
        """
        self._setParameter(self.getConst('ID_OUTPUT_ACTIVATE'), enable)

    def startServer(self):
        """
        Configures connection to daisybase and starts server.
        """
        binPath = self.serverPath.encode('utf-8')
        assert os.path.isdir(binPath)
        self._init(0, binPath, 0, self.portNr)
        self._run()

    def stopServer(self):
        """
        Configures connection to daisybase and starts server.
        """
        self._stop()

