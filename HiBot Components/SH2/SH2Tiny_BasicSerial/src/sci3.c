#include "iodefine.h"
#include "sci3.h"

void	myputc_sci3(char c);	//自作一文字送信
void	myputs_sci3(char* s);	//自作文字列送信

void init_sci3(void)
{
	INTC.IPRI.WORD		|= 0x0700;	
	SCI3.SCR.BYTE = 0x70;	//0111 00xx　受信割り込み，送受信を可能に
	SCI3.SMR.BYTE = 0x00;	// 0000 0000 調歩同期8bitノンパリティSTOP1bit
	SCI3.BRR      = 5;		// Pφ=22MHz, bps=115200 → n=0,N=5
}
/************************************/

void	myputc_sci3(char c)
{
	while(!SCI3.SSR.BIT.TDRE);			//送信可能状態まで待つ．
	SCI3.TDR = c;
	SCI3.SSR.BIT.TDRE = 0;				/* TDRE クリア			*/

}

void	myputs_sci3(char* s)
{
	short i;

	for(i=0; s[i]; i++)
	{
		while(!SCI3.SSR.BIT.TDRE);			//送信可能状態まで待つ．
		SCI3.TDR = s[i];
		SCI3.SSR.BIT.TDRE = 0;				/* TDRE クリア			*/
	}

}



