
class ASC500AFM():
    """ These funciotns control the AFM measurement method and related features."""
    
    def getTFExcicationFrequency(self):
        """
        This function retrieves the current excitation frequency of the tuning fork.

        Parameters
        ----------
        None.

        Returns
        -------
        frequency : float
            Current excitation frequency in [Hz]
        """
        frequency = self.getParameter(self.getConst('ID_AFM_F_IN'))*1e-3
        return frequency
    
    def setTFExcitationFrequency(self, frequency):
        """
        This function sets the excitation frequency of the tuning fork.

        Parameters
        ----------
        frequency : float
            Excitation frequency in [Hz]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_F_IN'), frequency*1e3)
    
    def getTFExcitationAmplitude(self):
        """
        This function retrieves the current excitation amplitude of the tuning fork.

        Parameters
        ----------
        None.
        
        Returns
        -------
        amplitude : float
            Current excitation amplitude in [V]
        """
        amplitude = self.getParameter(self.getConst('ID_AFM_R_AMP_OUT'))*19.074*1e-6
        return amplitude

    def setTFExcitationAmplitude(self, amplitude):
        """
        This function sets the excitation amplitude of the tuning fork.

        Parameters
        ----------
        amplitude : float
            Excitation amplitude in [V]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_AMP_OUT'), amplitude/19.074*1e6)

    def getTFDetectionSensitivity(self):
        """
        This function retrieves the current detection sensitivity range of the tuning fork.

        Parameters
        ----------
        None.
        
        Returns
        -------
        sensitivitiy : float
            Current detection sensitivity range in [V]
        """
        sensitivitiy = self.getParameter(self.getConst('ID_AFM_L_AMPL'))*305.2*1e-6
        return sensitivitiy

    def setTFDetectionSensitivity(self, sensitivitiy):
        """
        This function sets the detection sensitivity range of the tuning fork.

        Parameters
        ----------
        sensitivitiy : float
            Detection sensitivity range in [V]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_L_AMPL'), sensitivitiy/305.2*1e6)

    def getTFDetectionPhaseShift(self):
        """
        This function retrieves the current detection phaseshift of the tuning fork.

        Parameters
        ----------
        None.
        
        Returns
        -------
        phaseshift : float
            Current detection phaseshift in [rad]
        """
        phaseshift = self.getParameter(self.getConst('ID_AFM_L_PHASE'))*1.463*1e-9
        return phaseshift

    def setTFDetectionPhaseShift(self, phaseshift):
        """
        This function sets the detection phaseshift of the tuning fork.

        Parameters
        ----------
        phaseshift : float
            Detection phaseshift in [rad]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_L_PHASE'))/1.463*1e9

    def getTFDetectionSampleTime(self):
        """
        This function retrieves the current detection sampling time of the tuning fork.

        Parameters
        ----------
        None.

        Returns
        -------
        samptime : float 
            Current detection sampling time in [s]
        """
        samptime = self.getParameter(self.getConst('ID_AFM_L_SMPLTM'))*20*1e-9
        return samptime

    def setTFDetectionSampleTime(self, samptime):
        """
        This function sets the detection sampling time of the tuning fork.

        Parameters
        ----------
        samptime : float
            Detection sampling time in [s]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_L_SMPLTM'), samptime/20*1e9)

    def getTFAmplitudeSetpoint(self):
        """
        This function retrieves the setpoint amplitude of the tuning fork.

        Parameters
        ----------
        None.

        Returns
        -------
        setpoint : float
            Current amplitude setpoint [V]
        """
        rawvalue = self.getParameter(self.getConst('ID_AFM_R_AMP_DISP'))
        unit = self.getParameter(self.getConst('ID_GUI_UNIT_AREG'))
        setpoint = rawvalue*unit
        return setpoint

    def setTFAmplitudeSetpoint(self, setpoint):
        """
        This function sets the setpoint amplitude of the tuning fork.

        Parameters
        ----------
        setpoint : float
            Current amplitude setpoint [V]
        
        Returns
        -------
        None.
        """
        unit = self.getParameter(self.getConst('ID_GUI_UNIT_AREG'))
        rawvalue = setpoint/unit
        self.setParameter(self.getConst('ID_AFM_R_AMP_DISP'), rawvalue)

    def getTFFrequencySetpoint(self):
        """
        This function retrieves the setpoint frequency of the tuning fork.

        Parameters
        ----------
        None.

        Returns
        -------
        setpoint : float
            Current frequency setpoint [V]
        """
        rawvalue = self.getParameter(self.getConst('ID_AFM_R_FRQ_DISP'))
        unit = self.getParameter(self.getConst('ID_GUI_UNIT_PREG'))
        setpoint = rawvalue*unit
        return setpoint

    def setTFFrequencySetpoint(self, setpoint):
        """
        This function sets the setpoint frequency of the tuning fork.

        Parameters
        ----------
        setpoint : float
            Current frequency setpoint [V]
        
        Returns
        -------
        None.
        """
        unit = self.getParameter(self.getConst('ID_GUI_UNIT_PREG'))
        rawvalue = setpoint/unit
        self.setParameter(self.getConst('ID_AFM_R_FRQ_DISP'), rawvalue)
    
    def setTFExcitationEnable(self, enable: bool):
        """
        Since there is no way of actually turning of the excitation, we save the current amplitude and then set it
        to zero. Reenabling restores the previous amplitude value.
        
        Parameters
        ----------
        enable : bool
            [True/False] Set Excitation on/off
        
        Returns
        -------
        None.
        """
        if not enable:
            self._prevTfAmp = self.tfExcitationAmp
            self.tfExcitationAmp = 0
        else:
            currTfAmp = self.tfExcitationAmp
            if currTfAmp != 0:
                # already enabled
                return

            try:
                self.tfExcitationAmp = self._prevTfAmp
            except AttributeError:
                # if it hasn't been actively disabled, we don't have any value to restore.
                pass


