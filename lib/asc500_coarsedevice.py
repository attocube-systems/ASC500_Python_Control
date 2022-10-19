from .asc500_base import ASC500Base

#This class is not working with the ANC350 or AMC300

class ASC500CoarseDevice(ASC500Base):
    '''The adresses control the coarse step generator. Index is the coarse device (0...6).
    Note that not all coarse control commands work with all posslible power amplifiers.'''

    def getCoarseAxisMode(self, axis):
        """
        This function retrieves the mode for the axis of the coarse device.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device

        Returns
        -------
        mode : int
            [1, 2] Mode to set the axis (1=step, 2 = ground)
        """
        mode = self.getParameter(self.getConst('ID_CRS_AXIS_MODE'), index = int(axis))
        return mode

    def setCoarseAxisMode(self, axis, mode):
        """
        This function sets the mode for the axis of the coarse device.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        mode : int
            [1, 2] Mode to set the axis (1=step, 2 = ground)

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_CRS_AXIS_MODE'), int(mode), int(axis))
    
    def stepCoarseUp(self, axis, steps):
        """
        This function performs a number of upward steps on an axis of the coarse device.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        steps : int
            Number of upward steps

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_CRS_AXIS_UP'), int(steps), int(axis))

    def stepCoarseDown(self, axis, steps):
        """
        This function performs a number of downward steps on an axis of the coarse device.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        steps : int
            Number of downward steps

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_CRS_AXIS_DN'), int(steps), int(axis))
    
    def getCoarseContinuousDown(self, axis):
        """
        This function retrieves the continuous upward stepping status on axis of the coarse device.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        
        Returns
        -------
        enabled : int
            [0, 1] Continuous upward stepping [off/on]
        """
        enabled = self.getParameter(self.getConst('ID_CRS_AXIS_CUP'), index = int(axis))
        return enabled

    def setCoarseContinuousDown(self, axis, enable):
        """
        This function switches on/off the continuous upward stepping on axis of the coarse device.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        enable : int
            [0, 1] Set continuous upward stepping [off/on]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_CRS_AXIS_CUP'), int(enable), int(axis))

    def getCoarseContinuousDown(self, axis):
        """
        This function retrieves the continuous downward stepping status on axis of the coarse device.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        
        Returns
        -------
        enabled : int
            [0, 1] Continuous downward stepping [off/on]
        """
        enabled = self.getParameter(self.getConst('ID_CRS_AXIS_CDN'), index = int(axis))
        return enabled
        
    def setCoarseContinuousDown(self, axis, enable):
        """
        This function switches on/off the continuous downward stepping on axis of the coarse device.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        enable : int
            [0, 1] Set continuous downward stepping [off/on]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_CRS_AXIS_CDN'), int(enable), int(axis))

    def getCoarseFrequency(self, axis):
        """
        This function retrieves the coarse device axis frequency.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        
        Returns
        -------
        frequency : int
            Coarse axis frequency in [Hz]
        """
        frequency = self.getParameter(self.getConst('ID_CRS_FREQUENCY'), index = int(axis))
        return frequency

    def setCoarseFrequency(self, axis, frequency):
        """
        This function sets the coarse device axis frequency.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        frequency : int
            [0..8000] Coarse axis frequency in [Hz]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_CRS_FREQUENCY'), int(frequency), int(axis))
    
    def getCoarseVoltage(self, axis):
        """
        This function retrieves the coarse device axis voltage.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        
        Returns
        -------
        voltage : int
            Coarse axis voltage in [V]
        """
        voltage = self.getParameter(self.getConst('ID_CRS_VOLTAGE'), index = int(axis))
        return voltage

    def setCoarseVoltage(self, axis, voltage):
        """
        This function sets the coarse device axis voltage.

        Parameters
        ----------
        axis : int
            [0..7] Axis of the coarse device
        voltage : int
            [0..70] Coarse axis voltage in [V]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_CRS_VOLTAGE'), voltage, int(axis))