# -*- coding: utf-8 -*-
"""
Created on Mon Dez 09 10:04:04 2024

@author: gundch

A very basic example to position the scanners.
"""

from lib import ASC500
import time

#%% Initialise
#-----------------------------------------------------------------------
binPath = "Installer\\ASC500CL-V2.7.13\\"
dllPath = "64bit_lib\\ASC500CL-LIB-WIN64-V2.7.13\\daisybase\\lib\\"
asc500 = ASC500(binPath, dllPath)
# Start the server (always mandatory)
asc500.base.startServer()

# Send profile to the asc500 (not mandatory but helps with initially configuring some stuff)
asc500.base.sendProfile(binPath + 'afm.ngp')

#%% Configure the ASC500
#-----------------------------------------------------------------------
# Activates the outputs of the ASC500. This is mandatory if you want to use the analog outputs of the ASC500 (DAC1-6 and SCAN)
asc500.base.setOutputsWaiting(1)
# As this might take a little, we wait until the outputs are on:
while not asc500.base.getOutputStatus():
    print('Waiting for outputs to switch on')
    print(asc500.base.getOutputStatus())
    time.sleep(1)

# Set the scanner moving speed. Not mandatory.
asc500.scanner.setPositioningSpeed(1e-6)

# Set the scanner position (in m).
asc500.scanner.setPositionsXYRel([5e-6, 5e-6])

# Wait a short time for communication to take place
time.sleep(0.05)

# Wait while scanner is moving.
print('Scanner State: {}'.format(asc500.scanner.getScannerStateMoving()))
while asc500.scanner.getScannerStateMoving():
    time.sleep(0.5)

#Print the new position:
print(asc500.scanner.getPositionsXYZRel())

#%% Close ASC500
#-----------------------------------------------------------------------
# Switching off the outputs will lead to the scanners falling back to [0, 0]
asc500.base.setOutputsWaiting(0)
while asc500.base.getOutputStatus():
    print('Waiting for outputs to switch off')
    time.sleep(1)

# stops the server (not mandatory)
asc500.base.stopServer()

