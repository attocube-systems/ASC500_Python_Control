from time import time
from .asc500_base import ASC500Base


class ASC500Path(ASC500Base):
    """
    Parameters for selection and configuration of a scanner path.
    A Path can be configured with individual points or with a evenly spaced point grid.
    
    Example usage with individual points:
        Initialise points:      
        Prepare Path control:   
        Start path control:     setPathControlON(4)

    Example usage with grid of points:

    """
    #TODO: 
    def getPathPrep(self):
        """
        This function retrieves, if the path mode preparation is set.        

        Parameters
        ----------
        None.
        
        Returns
        -------
        prep : int
            [0, 1] path mode preperation is [off/on]
        """
        prep = self.getParameter(self.getConst('ID_SPEC_PATHPREP'))
        return prep

    def setPathPrep(self, prep):
        """
        This function sets the path mode preparation [off/on].
        Used before starting with value=1.

        Parameters
        ----------
        prep : int
            [0, 1] set path mode preperation [off/on]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_PATHPREP'), prep)
    
    def getPathControlON(self):
        """
        This function retrieves, if the path mode is off/in grid mode/in point mode(then the number of points is retrieved).

        Parameters
        ----------
        None.
        
        Returns
        -------
        enable : int
            [-1, 0, >1] starts/stops the path mode:
                 0: Stops
                -1: Grid
                >1: Number of Points
        """
        enabled = self.getParameter(self.getConst('ID_SPEC_PATHCTRL'))
        return enabled

    def setPathControlON(self, enable):
        """
        This function starts/stops the path mode.

        Parameters
        ----------
        enable : int
            [-1, 0, >1] starts/stops the path mode:
                 0: Stops
                -1: Grid
                >1: Number of Points
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_PATHCTRL'), enable)
    
    def getPathControlState(self):
        """
        This function retrieves the current state [0=not running/1=running] of the path mode.

        Parameters
        ----------
        enabled : int
            [0, 1] path mode is [not running/running]:
        
        Returns
        -------
        None.
        """
        enabled = self.getParameter(self.getConst('ID_PATH_RUNNING'))
        return enabled
    
    def getPathProceed(self):
        """
        This function retrieves the state of the handshake acknowledgement.

        Parameters
        ----------
        None.
        
        Returns
        -------
        proceed : int
            [0, 1] handshake acknowledgement is set [on/off]:
        """
        proceed = self.getParameter(self.getConst('ID_SPEC_PATHPROCEED'))
        return proceed

    def setPathProceed(self, proceed):
        """
        This function sets the state of the handshake acknowledgement.

        Parameters
        ----------
        proceed : int
            [0, 1] handshake acknowledgement is set [on/off]:
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_SPEC_PATHPROCEED'), proceed)
    
    def getPathHandshakeRequest(self):
        """
        This function retrieves, if a handshake is requested.

        Parameters
        ----------
        None.
        
        Returns
        -------
        request : int
            [0, 1] handshake request is [on/off]:
        """
        request = self.getParameter(self.getConst(''))
        return request
    
    def getGridPointsX(self):
        """
        This function retrieves the number of grid points in X

        Parameters
        ----------
        None.
        
        Returns
        -------
        pointsX : int
            Number of grid points in X
        """
        pointsX = self.getParameter(self.getConst('ID_PATH_GRIDP_X'))
        return pointsX

    def setGridPointsX(self, pointsX):
        """
        This function sets the number of grid points in X

        Parameters
        ----------
        pointsX : int
            Number of grid points in X
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_PATH_GRIDP_X'), pointsX)
    
    def getGridPointsY(self):
        """
        This function retrieves the number of grid points in Y

        Parameters
        ----------
        None.
        
        Returns
        -------
        pointsY : int
            Number of grid points in Y
        """
        pointsY = self.getParameter(self.getConst('ID_PATH_GRIDP_Y'))
        return pointsY

    def setGridPointsY(self, pointsY):
        """
        This function sets the number of grid points in Y

        Parameters
        ----------
        pointsY : int
            Number of grid points in Y
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_PATH_GRIDP_Y'), pointsY)
    
    def getGridPointsXY(self):
        """
        This function retrieves the number of grid points in X and Y

        Parameters
        ----------
        None.
        
        Returns
        -------
        pointsXY : list
            [pointsX, pointsY] Number of grid points in X and Y
        """
        pointsX = self.getParameter(self.getConst('ID_PATH_GRIDP_X'))
        pointsY = self.getParameter(self.getConst('ID_PATH_GRIDP_Y'))
        pointsXY = [pointsX, pointsY]
        return pointsXY

    def setGridPointsXY(self, pointsXY):
        """
        This function sets the number of grid points in X and Y

        Parameters
        ----------
        pointsXY : list
            [pointsX, pointsY] Number of grid points in X and Y
        
        Returns
        -------
        None.
        """
        [pointsX, pointsY] = pointsXY
        self.setParameter(self.getConst('ID_PATH_GRIDP_X'), pointsX)
        self.setParameter(self.getConst('ID_PATH_GRIDP_Y'), pointsY)
    
    def getExtHandshake(self):
        """
        This function retrieves, if an external handshake is [enabled/disabled]

        Parameters
        ----------
        None.
        
        Returns
        -------
        enabled : int
            [0, 1] external handshake is [enabled/disabled]
        """
        enabled = self.getParameter(self.getConst('ID_EXTTRG_HS'))
        return enabled
    
    def setExtHandshake(self, enabled):
        """
        This function sets an external handshake [enabled/disabled]

        Parameters
        ----------
        enabled : int
            [0, 1] external handshake is [enabled/disabled]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_EXTTRG_HS'), enabled)

    def getExtHandshakeCount(self):
        """
        This function retrieves the number of an external handshake triggers (default = 1)

        Parameters
        ----------
        None.
        
        Returns
        -------
        counts : int
            Number of external handshake triggers
        """
        counts = self.getParameter(self.getConst('ID_EXTTRG_COUNT'))
        return counts
    
    def setExtHandshakeCount(self, counts):
        """
        This function sets the number of an external handshake triggers (default = 1)

        Parameters
        ----------
        counts : int
            Number of external handshake triggers
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_EXTTRG_COUNT'), counts)
    
    def getExtHandshakeTimeout(self):
        """
        This function retrieves the timeout set for the external handshake trigger in [s]

        Parameters
        ----------
        None.
        
        Returns
        -------
        timeout : float
            timeout of the external handshake trigger in [s]
        """
        timeout = self.getParameter(self.getConst('ID_EXTTRG_TIMEOUT'))*1e-3
        return timeout

    def getExtHandshakeTimeout(self, timeout):
        """
        This function sets the timeout of the external handshake trigger in [s]

        Parameters
        ----------
        timeout : float
            timeout of the external handshake trigger in [s]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_EXTTRG_TIMEOUT'), timeout*1e3)
    
    def getExtHandshakeStatus(self):
        """
        This function retrieves, if the external handshake trigger is waiting

        Parameters
        ----------
        waiting : int
            [0, 1] External handshake trigger is [not waiting/waiting]
        
        Returns
        -------
        None.
        """
        waiting = self.getParameter(self.getConst('ID_EXTTRG_STATUS'))
        return waiting
    
    def getExtHandshakeDuration(self):
        """
        This function retrieves the external handshake pulse duration in [s]

        Parameters
        ----------
        None.
        
        Returns
        -------
        duration : float
            External handshake pulse duration in [s]
        """
        duration = self.getParameter(self.getConst('ID_EXTTRG_TIME'))*1e-6
        return duration
    
    def setExtHandshakeDuration(self, duration):
        """
        This function sets the external handshake pulse duration in [s]

        Parameters
        ----------
        duration : float
            External handshake pulse duration in [s]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_EXTTRG_TIME'), duration*1e6)
    
    def getExtHandshakeEdge(self):
        """
        This function retrieves the external handshake edge type (0=rising, 1=falling)

        Parameters
        ----------
        None.
        
        Returns
        -------
        edgetype : int
            [0, 1] External handshake edge type [rising, falling]
        """
        edgetype = self.getParameter(self.getConst('ID_EXTTRG_EDGE'))
        return edgetype

    def setExtHandshakeEdge(self, edgetype):
        """
        This function sets the external handshake edge type (0=rising, 1=falling)

        Parameters
        ----------
        edgetype : int
            [0, 1] External handshake edge type [rising, falling]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_EXTTRG_EDGE'), edgetype)
    
    def getHomeZ(self):
        """
        This function retrieves the home postition for the Z value in [m]

        Parameters
        ----------
        None.
        
        Returns
        -------
        homeZ : float
            Home postition for the Z value in [m]
        """
        homeZ = self.getParameter(self.getConst('ID_REG_Z_HOME_M'))*1e-12
        return homeZ
    
    def setHomeZ(self, homeZ):
        """
        This function sets the home postition for the Z value in [m]

        Parameters
        ----------
        homeZ : float
            Home postition for the Z value in [m]
        
        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_REG_Z_HOME_M'), homeZ*1e12)
    
    def getPathPointX(self, addr):
        """
        This function retrieves the path point X value set at a given address in [m] (relative to the scan centre)

        Parameters
        ----------
        addr : int
            address to retrieve the value of
        
        Returns
        -------
        pointX : float
            X value for point in [m]
        """
        pointX = self.getParameter(self.getConst('ID_PATH_GUI_X'), addr)*1e-11
        return pointX
    
    def setPathPointX(self, addr, pointX):
        """
        This function sets the path point X value for a given address in [m] (relative to the scan centre)

        Parameters
        ----------
        addr : int
            address to set the value of
        pointX : float
            X value for point in [m]
        
        Returns
        -------
        """
        self.setParameter(self.getConst('ID_PATH_GUI_X'), pointX*1e11, addr)

    def getPathPointY(self, addr):
        """
        This function retrieves the path point Y value set at a given address in [m] (relative to the scan centre)

        Parameters
        ----------
        addr : int
            address to retrieve the value of
        
        Returns
        -------
        pointY : float
            Y value for point in [m]
        """
        pointY = self.getParameter(self.getConst('ID_PATH_GUI_Y'), addr)*1e-11
        return pointY
    
    def setPathPointY(self, addr, pointY):
        """
        This function sets the path point Y value for a given address in [m] (relative to the scan centre)

        Parameters
        ----------
        addr : int
            address to set the value of
        pointX : float
            Y value for point in [m]
        
        Returns
        -------
        """
        self.setParameter(self.getConst('ID_PATH_GUI_Y'), pointY*1e11, addr)
    
    def getPathPointXY(self, addr):
        """
        This function retrieves the path point X and Y values set at a given address in [m] (relative to the scan centre)

        Parameters
        ----------
        addr : int
            address to retrieve the values of
        
        Returns
        -------
        pointXY : list
            [pointX, pointY] values for point at addr in [m]
        """
        pointX = self.getParameter(self.getConst('ID_PATH_GUI_X'), addr)*1e-11
        pointY = self.getParameter(self.getConst('ID_PATH_GUI_Y'), addr)*1e-11
        pointXY = [pointX, pointY]
        return pointXY
    
    def setPathPointXY(self, addr, pointXY):
        """
        This function sets the path point X and Y values for a given address in [m] (relative to the scan centre).
        In grid mode, only the top left and bottom right points are stored.

        Parameters
        ----------
        addr : int
            address to set the values of
        pointXY : list
            [pointX, pointY] values for point at addr in [m]
        
        Returns
        -------
        """
        [pointX, pointY] = pointXY
        self.setParameter(self.getConst('ID_PATH_GUI_X'), pointX*1e11, addr)
        self.setParameter(self.getConst('ID_PATH_GUI_Y'), pointY*1e11, addr)
    
    def getNumOfPathActions(self):
        """
        This function retrieves the number of actions which are currently performed at each point

        Parameters
        ----------
        None.

        Returns
        -------
        number : int
            [pointX, pointY] values for point at addr in [m]
        """
        number = self.getParameter(self.getConst('ID_PATH_ACTION'), 0)
        return number

    def getPathAction(self, index):
        """
        This function retrieves the action which is performed at "index" place.
        Defined actions are:
        0=manual handshake, 1..3=spectroscopy 1..3, 4=ext. handshake, 5=move Z home, 6=auto approach

        Parameters
        ----------
        index : int
            [>0] index to get the action from
        
        Returns
        -------
        action : int
            action which is performed at "index" place
        """
        action = self.getParameter(self.getConst('ID_PATH_ACTION'), index)
        return action
    
    def setPathAction(self, index, action):
        """
        This function sets the action which is performed at "index" place.
        Defined actions are:
        0=manual handshake, 1..3=spectroscopy 1..3, 4=ext. handshake, 5=move Z home, 6=auto approach

        Parameters
        ----------
        index : int
            [>0] index to get the action from
        action : int
            action which is performed at "index" place
        
        Returns
        -------
        """
        self.setParameter(self.getConst('ID_PATH_ACTION'), action, index)

    

    
