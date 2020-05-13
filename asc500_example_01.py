# -*- coding: utf-8 -*-
"""
Created on Sun May 10 13:04:04 2020

@author: schaecl
"""

import asc500_base as asc
import numpy as np
from matplotlib import pyplot as plt

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

print(asc500.getChannelConfig(chnNo))

asc500.configureDataBuffering(chnNo, bufSize)

asc500.setParameter(asc500.getConst('ID_CNT_EXP_TIME'),
                    expTime)

#%% Poll data

waitTime = 500

while True:
    # Wait until buffer is full
    ret = asc500.waitForEvent(waitTime,
                              asc500.getConst('DYB_EVT_DATA_00'),
                              0)
    print("Return value of waitForEvent {:}".format(ret))
    if ret != 0:
        break

out = \
asc500.getDataBuffer(chnNo,
                     0,
                     bufSize)

#%% Close ASC500

asc500.stopServer()

#%% Check data

print("Frame number: ", out[0])
print("Index       : ", out[1])
print("Data size   : ", out[2])
print("Meta data   : ", out[4])
counts = np.asarray(out[3][:])
print("Data        :\n", counts)

#%% Plot counts

plt.figure(0)

plt.scatter((np.arange(bufSize) + 1) * 2.5e-6 * expTime * 1e3,
            counts)
plt.xlabel('Time / ms')
plt.ylabel('Counts / 1')
