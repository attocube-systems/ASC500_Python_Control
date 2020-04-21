/*******************************************************************************
 *
 *  Project:        Daisy Client Library
 *
 *  Filename:       example500.c
 *
 *  Purpose:        Example for using daisybase lib with ASC500
 *
 *  Author:         NHands GmbH & Co KG
 *
 *******************************************************************************/
/* $Id: example500.c,v 1.10 2018/03/22 16:08:42 trurl Exp $ */

#define _USE_MATH_DEFINES // required by MSVC for M_PI
#include <math.h>
#include <stdio.h>
#include "daisybase.h"
#include "daisydata.h"
#include "asc500.h"

/*
 *  Adapt the path and filenames to your installation
 */
#ifdef unix
#define BIN_PATH     "../.."              /* Daisy installation directory */
#define PROFILE_FILE "../../afm.ngp"      /* Profile for base settings    */
#include <unistd.h>                       /* unistd.h for usleep          */
#include <stdlib.h>                       /* for atoi                     */
#define SLEEP(x) usleep(x*1000)

#else

#define BIN_PATH     "..\\.."             /* Daisy installation directory */
#define PROFILE_FILE "..\\..\\afm.ngp"    /* Profile for base settings    */
#include <windows.h>                      /* windows.h for Sleep          */
#define SLEEP(x) Sleep(x)
#endif


/*
 *  Some arbitrary parameter values used here
 */
#define CHANNELNO                0        /* Channel for data transfer     */
#define COLUMNS                100        /* Scanrange number of columns   */
#define LINES                  150        /* Scanrange number of lines     */
#define PIXELSIZE             1000        /* Width of a column/line [10pm] */
#define SAMPLETIME             100        /* Scanner sample time [2.5us]   */
#define FRAMESIZE  (COLUMNS*LINES*2)      /* Amount of data in a frame     */


/* Print error code if not "Ok" */
static void checkRc(const char *call, DYB_Rc rc)
{
    if(rc != DYB_Ok)
    {
        printf("%s failed : %s\n", call, DYB_printRc(rc));
    }
}


/* Set parameter with error reporting */
static void setParameter(Int32 id, Int32 index, Int32 value)
{
    DYB_Rc rc = DYB_setParameterAsync(id, index, value);
    if(rc != DYB_Ok)
    {
        printf("DYB_setParameterAsync failed for id %x,%x : %s\n", id, index, DYB_printRc(rc));
    }
}


/* Wait for the first full buffer and write it to a file */
static DYB_Rc pollDataFull()
{
    DYB_Rc   rc = DYB_Ok;
    Int32    frame[FRAMESIZE];
    Int32    event = 0, index = 0, dataSize = FRAMESIZE;
    DYB_Meta meta;

    /* Wait for full buffer and show progress */
    while(event == 0 /* means timeout */ && rc == DYB_Ok)
    {
        double x, y;
        event = DYB_waitForEvent(500, DYB_EVT_DATA_00, 0 /* not relevant */);
//    rc = ASC500_getXYPos( &x, &y );
//    checkRc( "ASC500_getXYPos", rc );
        printf("Scanner at (%.9g , %.9g) um\n", x, y);
    }

    /* Read and print data frame */
    if(rc == DYB_Ok)
    {
        printf("Reading frame; buffer size = %d, frame size = %d\n",
               dataSize, DYB_getFrameSize(CHANNELNO));
        rc = DYB_getDataBuffer(CHANNELNO, 1, NULL /* ignore */, &index, &dataSize, frame, &meta);
        checkRc("DYB_getDataBuffer", rc);
        rc = DYB_writeBuffer("demo_fwd", "ADC2", 0, 1, index, dataSize, frame, &meta);
        checkRc("DYB_writeBuffer", rc);
        rc = DYB_writeBuffer("demo_bwd", "ADC2", 0, 0, index, dataSize, frame, &meta);
        checkRc("DYB_writeBuffer", rc);
    }

    return rc;
}


