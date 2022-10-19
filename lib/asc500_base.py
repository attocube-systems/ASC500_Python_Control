
import ctypes as ct
import os
from .asc500_const import ASC500Const
import time
import numpy as np

#%%

class ASC500Base():
    """
    Base class for ASC500, consisting of error handling, wrapping of the DBY
    parameter set and get functions and server communication functionality.

    Parameters
    ----------
    binPath : str
        The folder where daisysrv.exe is found.
    dllPath : str
        The folder where daisybase.dll is found.
    portNr : int
        Port number of the device.
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
            raise RuntimeError('Error: {:} '.format(DYB_RC[ret_code]) +
                               str(func.__name__) +
                               ' with parameters: ' + str(args))
        return DYB_RC[ret_code]

    def ASC_metaErrcheck(self, ret_code, func, args):
        """
        Checks and interprets the return value of daisymeta calls.

        Parameters
        ----------
        ret_code : int
            Return value from the function.
        func : function
            Function that is called.
        args : list
            Parameters passed to the function.

        Returns
        -------
        str
            String of the return code.
        """
        # daisybase returns defined in "daisymeta.h"
        DYB_RC = {
            0 : "Function call was successful",
            1 : "Function not applicable for current data order",
            2 :  "Meta data set is invalid"}

        if ret_code != 0:
            raise RuntimeError('Error: {:} '.format(DYB_RC[ret_code]) +
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
        return int(ASC500Const.cc.get(symbol), base=0)

    def __init__(self, binPath, dllPath, portNr=-1):
        """
        Initialises the class. Make sure to have a complete installation of
        the Daisy software ready.

        Parameters
        ----------
        binPath : str
            The folder where daisysrv.exe is found.
        dllPath : str
            The folder where daisybase.dll is found.
        portNr : int
            Port number of the device.
        """
        dll_loc = dllPath + 'daisybase.dll'
        assert os.path.isfile(dll_loc)
        assert os.path.isdir(binPath)
        API = ct.cdll.LoadLibrary(dll_loc)
        self.binPath = binPath
        if portNr == -1:
            self.portNr = self.getConst('ASC500_PORT_NUMBER')
        else:
            self.portNr = portNr

        # Minimum exposure time of counter
        self.minExpTime = 2.5e-6

        # Aliases for the functions from the dll. For handling return
        # values: '.errcheck' is an attribute from ctypes.
        # Taken from daisybase.h,v 1.13 2016/10/24 17:55:23

        try:
            self._DataCallback = API.DYB_DataCallback
            self._DataCallback.errcheck = self.ASC_errcheck
            self._EventCallback = API.DYB_EventCallback
            self._EventCallback.errcheck = self.ASC_errcheck
        except:
            print("DYB_DataCallback or DYB_EventCallback not exported.")

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
        self._printRc.restype = ct.c_char_p
        self._printUnit = API.DYB_printUnit
        self._printUnit.restype = ct.c_char_p
        self._configureChannel = API.DYB_configureChannel
        self._configureChannel.errcheck = self.ASC_errcheck
        self._getChannelConfig = API.DYB_getChannelConfig
        self._getChannelConfig.errcheck = self.ASC_errcheck
        self._configureDataBuffering = API.DYB_configureDataBuffering
        self._configureDataBuffering.errcheck = self.ASC_errcheck
        self._getFrameSize = API.DYB_getFrameSize
        self._getFrameSize.restype = ct.c_int32
        self._getDataBuffer = API.DYB_getDataBuffer
        self._getDataBuffer.errcheck = self.ASC_errcheck
        self._writeBuffer = API.DYB_writeBuffer
        self._writeBuffer.errcheck = self.ASC_errcheck
        self._waitForEvent = API.DYB_waitForEvent
        self._waitForEvent.restype = ct.c_int32

        # Aliases for the functions from the dll. For handling return
        # values: '.errcheck' is an attribute from ctypes.
        # Taken from metadata.h,v 1.12.8.1 2018/10/11 08:50:55
        self._getOrder = API.DYB_getOrder
        self._getOrder.restype = ct.c_int32
        self._getPointsX = API.DYB_getPointsX
        self._getPointsX.errcheck = self.ASC_metaErrcheck
        self._getPointsY = API.DYB_getPointsY
        self._getPointsY.errcheck = self.ASC_metaErrcheck
        self._getUnitXY = API.DYB_getUnitXY
        self._getUnitXY.restype = ct.c_int32
        self._getUnitVal = API.DYB_getUnitVal
        self._getUnitVal.restype = ct.c_int32
        self._getRotation = API.DYB_getRotation
        self._getRotation.errcheck = self.ASC_metaErrcheck
        self._getPhysRangeX = API.DYB_getPhysRangeX
        self._getPhysRangeX.errcheck = self.ASC_metaErrcheck
        self._getPhysRangeY = API.DYB_getPhysRangeY
        self._getPhysRangeY.errcheck = self.ASC_metaErrcheck
        self._convIndex2Pixel = API.DYB_convIndex2Pixel
        self._convIndex2Pixel.errcheck = self.ASC_metaErrcheck
        self._convIndex2Direction = API.DYB_convIndex2Direction
        self._convIndex2Direction.errcheck = self.ASC_metaErrcheck
        self._convIndex2Phys1 = API.DYB_convIndex2Phys1
        self._convIndex2Phys1.errcheck = self.ASC_metaErrcheck
        self._convIndex2Phys2 = API.DYB_convIndex2Phys2
        self._convIndex2Phys2.errcheck = self.ASC_metaErrcheck
        self._convValue2Phys = API.DYB_convValue2Phys
        self._convValue2Phys.restype = ct.c_float
        self._convPhys2Print = API.DYB_convPhys2Print
        self._convPhys2Print.restype = ct.c_float

    #%% Callback definitions

    def DataCallback(self, chn, length, idx, data, meta):
        """
        Functions of this type can be registered as callback functions for
        data channels. They will be called by the event loop as soon as data
        for the specified channel arrive. The data are always transferred in
        32 bit items but the encoding depends on the product and the channel.
        The meta data buffer contains information required to interpret the
        data.

        The index counts the data since the begin of the measurement, i.e. it
        is incremented from call to call by length. It also counts data that
        have been lost due to performance problems of the control PC. To avoid
        overflow, the index is resetted from time to time in a way that doesn't
        affect the calculation of the independent variables. When data stem
        from a scan, every frame begins with a new data packet with an
        index of 0.

        The buffer that contains the data is static and will be overwritten in
        the next call. It must not be free()'d or used by the application to
        store data.

        To use the data channels they must be enabled by using ID_DATA_EN

        Parameters
        ----------
        chn : int
            Data channel that has sent the data.
        length : int
            Length of the packet (number of int32 items).
        idx : int
            Number of the first item of the packet.
        data : array (pointer to c_int32)
            Pointer to the data buffer.
        meta : array (pointer to c_int32)
            Pointer to the corresponding meta data.
        """
        self._DataCallback(chn,
                           length,
                           idx,
                           data,
                           meta)

    def EventCallback(self, addr, idx, val):
        """
        Functions of this type can be registered as callback functions for
        events.
        They will be called by the event loop as soon as the specified
        parameter arrives.

        "Event" here means the notification about the change of a parameter
        caused by the client itself, by another client, or autonomously by the
        server. Also the event may be the answer to a parameter inquiry to the
        server.

        Note that changing one parameter by the client may in turn cause the
        change of several others. Sometimes the events may be redundant, i.e.
        the value of the parameter hasn't changed since the last call.

        Parameters
        ----------
        addr : int
            Address of the parameter that has been changed.
        idx : int
            If defined for the parameter: subaddress, 0 otherwise.
        val : int
            New value of the parameter.
        """
        self._EventCallback(addr,
                            idx,
                            val)

    def setDataCallback(self, chn, callbck):
        """
        Registers a callback function for a data channel. That function will be
        called when new data arrive on the channel. A callback function
        registered previously is unregistered.

        The function is called in the context of a thread that serves the
        event loop. If it is not processed fast enough, events or data may be
        lost.

        To use the data channels they must be enabled by using ID_DATA_EN.

        Parameters
        ----------
        chn : int
            Number of the data channel. Numbers begin with 0, the maximum is
            product specific.
        callbck : _DataCallback function
            Callback function for that channel, use NULL to unregister a
            function.
        """
        self._setDataCallback(chn,
                              callbck)

    def setEventCallback(self, addr, eventbck):
        """
        Registers a callback function for an event. That function will be
        called when the event is recognized.  A callback function registered
        previously is unregistered.

        The function is called in the context of a thread that serves the
        event loop. If it is not processed fast enough, events or data may be
        lost.

        It is possible to register a "catchall" callback for all events not
        explicitly handled by using the invalid address -1.

        Parameters
        ----------
        addr : int
            Identification of the parameter that is observed, -1 for catchall.
        eventbck : _EventCallback function
            Callback function for that event.
        """
        self._setEventCallback(addr,
                               eventbck)

    #%% Base functions

    def startServer(self, unused=0, host=0):
        """
        Configures connection to daisybase and starts server.

        Parameters
        ----------
        unused : str
            Unused Parameter, left for backward compatibility only. Use NULL
            or empty string. Enter 'FindSim' to use run a virtual ASC500.
        host : str
            Hostname or IP address in "dotted decimal" notation for the host
            where the application server resides.
            NULL or empty if the server should run locally.
        """
        if host != 0:
            host = host.encode('utf-8')
        if unused != 0:
            unused = unused.encode('utf-8')
        b_binPath = self.binPath.encode('utf-8')
        self._init(ct.c_char_p(unused),
                   ct.c_char_p(b_binPath),
                   ct.c_char_p(host),
                   self.portNr)
        self._run()

    def setOutputsWaiting(self, enable, waitTime = 1000):
        self.setOutputs(enable)
        self._waitForEvent(waitTime,
                           self.getConst('DYB_EVT_CUSTOM'),
                           self.getConst('ID_OUTPUT_STATUS'))
        
    def stopServer(self, waitTime=1000):
        """
        Cleanly disconnects server.

        Parameters
        ----------
        waitTime : int
            Time to wait in ms for response from server to get an info about
            the output status.
        """
        self.setOutputs(0)
        self._waitForEvent(waitTime,
                           self.getConst('DYB_EVT_CUSTOM'),
                           self.getConst('ID_OUTPUT_STATUS'))
        outActive = \
        self.getParameter(self.getConst('ID_OUTPUT_STATUS'),
                          0)
        if outActive:
            print("Outputs are not deactivated!")
        self._stop()

    def resetServer(self):
        """
        Performs a reset of the controller, shuts down the server and
        terminates the event loop. This call is necessary to reboot the
        controller. It takes a few seconds.
        """
        self._reset()

    def setParameter(self, address, val, index=0, sync=False):
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
        val : int
            New value for parameter.
        index : int
            If defined for the parameter: subaddress, 0 otherwise.
        sync : bool
            Enable for SYNC call. If disabled, you have to catch data via an
            event.

        Returns
        -------
        ret.value : int
            The return of the SYNC call. In case of ASYNC, returns 0.
        """
        val = ct.c_int32(int(val))
        ret = ct.c_int32(0)
        if sync:
            self._setParameterSync(address, index, val, ct.byref(ret))
        else:
            self._setParameterASync(address, index, val)
        return ret.value

    def getParameter(self, address, index=0, sync=True):
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
        sync : bool
            Enable for SYNC call.

        Returns
        -------
        data.value : int
            The return of the SYNC call. In case of ASYNC, returns 0.
        """
        data = ct.c_int32(0)
        if sync:
            self._getParameterSync(address, index, ct.byref(data))
        else:
            self._getParameterASync(address, index)
        return data.value

    def sendProfile(self, pFile):
        """
        Sends a profile file to the server. The function may run several
        seconds. Note that a whole lot of parameter change notifications may
        be sent back during that time. It may be useful to deactivate the
        event callback functions temporarily. The function must not be called
        in the context of a data or event callback.

        Parameters
        ----------
        pFile : str
            Location and filename of ngp file.
        """
        pfile = ct.create_string_buffer(pFile.encode('utf-8'))
        assert os.path.isfile(pFile)
        self._sendProfile(pfile)

    def getOutputStatus(self):
        """
        Returns output status (*all* outputs) as a boolean: 0: off, 1: on.

        Returns
        -------
        status : list
            Output status of outputs.
        """
        status = self.getParameter(self.getConst('ID_OUTPUT_STATUS'))
        return status

    def setOutputs(self, enable):
        """
        Activates or deactivates all outputs of the ASC500.

        Parameters
        ----------
        enable : int
            0: disable, 1: enable.
        """
        self.setParameter(self.getConst('ID_OUTPUT_ACTIVATE'), enable)

    #%% Data functions

    def printReturnCode(self, retC):
        """
        Returns a descriptive text for a given daisybase return code.

        Parameters
        ----------
        retC : int
            Return code of a daisybase function.

        Returns
        -------
        str
            Error description.
        """
        out = self._printRc(retC)
        return out # @todo check if conversion needs to be performed
    
    def waitForEvent(self, timeout, eventMask, customID):
        """
        The function waits until one of the specified events occur or on
        timeout. Note that there is a danger of race conditions: the event may
        have been occured before you begin waiting for it. The function can't
        recognize this case.

        Parameters
        ----------
        timeout : int
            Wait timeout in ms.
        eventMask : int
            Events to wait for: bitfield that combines some of the EventTypes
            "event types".
        customID : int
            Address of a parameter to wait for. Only relevant if the
            corresponding eventMask flag is set.

        Returns
        -------
        int
            Event that actually woke up the function: bitfield of EventTypes
            "event types".
        """
        out = self._waitForEvent(timeout, eventMask, customID)
        return out

    #%% Unit handling

    def ASC_units(self, unitCode):
        """
        Takes unit code from meta data and converts it into a string.

        Parameters
        ----------
        unitCode : int
            Code from meta data.

        Returns
        -------
        str
            Human readable string.
        """
        units = {
            0x0080 : "No unit, invalid",
            0x0180 : "Meter",
            0x017F : "MilliMeter",
            0x017E : "MicroMeter",
            0x017D : "NanoMeter",
            0x017C : "PicoMeter",
            0x0280 : "Volt",
            0x027F : "MilliVolt",
            0x027E : "MicroVolt",
            0x027D : "NanoVolt",
            0x0382 : "MegaHertz",
            0x0381 : "KiloHertz",
            0x0380 : "Hertz",
            0x037F : "MilliHertz",
            0x037E : "KiloSecond",
            0x0480 : "Second",
            0x047F : "MilliSecond",
            0x047E : "MicroSecond",
            0x047D : "NanoSecond",
            0x047C : "PicoSecond",
            0x0580 : "Ampere",
            0x057F : "MilliAmpere",
            0x057E : "MicroAmpere",
            0x057D : "NanoAmpere",
            0x0680 : "Watt",
            0x067F : "MilliWatt",
            0x067E : "MicroWatt",
            0x067D : "NanoWatt",
            0x0780 : "Tesla",
            0x077F : "MilliTesla",
            0x077E : "MicroTesla",
            0x077D : "NanoTesla",
            0x0880 : "Kelvin",
            0x087F : "MilliKelvin",
            0x087E : "MicroKelvin",
            0x087D : "NanoKelvin",
            0x0980 : "Angular Degree",
            0x097F : "MilliDegree",
            0x097E : "MicroDegree",
            0x097D : "NanoDegree",
            0x0A80 : "Cosine",
            0x0B80 : "dB",
            0x0C80 : "LSB"}

        if unitCode in (0x0480, 0x097E):
            print("Ambigious decoding")

        return units[unitCode]

    def printUnit(self, unit):
        """
        Returns the unit as an ASCII string (no greek letters).

        Parameters
        ----------
        unit : int
            Unit encoding from a DYB_Meta structure.

        Returns
        -------
        str
            Unit as ASCII string.
        """
        out = self._printUnit(unit)
        return out.decode("utf-8")
    
    def convertUnitToFactor(self, unit_raw):
        """
        Converts a raw unit into a factor.

        Parameters
        ----------
        unit_raw : int
            Raw unit value recieved from ASC500.

        Returns
        -------
        factor : float
            Factor for the corresponding unit (e.g. 'mV' -> 1e-3).
        """
        unitStr = self.printUnit(unit_raw)
        if unitStr[0] == 'm':
            factor = 1e-3
        elif unitStr[0] == 'u':
            factor = 1e-6
        elif unitStr[0] == 'n':
            factor = 1e-9
        elif unitStr[0] == 'p':
            factor = 1e-12
        elif unitStr[0] == 'k':
            factor = 1e3
        elif unitStr[0] == 'M':
            factor = 1e6
        else:
            factor = 1
        
        return factor

    unit_dict = {
        'mm' : '0',
        'um' : '1',
        'nm' : '2',
        'pm' : '3',
        'V' : '4',
        'mV' : '5',
        'uV' : '6',
        'nV' : '7',
        'MHz' : '8',
        'kHz' : '9',
        'Hz' : '10',
        'mHz' : '11',
        's' : '12',
        'ms' : '13',
        'us' : '14',
        'ns' : '15',
        'A' : '16',
        'mA' : '17',
        'uA' : '18',
        'nA' : '19',
        'deg' : '20',
        '[cos]' : '24',
        'dB' : '28',
        'W' : '32',
        'mW' : '33',
        'uW' : '34',
        'nW' : '35'
    }

    def unitToASC(self, unit):
        """
        This function converts a unit into a ASC500 interpretable value.

        Parameters
        ----------
        unit : str
            Unit string to convert (e.g. 'mV')

        Returns
        -------
        value : float
            Value for ASC500
        """
        if unit not in self.unit_dict:
            print('Unit not convertable')
            return 'UnitError'
        else:
            raw = int(self.unit_dict.get(unit), base=0)
            return raw
    