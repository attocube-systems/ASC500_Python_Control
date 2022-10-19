from .asc500_base import ASC500Base

class ASC500AFM(ASC500Base):
    """ These funciotns control the AFM measurement method and related features."""
    
    def getAFMExcicationFrequency(self):
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
    
    def setAFMExcitationFrequency(self, frequency):
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
    
    def getAFMExcitationAmplitude(self):
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

    def setAFMExcitationAmplitude(self, amplitude):
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

    def getAFMDetectionSensitivity(self):
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

    def setAFMDetectionSensitivity(self, sensitivitiy):
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

    def getAFMDetectionPhaseShift(self):
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

    def setAFMDetectionPhaseShift(self, phaseshift):
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
        self.setParameter(self.getConst('ID_AFM_L_PHASE'), phaseshift/1.463*1e9)

    
    def getAFMAutoPhase(self):
        """
        This function retrieves, if auto phase of the tuning fork is [disabeld/enabled].

        Parameters
        ----------
        None.

        Returns
        -------
        enabled : int 
            [0, 1] Auto phase is [disabeld/enabled]
        """
        enabled = self.getParameter(self.getConst('ID_AFM_AUTO_PHASE'))
        return enabled

    def setAFMAutoPhase(self, enable):
        """
        This function sets the auto phase of the tuning fork to [disabeld/enabled].

        Parameters
        ----------
        enabled : int 
            [0, 1] Set auto phase to [disabeld/enabled]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_AUTO_PHASE'), enable)

    def getAFMFDetectionSampleTime(self):
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

    def setAFMDetectionSampleTime(self, samptime):
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

    def getAFMQControl(self):
        """
        This function retrieves, if the AFM Q control feature is enabled.

        Parameters
        ----------
        None.
        
        Returns
        -------
        enabled : int
            [0, 1] Q control is [disabled, enabled]
        """
        enabled = self.getParameter(self.getConst('ID_QCONTROL_EN'))
        return enabled
    
    def setAFMQControl(self, enable):
        """
        This function [disables/enables] the AFM Q control feature.

        Parameters
        ----------
        enable : int
            [0, 1] Set Q control [disabled, enabled]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_QCONTROL_EN'), enable)
    
    def getAFMQControlPhase(self):
        """
        This function retrieves the phase in [deg] of the AFM Q control.

        Parameters
        ----------
        None.

        Returns
        -------
        phase : float
            Q control phase in [deg]
        """
        phase = self.getParameter(self.getConst('ID_QCONTROL_PHASE'))*1e-3
        return phase
    
    def setAFMQControlPhase(self, phase):
        """
        This function sets the phase in [deg] of the AFM Q control.

        Parameters
        ----------
        phase : float
            Q control phase in [deg]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_QCONTROL_PHASE'), phase*1e3)

    def getAFMQControlFeedback(self):
        """
        This function retrieves the feedback of the AFM Q control.

        Parameters
        ----------
        None.

        Returns
        -------
        feedback : float
            Q control feedback
        """
        feedback = self.getParameter(self.getConst('ID_QCONTROL_FEEDBACK'))*1e-3
        return feedback
    
    def setAFMQControlFeedback(self, feedback):
        """
        This function sets the feedback in of the AFM Q control.

        Parameters
        ----------
        feedback : float
            Q control feedback

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_QCONTROL_FEEDBACK'), feedback*1e3)

    def getAFMAmplitudeCtrlLoopOn(self):
        """
        This function retrieves, if the AFM Amplitude controller loop is [disabled/enabled].

        Parameters
        ----------
        None.
        
        Returns
        -------
        enabled : int
            [0, 1] amplitude controller loop is [disabled, enabled]
        """
        enabled = self.getParameter(self.getConst('ID_AFM_R_AMP_CTRL'))
        return enabled
    
    def setAFMAmplitudeCtrlLoopOn(self, enable):
        """
        This function [disables/enables] the AFM Amplitude controller loop.

        Parameters
        ----------
        enable : int
            [0, 1] Set amplitude controller loop [disabled, enabled]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_AMP_CTRL'), enable)
    
    def getAFMAmplitudeCtrlMin(self):
        """
        This function retrieves the minimum value for the AFM Amplitude controller loop in [V].

        Parameters
        ----------
        None.
        
        Returns
        -------
        ampMin : float
            Minimum amplitude controller loop [V]
        """
        ampMin = self.getParameter(self.getConst('ID_AFM_R_AMPMIN_DISP'))*19.074*1e-6
        return ampMin
    
    def setAFMAmplitudeCtrlMin(self, ampMin):
        """
        This function sets the minimum value for the AFM Amplitude controller loop in [V].

        Parameters
        ----------
        ampMin : float
            Minimum amplitude controller loop [V]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_AMPMIN_DISP'), ampMin/19.074*1e6)

    def getAFMAmplitudeCtrlMax(self):
        """
        This function retrieves the maximum value for the AFM Amplitude controller loop in [V].

        Parameters
        ----------
        None.
        
        Returns
        -------
        ampMax : float
            Maximum amplitude controller loop [V]
        """
        ampMax = self.getParameter(self.getConst('ID_AFM_R_AMPMAX_DISP'))*19.074*1e-6
        return ampMax
    
    def setAFMAmplitudeCtrlMax(self, ampMax):
        """
        This function sets the maximum value for the AFM Amplitude controller loop in [V].

        Parameters
        ----------
        ampMax : float
            Maximum amplitude controller loop [V]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_AMPMAX_DISP'), ampMax/19.074*1e6)

    def getAFMAmplitudeCtrlPolarity(self):
        """
        This function retrieves, if the polarity of the AFM Amplitude controller loop is [not inverted/inverted].

        Parameters
        ----------
        None.
        
        Returns
        -------
        polarity : int
            [0, 1] Polarity is [not inverted/inverted]
        """
        polarity = self.getParameter(self.getConst('ID_AFM_R_AMP_POL'))
        return polarity
    
    def setAFMAmplitudeCtrlPolarity(self, polarity):
        """
        This function sets the polarity of the AFM Amplitude controller loop to [not inverted/inverted].

        Parameters
        ----------
        polarity : int
            [0, 1] Set polarity [not inverted/inverted]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_AMP_POL'), polarity)

    def getAFMAmplitudeCtrlI(self):
        """
        This function retrieves the I value of the AFM Amplitude controller loop in [Hz].

        Parameters
        ----------
        None.
        
        Returns
        -------
        value : float
            I value in [Hz]
        """
        value = self.getParameter(self.getConst('ID_REG_A_KI_DISP'))*1e-3
        return value
    
    def setAFMAmplitudeCtrlI(self, value):
        """
        This function sets the I value of the AFM Amplitude controller loop in [Hz].

        Parameters
        ----------
        value : float
            I value in [Hz]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_A_KI_DISP'), value*1e3)
    
    def getAFMAmplitudeCtrlP(self):
        """
        This function retrieves the P value of the AFM Amplitude controller loop.

        Parameters
        ----------
        None.
        
        Returns
        -------
        value : float
            P value
        """
        value = self.getParameter(self.getConst('ID_REG_A_KP_DISP'))*1e-6
        return value
    
    def setAFMAmplitudeCtrlP(self, value):
        """
        This function sets the P value of the AFM Amplitude controller loop.

        Parameters
        ----------
        value : float
            P value
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_A_KP_DISP'), value*1e6)
#------------------------------------------    

    def getAFMFrequencyCtrlLoopOn(self):
        """
        This function retrieves, if the AFM Frequency controller loop is [disabled/enabled].

        Parameters
        ----------
        None.
        
        Returns
        -------
        enabled : int
            [0, 1] frequency controller loop is [disabled, enabled]
        """
        enabled = self.getParameter(self.getConst('ID_AFM_R_FRQ_CTRL'))
        return enabled
    
    def setAFMFrequencyCtrlLoopOn(self, enable):
        """
        This function [disables/enables] the AFM Frequency controller loop.

        Parameters
        ----------
        enable : int
            [0, 1] Set frequency controller loop [disabled, enabled]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_FRQ_CTRL'), enable)
    
    def getAFMFrequencyCtrldf(self):
        """
        This function retrieves the df value of the AFM Frequency controller loop in [Hz].

        Parameters
        ----------
        None.
        
        Returns
        -------
        value : float
            df value in [Hz]
        """
        value = self.getParameter(self.getConst('ID_AFM_L_DF_DISP'))*1e-3
        return value
    
    def setAFMFrequencyCtrldf(self, value):
        """
        This function sets the df value of the AFM Frequency controller loop in [Hz].

        Parameters
        ----------
        value : float
            df value in [Hz]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_L_DF_DISP'), value*1e3)

    def getAFMFrequencyCtrlMin(self):
        """
        This function retrieves the minimum value for the AFM Frequency controller loop in [V].

        Parameters
        ----------
        None.
        
        Returns
        -------
        freqMin : float
            Minimum frequency controller loop [V]
        """
        freqMin = self.getParameter(self.getConst('ID_AFM_R_FRQMIN'))*1e-3
        return freqMin
    
    def setAFMFrequencyCtrlMin(self, freqMin):
        """
        This function sets the minimum value for the AFM Frequency controller loop in [V].

        Parameters
        ----------
        freqMin : float
            Minimum frequency controller loop [V]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_FRQMIN'), freqMin*1e3)

    def getAFMFrequencyCtrlMax(self):
        """
        This function retrieves the maximum value for the AFM Frequency controller loop in [V].

        Parameters
        ----------
        None.
        
        Returns
        -------
        freqMax : float
            Maximum frequency controller loop [V]
        """
        freqMax = self.getParameter(self.getConst('ID_AFM_R_FRQMAX'))*1e-3
        return freqMax
    
    def setAFMFrequencyCtrlMax(self, freqMax):
        """
        This function sets the maximum value for the AFM Frequency controller loop in [V].

        Parameters
        ----------
        freqMax : float
            Maximum frequency controller loop [V]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_FRQMAX'), freqMax*1e3)

    def getAFMFrequencyCtrlPolarity(self):
        """
        This function retrieves, if the polarity of the AFM Frequency controller loop is [not inverted/inverted].

        Parameters
        ----------
        None.
        
        Returns
        -------
        polarity : int
            [0, 1] Polarity is [not inverted/inverted]
        """
        polarity = self.getParameter(self.getConst('ID_AFM_R_FRQ_POL'))
        return polarity
    
    def setAFMFrequencyCtrlPolarity(self, polarity):
        """
        This function sets the polarity of the AFM Frequency controller loop to [not inverted/inverted].

        Parameters
        ----------
        polarity : int
            [0, 1] Set polarity [not inverted/inverted]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_FRQ_POL'), polarity)

    def getAFMFrequencyCtrlI(self):
        """
        This function retrieves the I value of the AFM Frequency controller loop in [Hz].

        Parameters
        ----------
        None.
        
        Returns
        -------
        value : float
            I value in [Hz]
        """
        value = self.getParameter(self.getConst('ID_REG_F_KI_DISP'))*1e-6
        return value
    
    def setAFMFrequencyCtrlI(self, value):
        """
        This function sets the I value of the AFM Frequency controller loop in [Hz].

        Parameters
        ----------
        value : float
            I value in [Hz]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_F_KI_DISP'), value*1e6)
    
    def getAFMFrequencyCtrlP(self):
        """
        This function retrieves the P value of the AFM Frequency controller loop.

        Parameters
        ----------
        None.
        
        Returns
        -------
        value : float
            P value
        """
        value = self.getParameter(self.getConst('ID_REG_F_KP_DISP'))*1e-9
        return value
    
    def setAFMFrequencyCtrlP(self, value):
        """
        This function sets the P value of the AFM Frequency controller loop.

        Parameters
        ----------
        value : float
            P value
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_F_KP_DISP'), value*1e9)

    def getAFMFrequencyCtrlInput(self):
        """
        This function retrieves the input signal source channel for the AFM Frequency controller loop.

        Parameters
        ----------
        None.
        
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
        channel = self.getParameter(self.getConst('ID_AFM_R_FRQ_ACTVAL'))
        return channel
    
    def setAFMFrequencyCtrlInput(self, channel):
        """
        This function sets the input signal source channel for the AFM Frequency controller loop.

        Parameters
        ----------
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
        None.
        """
        self.setParameter(self.getConst('ID_AFM_R_FRQ_ACTVAL'), channel)

    def getAFMLockInAmplitude(self):
        """
        This function retrieves the AFM lockin modulation amplitude in [V]

        Parameters
        ----------
        None.
        
        Returns
        -------
        amplitude : float
            Modulation amplitude in [V]
        """
        amplitude = self.getParameter(self.getConst('ID_AFM_M_AMP'))*305.2*1e-6
        return amplitude
    
    def setAFMLockInAmplitude(self, amplitude):
        """
        This function sets the AFM lockin modulation amplitude in [V]

        Parameters
        ----------
        amplitude : float
            Modulation amplitude in [V]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_M_AMP'), amplitude/305.2*1e6)
    
    def getAFMLockInFrequency(self):
        """
        This function retrieves the AFM lockin modulation frequency in [Hz]

        Parameters
        ----------
        None.
        
        Returns
        -------
        frequency : float
            Modulation frequency in [Hz]
        """
        frequency = self.getParameter(self.getConst('ID_AFM_M_FREQ'))*1e-3
        return frequency
    
    def setAFMLockInFrequency(self, frequency):
        """
        This function sets the AFM lockin modulation frequency in [Hz]

        Parameters
        ----------
        frequency : float
            Modulation frequency in [Hz]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_M_FREQ'), frequency*1e3)

    def getAFMLockInPhaseShift(self):
        """
        This function retrieves the AFM lockin phase shift in [rad]

        Parameters
        ----------
        None.
        
        Returns
        -------
        phaseshift : float
            Phase shift in [rad]
        """
        phaseshift = self.getParameter(self.getConst('ID_AFM_M_SHIFT'))*1.463*1e-9
        return phaseshift
    
    def setAFMLockInPhaseShift(self, phaseshift):
        """
        This function sets the AFM lockin phase shift in [rad]

        Parameters
        ----------
        phaseshift : float
            Phase shift in [rad]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_M_SHIFT'), phaseshift/1.463*1e9)

    def getAFMLockInOutputConnect(self):
        """
        This function retrieves the output (0=Off, 1=DAC1, 2=DAC2, 3=DAC1+DAC2) connected to the lockin.

        Parameters
        ----------
        None.
        
        Returns
        -------
        output : int
            output connected to the lockin.
            (0=Off, 1=DAC1, 2=DAC2, 3=DAC1+DAC2)
        """
        output = self.getParameter(self.getConst('ID_AFM_M_DA'))
        return output
    
    def setAFMLockInOutputConnect(self, output):
        """
        This function sets the output (0=Off, 1=DAC1, 2=DAC2, 3=DAC1+DAC2) to connected to the lockin.

        Parameters
        ----------
        output : int
            output to connected to the lockin.
            (0=Off, 1=DAC1, 2=DAC2, 3=DAC1+DAC2)
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_M_DA'), output)

    def getAFMLockInInputConnect(self):
        """
        This function retrieves the input (one of CHANADC_...) connected to the lockin.

        Parameters
        ----------
        None.
        
        Returns
        -------
        input : int
            input connected to the lockin.

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
        input = self.getParameter(self.getConst('ID_AFM_M_AD'))
        return input
    
    def setAFMLockInInputConnect(self, input):
        """
        This function sets the input (one of CHANADC_...) to connected to the lockin.

        Parameters
        ----------
        input : int
            input to connected to the lockin.

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
        self.setParameter(self.getConst('ID_AFM_M_AD'), input)

    def getAFMLockInSensitivityRange(self):
        """
        This function retrieves the AFM lockin sensetivity range in [V]

        Parameters
        ----------
        None.
        
        Returns
        -------
        range : float
            Sensetivity range in [V]
        """
        range = self.getParameter(self.getConst('ID_AFM_M_DEMAMP'))*305.2*1e-6
        return range
    
    def setAFMLockInSensitivityRange(self, range):
        """
        This function sets the AFM lockin sensetivity range in [V]

        Parameters
        ----------
        range : float
            Sensetivity range in [V]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_M_DEMAMP'), range/305.2*1e6)

    def getAFMLockInSamplingTime(self):
        """
        This function retrieves the AFM lockin sampling time in [s]

        Parameters
        ----------
        None.
        
        Returns
        -------
        sampT : float
            Sampling time in [s]
        """
        sampT = self.getParameter(self.getConst('ID_AFM_M_SMPLTM'))*20*1e-9
        return sampT
    
    def setAFMLockInSamplingTime(self, sampT):
        """
        This function sets the AFM lockin sampling time in [s]

        Parameters
        ----------
        sampT : float
            Sampling time in [s]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AFM_M_SMPLTM'), sampT/20*1e9)

