from .asc500_base import ASC500Base


class ASC500Crosslink(ASC500Base):
    """
    The addresses are used to configure the two generic feedback loops (crosslink 1 and 2).
    Index 0 is used to access crosslink 1, index 1 for crosslink 2.
    """
    def getCrosslinkON(self, crosslink):
        """
        This function retrieves, if the generic feedback loop at crosslink 1 or 2 [0, 1] is disabled/enabled.

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        
        Returns
        -------
        enabled : int
            [0, 1] generic feedback loop is [disabled/enabled]
        """
        enabled = self.getParameter(self.getConst('ID_REG_GEN_CTL'), crosslink)
        return enabled

    def setCrosslinkON(self, crosslink, enable):
        """
        This function sets the generic feedback loop at crosslink 1 or 2 [0, 1] to disabled/enabled.

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        enabled : int
            [0, 1] set generic feedback loop to [disabled/enabled]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_GEN_CTL'), enable, crosslink)
    
    def getCrosslinkInvPolarity(self, crosslink):
        """
        This function retrieves, if the polarity at crosslink 1 or 2 [0, 1] is inverted or not.

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        
        Returns
        -------
        invert : int
            [0, 1] crosslink polarity is [not inverted/inverted]
        """
        invert = self.getParameter(self.getConst('ID_REG_GEN_POL'), crosslink)
        return invert

    def setCrosslinkInvPolarity(self, crosslink, invert):
        """
        This function sets the polarity at crosslink 1 or 2 [0, 1] to not inverted/inverted.

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        invert : int
            [0, 1] set crosslink polarity [not inverted/inverted]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_GEN_POL'), invert, crosslink)
    
    def getCrosslinkInput(self, crosslink):
        """
        This function retrieves the input signal source channel at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        
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
        channel = self.getParameter(self.getConst('ID_REG_GEN_INPUT'), crosslink)
        return channel
    
    def setCrosslinkInput(self, crosslink, channel):
        """
        This function sets the input signal source channel at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
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
        
        Returns
        -------
        """
        self.setParameter(self.getConst('ID_REG_GEN_INPUT'), channel, crosslink)

    def getCrosslinkOutput(self, crosslink):
        """
        This function retrieves the controller output channel (DAC1..4) at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        
        Returns
        -------
        channel : int
            [0..3] for DAC1..4
        """
        channel = self.getParameter(self.getConst('ID_REG_GEN_DAC'), crosslink)
        return channel
    
    def setCrosslinkOutput(self, crosslink, channel):
        """
        This function sets the controller output channel (DAC1..4) at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        channel : int
            [0..3] for DAC1..4
        
        Returns
        -------
        """
        self.setParameter(self.getConst('ID_REG_GEN_DAC'), channel, crosslink)
    
    def getCrosslinkOutputMin(self, crosslink):
        """
        This function retrieves the minimum output voltage in [V] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        
        Returns
        -------
        outMin : float
            Minimum voltage in [V]
        """
        outMin = self.getParameter(self.getConst('ID_REG_GEN_MIN_DISP'), crosslink)*1e-6
        return outMin
    
    def setCrosslinkOutputMin(self, crosslink, outMin):
        """
        This function sets the minimum output voltage in [V] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        outMin : float
            Minimum voltage in [V]
        
        Returns
        -------
        """
        self.setParameter(self.getConst('ID_REG_GEN_MIN_DISP'), outMin*1e6, crosslink)
    
    def getCrosslinkOutputMax(self, crosslink):
        """
        This function retrieves the maximum output voltage in [V] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        
        Returns
        -------
        outMax : float
            Maximum voltage in [V]
        """
        outMax = self.getParameter(self.getConst('ID_REG_GEN_MAX_DISP'), crosslink)*1e-6
        return outMax
    
    def setCrosslinkOutputMax(self, crosslink, outMax):
        """
        This function sets the maximum output voltage in [V] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        outMax : float
            Maximum voltage in [V]
        
        Returns
        -------
        """
        self.setParameter(self.getConst('ID_REG_GEN_MAX_DISP'), outMax*1e6, crosslink)
    
    def getCrosslinkOutputMinMax(self, crosslink):
        """
        This function retrieves the minimum and maximum output voltage in [V] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        
        Returns
        -------
        output : list
            [outMin, outMax] Minimum and maximum voltage in [V]
        """
        outMin = self.getParameter(self.getConst('ID_REG_GEN_MIN_DISP'), crosslink)*1e-6
        outMax = self.getParameter(self.getConst('ID_REG_GEN_MAX_DISP'), crosslink)*1e-6
        output = [outMin, outMax]
        return output

    def setCrosslinkOutputMinMax(self, crosslink, output):
        """
        This function sets the minimum and maximum output voltage in [V] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        output : list
            [outMin, outMax] Minimum and maximum voltage in [V]
        
        Returns
        -------
        """
        outMin = output[0]
        outMax = output[1]
        self.setParameter(self.getConst('ID_REG_GEN_MIN_DISP'), outMin*1e6, crosslink)
        self.setParameter(self.getConst('ID_REG_GEN_MAX_DISP'), outMax*1e6, crosslink)
    
    def getCrosslinkOutputVoltage(self, crosslink):
        """
        This function retrieves the current output voltage in [V] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        
        Returns
        -------
        voltOut : float
            Current voltage in [V]
        """
        voltOut = self.getParameter(self.getConst('ID_REG_GEN_OUT_DISP'), crosslink)*1e-6
        return voltOut
    
    def setCrosslinkOutputVoltage(self, crosslink, voltOut):
        """
        This function sets the current output voltage in [V] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        voltOut : float
            Current voltage in [V]
        
        Returns
        -------
        """
        self.setParameter(self.getConst('ID_REG_GEN_OUT_DISP'), voltOut*1e6, crosslink)
    
    def resetCrosslink(self, crosslink):
        """
        This function resets the crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        
        Returns
        -------
        """
        self.setParameter(self.getConst('ID_REG_GEN_RESET'), 0, crosslink)
    
    def getCrosslinkI(self, crosslink):
        """
        This function retrieves the controller integral part I [Hz] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2

        Returns
        -------
        value : float
            Controller integral part I in [Hz]
        """
        value = self.getParameter(self.getConst('ID_REG_GEN_KI_DISP'), crosslink)*1e-3
        return value
    
    def setCrosslinkI(self, crosslink, value):
        """
        This function sets the controller integral part I [Hz] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        value : float
            Controller integral part I in [Hz]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_GEN_KI_DISP'), value*1e3, crosslink)
    
    def getCrosslinkP(self, crosslink):
        """
        This function retrieves the controller proportional part P at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2

        Returns
        -------
        value : float
            Controller proportional part P
        """
        value = self.getParameter(self.getConst('ID_REG_GEN_KP_DISP'), crosslink)*1e-6
        return value
    
    def setCrosslinkP(self, crosslink, value):
        """
        This function sets the controller proportional part P [Hz] at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        value : float
            Controller proportional part P

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_GEN_KP_DISP'), value*1e6, crosslink)
    
    def getCrosslinkIConstant(self, crosslink):
        """
        This function retrieves if controller P and I values are forced to be constant at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2

        Returns
        -------
        enabled : int
            [0, 1] forced P and I to be constant [off/on]
        """
        enabled = self.getParameter(self.getConst('ID_REG_GEN_PI_CONST'), crosslink)
        return enabled

    def setCrosslinkPIConstant(self, crosslink, enable):
        """
        This function forces the controller P and I values to be constant at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        enable : int
            [0, 1] forces P and I to be constant [off/on]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_GEN_PI_CONST'), enable, crosslink)
    
    def getCrosslinkSetpoint(self, crosslink):
        """
        This function retrieves the setpoint amplitude at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2

        Returns
        -------
        setpoint : float
            Setpoint amplitude in [V]
        """
        setpoint = self.getParameter(self.getConst('ID_REG_GEN_SP_DISP'), crosslink)*1e-3
        return setpoint
    
    def setCrosslinkSetpoint(self, crosslink, setpoint):
        """
        This function sets the setpoint amplitude at crosslink 1 or 2 [0, 1].

        Parameters
        ----------
        crosslink : int
            [0, 1] crosslink 1 or 2
        setpoint : float
            Setpoint amplitude in [V]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_GEN_SP_DISP'), setpoint, crosslink)
    
