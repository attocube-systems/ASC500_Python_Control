from .asc500_base import ASC500Base

class ASC500ZControl(ASC500Base):

    def getPositionZ(self):
        """
        This function retrieves the position of the Z piezo.

        Parameters
        ----------
        None.

        Returns
        -------
        position : float
            Current position of the Z piezo in [m]
        """
        position = self.getParameter(self.getConst('ID_REG_GET_Z_M')) * 1e-12
        return position

    def setPositionZ(self, position):
        """
        This function sets the position of the Z piezo.

        Parameters
        ----------
        position : float
            Position of the Z piezo in [m]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_SET_Z_M'), position*1e12)

    def getZOutputSlewRate(self):
        """
        This function retrieves the current slewrate of the Z piezo.

        Parameters
        ----------
        None.
        
        Returns
        -------
        position : float
            Current slewrate of the Z piezo in [V/s]
        """
        slewrate = self.setParameter(self.getConst('ID_DAC_FB_STEP'))*466*1e-6
        return slewrate

    def setZOutputSlewRate(self, slewrate):
        """
        This function sets the slewrate of the Z piezo.

        Parameters
        ----------
        slewrate : float
            Slewrate of the Z piezo in [V/s]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_DAC_FB_STEP'), slewrate/466*1e6)