from lib.asc500_base import ASC500Base


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

    def getZFeedbackLimits(self):
        """
        This function retrieves the Z feedback limits.

        Parameters
        ----------
        None
        
        Returns
        -------
        limits : list
            [limMin, limMax] Minimum and maximum feedback limits in [m]
        """
        limMin = self.getParameter(self.getConst('ID_REG_LIM_MINUSR_M'))*1e-12
        limMax = self.getParameter(self.getConst('ID_REG_LIM_MAXUSR_M'))*1e-12
        limits = [limMin, limMax]
        return limits
    
    def setZFeedbackLimits(self, limits):
        """
        This function sets the Z feedback limits.

        Parameters
        ----------
        limits : list
            [limMin, limMax] Minimum and Maximum feedback limits in [m]

        Returns
        -------
        None
        """
        self.setParameter(self.getConst('ID_REG_LIM_MINUSR_M'), limits[0]*1e12)
        self.setParameter(self.getConst('ID_REG_LIM_MAXUSR_M'), limits[1]*1e12)

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

    def getZFeedbackSetpoint(self):
        """
        This function retrieves the setpoint amplitude for the Z feedback.

        Parameters
        ----------
        None
        
        Returns
        -------
        setpoint : int 
            Coarse axis amplitude in [V]
        """
        raw_val = self.getParameter(self.getConst('ID_REG_SETP_DISP'))
        offset = self.getParameter(self.getConst('ID_GUI_OFFS_ZREG'))
        scale = self.getParameter(self.getConst('ID_GUI_SCAL_ZREG'))
        unit = self.getParameter(self.getConst('ID_GUI_UNIT_ZREG'))
        
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
        setpoint : int
            Coarse axis amplitude in [V]
        """
        offset = self.getParameter(self.getConst('ID_GUI_OFFS_ZREG'))
        scale = self.getParameter(self.getConst('ID_GUI_SCAL_ZREG'))
        unit = self.getParameter(self.getConst('ID_GUI_UNIT_ZREG'))
        
        raw_val = (setpoint * scale)/unit - offset
        
        self.setParameter(self.getConst('ID_REG_SETP_DISP'), raw_val)