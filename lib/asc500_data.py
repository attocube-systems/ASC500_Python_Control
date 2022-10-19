from .asc500_base import ASC500Base
import ctypes as ct


class ASC500Data(ASC500Base):
    """ADC data can be passed through a linear output transfer function after the transfer
    via a data channel in order to allow for external wiring.
    The transfer function depends on the data source, therefore the index has to be
    between @ref CHANADC_ADC_MIN [0] and @ref CHANADC_ADC_MAX [5]."""

    def getChannelGain(self, channel):
        """
        This function retrieves the gain set for the given data source.

        Parameters
        ----------
        channel : int
            [0..5] channel to retrieve the gain for

        Returns
        -------
        gain : float
            Currently set gain [output_unit/V]
        """
        gain = self.getParameter(self.getConst('ID_ADC_ECAL_FACT'), index=channel)/1e-6
        return gain

    def setChannelGain(self, channel, gain):
        """
        This function sets the gain for the given data source.

        Parameters
        ----------
        channel : int
            [0..5] channel to retrieve the gain for
        gain : float
            Currently set gain [output_unit/V]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_ADC_ECAL_FACT'), gain, channel)

    def getChannelOffset(self, channel):
        """
        This function retrieves the offset set for the given data source.

        Parameters
        ----------
        channel : int
            [0..5] channel to retrieve the offset for

        Returns
        -------
        offset : float
            Currently set offset [V]
        """
        offset = self.getParameter(self.getConst('ID_ADC_ECAL_OFFS'), index=channel)*1e-6
        return offset

    def setChannelOffset(self, channel, offset):
        """
        This function sets the offset for the given data source.

        Parameters
        ----------
        channel : int
            [0..5] channel to retrieve the offset for
        offset : float
            Currently set offset [V]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_ADC_ECAL_OFFS'), offset, channel)

    def getChannelUnit(self, channel):
        """
        This function retrieves the unit set for the given data source (e.g. 'mV').

        Parameters
        ----------
        channel : int
            [0..5] channel to retrieve the unit for

        Returns
        -------
        unit : str
            Currently set unit as string
        """
        unit_raw = self.getParameter(self.getConst('ID_ADC_ECAL_UNIT'), index=channel)
        unit = self.printUnit(unit_raw)
        return unit

    def setChannelUnit(self, channel, unit):
        """
        This function sets the unit for the given data source (e.g. 'mV').

        Parameters
        ----------
        channel : int
            [0..5] channel to set the unit for
        unit : str
            Data unit (e.g. 'mV')

        Returns
        -------
        None.
        """
        raw = self.unitToASC(unit)
        self.setParameter(self.getConst('ID_ADC_ECAL_UNIT'), raw, channel)

    def getADCValue(self, channel):
        """
        This function retrieves the the value at the given data source.

        Parameters
        ----------
        channel : int
            [0..5] channel to set the unit for

        Returns
        -------
        value : float
            Value at the given data source
        """
        value = self.getParameter(self.getConst('ID_ADC_VALUE'), channel) #TODO: Check scaling: 'The ADC value itself is multiplied with 1.000.000 to provide sufficent accuracy.'
        return value

    def getADCUnit(self, channel):
        """
        This function retrieves the unit for the value at the given data source (e.g. 'mV').

        Parameters
        ----------
        channel : int
            [0..5] channel to set the unit for
        unit : str
            Data unit (e.g. 'mV')

        Returns
        -------
        None.
        """
        raw_unit = self.getParameter(self.getConst('ID_ADC_VAL_UNIT'), channel)
        unit = self.printUnit(raw_unit)
        return unit

    def getADCValueBase(self, channel):
        """
        This function retrieves the value in its base units at the given data source.

        Parameters
        ----------
        channel : int
            [0..5] channel to set the unit for

        Returns
        -------
        value : float
            Value at the given data source (in its base unit)
        """
        value = self.getParameter(self.getConst('ID_ADC_VALUE'), channel)
        factor = self.convertUnitToFactor(self.getADCUnit(channel))
        value = value * factor
        return value

    def getDACValue(self, channel):
        """
        This function retrieves the currently set value at the given DAC output in [V].

        Parameters
        ----------
        channel : int
            [0..5] channel to set the unit for

        Returns
        -------
        value : float
            Value at the given data source in [V]
        """
        value = self.getParameter(self.getConst('ID_DAC_VALUE'), channel)*305.19*1e-6
        return value

    def setDACValue(self, channel, value):
        """
        This function sets the value at the given DAC output in [V].

        Parameters
        ----------
        channel : int
            [0..5] channel to set the unit for
        value : float
            Value at the given data source in [V]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_DAC_VALUE'), value/305.19*1e6, channel)

    def getDACSlewRate(self, channel):
        """
        This function retrieves the slew rate at the given DAC output in [V].

        Parameters
        ----------
        channel : int
            [0..5] channel to set the unit for

        Returns
        -------
        slew : float
            Slew rate at the given data source in [V]
        """
        slew = self.getParameter(self.getConst('ID_DAC_GEN_STEP'), channel)*305.19*1e-6
        return slew

    def setDACSlewRate(self, channel, slew):
        """
        This function retrieves the slew rate at the given DAC output in [V].

        Parameters
        ----------
        channel : int
            [0..5] channel to set the unit for
        slew : float
            Slew rate at the given data source in [V]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_DAC_GEN_STEP'), slew/305.19*1e6, channel)

    def setDataEnable(self, enable):
        """
        Activates or deactivates all data channels of the ASC500.

        Parameters
        ----------
        enable : int
            0: disable, 1: enable.
        """
        self.setParameter(self.getConst('ID_DATA_EN'), enable)

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
        rangeX = ct.c_float(0.)
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
        rangeY = ct.c_float(0.)
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
        xVar = ct.c_float(0.)
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
        xVar = ct.c_float(0.)
        yVar = ct.c_float(0.)
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
        rotation = ct.c_float(0.)
        self._getRotation(meta,
                          ct.byref(rotation))
        return rotation.value

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
        to avoid too many buffer-full events.
        If buffering is enabled, no data callback function can be used for the
        channel.

        Parameters
        ----------
        chn : int
            Number of the channel of interest (0 ... 13).
        size : int
            Buffer size in '32 bit items'.
        """
        if size < 128:
            print('If size is too small (< 128), \
                  timer triggered data will not be buffered \
                      to avoid too many buffer-full events.')
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
