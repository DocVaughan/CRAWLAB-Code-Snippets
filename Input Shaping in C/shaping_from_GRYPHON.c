

/*
void doInputShaping(int axis[3],float correspondingJointValues[3],unsigned char reset)
{
	#define inputShapingYawAxisDT (40)
	#define inputShapingOtherAxisDT (33)
	#define inputShapingBufferLength2 (inputShapingYawAxisDT*2 + 2)
	#define inputShapingBufferLength01 (inputShapingOtherAxisDT*2 + 2)
	static int axis0[inputShapingBufferLength01];
	static int axis1[inputShapingBufferLength01];
	static int axis2[inputShapingBufferLength2];
	static char bufferStartPos2=-1;
	static char bufferStartPos01=-1;
	char i;

	if (bufferStartPos2==-1) // the very first time we pass here
		reset=1;
	if (reset)
	{ // we reset the buffers:
		bufferStartPos2=0;
		bufferStartPos01=0;
		for (i=0;i<inputShapingBufferLength2;i++)
			axis2[i]=axis[2];
		for (i=0;i<inputShapingBufferLength01;i++)
		{
			axis0[i]=axis[0];
			axis1[i]=axis[1];
		}
		return;
	}
	else
	{ // we have to shift the 3 buffers and actualize the first values:
		bufferStartPos2--;
		if (bufferStartPos2<0)
			bufferStartPos2+=inputShapingBufferLength2;
		bufferStartPos01--;
		if (bufferStartPos01<0)
			bufferStartPos01+=inputShapingBufferLength01;
		axis0[bufferStartPos01]=axis[0];	
		axis1[bufferStartPos01]=axis[1];	
		axis2[bufferStartPos2]=axis[2];	
	}	


	// Now we compute input-shaped values for the 3 axis:
	// base axis (yaw angle):
	axis[2]=axis2[bufferStartPos2]/4;
	i=bufferStartPos2+inputShapingYawAxisDT;
	if (i>=inputShapingBufferLength2)
		i-=inputShapingBufferLength2;
	axis[2]+=axis2[i]/2;
	i+=inputShapingYawAxisDT;	
	if (i>=inputShapingBufferLength2)
		i-=inputShapingBufferLength2;
	axis[2]+=axis2[i]/4;

	// other two axis (left and right joints):
	axis[0]=axis0[bufferStartPos01]/4;
	axis[1]=axis1[bufferStartPos01]/4;
	i=bufferStartPos01+inputShapingOtherAxisDT;
	if (i>=inputShapingBufferLength01)
		i-=inputShapingBufferLength01;
	axis[0]+=axis0[i]/2;
	axis[1]+=axis1[i]/2;
	i+=inputShapingOtherAxisDT;	
	if (i>=inputShapingBufferLength01)
		i-=inputShapingBufferLength01;
	axis[0]+=axis0[i]/4;
	axis[1]+=axis1[i]/4;
}
*/

