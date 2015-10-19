#! /usr/bin/python

'''#######################################################################################
# Basic polling of a gps unit via gpsd and reporting of data in terminal
#
# Adapted from code written at 
#   https://github.com/FishPi/FishPi-POCV---Command---Control September 2012
# License: BSD 2-Clause License.
#
# Modified:
#   * 06/04/14 - Joshua Vaughan - joshua.vaughan@louisiana.edu
#       - Merged with other CRAWLAB gps processing
#       - Adapted the existing gpsd-based code to pyNMEA for easier use
#       - 
##########################################################################################
'''

import os
import datetime, csv
import dateutil.parser
import threading
import logging
import serial

import time

import numpy as np
import pynmea.nmea


# logging.basicConfig(level=logging.DEBUG,
#                     format='From %(threadName)-10s: %(message)s',
#                     )


class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = 'GPS Thread')
        self.session = gps(mode=WATCH_ENABLE)   # Start the stream of GPS info
        self.current_value = None
        self.running = True                     # Set the thread running to true

    def get_current_value(self):
        return self.current_value

    def run(self):
        while self.running:
            # Continue to loop and grab EACH set of gpsd info to clear the buffer
            self.session.next()


class GPS_reader(object):
    #  how long to wait when we're looking for a response
    MAXWAITSENTENCE = 0.5
    
    # TODO: Should this be on its own thread?

    def __init__(self, interface="", hw_interface="/dev/tty.usbserial-FTWZ6G44", baud=19200):
        self._GPS = serial.Serial(hw_interface, baud)
        #self._GPS.write(self.PMTK_Q_RELEASE)
        #self._version = self._GPS.readline(20)
#         self._GPS.write(self.PMTK_SET_NMEA_UPDATE_1HZ)
#         self._GPS.write(self.PMTK_SET_BAUD_9600)
#         self._GPS.write(self.PMTK_SET_NMEA_OUTPUT_RMCVTGGGA)
        self._GPS.flush()
        self.timestamp = np.nan
        self.datestamp = np.nan
        self.lat = np.nan
        self.long = np.nan
        self.alt = np.nan
        self.heading = np.nan
        self.speed = np.nan
        self.mode = np.nan
        self.num_sats = np.nan
    
    def __del__(self):
        print '\nClosing serial port...\n'
        self._GPS.close()
    
    def parse_gps_data(self):
        """ Reads GPS and returns (fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp). """
        if not(self._GPS.inWaiting()):
            return# self.zero_response()

        # read gps rmc (recommended minimum) packet
        has_read_rmc, gps_rmc = self.wait_for_sentence('$GPRMC')
        
        if not(has_read_rmc):
            return
#             return self.zero_response()
#             
#         if not(gps_rmc.data_validity == 'A'):
#             return self.zero_response()
        logging.debug('Reading $GPRMC')
        self.timestamp = datetime.datetime.strptime(gps_rmc.timestamp.rstrip('.000'), "%H%M%S").time()
        self.datestamp = datetime.datetime.strptime(gps_rmc.datestamp, "%d%m%y").date()
        self.lat = float(gps_rmc.lat) * (1.0 if gps_rmc.lat_dir == 'N' else -1.0)
        self.long = float(gps_rmc.lon) * (1.0 if gps_rmc.lon_dir == 'E' else -1.0)
        
        # Convert from DDMM.mmmm to DD.ddddd forms
        lat_deg, lat_min = divmod(self.lat/100,1)
        self.lat = lat_deg + lat_min*100./60

        # Convert from DDMM.mmmm to DD.ddddd forms
        lon_deg, lon_min = divmod(self.long/100.0,1)
        self.long = (lon_deg + lon_min*100./60)
         
        self.heading = float(gps_rmc.true_course)
        self.speed = float(gps_rmc.spd_over_grnd)
        
        # read gps gga (fix data) packet
        has_read_gga, gps_gga = self.wait_for_sentence('$GPGGA')
        
        if not(has_read_gga):
            return # return self.zero_response()
            
#         if not(gps_gga.gps_qual > 0):
#             return #self.zero_response()
#             
#         if not(gps_gga.latitude) or not(gps_gga.longitude):
#             return #self.zero_response()
        
        logging.debug('Reading $GPGGA')
        self.mode = float(gps_gga.gps_qual)
        # self.lat = float(gps_gga.latitude) * (1.0 if gps_gga.lat_direction == 'N' else -1.0)
