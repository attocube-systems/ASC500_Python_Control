# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 13:40:13 2021

@author: grundch
"""
import re
import time
import numpy as np
import enum
from .asc500_base import ASC500Base


class ASC500AutoApproach(ASC500Base):
    
    def getAApEnabled(self):
        """
        This function gets the auto approach status.

        Parameters
        ----------
        None.
        
        Returns
        -------
        enabled : int
            [0, 1] Off/On
        """
        enabled = self.getParameter(self.getConst('ID_AAP_CTRL'))
        return enabled
    
    def setAApEnabled(self, enable):
        """
        This function sets the auto approach on/off.

        Parameters
        ----------
        enable : int
            [0, 1] Off/On

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_CTRL'), enable)
    
    def getAApSpeed(self):
        """
        This function retrieves the auto approach speed.

        Parameters
        ----------
        None.

        Returns
        -------
        speed : float
            Approach speed in [V/s]
        """
        speed = self.setParameter(self.getConst('ID_AAP_SPEED'))*976.6*1e-6
        return speed
    
    def setAApSpeed(self, speed):
        """
        This function sets the auto approach speed.

        Parameters
        ----------
        speed : float
            Approach speed in [V/s]

        Returns
        -------
        """
        self.setParameter(self.getConst('ID_AAP_SPEED'), speed/976.6*1e6)

    def getAApAproachMode(self):
        """
        This function retrieves the auto approach mode.

        Parameters
        ----------
        None.
        
        Returns
        -------
        mode : int
            [0, 1] Ramp/Loop
        """
        mode = self.setParameter(self.getConst('ID_AAP_APR_MODE'))
        return mode

    def setAApAproachMode(self, mode):
        """
        This function sets the auto approach mode.

        Parameters
        ----------
        mode : int
            [0, 1] Ramp/Loop

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_APR_MODE'), mode)

    def getAApModeAfter(self):
        """
        This function retrieves the mode after the auto approach.

        Parameters
        ----------
        None.

        Returns
        -------
        mode : int
            [0, 1, 2] On/Retract/Off
        """
        mode = self.setParameter(self.getConst('ID_AAP_MODE'))
        return mode

    def setAApModeAfter(self, mode):
        """
        This function sets the mode after the auto approach.

        Parameters
        ----------
        mode : int
            [0, 1, 2] On/Retract/Off

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_MODE'), mode)

    def getAApThreshold(self):
        """
        This function retrieves the stop threshold for the auto approach.

        Parameters
        ----------
        None.

        Returns
        -------
        threshold : float
            Threshold value in [V]
        """
        unit_raw = self.getParameter(self.getConst('ID_GUI_UNIT_ZREG'))
        scale = self.getParameter(self.getConst('ID_GUI_SCAL_ZREG'))
        offset = self.getParameter(self.getConst('ID_GUI_OFFS_ZREG'))
        raw_val = self.getParameter(self.getConst('ID_AAP_THRESHOLD'))
        unit = self.convertUnitToFactor(unit_raw)



        threshold = (raw_val + offset) / scale * unit
        
        return threshold

    def setAApThreshold(self, threshold):
        """
        This function sets the stop threshold for the auto approach.

        Parameters
        ----------
        threshold : float
            Threshold value in [V]

        Returns
        -------
        None.
        """
        unit_raw = self.getParameter(self.getConst('ID_GUI_UNIT_ZREG'))
        scale = self.getParameter(self.getConst('ID_GUI_SCAL_ZREG'))
        offset = self.getParameter(self.getConst('ID_GUI_OFFS_ZREG'))
        unit = self.convertUnitToFactor(unit_raw)
        raw_val = (threshold * scale) * unit #) - offset
        
        self.setParameter(self.getConst('ID_AAP_THRESHOLD'), raw_val)

    def getAApStopCondition(self):
        """
        This function retrieves the stop condition for the auto approach.

        Parameters
        ----------
        None.

        Returns
        -------
        condition : int
            [0, 1] >threshold/<threshold
        """
        condition = self.setParameter(self.getConst('ID_AAP_THRCOND'))
        return condition
    
    def setAApStopCondition(self, condition):
        """
        This function sets the stop condition for the auto approach.

        Parameters
        ----------
        condition : int
            [0, 1] >threshold/<threshold

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_THRCOND'), condition)

    def getAApDelay(self):
        """
        This function retrieves the delay of the coarse trigger after a step.

        Parameters
        ----------
        None.

        Returns
        -------
        delay : float
            Delay in [s]
        """
        delay = self.getParameter(self.getConst('ID_AAP_DELAY')) 
        return delay

    def setAApDelay(self, delay):
        """
        This function sets the delay of the coarse trigger after a step.

        Parameters
        ----------
        delay : float
            Delay in [s]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_DELAY'), delay*1e6)
    
    def getAApCoarseAxis(self):
        """
        This function retrieves the axis of the coarse device.

        Parameters
        ----------
        None.

        Returns
        -------
        axis : int
            [0..2] or [0..7] depending on HW
        """
        axis = self.getParameter(self.getConst('ID_AAP_AXIS'))
        return axis
    
    def setAApCoarseAxis(self, axis):
        """
        This function sets the axis of the coarse device.

        Parameters
        ----------
        axis : int
            [0..2] or [0..7] depending on HW

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_AXIS'), axis)
    
    def getAApStepsPerApproach(self):
        """
        This function retrieves the number of steps for the coarse device per approach.

        Parameters
        ----------
        None.

        Returns
        -------
        steps : int
            Number of steps
        """
        steps = self.getParameter(self.getConst('ID_AAP_STEPSAPR'))
        return steps

    def setAApStepsPerApproach(self, steps):
        """
        This function sets the number of steps for the coarse device per approach.

        Parameters
        ----------
        steps : int
            Number of steps

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_STEPSAPR'), steps)

    def getAApCoarseDirection(self):
        """
        This function retrieves the step direction of the coarse device.

        Parameters
        ----------
        None.

        Returns
        -------
        direction : int
            [0, 1] forward/backward
        """
        direction = self.getParameter(self.getConst('ID_AAP_CRS_DIR'))
        return direction

    def setAApCoarseDirection(self, direction):
        """
        This function sets the step direction of the coarse device.

        Parameters
        ----------
        direction : int
            [0, 1] forward/backward

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_CRS_DIR'), direction)

    def setAApCoarseUpEnabled(self, enabled):
        """
        This function sets the upwards movement with the coarse device.

        Parameters
        ----------
        enabled : int
            [0, 1] Coarse stage upwards movement [disabled, enabled]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_CRSADJ_UP'), enabled)
    
    def setAApCoarseDownEnabled(self, enabled):
        """
        This function sets the downwards movement with the coarse device.

        Parameters
        ----------
        enabled : int
            [0, 1] Coarse stage downwards movement [disabled, enabled]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_CRSADJ_DN'), enabled)

    def getAApCoarseStatus(self):
        """
        This function retrieves the current status of the coarse adjust feature.

        Parameters
        ----------
        None.

        Returns
        -------
        status : int
            [0, 1, -1] Status [Off, OK, Error]
        """
        status = self.getParameter(self.getConst('ID_AAP_CRSADJ_ST'))
        return status

    def getAApCoarseTrigPolarity(self):
        """
        This function retrieves the polarity of the coarse device trigger.

        Parameters
        ----------
        None.

        Returns
        -------
        polarity : int
            [0, 1] high/low
        """
        polarity = self.getParameter(self.getConst('ID_AAP_CRS_POL'))
        return polarity
    
    def setAApCoarseTrigPolarity(self, polarity):
        """
        This function sets the polarity of the coarse device trigger.

        Parameters
        ----------
        polarity : int
            [0, 1] high/low

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_CRS_POL'), polarity)

    def getAApCoarseTrigHoldTime(self):
        """
        This function retrieves the hold time of the coarse device trigger.

        Parameters
        ----------
        None.

        Returns
        -------
        time : float
            Hold time in [s]
        """
        time = self.getParameter(self.getConst('ID_AAP_CRS_HLDTIME'))
        return time
    
    def setAApCoarseTrigHoldTime(self, time):
        """
        This function sets the hold time of the coarse device trigger.

        Parameters
        ----------
        time : float
            Hold time in [s]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_CRS_HLDTIME'), time*1e6)

    def getAApSwitchToGround(self):
        """
        This function retrieves if the amplifiers is switched to GND between the approaches.

        Parameters
        ----------
        None.

        Returns
        -------
        enabled : int
            [0, 1] Switch to GND is [disabled/enabled]
        """
        enabled = self.getParameter(self.getConst('ID_AAP_GNDWHILEAP'))
        return enabled

    def setAApSwitchToGround(self, enable):
        """
        This function sets if the amplifiers is switched to GND between the approaches.

        Parameters
        ----------
        enable : int
            [0, 1] Switch to GND is [disabled/enabled]

        Returns
        -------
        None.
        """
        self.setParameter(self.getConst('ID_AAP_GNDWHILEAP'), enable)

    def getAApCoarseDevice(self):
        """
        This function retrieves which auto approach coarse divce is currently set.

        Parameters
        ----------
        None.

        Returns
        -------
        device : int
            [1..5] ANC, TTL via DAC2, LVTTL via DAC2, ANC350 via NSL, AttoSTM
        """
        device = self.getParameter(self.getConst('ID_AAP_CRS_DEV'))
        return device

    def setAApCoarseDevice(self, device):
        """
        This function sets the auto approach coarse device.

        Parameters
        ----------
        device : int
            [1..5] ANC, TTL via DAC2, LVTTL via DAC2, ANC350 via NSL, AttoSTM

        Returns
        -------
        None.
        """
        if device == 1:
            self.setParameter(self.getConst('ID_AAP_CRS_DEV'), self.getConst('CRS_DEVICE_ANC'))
        elif device == 2:
            self.setParameter(self.getConst('ID_AAP_CRS_DEV'), self.getConst('CRS_DEVICE_TTL'))
        elif device == 3:
            self.setParameter(self.getConst('ID_AAP_CRS_DEV'), self.getConst('CRS_DEVICE_LVTTL'))
        elif device == 4:
            self.setParameter(self.getConst('ID_AAP_CRS_DEV'), self.getConst('CRS_DEVICE_ANC_NSL'))
        elif device == 5:
            self.setParameter(self.getConst('ID_AAP_CRS_DEV'), self.getConst('CRS_DEVICE_ATTOSTM'))
        else:
            print('Error: Devicecode')