/* Cyclically read incomplete frame and write it to a file */
static DYB_Rc pollDataPartial()
{
    DYB_Rc   rc = DYB_Ok;
    int      loop = 0;

    while(rc == DYB_Ok && loop < 100)
    {
        Int32    frame[FRAMESIZE];
        DYB_Meta meta;
        Int32 index = 0, frameNo = 0, dataSize = FRAMESIZE;
        char  fn[128];

        SLEEP(200);
        /* Read as much data as available */
        rc = DYB_getDataBuffer(CHANNELNO, 0, &frameNo, &index, &dataSize, frame, &meta);
        checkRc("DYB_getDataBuffer", rc);
        printf("Data Read: loop %2d frame %d, index %d, size %d\n", loop, frameNo, index, dataSize);

        if(dataSize > 0)
        {
            /* Writing empty buffer ends up with error */
            sprintf(fn, "demo_fwd_%d", loop);
            rc = DYB_writeBuffer(fn, "ADC2", 0, 1, index, dataSize, frame, &meta);
            checkRc("DYB_writeBuffer", rc);
        }
        loop++;
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
    DYB_Rc   rc = DYB_Ok;
    Int32    outActive = 0, event = 0, variant = 0;

    if(argc > 1)
    {
        variant = atoi(argv[1]);    /* Selects data acquisition variant */
    }

    /* Initialize & start */
    rc = DYB_init(0, BIN_PATH, 0, ASC500_PORT_NUMBER);
    checkRc("DYB_Init", rc);
    rc = DYB_run();
    checkRc("DYB_Run", rc);

    /* Configure the scanner by sending a profile. */
    rc = DYB_sendProfile(PROFILE_FILE);
    checkRc("DYB_sendProfile", rc);

    /* Configure data channel 0 and enable data buffering */
    rc = DYB_configureChannel(CHANNELNO,             /* Channel 0           */
                              CHANCONN_SCANNER,     /* Trigger by scanner  */
                              CHANADC_ADC_MIN + 1,  /* Source is ADC 2     */
                              0,                    /* Don't average       */
                              0.);                  /* Sample time ignored */
    checkRc("DYB_configureChannel", rc);
    DYB_configureDataBuffering(CHANNELNO, 1024 /* not relevant but nonzero */);

    /* Switch off annoying automatics that are useful only for GUI users */
    setParameter(ID_SCAN_X_EQ_Y,  0, 0);
    setParameter(ID_SCAN_GEOMODE, 0, 0);

    /* Adjust scanner parameters */
    setParameter(ID_SCAN_PIXEL,    0, PIXELSIZE);
    setParameter(ID_SCAN_COLUMNS,  0, COLUMNS);
    setParameter(ID_SCAN_LINES,    0, LINES);
    setParameter(ID_SCAN_OFFSET_X, 0, 150 * PIXELSIZE);
    setParameter(ID_SCAN_OFFSET_Y, 0, 150 * PIXELSIZE);
    setParameter(ID_SCAN_MSPPX,    0, SAMPLETIME);

    /* Enable Outputs, wait for success (use polling for demonstration). */
    setParameter(ID_OUTPUT_ACTIVATE, 0, 1);
    while(!outActive && rc == DYB_Ok)
    {
        rc = DYB_getParameterSync(ID_OUTPUT_STATUS, 0, &outActive);
        checkRc("DYB_getParameterSync", rc);
        printf("Output Status: %d\n", outActive);
        SLEEP(50);
    }

    /* Start scanner */
//  rc = sendScannerCommand( SCANRUN_ON );
//  checkRc( "sendScannerCommand", rc );

    /* Acquire data using the selected method */
    switch(variant)
    {
    case 0:
        rc = pollDataFull();
        break;
    case 1:
        rc = pollDataPartial();
        break;
    default:
        ;
    }

    /* Stop it and exit. This time use wait for event instead of polling */
//    sendScannerCommand(SCANRUN_OFF);
    setParameter(ID_OUTPUT_ACTIVATE, 0, 0);
    DYB_waitForEvent(5000, DYB_EVT_CUSTOM, ID_OUTPUT_STATUS);
    DYB_getParameterSync(ID_OUTPUT_STATUS, 0, &outActive);
    if(outActive)
    {
        printf("Outputs are not deactivated!\n");
    }

    DYB_stop();
    return rc;
}
