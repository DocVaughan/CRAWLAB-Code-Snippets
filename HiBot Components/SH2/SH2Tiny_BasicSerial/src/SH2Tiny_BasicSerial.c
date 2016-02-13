/****************************************************************
KPIT Cummins Infosystems Ltd, Pune, India. - 10-Mar-2003.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

The automatic generation of the project from KPIT has a problem
in the linker. After compiling you would get OUT OF MEMORY when
downloading the firmware on the board.

Workaround:
Select from the menu: Buil->Linker->Section
select .data and press MODIFY
press ADVANCED in the new window and select from map address the option Label
press OK to all windows.

Project Description:
Simple example of Serial Module SCI3 for HiBot SH2Tiny Controller
What is received in input from the keyboard it will be displayed as ASCII value in output

Terminal or TeraTerm Serial configuration

Baudrate: 115200
Data bit: 8
Parity: no
Stop bit: 1
Flow control: no


contact: info@hibot.co.jp
		 www.hibot.co.jp
		 ver 1.0 2009.12.29
*****************************************************************/

#include "iodefine.h"
#include "boot.h"
#include <math.h>
#include "interrupt_handlers.h"
#include "sci3.h"
#include <stdio.h>
#include <stdlib.h>

//static double time = 0.0;
//static double time_old = 0.0;
unsigned char str[11];
unsigned char order[4][4];
unsigned char data='0';

void INT_CMT_CMT1(void)
{

	CMT1.CMCSR.BIT.CMF = 0;
}



int main(void)
{
    // TODO: add application code here


	//Initialization of the Timer CMT1
	//refer to the SH2 hardware manual for a detailed explanation
	//on the register settings on Section Compare Match Timer (CMT)
	unsigned int PeriodCNT =(samplingTime*(peripheralClock/8.0+0.5))-1;
	CMT.CMSTR.BIT.STR1 = 0;	 		//Stop the count operation
	CMT1.CMCSR.BIT.CMIE = 1; 		//Enable interrupts
	CMT1.CMCSR.BIT.CKS = 0;  		//Select the peripheral clock
	CMT1.CMCNT		= 0;			//Reset the counter
	CMT1.CMCOR		= PeriodCNT;	//Set the constant register for matching
	CMT1.CMCSR.BIT.CMF &= 0;		//set to zero to set a "NOT MATCHED CONDITION"
	INTC.IPRG.WORD	|= 0x0007;		//Interrupt priority
	CMT.CMSTR.BIT.STR1 = 1;			//Start the count operation

	//initialize the SERIAL PORT SCI3
	init_sci3();

    while (1) {
				sprintf(str, "CRAWLAB data: %3d\r\n",data);
				myputs_sci3(str);

    }
    return 0;
}
