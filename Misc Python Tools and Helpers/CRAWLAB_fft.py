def CRAWLAB_fft(data,time,plotflag):
    ''' CRAWLAB_fft.py
    Function to get the FFT for a response
    #
    # Usage: 
    # fft_freq, fft_mag = CRAWLAB_fft(data,time,plotflag)
    #
    # Inputs:
    #   time = time array corresponding to the data
    #   data = the response data array (only pass a single dimension/state at at time)
    #   plotflag = will plot the FFT if nonzero
    #   
    # Output:
    #   fft_freq = an array of the freqs used in the FFT
    #   fft_mag = an array of the amplitude of the FFT at each freq in fft_freq
    #
    # Created: 03/28/14
    #   - Joshua Vaughan
    #   - joshua.vaughan@louisiana.edu
    #   - http://www.ucs.louisiana.edu/~jev9637
    ######################################################################################
    '''
    import numpy as np
    from scipy.fftpack import fft
    
    # correct for any DC offset
    offset = np.mean(data) 

    # Get the natural frequency
    sample_time = time[1] - time[0]
    n = len(data)

    fft_mag = fft((data - offset)*np.hanning(len(data)))
    fft_freq = np.linspace(0.0, 1.0/(2.0*sample_time), n/2)
    
    if plotflag:
        # Plot the relationshiop
        #   Many of these setting could also be made default by the .matplotlibrc file
        fig = figure(figsize=(6,4))
        ax = gca()
        subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
        setp(ax.get_ymajorticklabels(),fontsize=18)
        setp(ax.get_xmajorticklabels(),fontsize=18)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.grid(True,linestyle=':',color='0.75')
        ax.set_axisbelow(True)

        xlabel('Frequency (Hz)',fontsize=22,labelpad=8)
        ylabel('FFT magnitude',fontsize=22,labelpad=10)
    
        plot(fft_freq, 2.0/n * np.abs(fft_mag[0:n/2]), linewidth=2, linestyle='-')
        
        # Adjust the page layout filling the page using the new tight_layout command
        tight_layout(pad=0.5)
        show()
    
    # Uncomment below to find and print the frequency at which the highest peak occurs
    # freq_index = np.argmax(2.0/n * np.abs(fft_mag[0:n/2]))
    # print fft_freq[freq_index]
    return fft_freq, fft_mag