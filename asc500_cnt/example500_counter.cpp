
#include <cmath>
#include <cstdio>
#include <cassert>
#include <string>

#include "metadata.h"
#include "daisybase.h"
#include "daisydata.h"
#include "asc500.h"
#include <windows.h>


/* Print error code if not "Ok" */
static void checkRc(const char *call, const DYB_Rc rc)
{
    if(rc != DYB_Ok)
        fprintf(stdout, "%s failed : %s\n", call, DYB_printRc(rc));
}


/* Set parameter with error reporting */
static void setParameter(const int32_t id, const int32_t index, const int32_t value)
{
    DYB_Rc rc = DYB_setParameterAsync(id, index, value);
    if(rc != DYB_Ok)
        fprintf(stdout,
                "DYB_setParameterAsync failed for id %x,%x : %s\n",
                id, index, DYB_printRc(rc));
}


/* Wait for the first full buffer and write it to a file */
static DYB_Rc pollDataFull(const int32_t channel_no, const int32_t framesize)
{
    DYB_Rc rc = DYB_Ok;
    int32_t *frame = new int32_t[framesize];
    int32_t event = 0,
            index = 0,
            dataSize = framesize;
    DYB_Meta meta;

    /* Wait for full buffer and show progress */
    while(event == 0 /* means timeout */ && rc == DYB_Ok)
        event = DYB_waitForEvent(500, DYB_EVT_DATA_00, 0 /* not relevant */);

    /* Read and print data frame */
    assert(rc == DYB_Ok);

    fprintf(stdout, "Reading frame; buffer size = %d, frame size = %d\n",
            dataSize, DYB_getFrameSize(channel_no));
    rc = DYB_getDataBuffer(channel_no, 1, NULL /* ignore */, &index, &dataSize, frame, &meta);
    checkRc("DYB_getDataBuffer", rc);
    rc = DYB_writeBuffer("data_output//demo_fwd", "ADC2", 0, 1, index, dataSize, frame, &meta);
    checkRc("DYB_writeBuffer", rc);
    rc = DYB_writeBuffer("data_output//demo_bwd", "ADC2", 0, 0, index, dataSize, frame, &meta);
    checkRc("DYB_writeBuffer", rc);

    delete[] frame;
    return rc;
}


/* Wait for the first full buffer and write it to a file */
static DYB_Rc pollDataNow(const int32_t channel_no, const int32_t framesize)
{
    DYB_Rc rc = DYB_Ok;
    int32_t *frame = new int32_t[framesize];
    int32_t event = 0,
            index = 0,
            dataSize = framesize;
    DYB_Meta meta;

    /* Wait for full buffer and show progress */
    while(event == 0 /* means timeout */ && rc == DYB_Ok)
        event = DYB_waitForEvent(500, DYB_EVT_DATA_00, 0 /* not relevant */);

    /* Read and print data frame */
    assert(rc == DYB_Ok);

    fprintf(stdout, "Reading frame; buffer size = %d, frame size = %d\n",
            dataSize, DYB_getFrameSize(channel_no));
    rc = DYB_getDataBuffer(channel_no, 1, NULL /* ignore */, &index, &dataSize, frame, &meta);
    checkRc("DYB_getDataBuffer", rc);
    rc = DYB_writeBuffer("data_output//demo_fwd", "ADC2", 0, 1, index, dataSize, frame, &meta);
    checkRc("DYB_writeBuffer", rc);
    rc = DYB_writeBuffer("data_output//demo_bwd", "ADC2", 0, 0, index, dataSize, frame, &meta);
    checkRc("DYB_writeBuffer", rc);

    delete[] frame;
    return rc;
}


/* Cyclically read incomplete frame and write it to a file */
static DYB_Rc pollDataPartial(const int32_t channel_no, const int32_t framesize)
{
    DYB_Rc rc = DYB_Ok;
    int loop = 0;

    while(rc == DYB_Ok && loop < 10)
    {
        int32_t *frame = new int32_t[framesize];
        DYB_Meta meta;
        int32_t index = 0,
                frameNo = 0,
                dataSize = framesize;
        char fn[128];

        Sleep(200);
        /* Read as much data as available */
        rc = DYB_getDataBuffer(channel_no, 0, &frameNo, &index, &dataSize, frame, &meta);
        checkRc("DYB_getDataBuffer", rc);
        fprintf(stdout, "Data Read: loop %2d frame %d, index %d, size %d\n", loop, frameNo, index, dataSize);

        if(dataSize > 0)
        {
            /* Writing empty buffer ends up with error */
            sprintf(fn, "data_output//demo_fwd_%d", loop);
            rc = DYB_writeBuffer(fn, "ADC2", 0, 1, index, dataSize, frame, &meta);
            checkRc("DYB_writeBuffer", rc);
        }
        loop++;
        delete[] frame;
    }

    return rc;
}


