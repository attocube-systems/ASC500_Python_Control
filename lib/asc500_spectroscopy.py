from .asc500_base import ASC500Base

class ASC500Spectroscopy(ASC500Base):
    """
    These parameters control the built-in spectroscopy machines. The index is used to address
    the spectroscopy number (0-2). Spectroscopy engine 3 is reserved for resonance measurement.
    """
    def getSpecActuator(self, spec):
        """
        This function retrieves the actuator (0..3=DAC1..4, 26=Z, 27=Low Freq) set for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        actuator : int
            actuator set for the given spectroscopy engine
            (0..3=DAC1..4, 26=Z, 27=Low Freq)
        """
        actuator = self.getParameter(self.getConst('ID_SPEC_DAC_NO'), spec)
        return actuator
    
    def setSpecActuator(self, spec, actuator):
        """
        This function sets the actuator (0..3=DAC1..4, 26=Z, 27=Low Freq) for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        actuator : int
            actuator set for the given spectroscopy engine
            (0..3=DAC1..4, 26=Z, 27=Low Freq)
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_DAC_NO'), actuator, spec)
    
    def getSpecStartValue(self, spec):
        """
        This function retrieves the start value set for the given spectroscopy engine [spec].
        (unit actuator specific)

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        value : float
            Start value
            (unit actuator specific)
        """
        value = self.getParameter(self.getConst('ID_SPEC_START_DISP'), spec)
        return value
    
    def setSpecStartValue(self, spec, value):
        """
        This function sets the start value for the given spectroscopy engine [spec].
        (unit actuator specific)

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        value : float
            Start value
            (unit actuator specific)
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_START_DISP'), value, spec)
    
    def getSpecEndValue(self, spec):
        """
        This function retrieves the end value set for the given spectroscopy engine [spec].
        (unit actuator specific)

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        value : float
            End value
            (unit actuator specific)
        """
        value = self.getParameter(self.getConst('ID_SPEC_END_DISP'), spec)
        return value
    
    def setSpecEndValue(self, spec, value):
        """
        This function sets the end value for the given spectroscopy engine [spec].
        (unit actuator specific)

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        value : float
            End value
            (unit actuator specific)
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_END_DISP'), value, spec)
    
    def getSpecUnit(self, spec):
        """
        This function retrieves the unit of the start and end values for the given spectroscopy engine [spec].
        (unit actuator specific)

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        unit : str
            Start/End unit as string (e.g. 'mV')
        """
        unit_raw = self.getParameter(self.getConst('ID_SPEC_UNIT_DISP'), spec)
        unit = self.printUnit(unit_raw)
        return unit
    
    def getSpecSteps(self, spec):
        """
        This function retrieves the number of steps set for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        steps : int
            Number of steps
        """
        steps = self.getParameter(self.getConst('ID_SPEC_COUNT'), spec)
        return steps
    
    def setSpecSteps(self, spec, steps):
        """
        This function sets the number of steps for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        steps : float
            Number of steps
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_COUNT'), steps, spec)
    
    def getSpecAveraging(self, spec):
        """
        This function retrieves the averaging time per step in [s] set for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        averaging : float
            Averaging time per step in [s]
        """
        averaging = self.getParameter(self.getConst('ID_SPEC_MSPOINTS'), spec)*2.5*1e-6
        return averaging
    
    def setSpecAveraging(self, spec, averaging):
        """
        This function sets the averaging time per step in [s] for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        averaging : float
            Averaging time per step in [s]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_MSPOINTS'), averaging/2.5*1e6, spec)
    
    def getSpecWait(self, spec):
        """
        This function retrieves the delay time before measurement in [s] set for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        delay : float
            delay time before measurement in [s]
        """
        delay = self.getParameter(self.getConst('ID_SPEC_WAIT'), spec)*2.5*1e-6
        return delay
    
    def setSpecWait(self, spec, delay):
        """
        This function sets the delay time before measurement in [s] for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        delay : float
            delay time before measurement in [s]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_WAIT'), delay/2.5*1e6, spec)
    
    def getSpecStatus(self, spec):
        """
        This function retrieves the status (0=stop, 1=run) of the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        status : int
            [0, 1] Status of the given spectroscopy engine [stop, running]
        """
        status = self.getParameter(self.getConst('ID_SPEC_STATUS'), spec)
        return status
    
    def setSpecStatus(self, spec, status):
        """
        This function sets the status (0=stop, 1=run) of the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        status : int
            [0, 1] Status of the given spectroscopy engine [stop, run]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_STATUS'), status, spec)
    
    def getSpecRuns(self, spec):
        """
        This function retrieves the number of runs set for of the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        runs : int
            Number of runs set for the given spectroscopy engine
        """
        runs = self.getParameter(self.getConst('ID_SPEC_RUNCOUNT'), spec)
        return runs
    
    def setSpecRuns(self, spec, runs):
        """
        This function sets the number of runs for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        runs : int
            Number of runs for the given spectroscopy engine
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_RUNCOUNT'), runs, spec)
    
    def getSpecDirection(self, spec):
        """
        This function retrieves the direction set for of the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        direction : int
            [0, 1] Direction [foreward/backward] set for the given spectroscopy engine
        """
        direction = self.getParameter(self.getConst('ID_SPEC_FORBACK'), spec)
        return direction
    
    def setSpecDirection(self, spec, direction):
        """
        This function sets the direction for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        direction : int
            [0, 1] Direction [foreward/backward] for the given spectroscopy engine
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_FORBACK'), direction, spec)
    
    def getSpecLimiterOn(self, spec):
        """
        This function retrieves, if a limiter is set for of the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        enabled : int
            [0, 1] Limiter is [disabled/enabled] for the given spectroscopy engine
        """
        enabled = self.getParameter(self.getConst('ID_SPEC_COMP_EN'), spec)
        return enabled
    
    def setSpecLimiterOn(self, spec, enable):
        """
        This function enables/disables the limiter for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        enable : int
            [0, 1] Set limiter [disabled/enabled] for the given spectroscopy engine
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_COMP_EN'), enable, spec)
    
    def getSpecLimiterChannel(self, spec):
        """
        This function retrieves the limiter input channel set for of the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        channel : int
            Limiter input channel for the given spectroscopy engine

                One of CHANADC_...:
                    0  - CHANADC_ADC_MIN     
                    5  - CHANADC_ADC_MAX     
                    7  - CHANADC_AFMAEXC     
                    8  - CHANADC_AFMFEXC     
                    9  - CHANADC_ZOUT        
                    12 - CHANADC_AFMSIGNAL   
                    13 - CHANADC_AFMAMPL     
                    14 - CHANADC_AFMPHASE    
                    16 - CHANADC_AFMMAMPL    
                    17 - CHANADC_AFMMPHASE   
                    18 - CHANADC_ZOUTINV     
                    29 - CHANADC_CROSSLINK_1 
                    30 - CHANADC_CROSSLINK_2 
                    31 - CHANADC_SENSOR_POS_X
                    32 - CHANADC_SENSOR_POS_Y
        """
        channel = self.getParameter(self.getConst('ID_SPEC_COMP_CH'), spec)
        return channel
    
    def setSpecLimiterChannel(self, spec, channel):
        """
        This function sets the limiter input channel for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        channel : int
            Limiter input channel for the given spectroscopy engine
                
                One of CHANADC_...:
                    0  - CHANADC_ADC_MIN     
                    5  - CHANADC_ADC_MAX     
                    7  - CHANADC_AFMAEXC     
                    8  - CHANADC_AFMFEXC     
                    9  - CHANADC_ZOUT        
                    12 - CHANADC_AFMSIGNAL   
                    13 - CHANADC_AFMAMPL     
                    14 - CHANADC_AFMPHASE    
                    16 - CHANADC_AFMMAMPL    
                    17 - CHANADC_AFMMPHASE   
                    18 - CHANADC_ZOUTINV     
                    29 - CHANADC_CROSSLINK_1 
                    30 - CHANADC_CROSSLINK_2 
                    31 - CHANADC_SENSOR_POS_X
                    32 - CHANADC_SENSOR_POS_Y
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_COMP_CH'), channel, spec)
    
    def getSpecLimiterCondition(self, spec):
        """
        This function retrieves the limiter condition set for of the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        condition : int
            [0, 1] Limiter condition is ['>', '<'] threshold for the given spectroscopy engine
        """
        condition = self.getParameter(self.getConst('ID_SPEC_COMP_SGN'), spec)
        return condition
    
    def setSpecLimiterCondition(self, spec, condition):
        """
        This function sets the limiter condition for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        condition : int
            [0, 1] Set limiter condition ['>', '<'] threshold for the given spectroscopy engine
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_COMP_SGN'), condition, spec)
    
    def getSpecLimiterThreshold(self, spec):
        """
        This function retrieves limiter threshold set for of the given spectroscopy engine [spec].
        (actuator units)

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        threshold : float
            Limiter threshold for the given spectroscopy engine (actuator units)
        """
        threshold = self.getParameter(self.getConst('ID_SPEC_COMP_VAL_DISP'), spec)
        return threshold
    
    def setSpecLimiterThreshold(self, spec, threshold):
        """
        This function sets the limiter threshold for the given spectroscopy engine [spec].
        (actuator units)

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        threshold : float
            Limiter threshold for the given spectroscopy engine (actuator units)
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_COMP_VAL_DISP'), threshold, spec)
    
    def getSpecZLoopOff(self, spec):
        """
        This function retrieves, if the Z loop is switched off while running for of the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine
        
        Returns
        -------
        enabled : int
            [0, 1] Z loop is switched [on, off] while running, for the given spectroscopy engine (actuator units)
        """
        enabled = self.getParameter(self.getConst('ID_SPEC_LOOP_OFF'), spec)
        return enabled
    
    def setSpecLimiterZLoopOff(self, spec, enable):
        """
        This function sets, if the Z loop is switched off while running for the given spectroscopy engine [spec].

        Parameters
        ----------
        spec : int
            [0..2] Spectroscopy engine

        enable : int
            [0, 1] Z loop is switched [on, off] while running, for the given spectroscopy engine (actuator units)
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_LOOP_OFF'), enable, spec)