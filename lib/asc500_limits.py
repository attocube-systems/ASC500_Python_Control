from lib.asc500_base import ASC500Base


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
        vLimAct = self.getParameter(self.getConst('ID_PIEZO_ACTVOLT_HX')*305.2*1e-6)
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
        vLimAct =self.getParameter(self.getConst('ID_PIEZO_ACTVOLT_HY')*305.2*1e-6)
        return yLimAct

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
        vLimAct = self.getParameter(self.getConst('ID_REG_ZABS_LIM')*19.07*1e-6)
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
        tLimAct = self.getParameter(self.getConst('ID_PIEZO_ACTRG_X'))*1e-11
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
            [maxRT, maxLT] in [V]

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
            [maxRT, maxLT] in [V]

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
            [maxRT, maxLT] in [V]

        Returns
        -------
        None.
        """
        maxTravel = [(t*1e12) for t in tLim]
        self.setParameter(self.getConst('ID_REG_ZABS_LIMM_A'), maxTravel[0], index=0)
        self.setParameter(self.getConst('ID_REG_ZABS_LIMM_A'), maxTravel[1], index=1)
    
    
    