#         self.long = float(gps_gga.longitude) * (1.0 if gps_gga.lon_direction == 'E' else -1.0)
#         
#         # Convert from DDMM.mmmm to DD.ddddd forms
#         lat_deg, lat_min = divmod(self.lat/100,1)
#         self.lat = lat_deg + lat_min*100./60
# 
#         # Convert from DDMM.mmmm to DD.ddddd forms
#         lon_deg, lon_min = divmod(self.long/100.0,1)
#         self.long = (lon_deg + lon_min*100./60)

        
        self.altitude = float(gps_gga.antenna_altitude)
        self.num_sats = float(gps_gga.num_sats)
#         self.timestamp = datetime.datetime.strptime(gps_gga.timestamp.rstrip('.000'), "%H%M%S").time()
#         
        #logging.debug(self.lat, self.long, self.timestamp, self.datestamp, self.heading, self.speed)


    def show_gps_data(self):
        
        # Parse the GPS data first
        self.parse_gps_data()
        
        # Clear the terminal (optional)
        os.system('clear')
        # Then print it to the screen
        print ''
        print 'GPS Data via pyNMEA'
        print '==========================================================='
        print ''
        print 'Date                                            ', self.datestamp
        print 'Time (UTC)                                        ',self.timestamp
        print ''
        print 'Latitude (+/- = North/South)                     {:10.4f}'.format(self.lat)
        print 'Longitude (+/- = East/West)                      {:10.4f}'.format(self.long)
        print 'Altitude (m)                                     {:10.4f}'.format(self.alt)
        print ''
        print '-----------------------------------------------------------'
        print ''
        print 'Speed (m/s)                                      {:10.2f}'.format(self.speed)
        print 'Heading Over Ground (deg from N)                 {:10.0f}'.format(self.heading)
        print ''
        print '-----------------------------------------------------------'
        print ''
        print 'NMEA mode (0 = none, 1 = GPS, 2 = DPGS)          {:10.0f}'.format(self.mode)
        print 'Number of Satellites                             {:10.0f}'.format(self.num_sats)
        print ''
        print '==========================================================='


    def setup_data_file(self):
        # Set up the csv file to write to. 
        # The filename contains a date/time string of format gpsData_YYYY-MM-DD_HHMMSS.csv
        data_filename = 'gpsData_' + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')+'.csv'
        with open(data_filename, "wb") as data_file: 
            writer = csv.writer(data_file)
    
            # Define and write the header row immediately after opening
            header = ('Time (UTC)', 'Latitude (+/- = North/South)','Longitude (+/- = East/West)',
                    'Altitude (m)','Speed (m/s)','Heading (deg from N)',
                     'Mode','Number of Satellites')
            writer.writerow(header) 
        
        return writer, data_filename
        
        
    def write_data_file(self,writer,data_filename):
        data = [self.timestamp, self.lat, self.long, self.alt, self.speed, self.heading, self.mode, self.num_sats]
            
        with open(data_filename, "ab") as data_file: 
            # TODO: Be smarter about how and when to save data
            writer = csv.writer(data_file)
            writer.writerow(data)
        
    def read_sensor_raw(self):
        """ Read raw sensor values. """
        return self.read_sensor()

    def zero_response(self):
        self.timestamp = np.nan
        self.datestamp = np.nan
        self.lat = np.nan
        self.long = np.nan
        self.alt = np.nan
        self.heading = np.nan
        self.speed = np.nan
        self.mode = np.nan
        self.num_sats = np.nan
        
        

    def wait_for_sentence(self, wait4me):
        i = 0
        
        while (i < self.MAXWAITSENTENCE):
            i += 1
            if self._GPS.inWaiting():
                line = self._GPS.readline()
                if line.startswith(wait4me):
                    if line.startswith('$GPGGA'):
                        logging.debug("SENSOR:\tGPS_serial:\tReceived GPGGA: %s", line)
                        p = pynmea.nmea.GPGGA()
                        p.parse(line)
                        return True, p
                        
                    if line.startswith('$GPRMC'):
                        logging.debug("SENSOR:\tGPS_serial:\tReceived GPRMC: %s", line)
                        p = pynmea.nmea.GPRMC()
                        p.parse(line)
                        return True, p

        return False, None
    
    
    def stop_gps(self):   
        print '\nClosing serial port...\n'
        self._GPS.close()
#         print "\nStopping GpsPoller Thread..."
#         self.gpsp.running = False
#         self.gpsp.join(2)             # wait for the thread to finish what it's doing



if __name__ == '__main__':
    gps = GPS_reader() # create the thread
    last_time = 0.0
    
    try:
        data_writer, data_filename = gps.setup_data_file()
        
        while True:
            gps.show_gps_data()
            
            # If the GPS has a fix, save the data
            if gps.mode > 0 and gps.timestamp <> last_time:
                gps.write_data_file(data_writer, data_filename)
                last_time = gps.timestamp
            # Time between printing readings
            time.sleep(0.1) 
            
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        time.sleep(0.5)
        print "Done.\nExiting."