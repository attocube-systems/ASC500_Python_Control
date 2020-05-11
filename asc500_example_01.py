# -*- coding: utf-8 -*-
"""
Created on Sun May 10 13:04:04 2020

@author: schaecl
"""

import asc500_base as asc

binPath = "Installer\\ASC500CL-V2.7.6\\"
dllPath = "64bit_lib\\ASC500CL-LIB-WIN64-V2.7.6\\daisybase\\lib\\"
asc500 = asc.ASC500Base(binPath, dllPath)

asc500.startServer()

asc500.setDataEnable(1)

sampTime = 1e-3
average = 0
chnNo = 0
bufSize = 256
expTime = 1 # Scanner sample time in multiples of 2.5 us

asc500.configureChannel(chnNo,
                        asc500.getConst('CHANCONN_PERMANENT'),
                        asc500.getConst('CHANADC_COUNTER'),
                        average,
                        sampTime)

asc500.configureDataBuffering(chnNo, bufSize)

asc500.setParameter(asc500.getConst('ID_CNT_EXP_TIME'),
                    expTime)

waitTime = 500

while True:
    ret = asc500.waitForEvent(waitTime,
                              asc500.getConst('DYB_EVT_DATA_00'),
                              0)
    if ret != 0:
        break

out = \
asc500.getDataBuffer(chnNo,
                     0,
                     bufSize)

print("Frame number: ", out[0])
print("Index       : ", out[1])
print("Data size   : ", out[3])
print("Meta data   : ", out[4])
print("Data        :\n", out[2])

asc500.stop()
