from lib.asc500_base import ASC500Base

class ASC500DataScaling(ASC500Base):
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
        This function retrieves the unit set for the given data source, see @ref DUnits "Data Units".

        Parameters
        ----------
        channel : int
            [0..5] channel to retrieve the unit for
        
        Returns
        -------
        unit : int
            Currently set unit, see @ref DUnits "Data Units"
        """
        unit = self.getParameter(self.getConst('ID_ADC_ECAL_UNIT'), index=channel)
        return unit
    
    def setChannelGain(self, channel, unit):
        """
        This function sets the unit set for the given data source, see @ref DUnits "Data Units".

        Parameters
        ----------
        channel : int
            [0..5] channel to retrieve the unit for
        unit : int
            Data unit, see @ref DUnits "Data Units"
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_ADC_ECAL_UNIT'), unit, channel)