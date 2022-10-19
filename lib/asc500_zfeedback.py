from .asc500_base import ASC500Base


class ASC500ZFeedback(ASC500Base):

    def getZFeedbackLoop(self):
        """
        This function retrieves the status of Z feedback loop.

        Parameters
        ----------
        None
        
        Returns
        -------
        enabled : int
            [0, 1] Feedback loop is [on/off]
        """
        enabled = self.getParameter(self.getConst('ID_REG_LOOP_ON'))
        return enabled

    def setZFeedbackLoop(self, enable):
        """
        This function sets the of Z feedback loop on/off.

        Parameters
        ----------
        enable : int
            [0, 1] Set feedback loop [on/off]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_LOOP_ON'), enable)
    
    def getZFeedbackInputSignal(self):
        """
        This function retrieves the input signal source channel for the Z feedback loop. 

        Parameters
        ----------
        None

        Returns
        -------
        channel : int
            
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
        channel = self.getPatameter(self.getConst('ID_REG_INPUT'))
        return channel

    def setZFeedbackInputSignal(self, channel):
        """
        This function sets the input signal source channel for the Z feedback loop. 

        Parameters
        ----------
        channel :  int
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
        self.setParameter(self.getConst('ID_REG_INPUT'), channel)

    def getZFeedbackI(self):
        """
        This function retrieves the Z feedback controller integral part I [Hz].

        Parameters
        ----------
        None

        Returns
        -------
        value : float
            Feedback controller integral part I in [Hz]
        """
        value = self.getParameter(self.getConst('ID_REG_KI_DISP'))*1e-3
        return value
    
    def setZFeedbackI(self, value):
        """
        This function sets the Z feedback controller integral part I [Hz].

        Parameters
        ----------
        value : float
            Feedback controller integral part I in [Hz]

        Returns
        -------
        None
        """
        self.setParameter(self.getConst('ID_REG_KI_DISP'), value*1e3)
        
    def getZFeedbackP(self):
        """
        This function retrieves the Z feedback controller proportional part P.

        Parameters
        ----------
        None

        Returns
        -------
        value : int
            Feedback proportional part P
        """
        value = self.getParameter(self.getConst('ID_REG_KP_DISP'))*1e-6
        return value
    
    def setZFeedbackP(self, value):
        """
        This function sets the Z feedback controller proportional part P.

        Parameters
        ----------
        value : int
            Feedback proportional part P

        Returns
        -------
        None
        """
        self.setParameter(self.getConst('ID_REG_KP_DISP'), value *1e6)
    
    def getZFeedbackPIConstant(self):
        """
        This function retrieves if the Z feedback controller P and I values are forced to be constant.

        Parameters
        ----------
        None.

        Returns
        -------
        enabled : int
            [0, 1] forced P and I to be constant [off/on]
        """
        enabled = self.getParameter(self.getConst('ID_REG_PI_CONST'))
        return enabled

    def setZFeedbackPIConstant(self, enable):
        """
        This function forces the Z feedback controller P and I values to be constant.

        Parameters
        ----------
        enable : int
            [0, 1] forces P and I to be constant [off/on]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_PI_CONST'), enable)

    def getZFeedbackPolarity(self):
        """
        This function retrieves if the feedback output polarity is inverted.

        Parameters
        ----------
        None

        Returns
        -------
        polarity : int
            [0, 1] Feedback output is [0] not inverted or [1] inverted
        """
        polarity = self.getParameter(self.getConst('ID_REG_POLARITY'))
        return polarity

    def setZFeedbackPolarity(self, polarity):
        """
        This function retrieves if the feedback output polarity is inverted.

        Parameters
        ----------
        polarity : int
            [0,1] Feedback output is [0] not inverted or [1] inverted

        Returns
        -------
        None
        """
        self.setParameter(self.getConst('ID_REG_POLARITY'), polarity)
        pass

    def getSlopeCompensation(self):
        """
        This function retrieves if the feedback slope compensation is enabled.

        Parameters
        ----------
        None

        Returns
        -------
        enabled : int
            [0, 1] Feedback slope compensation is [off/on]
        """
        enabled = self.getParameter(self.getConst('ID_REG_SLOPE_REQUEST'))
        return enabled

    def setSlopeCompensation(self, enable):
        """
        This function sets the feedback slope compensation [off/on].

        Parameters
        ----------
        enabled : int
            [0, 1] feedback slope compensation [off/on]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_SLOPE_REQUEST'), enable)
    
    def getSlopeCompensationStatus(self):
        """
        This function retrieves current status of the feedback slope compensation [0=off, 1=on, other=adjusting].

        Parameters
        ----------
        None.

        Returns
        -------
        status : int
            Status of the feedback slope compensation [0=off, 1=on, other=adjusting]
        """
        status = self.getParameter(self.getConst('ID_REG_SLOPE_STATUS'))
        return status

    def setSlopeCompensationStatus(self, status):
        """
        This function sets the status of the feedback slope compensation [0=off, 1=on, other=adjusting].

        Parameters
        ----------
        status : int
            Status of the feedback slope compensation [0=off, 1=on, other=adjusting]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_SLOPE_STATUS'), status)

    def getSlopeX(self):
        """
        This function retrieves the slope compensation X value in [%].

        Parameters
        ----------
        None.

        Returns
        -------
        slopeX : float
            Slope compensation X value in [%]
        """
        slopeX = self.getParameter(self.getConst('ID_REG_SLOPE_X'))*6.104*1e-4
        return slopeX

    def setSlopeX(self, slopeX):
        """
        This function sets the slope compensation X value in [%].

        Parameters
        ----------
        slopeX : float
            Slope compensation X value in [%]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_SLOPE_X'), slopeX/6.104*1e4)
    
    def getSlopeY(self):
        """
        This function retrieves the slope compensation Y value in [%].

        Parameters
        ----------
        None.

        Returns
        -------
        slopeY : float
            Slope compensation Y value in [%]
        """
        slopeY = self.getParameter(self.getConst('ID_REG_SLOPE_Y'))*6.104*1e-4
        return slopeY

    def setSlopeY(self, slopeY):
        """
        This function sets the slope compensation Y value in [%].

        Parameters
        ----------
        slopeY : float
            Slope compensation Y value in [%]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_SLOPE_Y'), slopeY/6.104*1e4)
    
    def getSlopeY(self):
        """
        This function retrieves the slope compensation X and Y value as list in [%].

        Parameters
        ----------
        None.

        Returns
        -------
        slopeXY : list
            [slopeX, slopeY] Slope compensation X and Y values in [%]
        """
        slopeX = self.getParameter(self.getConst('ID_REG_SLOPE_X'))*6.104*1e-4
        slopeY = self.getParameter(self.getConst('ID_REG_SLOPE_Y'))*6.104*1e-4
        slopeXY = [slopeX, slopeY]
        return slopeXY

    def setSlopeXY(self, slopeXY):
        """
        This function sets the slope compensation X and Y values as list in [%].

        Parameters
        ----------
        slopeXY : list
            [slopeX, slopeY] Slope compensation X and Y values in [%]

        Returns
        -------
        None.
        """
        [slopeX, slopeY] = slopeXY
        self.setParameter(self.getConst('ID_REG_SLOPE_X'), slopeX/6.104*1e4)
        self.setParameter(self.getConst('ID_REG_SLOPE_Y'), slopeY/6.104*1e4)


    def getZFeedbackSetpoint(self):
        """
        This function retrieves the setpoint amplitude for the Z feedback.

        Parameters
        ----------
        None
        
        Returns
        -------
        setpoint : float 
            Setpoint amplitude in [V]
        """
        raw_val = self.getParameter(self.getConst('ID_REG_SETP_DISP'))
        offset = self.getParameter(self.getConst('ID_GUI_OFFS_ZREG'))
        scale = self.getParameter(self.getConst('ID_GUI_SCAL_ZREG'))
        unit_raw = self.getParameter(self.getConst('ID_GUI_UNIT_ZREG'))
        unit = self.convertUnitToFactor(unit_raw)
        setpoint = (raw_val + offset)/scale * unit
        
        return setpoint


    def setZFeedbackSetpoint(self, setpoint):
        """
        This function sets the setpoint amplitude for the Z feedback.

        Parameters
        ----------
        None
        
        Returns
        -------
        setpoint : float
            Setpoint amplitude in [V]
        """
        offset = self.getParameter(self.getConst('ID_GUI_OFFS_ZREG'))
        scale = self.getParameter(self.getConst('ID_GUI_SCAL_ZREG'))
        unit_raw = self.getParameter(self.getConst('ID_GUI_UNIT_ZREG'))
        unit = self.convertUnitToFactor(unit_raw)
        raw_val = (setpoint * scale)/unit # - offset
        
        self.setParameter(self.getConst('ID_REG_SETP_DISP'), raw_val)
    
    def getZFeedbackSetpointUnit(self):
        """
        This function retrieves the currently set unit of the Z feedback setpoint.

        Parameters
        ----------
        None
        
        Returns
        -------
        unit : str
            Setpoint unit (e.g. 'mV')
        """
        unit_raw = self.getParameter(self.getConst('ID_GUI_UNIT_ZREG'))
        unit = self.printUnit(unit_raw)
        return unit
    
    