void doInputShaping(int axis[3], float correspondingJointValues[3], unsigned char reset)
{
	#define inputShapingBufferLength (72) // 100 not good, 86 shaking
	static int axis0[inputShapingBufferLength];
	static int axis1[inputShapingBufferLength];
	static int axis2[inputShapingBufferLength];
	static char bufferStartPos=-1;
	char inputShapingYawAxisDT;
	char inputShapingOtherAxisDT;
	float j1, j2, r;
	char i;

	if (bufferStartPos==-1) // the very first time we pass here
		reset=1;
	if (reset)
	{ // we reset the buffers:
		bufferStartPos=0;
		for (i=0;i<inputShapingBufferLength;i++)
		{
			axis0[i]=axis[0];
			axis1[i]=axis[1];
			axis2[i]=axis[2];
		}
		return;
	}
	else
	{ // we have to shift the 3 buffers and actualize the first values:
		bufferStartPos--;
		if (bufferStartPos<0)
			bufferStartPos+=inputShapingBufferLength;
		axis0[bufferStartPos]=axis[0];	
		axis1[bufferStartPos]=axis[1];	
		axis2[bufferStartPos]=axis[2];	
	}	

	// We compute the inputShapingYawAxisDT and the inputShapingOtherAxisDT values:
	j1=piValD2-correspondingJointValues[0];
	j2=piVal-correspondingJointValues[1];
	r=WRIST_POS_PARAM1*sinf(j1)+WRIST_POS_PARAM4*cosf(j2);
	if (gryphonVersion==6)
	{ // this is with LAMDAR4 attached!
		j1=(r-2.0f)/1.3f; // interpolated between 2.0 and 3.3 meters
		inputShapingYawAxisDT=(char)(30.0f*(1.0f-j1)+32.0f*j1); // 30 and 32 are computer from 0.5/f at 2.0 and 3.3 meters
		inputShapingOtherAxisDT=(char)(23.0f*(1.0f-j1)+21.0f*j1); // 23 and 60 are computer from 0.5/f at 2.0 and 3.3 meters
//		inputShapingOtherAxisDT=(char)(30.0f*(1.0f-j1)+32.0f*j1); // 30 and 32 are computer from 0.5/f at 2.0 and 3.3 meters
	}
	else if (gryphonVersion==5)
	{ // this is with NQR attached!
		j1=(r-2.0f)/1.0f; // interpolated between 2.0 and 3.0 meters
		inputShapingYawAxisDT=(char)(44.0f*(1.0f-j1)+46.0f*j1); // 30 and 32 are computer from 0.5/f at 2.0 and 3.0 meters
		inputShapingOtherAxisDT=(char)(31.0f*(1.0f-j1)+35.0f*j1); // 23 and 60 are computer from 0.5/f at 2.0 and 3.0 meters
	}
	else
	{
		j1=(r-1.5f)/1.5f; // interpolated between 1.5 and 3.0 meters
		inputShapingYawAxisDT=(char)(20.0f*(1.0f-j1)+25.0f*j1); // 20 and 25 are computer from 0.5/f at 1.5 and 3.0 meters
		inputShapingOtherAxisDT=(char)(19.0f*(1.0f-j1)+15.0f*j1); // 19 and 15 are computer from 0.5/f at 1.5 and 3.0 meters
	}

	// Limit DTs to min and max values:
	if (inputShapingYawAxisDT<0)
		inputShapingYawAxisDT=0;
//	else if (inputShapingYawAxisDT>=inputShapingBufferLength)
//		inputShapingYawAxisDT=inputShapingBufferLength-1;
	else if (inputShapingYawAxisDT>(inputShapingBufferLength-1)/2)
		inputShapingYawAxisDT=(inputShapingBufferLength-1)/2;
	if (inputShapingOtherAxisDT<0)
		inputShapingOtherAxisDT=0;
//	else if (inputShapingOtherAxisDT>=inputShapingBufferLength)
//		inputShapingOtherAxisDT=inputShapingBufferLength-1;
	else if (inputShapingOtherAxisDT>(inputShapingBufferLength-1)/2)
		inputShapingOtherAxisDT=(inputShapingBufferLength-1)/2;

	if (inputShapingYawAxisDT>35)
		inputShapingYawAxisDT=35;

	if (inputShapingOtherAxisDT>35)
		inputShapingOtherAxisDT=35;



	// Now we compute input-shaped values for the 3 axis:
	// base axis (yaw angle):
	axis[2]=axis2[bufferStartPos]/4;
	i=bufferStartPos+inputShapingYawAxisDT;
	if (i>=inputShapingBufferLength)
		i-=inputShapingBufferLength;
	axis[2]+=axis2[i]/2;
	i+=inputShapingYawAxisDT;	
	if (i>=inputShapingBufferLength)
		i-=inputShapingBufferLength;
	axis[2]+=axis2[i]/4;

	// other two axis (left and right joints):
	axis[0]=axis0[bufferStartPos]/4;
	axis[1]=axis1[bufferStartPos]/4;
	i=bufferStartPos+inputShapingOtherAxisDT;
	if (i>=inputShapingBufferLength)
		i-=inputShapingBufferLength;
	axis[0]+=axis0[i]/2;
	axis[1]+=axis1[i]/2;
	i+=inputShapingOtherAxisDT;	
	if (i>=inputShapingBufferLength)
		i-=inputShapingBufferLength;
	axis[0]+=axis0[i]/4;
	axis[1]+=axis1[i]/4;
}