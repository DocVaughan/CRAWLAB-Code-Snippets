/***********************************************************************/
/*  													               */
/*      PROJECT NAME :  SH2Tiny_Sample1EclipseV3                       */
/*      FILE         :  SH2Tiny_Sample1EclipseV3.c                     */
/*      DESCRIPTION  :  Main Program                                   */
/*      CPU SERIES   :  SH2                                            */
/*      CPU TYPE     :  SH7047                                         */
/*  													               */
/*      This file is generated by KPIT Eclipse.                        */
/*  													               */
/***********************************************************************/                                                                        
																							
																							
#include "iodefine.h"

#ifdef CPPAPP
//Initialize global constructors
extern "C" void __main()
{
  static int initialized;
  if (! initialized)
    {
      typedef void (*pfunc) ();
      extern pfunc __ctors[];
      extern pfunc __ctors_end[];
      pfunc *p;

      initialized = 1;
      for (p = __ctors_end; p > __ctors; )
	(*--p) ();

    }
}
#endif 

void test(int x)
{
	int u;
	u = x;
	return;
}

int main(void)
{
	   // TODO: add application code here


		int ii = 0;
		int jj = 0;
//		PE.DRH.BIT.B16 = 1;
//		PE.DRH.BIT.B17 = 1;
//		PE.DRH.BIT.B18 = 0;
//		PE.DRH.BIT.B19 = 0;
		PE.DRH.BIT.B20 = 0;
		PE.DRH.BIT.B21 = 1;

		PD.DRL.WORD = 0xFFFF;
		PD.DRL.BIT.B6 = 0;
//		PD.DRL.BIT.B7 = 1;

		while (1) {

			for(ii=0; ii<100000000; ii++)
				{
				for (jj=0; jj < 100000; jj++)
					{}
				}

			PE.DRH.BIT.B21 = ~PE.DRH.BIT.B21 ;
	    	PE.DRH.BIT.B20 = ~PE.DRH.BIT.B20 ;

	    	PD.DRL.BIT.B6 = ~PD.DRL.BIT.B6;

	    }
		return 0;
}


