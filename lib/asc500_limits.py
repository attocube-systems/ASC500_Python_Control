from .asc500_base import ASC500Base


class ASC500Limits(ASC500Base):
    
    # Voltage Limits:
    def getXVoltageLimit(self):
        """
        Retrieves the currently set voltage limit for X axis, as a List [maxRT, maxLT] in [V]
        
        Parameters
        ----------
        None.

        Returns
        -------
        vLim : list
            [maxRT, maxLT] in [V]
        """
        vLim = [(self.getParameter(self.getConst('ID_PIEZO_VOLTLIM_X'), index=i)*305.2*1e-6) for i in [0, 1]]
        return vLim

    def getYVoltageLimit(self):
        """
        Retrieves the currently set voltage limit for Y axis, as a List [maxRT, maxLT] in [V]
        
        Parameters
        ----------
        None.

        Returns
        -------
        vLim : list
            [maxRT, maxLT] in [V]
        """
        vLim = [(self.getParameter(self.getConst('ID_PIEZO_VOLTLIM_Y'), index=i)*305.2*1e-6) for i in [0, 1]]
        return vLim

    def getZVoltageLimit(self):
        """
        Retrieves the currently set voltage limit for Z axis, as a List [maxRT, maxLT] in [V]
        
        Parameters
        ----------
        None.

        Returns
        -------
        vLim : list
            [maxRT, maxLT] in [V]
        """
        vLim = [(self.getParameter(self.getConst('ID_REG_ZABS_LIM_A'), index=i)*19.07*1e-6) for i in [0, 1]]
        return vLim

    def getXActualVoltageLimit(self):
        """
        Retrieves the currently set voltage limit for X axis, at the operational Temperature in [V]
        
        Parameters
        ----------
        None.

        Returns
        -------
        vLimAct : float
            Actual T-dependent voltage in [V]
        """
        vLimAct = self.getParameter(self.getConst('ID_PIEZO_ACTVOLT_HX'))*305.2*1e-6
        return vLimAct

    def getYActualVoltageLimit(self):
        """
        Retrieves the currently set voltage limit for Y axis, at the operational Temperature in [V]
        
        Parameters
        ----------
        None.

        Returns
        -------
        vLimAct : float
            actual T-dependent voltage in [V]
        """
        vLimAct =self.getParameter(self.getConst('ID_PIEZO_ACTVOLT_HY'))*305.2*1e-6
        return vLimAct

    def getZActualVoltageLimit(self):
        """
        Retrieves the currently set voltage limit for Z axis, at the operational Temperature in [V]
        
        Parameters
        ----------
        None.

        Returns
        -------
        vLimAct : float
            actual T-dependent voltage in [V]
        """
        vLimAct = self.getParameter(self.getConst('ID_REG_ZABS_LIM'))*19.07*1e-6
        return vLimAct

    def setXVoltageLimit(self, vLim):
        """
        Sets the voltage limit for X axis, input is given as a List [maxRT, maxLT] in [V]
        
        Parameters
        ----------
        vLim : list
            [maxRT, maxLT] in [V]

        Returns
        -------
        None.
        """
        maxVscn = [(v/305.2*1e6) for v in vLim]
        self.setParameter(self.getConst('ID_PIEZO_VOLTLIM_X'), maxVscn[0], index=0)
        self.setParameter(self.getConst('ID_PIEZO_VOLTLIM_X'), maxVscn[1], index=1)

    def setYVoltageLimit(self, vLim):
        """
        Sets the voltage limit for Y axis, input is given as a List [maxRT, maxLT] in [V]
        
        Parameters
        ----------
        vLim : list
            [maxRT, maxLT] in [V]

        Returns
        -------
        None.
        """
        maxVscn = [(v/305.2*1e6) for v in vLim]
        self.setParameter(self.getConst('ID_PIEZO_VOLTLIM_Y'), maxVscn[0], index=0)
        self.setParameter(self.getConst('ID_PIEZO_VOLTLIM_Y'), maxVscn[1], index=1)
    
    def setZVoltageLimit(self, vLim):
        """
        Sets the voltage limit for Z axis, input is given as a List [maxRT, maxLT] in [V]
        
        Parameters
        ----------
        vLim : list
            [maxRT, maxLT] in [V]

        Returns
        -------
        None.
        """
        maxVscn = [(v/19.07*1e6) for v in vLim]
        self.setParameter(self.getConst('ID_REG_ZABS_LIM_A'), maxVscn[0], index=0)
        self.setParameter(self.getConst('ID_REG_ZABS_LIM_A'), maxVscn[1], index=1)

    # Travel Limits:
    def getXTravelLimit(self):
        """
        Retrieves the currently set deflection limit for X axis, as a List [maxRT, maxLT] in [m]
        
        Parameters
        ----------
        None.

        Returns
        -------
        tLim : list
            [maxRT, maxLT] in [V]
        """
        tLim = [(self.getParameter(self.getConst('ID_PIEZO_RANGE_X'), index=i)*1e-11) for i in [0, 1]]
        return tLim

    def getYTravelLimit(self):
        """
        Retrieves the currently set deflection limit for Y axis, as a List [maxRT, maxLT] in [m]
        
        Parameters
        ----------
        None.

        Returns
        -------
        tLim : list
            [maxRT, maxLT] in [V]
        """
        tLim = [(self.getParameter(self.getConst('ID_PIEZO_RANGE_Y'), index=i)*1e-11) for i in [0, 1]]
        return tLim

    def getZTravelLimit(self):
        """
        Retrieves the currently set deflection limit for Z axis, as a List [maxRT, maxLT] in [m]
        
        Parameters
        ----------
        None.

        Returns
        -------
        tLim : list
            [maxRT, maxLT] in [V]
        """
        tLim = [(self.getParameter(self.getConst('ID_REG_ZABS_LIMM_A'), index=i)*1e-12) for i in [0, 1]]
        return tLim

    def getXActualTravelLimit(self):
        """
        Retrieves the currently set deflection limit for X axis, at the operational Temperature in [m]
        
        Parameters
        ----------
        None.

        Returns
        -------
        tLimAct : float
            actual T-dependent deflection limit in [m]
        """
        tLimAct = self.getParameter(self.getConst('ID_PIEZO_ACTRG_X'))*1e-11
        return tLimAct

    def getYActualTravelLimit(self):
        """
        Retrieves the currently set deflection limit for Y axis, at the operational Temperature in [m]
        
        Parameters
        ----------
        None.

        Returns
        -------
        tLimAct : float
            actual T-dependent deflection limit in [m]
        """
        tLimAct = self.getParameter(self.getConst('ID_PIEZO_ACTRG_Y'))*1e-11
        return tLimAct
    
    def getZActualTravelLimit(self):
        """
        Retrieves the currently set deflection limit for Z axis, at the operational Temperature in [m]
        
        Parameters
        ----------
        None.

        Returns
        -------
        tLimAct : float
            actual T-dependent deflection limit in [m]
        """
        tLimAct = self.getParameter(self.getConst('ID_REG_ZABS_LIMM'))*1e-12
        return tLimAct

    def setXTravelLimit(self, tLim):
        """
        Sets the deflection limit for X axis, input is given as a List [maxRT, maxLT] in [m]
        
        Parameters
        ----------
        tLim : list
            [maxRT, maxLT] in [m]

        Returns
        -------
        None.
        """
        maxTravel = [(t*1e11) for t in tLim]
        self.setParameter(self.getConst('ID_PIEZO_RANGE_X'), maxTravel[0], index=0)
        self.setParameter(self.getConst('ID_PIEZO_RANGE_X'), maxTravel[1], index=1)

    def setYTravelLimit(self, tLim):
        """
        Sets the deflection limit for Y axis, input is given as a List [maxRT, maxLT] in [m]
        
        Parameters
        ----------
        tLim : list
            [maxRT, maxLT] in [m]

        Returns
        -------
        None.
        """
        maxTravel = [(t*1e11) for t in tLim]
        self.setParameter(self.getConst('ID_PIEZO_RANGE_Y'), maxTravel[0], index=0)
        self.setParameter(self.getConst('ID_PIEZO_RANGE_Y'), maxTravel[1], index=1)

    def setZTravelLimit(self, tLim):
        """
        Sets the deflection limit for Z axis, input is given as a List [maxRT, maxLT] in [m]
        
        Parameters
        ----------
        tLim : list
            [maxRT, maxLT] in [m]

        Returns
        -------
        None.
        """
        maxTravel = [(t*1e12) for t in tLim]
        self.setParameter(self.getConst('ID_REG_ZABS_LIMM_A'), maxTravel[0], index=0)
        self.setParameter(self.getConst('ID_REG_ZABS_LIMM_A'), maxTravel[1], index=1)

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
    
    def getTemperatureLimits(self):
        """
        Retrieves the temperature limits set for room and low temperature as a List [RT, LT] in [K]
        
        Parameters
        ----------

        Returns
        -------
        tempLim : list
            [RT, LT] in [K]
        None.
        """
        tempLim = self.setParameter(self.getConst('ID_PIEZO_T_LIM'))*1e-3
        return tempLim

    def setTemperatureLimits(self, tempLim):
        """
        Sets the temperature limits for room and low temperature, input is given as a List [RT, LT] in [K]
        
        Parameters
        ----------
        tempLim : list
            [RT, LT] in [K]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_PIEZO_T_LIM'), tempLim*1e3)
    
    def getTemperature(self):
        """
        Retrieves the currently set temperature value for interpolation.
        
        Parameters
        ----------

        Returns
        -------
        temp : float
            Temperature in [K]
        None.
        """
        temp = self.getParameter(self.getConst('ID_PIEZO_TEMP'))*1e-3
        return temp
    
    def setTemperature(self, temp):
        """
        Sets the temperature value for interpolation.
        
        Parameters
        ----------
        temp : float
            Temperature in [K]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_PIEZO_TEMP'), temp*1e3)
    

    def getDACLimits(self, channel):
        """
        This function retrieves the output limits for the given DAC output.
        
        Parameters
        ----------
        channel : int
            [0..5] DAC-Channel number

        Returns
        -------
        limits : list
            [limitRT, limitLT] DAC output limits
        None.
        """
        limitRT = self.getParameter(self.getConst('ID_GENDAC_LIMIT_RT'), channel)*1e-6
        limitLT = self.getParameter(self.getConst('ID_GENDAC_LIMIT_LT'), channel)*1e-6
        limits = [limitRT, limitLT]
        return limits
    
    def setDACLimits(self, channel, limits):
        """
        This function sets the output limits for the given DAC output.
        
        Parameters
        ----------
        channel : int
            [0..5] DAC-Channel number

        limits : list
            [limitRT, limitLT] DAC output limits

        Returns
        -------
        None.
        """
        [limitRT, limitLT] = limits
        self.setParameter(self.getConst('ID_GENDAC_LIMIT_RT'), limitRT*1e6, channel)
        self.setParameter(self.getConst('ID_GENDAC_LIMIT_LT'), limitLT*1e6, channel)
    
    def getDACLimitsCT(self, channel):
        """
        This function retrieves the output limit at the currently set temperature for the given DAC output.
        
        Parameters
        ----------
        channel : int
            [0..5] DAC-Channel number

        Returns
        -------
        limitCT : list
            DAC output limits at current temp
        None.
        """
        limitCT = self.getParameter(self.getConst('ID_GENDAC_LIMIT_CT'), channel)*1e-6
        return limitCT
    