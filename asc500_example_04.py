# -*- coding: utf-8 -*-
"""
Created on Sun May 10 13:04:04 2020

@author: schaecl
"""

from lib import ASC500

binPath = "Installer\\ASC500CL-V2.7.13\\"
dllPath = "64bit_lib\\ASC500CL-LIB-WIN64-V2.7.13\\daisybase\\lib\\"

asc500 = ASC500(binPath, dllPath)

asc500.base.startServer()

asc500.base.sendProfile(binPath + 'afm.ngp')

asc500.data.setDataEnable(1)

print("Getting Scanner State: ")
print(asc500.scanner.getScannerState())

print("Getting Scanner Position: ")
print(asc500.scanner.getPositionsXYZRel())

#%% Close ASC500

asc500.base.stopServer()
