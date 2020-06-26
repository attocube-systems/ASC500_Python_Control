
import ctypes as ct
import os
import asc500_const

#%%

class ASC500Base:
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
        return int(asc500_const.cc.get(symbol), base=0)

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
        self._convValue2Phys.restype = ct.c_double
        self._convPhys2Print = API.DYB_convPhys2Print
        self._convPhys2Print.restype = ct.c_double

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
            or empty string.
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
        index : int
            If defined for the parameter: subaddress, 0 otherwise.
        val : int
            New value for parameter.
        sync : bool
            Enable for SYNC call. If disabled, you have to catch data via an
            event.

        Returns
        -------
        ret.value : int
            The return of the SYNC call. In case of ASYNC, returns 0.
        """
        val = ct.c_int32(val)
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
        assert os.path.isfile(pfile)
        self._sendProfile(pfile)

    def getOutputStatus(self):
        """
        Returns output status (*all* outputs) as a boolean: 0: off, 1: on.

        Returns
        -------
        list
            Output status of outputs.
        """
        return self.getParameter(self.getConst('ID_OUTPUT_STATUS'))

    def setOutputs(self, enable):
        """
        Activates or deactivates all outputs of the ASC500.

        Parameters
        ----------
        enable : int
            0: disable, 1: enable.
        """
        self.setParameter(self.getConst('ID_OUTPUT_ACTIVATE'), enable)

    def setDataEnable(self, enable):
        """
        Activates or deactivates all data channels of the ASC500.

        Parameters
        ----------
        enable : int
            0: disable, 1: enable.
        """
        self.setParameter(self.getConst('ID_DATA_EN'), enable)

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
        return out # @todo check if conversion needs to be performed

    def configureChannel(self, chn, trig, src, avg, sampT):
        """
        Configures what kind of data is sent on a specific data channel.

        Parameters
        ----------
        chn : int
            Number of the channel to be configured (0 ... 13).
        trig : int
            Trigger source for data output (one of CHANCONN_..).
        src : int
            Data source for the channel (one of CHANADC_..).
        avg : bool
            If data should be averaged over the sample time.
        sampT : float
            Time per sample sent to PC. Has no effect unless the channel is
            timer triggered. Unit: s.
        """
        self._configureChannel(ct.c_int32(chn),
                               ct.c_int32(trig),
                               ct.c_int32(src),
                               ct.c_bool(avg),
                               ct.c_double(sampT))

    def getChannelConfig(self, chn):
        """
        Reads out the channel configuration as set by _configureChannel.

        Parameters
        ----------
        chn : int
            Number of the channel to be configured (0 ... 13).

        Returns
        -------
        trig : int
            Trigger source for data output (one of CHANCONN_...).
        src : int
            Data source for the channel (one of CHANADC_...).
        avg : bool
            If data should be averaged over the sample time.
        sampT : float
            Time per sample sent to PC. Has no effect unless the channel is
            timer triggered. Unit: s.
        """
        trig = ct.c_int32(0)
        src = ct.c_int32(0)
        avg = ct.c_bool(0)
        sampT = ct.c_double(0)
        self._getChannelConfig(chn,
                               ct.byref(trig),
                               ct.byref(src),
                               ct.byref(avg),
                               ct.byref(sampT))
        return trig.value, src.value, avg.value, sampT.value

    def configureDataBuffering(self, chn, size):
        """
        The function configures if data arriving from a specific data channel
        are buffered and sets the default size of the buffer.
        If the default size is set to 0, data are not buffered and data
        callback functions of daisybase (_setDataCallback) can be used.
        If it is set to a positive value, the data are buffered and can be
        retreived with _getDataBuffer. The actual value of the size is relevant
        only for data channels that are triggered by timer; in all other cases
        the "native" buffer size is used.
        If size is too small (< 128), timer triggered data will not be buffered
        to avoid too mucht buffer-full events.
        If buffering is enabled, no data callback function can be used for the
        channel.

        Parameters
        ----------
        chn : int
            Number of the channel of interest (0 ... 13).
        size : int
            Buffer size in '32 bit items'.
        """
        self._configureDataBuffering(chn,
                                     size)

    def getFrameSize(self, chn):
        """
        The function returns the size of a complete data frame for the channel.
        This is the buffer size required for a call to _getDataBuffer.
        The size may vary when measurement parameters are changed.
        It is not valid before the data acquisition has started!

        Parameters
        ----------
        chn : int
            Number of the channel of interest (0 ... 13).

        Returns
        -------
        int
            Size of the complete data buffer.
        """
        out = self._getFrameSize(chn)
        return out

    def getDataBuffer(self, chn, fullOnly, dataSize):
        """
        Retrieve Data Channel Buffer.

        If a data channel is configured for buffering with
        _configureDataBuffering, the next buffer can be retrieved with this
        function without using data callback functions.
        Normally, only completely filled buffers are returned and an error
        DYB_OutOfRange is signalled when no full buffer is available.
        No data will be returned twice.
        The user can change this behaviour by requesting also partially filled
        buffers with the parameter fullOnly = 0.
        The partially filled buffer may be returned multiple times
        until it is full.
        In the case of scanner triggered data, a frame is considered full when
        the upmost OR the lowermost line has been scanned.
        A data frame is available when it is complete until it is retrieved or
        the next frame is complete. If it is not retrieved in time, the frame
        number may "jump".

        Parameters
        ----------
        chn : int
            Number of the channel of interest (0 ... 13).
        fullOnly : bool
            If only completely filled buffers are requested.
        dataSize : int
            Size of the data buffer provided by the user.
            If insufficient, DYB_OutOfRange will be returned.

        Returns
        -------
        frameN : int
            Number of the frame. With fullOnly == False the same frame can
            be returned repeatedly.
        index : int
            Output: Index of the first element in the buffer.
        dataSize : int
            Number of valid data (32-bit items) in the buffer.
        data : array (int32)
            Pointer to an array to store the data. The array
            must be provided by the caller and its size must be
            at least one frame size (_getFrameSize).
        meta : array (int32 * 13)
            Pointer to a space to copy the meta data.
            The space must be provided by the caller.
        """
        frameN = ct.c_int32(0)
        index = ct.c_int32(0)
        dSize = ct.c_int32(dataSize)
        data = (ct.c_int32 * dataSize)()
        meta = (ct.c_int32 * 13)()
        self._getDataBuffer(ct.c_int32(chn),
                            ct.c_bool(fullOnly),
                            ct.byref(frameN),
                            ct.byref(index),
                            ct.byref(dSize),
                            data,
                            meta)
        return frameN, index, dSize, data, meta

    def writeBufferToFile(self, fName, comm, binary, fwd, index, dataSize, data, meta):
        """
        Write Buffer to file.

        Writes a buffer (as retrieved with _getDataBuffer) to a file of an
        appropriate ASCII or binary format. The format is chosen automatically
        according to the meta data.
        Available formats are "bcrf" (binary) and "asc" (ascii) for scanner
        triggered data and "csv" for all other data.
        The formats are "Daisy compatible".

        Parameters
        ----------
        fName: str
            Name of the file to write, without extension (selected
            automatically).
        comm : str
            Data or channel description for the file header. Can be left blank.
        binary : bool
            If the desired format is binary. Relevant only for scanner
            triggered data, ignored otherwise.
        fwd: bool
            If the forward scan (in X direction) is to be written.
            Relevant only for scanner triggered data, ignored otherwise.
        index : int
            Index of the first element in the buffer.
        dataSize : int
            Number of valid data (32-bit items) in the buffer.
        data : array (pointer to c_int32)
            The data buffer.
        meta : array (pointer to c_int32)
            Meta data belonging to the buffer.
        """
        self._writeBuffer(ct.create_string_buffer(fName.encode('utf-8')),
                          ct.create_string_buffer(comm.encode('utf-8')),
                          ct.c_bool(binary),
                          ct.c_bool(fwd),
                          index,
                          dataSize,
                          data,
                          meta)

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

    #%% Meta data functions

    def getOrder(self, meta):
        """
        Extract data order from the meta data set.

        Ordering of the data, i.e. the kind of mapping of the data index to the
        physical independent variable(s). The variable(s) may:

            - be one (like time) or two (a scan),

            - grow unlimited (like time) or may be cyclic (like a scan),

            - have an absolutely defined origin (e.g. spectroscopy) or not
            (like time, again)

            - perform a scan beginning with a line in forward or backward
            direction,

            - have subsequent scan lines in the same direction only or
            alternating between forward and backward.

        The first frame of a scan always runs bottom to top, the Y direction
        of subsequent frames alternate.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.

        Returns
        -------
        int, str
            Data Order as code and string.
        """
        order_RC = {
            0 : "1 Variable, unlimited, no origin defined",
            1 : "1 Variable, unlimited, absolute origin defined",
            2 : "1 Variable, ranging from absolute origin to limit",
            3 : "2 Variables, forward-forward scan, origin defined",
            4 : "2 Variables, forward-backward scan, origin defined",
            5 : "2 Variables, backward-backward scan, origin defined",
            6 : "2 Variables, backward-forward scan, origin defined",
            7 : "Invalid order"}
        out = self._getOrder(meta)

        return out, order_RC[out]

    def getPointsX(self, meta):
        """
        Data Points in a line.

        Extract the number of data points in a row if applicable.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.

        Returns
        -------
        int
            Number of points.
        """
        pntsX = ct.c_int32(0)
        self._getPointsX(meta,
                         ct.byref(pntsX))
        return pntsX.value

    def getPointsY(self, meta):
        """
        Number of lines.

        Extract the number of lines of a scan if applicable.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.

        Returns
        -------
        int
            Number of lines.
        """
        pntsY = ct.c_int32(0)
        self._getPointsY(meta,
                         ct.byref(pntsY))
        return pntsY.value

    def getUnitXY(self, meta):
        """
        Unit of independent variable(s).

        Returns the common unit of all independent variables.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.

        Returns
        -------
        str
            Name of the unit.
        """
        out = self._getUnitXY(meta)
        return self.ASC_units(out)

    def getUnitVal(self, meta):
        """
        Unit of dependent variable.

        Returns the unit of the data.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.

        Returns
        -------
        str
            Name of the unit.
        """
        out = self._getUnitVal(meta)
        return self.ASC_units(out)

    def getRotation(self, meta):
        """
        Scan range rotation.

        Returns the rotation angle of the scan area if the data originate from
        a scan.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.

        Returns
        -------
        float
            Rotation angle in rad.
        """
        rotation = ct.c_double(0.)
        self._getRotation(meta,
                          ct.byref(rotation))
        return rotation.value

    def getPhysRangeX(self, meta):
        """
        Physical range X.

        Returns the physical length of a line of data for cyclic data order.
        The length is the distance between the first and the last point of the
        line.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.

        Returns
        -------
        float
            Line length.
        """
        rangeX = ct.c_double(0.)
        self._getPhysRangeX(meta,
                            ct.byref(rangeX))
        return rangeX.value

    def getPhysRangeY(self, meta):
        """
        Physical range Y.

        Returns the physical height of the scan area if applicable.
        The height is the distance between the first and the last line of the
        frame.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.

        Returns
        -------
        float
            Column height.
        """
        rangeY = ct.c_double(0.)
        self._getPhysRangeY(meta,
                            ct.byref(rangeY))
        return rangeY.value

    def convIndex2Pixel(self, meta, idx):
        """
        Pixel position from data index.

        Converts a data index to the pixel position (i.e. column and line
        number) if the data originate from a scan. The coordinate origin is
        bottom left.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.
        idx : int
            Data index.

        Returns
        -------
        int
            Horizontal pixel position (column number).
        int
            Vertical pixel position (line number).
        """
        col = ct.c_int32(0)
        lin = ct.c_int32(0)
        self._convIndex2Pixel(meta,
                              idx,
                              ct.byref(col),
                              ct.byref(lin))
        return col.value, lin.value

    def convIndex2Direction(self, meta, idx):
        """
        Scan direction from data index.

        Calculates the current scan direction corresponding to a particular
        index.
        The direction is seen from the coordinate origin which is bottom left.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.
        idx : int
            Data index.

        Returns
        -------
        int
            If the current scan direction is forward.
        int
            If the current scan direction is upward.
        """
        fwd = ct.c_int32(0)
        uwd = ct.c_int32(0)
        self._convIndex2Direction(meta,
                                  idx,
                                  ct.byref(fwd),
                                  ct.byref(uwd))
        return fwd.value, uwd.value

    def convIndex2Phys1(self, meta, idx):
        """
        Physical Position from Data Index for one variable.

        Converts a data index to the physical coordinates of the data point
        if one independent variable exists. If the data order is DYB_Linear,
        the absolute value is meaningless but differences are valid.
        The corresponding unit can be retreived by _getUnitXY.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.
        idx : int
            Data index.

        Returns
        -------
        float
            Independent variable.
        """
        xVar = ct.c_double(0.)
        self._convIndex2Phys1(meta,
                              idx,
                              ct.byref(xVar))
        return xVar.value

    def convIndex2Phys2(self, meta, idx):
        """
        Physical Position from Data Index for two variables.

        Converts a data index to the physical coordinates of the data point
        if the data originate from a scan. The origin is bottom left.
        The corresponding unit can be retreived by _getUnitXY.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.
        idx : int
            Data index.

        Returns
        -------
        float
            Horizontal position.
        float
            Vertical position.
        """
        xVar = ct.c_double(0.)
        yVar = ct.c_double(0.)
        self._convIndex2Phys2(meta,
                              idx,
                              ct.byref(xVar),
                              ct.byref(yVar))
        return xVar.value, yVar.value

    def convValue2Phys(self, meta, val):
        """
        Convert data value.

        Converts a raw data value to the physical value.
        The unit can be retreived by _getUnitVal.

        Parameters
        ----------
        meta : array (pointer to c_int32)
            Meta data set.
        val : int
            Raw data value.

        Returns
        -------
        float
            Physical value.
        """
        out = \
        self._convValue2Phys(meta,
                             val)
        return out

    def convPhys2Print(self, number, unit, unitStr):
        """
        Make up value for printing.

        A physical value consisting of number and unit is rescaled for
        comfortable reading. The unit is prefixed with a magnitude prefix
        (like "k" or "n") so that the number ranges between 1 and 1000.

        Prefix and unit are provided as a printable string.
        If the unit is invalid, the number will be unchanged and the unit
        string will be "?".

        Parameters
        ----------
        number : float
            Number belonging to the physical value.
        unit : int
            Unit belonging to the physical value.
        unitStr : str
            String buffer of at least 10 chars.

        Returns
        -------
        str
            On output it will contain the prefixed unit after rescaling
            (encoded in Latin1).
        float
            Number after rescaling.

        """
        unitstr = ct.create_string_buffer(unitStr.encode('utf-8'))
        out = \
        self._convPhys2Print(number,
                             unit,
                             unitstr)
        return unitstr, out

    #%% Additional base functions built-upon dll calls

    def setCounterExposureTime(self, expTime=2.5e-6):
        """
        Sets exposure time of the counter unit.
        The exposure time can be set between 2.5 us to
        2**16 * 2.5 us = 163.84 ms. If the data channel is timer triggered,
        setting an exposure time longer than the transfer rate (set in
        setChannelConfig) is not meaningful. It makes sense to set both times
        equal.

        Parameters
        ----------
        expTime : float
            Exposure time in seconds.

        Returns
        -------
        float
            The set exposure time in seconds.
        """
        maxExpTime = self.minExpTime * 2**16
        if expTime < self.minExpTime:
            expTime = self.minExpTime
        elif expTime > maxExpTime:
            expTime = maxExpTime

        expTimeInt = int(expTime / self.minExpTime) - 1
        self.setParameter(self.getConst('ID_CNT_EXP_TIME'),
                          expTimeInt)
        return (expTimeInt + 1) * self.minExpTime

    def getCounterExposureTime(self):
        """
        Gets exposure time of the counter unit.

        Returns
        -------
        float
            The set exposure time in seconds.
        """
        ret = self.getParameter(self.getConst('ID_CNT_EXP_TIME'))
        return (ret + 1) * self.minExpTime

    def waitForFullBuffer(self, chnNo, waitTime=500):
        """
        Wait until a channel buffer is full.

        Parameters
        ----------
        chnNo : int
            Channel number (0 ... 13).
        waitTime : int, optional
            The waiting time in ms for the call to return. The default is 500.

        Returns
        -------
        int
            Event that actually woke up the function: bitfield of EventTypes
            "event types". Returns 0
        """
        chnConst = 'DYB_EVT_DATA_{:02d}'.format(chnNo)
        chnCode = self.getConst(chnConst)
        ret = \
        self.waitForEvent(waitTime,
                          chnCode,
                          0)
        return ret