/*
 * The application loads the afm profile, configures the scanner and one data channel.
 * It starts the scanner and runs it until an amount of data is received, then stops it.
 * Data are received and stored in a file.
 * Depending on the commandline parameter, buffers are processed partially (1) or only
 * when complete.
 */
int main(int argc, char **argv)
{

    std::string bin_path = "..\\Installer\\ASC500CL-V2.7.6",
                profile_path = bin_path + "\\afm.ngp";
    DYB_Rc ret = DYB_Ok;
    int32_t outActive = 0,
            variant = 1,
            buffer_size = 2048,
            channel_no = 0,
            columns = 100, /* Scanrange number of columns */
            lines = 150, /* Scanrange number of lines */
            pixelsize = 1000, /* Width of a column/line [10pm] */
            sampletime = 100, /* Scanner sample time [2.5us] */
            framesize = columns * lines * 2; /* Amount of data in a frame */


    if(argc > 1)
        variant = atoi(argv[1]); /* Selects data acquisition variant */

    /* Initialize & start */
    ret = DYB_init(nullptr, bin_path.c_str(), nullptr, ASC500_PORT_NUMBER);
    checkRc("DYB_Init", ret);
    ret = DYB_run();
    checkRc("DYB_Run", ret);

    /* Configure the scanner by sending a profile. */
    ret = DYB_sendProfile(profile_path.c_str());
    checkRc("DYB_sendProfile", ret);

    /* Configure data channel 0 and enable data buffering */
    ret = DYB_configureChannel(channel_no,
                               CHANCONN_PERMANENT, /* Trigger by timer */
                               CHANADC_COUNTER, /* Source is counter */
                               false, /* Don't average */
                               0.); /* Time per sample @todo is this the same as exposition? */
    checkRc("DYB_configureChannel", ret);
    DYB_configureDataBuffering(channel_no, buffer_size);

    /* Switch off annoying automatics that are useful only for GUI users */
    setParameter(ID_SCAN_X_EQ_Y,  0, 0);
    setParameter(ID_SCAN_GEOMODE, 0, 0);

    /* Adjust scanner parameters */
    setParameter(ID_SCAN_PIXEL, 0, pixelsize);
    setParameter(ID_SCAN_COLUMNS, 0, columns);
    setParameter(ID_SCAN_LINES, 0, lines);
    setParameter(ID_SCAN_OFFSET_X, 0, 150 * pixelsize);
    setParameter(ID_SCAN_OFFSET_Y, 0, 150 * pixelsize);
    setParameter(ID_SCAN_MSPPX, 0, sampletime);
    setParameter(ID_CNT_EXP_TIME, 0, sampletime);

    /* Enable Outputs, wait for success (use polling for demonstration). */
    setParameter(ID_OUTPUT_ACTIVATE, 0, 1);

    while(!outActive && ret == DYB_Ok)
    {
        ret = DYB_getParameterSync(ID_OUTPUT_STATUS, 0, &outActive);
        checkRc("DYB_getParameterSync", ret);
        printf("Output Status: %d\n", outActive);
        Sleep(50);
    }

    /* Acquire data using the selected method */
    switch(variant)
    {
    case 0:
        ret = pollDataFull(channel_no, framesize);
        break;
    case 1:
        ret = pollDataPartial(channel_no, framesize);
        break;
    default:
        ret = pollDataNow(channel_no, buffer_size);
    }

    /* Stop it and exit. This time use wait for event instead of polling */
    setParameter(ID_OUTPUT_ACTIVATE, 0, 0);
    DYB_waitForEvent(2000, DYB_EVT_CUSTOM, ID_OUTPUT_STATUS);
    DYB_getParameterSync(ID_OUTPUT_STATUS, 0, &outActive);
    if(outActive)
        fprintf(stdout, "Outputs are not deactivated!\n");

    DYB_stop();
    return ret;
}
