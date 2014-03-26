def accel_input(Amax,Vmax,Distance,StartTime,CurrTime,Shaper):
    import numpy as np
    # Original MATLAB/Octave premable
    ###########################################################################
    # function [accel] = accel_input(Amax,Vmax,Distance,CurrTime,Shaper)
    #
    # Function returns acceleration at a given timestep based on user input
    #
    # Amax = maximum accel, assumed to besymmetric +/-
    # Vmax = maximum velocity, assumed to be symmetric in +/-
    # Distance = desired travel distance 
    # StartTime = Time command should begin
    # CurrTime = current time 
    # Shaper = array of the form [Ti Ai] - matches output format of shaper functions
    #           in toolbox
    #          * If no Shaper input is given, then unshaped in run
    #          * If Shaper is empty, then unshaped is run
    #
    #
    # Assumptions:
    #   * +/- maximums are of same amplitude
    #   * command will begin at StartTime (default = 0)
    #   * rest-to-rest bang-coast-bang move (before shaping)
    #
    # Created: 9/23/11 - Joshua Vaughan - vaughanje@gatech.edu
    #
    # Modified: 
    #   10/11/11
    # 		* Added hard-coded shaping option - JEV (vaughanje@gatech.edu)
    # 		* embedded into shaped_jumping.m for use there
    #
    ###########################################################################
    #
    #
    # Converted to Python on 3/3/13 by Joshua Vaughan (joshua.vaughan@louisiana.edu)
    #
    # Modified:
    #   * 3/26/14 - Joshua Vaughan - joshua.vaughan@louisiana.edu
    #       - Updated some commenting, corrected typos
    #       - Updated numpy import as np

    # These are the times for a bang-coast-bang input 
    t1 = StartTime
    t2 = (Vmax/Amax) + t1
    t3 = (Distance/Vmax) + t1
    t4 = (t2 + t3)-t1
    end_time = t4


    if len(Shaper) == 0:
        # If no shaper is input, create an unshaped command
        if t3 <= t2: # command should be bang-bang, not bang-coast-bang
            t2 = np.sqrt(Distance/Amax)+t1
            t3 = 2.0 * np.sqrt(Distance/Amax)+t1
            end_time = t3
        
            accel = Amax*(CurrTime > t1) - 2*Amax*(CurrTime > t2) + Amax*(CurrTime > t3)
    
        else: # command is bang-coast-bang
            accel = Amax*(CurrTime > t1) - Amax*(CurrTime > t2) - Amax*(CurrTime > t3) + Amax*(CurrTime > t4)

    else: # create a shaped command
        ts = np.zeros((9,1))
        A = np.zeros((9,1))
        # 	Parse Shaper parameters
        for ii in range(len(Shaper)):
            ts[ii] = Shaper[ii,0]  # Shaper impulse times
            A[ii] = Shaper[ii,1]  # Shaper impulse amplitudes
        print A
        print ts

        # Hard-coded for now
        # TODO: be smarter about constructing the total input - JEV - 10/11/11
        accel = (A[0]*(Amax*(CurrTime > (t1+ts[0])) - Amax*(CurrTime > (t2+ts[0])) - Amax*(CurrTime > (t3+ts[0])) + Amax*(CurrTime > (t4+ts[0])))
        +	A[1]*(Amax*(CurrTime > (t1+ts[1])) - Amax*(CurrTime > (t2+ts[1])) - Amax*(CurrTime > (t3+ts[1])) + Amax*(CurrTime > (t4+ts[1])))
        +   A[2]*(Amax*(CurrTime > (t1+ts[2])) - Amax*(CurrTime > (t2+ts[2])) - Amax*(CurrTime > (t3+ts[2])) + Amax*(CurrTime > (t4+ts[2])))
        +   A[3]*(Amax*(CurrTime > (t1+ts[3])) - Amax*(CurrTime > (t2+ts[3])) - Amax*(CurrTime > (t3+ts[3])) + Amax*(CurrTime > (t4+ts[3])))
        +   A[4]*(Amax*(CurrTime > (t1+ts[4])) - Amax*(CurrTime > (t2+ts[4])) - Amax*(CurrTime > (t3+ts[4])) + Amax*(CurrTime > (t4+ts[4])))
        +   A[5]*(Amax*(CurrTime > (t1+ts[5])) - Amax*(CurrTime > (t2+ts[5])) - Amax*(CurrTime > (t3+ts[5])) + Amax*(CurrTime > (t4+ts[5])))
        +   A[6]*(Amax*(CurrTime > (t1+ts[6])) - Amax*(CurrTime > (t2+ts[6])) - Amax*(CurrTime > (t3+ts[6])) + Amax*(CurrTime > (t4+ts[6])))
        +   A[7]*(Amax*(CurrTime > (t1+ts[7])) - Amax*(CurrTime > (t2+ts[7])) - Amax*(CurrTime > (t3+ts[7])) + Amax*(CurrTime > (t4+ts[7])))
        +   A[8]*(Amax*(CurrTime > (t1+ts[8])) - Amax*(CurrTime > (t2+ts[8])) - Amax*(CurrTime > (t3+ts[8])) + Amax*(CurrTime > (t4+ts[8]))))

    return accel