#------------------------------------------
    def getAFMAmplitudeSetpoint(self):
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
        unit_raw = self.getParameter(self.getConst('ID_GUI_UNIT_AREG'))
        unit = self.convertUnitToFactor(unit_raw)
        setpoint = rawvalue*unit
        return setpoint

    def setAFMAmplitudeSetpoint(self, setpoint):
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
        unit_raw = self.getParameter(self.getConst('ID_GUI_UNIT_AREG'))
        unit = self.convertUnitToFactor(unit_raw)
        setpoint = setpoint/unit
        
        self.setParameter(self.getConst('ID_AFM_R_AMP_DISP'), setpoint)

    def getAFMFrequencySetpoint(self):
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
        unit_raw = self.getParameter(self.getConst('ID_GUI_UNIT_PREG'))
        unit = self.convertUnitToFactor(unit_raw)
        setpoint = rawvalue*unit
        return setpoint

    def setAFMFrequencySetpoint(self, setpoint):
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
        unit_raw = self.getParameter(self.getConst('ID_GUI_UNIT_PREG'))
        unit = self.convertUnitToFactor(unit_raw)
        rawvalue = setpoint/unit
        self.setParameter(self.getConst('ID_AFM_R_FRQ_DISP'), rawvalue)
    
    def setAFMExcitationEnable(self, enable: bool):
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


