/***********************************************************************/
/*  													               */
/*      PROJECT NAME :  SH2Tiny_Sample2ECLIPSE                         */
/*      FILE         :  boot.h					                       */
/*      DESCRIPTION  :  LED blinking by interrupt timer CMT1           */
/*      CPU SERIES   :  SH2                                            */
/*      CPU TYPE     :  SH7047                                         */
/*  	Board		 :  HiBot SH2TinyController www.hibot.co.jp        */
/*  													               */
/*  													               */
/***********************************************************************/



#ifndef BOOT_H_
#define BOOT_H_

#define CRYSTAL_FREQ 11.0592
static double samplingTime=1.0e-3;
static double systemClock = CRYSTAL_FREQ * 4.0e6;    //SH2Tiny Controller Spec
static double peripheralClock = CRYSTAL_FREQ * 2.0e6; //SH2Tiny Controller Spec


#endif /* BOOT_H_ */
