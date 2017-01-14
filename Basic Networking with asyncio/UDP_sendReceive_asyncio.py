#! /usr/bin/env python

###############################################################################
# UDP_sendReceive_asyncio.py
#
# Code to both send and receive data indefinitely using Python 3 asyncio
#
# Extended from code at:
#  https://docs.python.org/3/library/asyncio-protocol.html
#  https://github.com/python/asyncio/blob/master/examples/udp_echo.py
#  http://stackoverflow.com/questions/37512182/how-can-i-periodically-execute-a-function-with-asyncio
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/11/17
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 01/13/17 - JEV - joshua.vaughan@louisiana.edu
#       - Added check for event loop to allow running repeatedly in IPython
#
# TODO:
#   * Do try...except blocks work in async functions? - 01/11/17
###############################################################################

import numpy as np
import matplotlib.pyplot as plt

from contextlib import suppress
import time

# Import the asyncio library and uvloop, which promises to improve speed
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

LOCAL_IP, LOCAL_PORT = '127.0.0.1', 2390
REMOTE_IP, REMOTE_PORT = '127.0.0.1', 2390


class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        """ This method gets called for each UDP packet received """
        message = data.decode()
        
        # Print out the message received 
        print('Received {} from {}'.format(message, addr))


class PeriodicSender:
    """ 
    Handles the starting and stopping of repeated, timed calls to send the
    data. 
    
    Arguments:
      rate : Rate at which to send data (Hz)
      transport : object returned from setting up the UDP server in the asyncio
                  loop
      address_tuple : the IP address and port to send to
    """
    
    def __init__(self, rate, transport, address_tuple):
        self.wait_time = 1 / rate
        self.start_time = time.time()
        self.transport = transport
        self.address_tuple = address_tuple
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            
            with suppress(asyncio.CancelledError):
                 await self._task

    async def _run(self):
        while True:
            await asyncio.sleep(self.wait_time)
            
            # Calculate the data to send at this time-step
            dt = time.time() - self.start_time
            signal = 25 * np.sin(0.5 * np.pi * dt) + 25
            data = '{}\r\n'.format(int(signal)).encode('utf-8')
            
            print('Sending {} to {}.'.format(data, self.address_tuple))

            # send it
            self.transport.sendto(data, self.address_tuple)


async def periodic_sender(rate, transport, address_tuple):
    """ 
    Starts the sender and monitor for try...except to close 

    Arguments:
      rate : Rate at which to send data (Hz)
      transport : object returned from setting up the UDP server in the asyncio
                  loop
      address_tuple : the IP address and port to send to
    """
    sender = PeriodicSender(rate, transport, (REMOTE_IP, REMOTE_PORT))

    # TODO: Do try...except blocks work in async functions? - 01/11/17 - JEV
    try:
        # repeated calls to start the sender are checked for in this method,
        # so that they are not damaging
        await sender.start()
        while True:
            
            # Sleep for a little while
            await asyncio.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        # Do stuff on exit
        await sender.stop()


if __name__ == "__main__":
    try:
        # Now use asyncio to manage the sending and receiving of data
        loop = asyncio.get_event_loop()
        
        # This check will allow us to run this multiple times in IPython, without 
        # getting an error about the event loop being closed
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()

    
        server = loop.create_datagram_endpoint(EchoServerProtocol, 
                                               local_addr=(LOCAL_IP, LOCAL_PORT))

        # Tell the server loop to run. This run_until_complete here will run
        # forever, because the protocol never closes it
        transport, protocol = loop.run_until_complete(server)
    
        rate = 1000       # Rate at which to send data (Hz)
    
        # Now, start the sender, which also had an internal infinite loop so that 
        # it will keep sending data indefinitely
        loop.run_until_complete(periodic_sender(rate, 
                                                transport,
                                                (REMOTE_IP, REMOTE_PORT)))
        while True:
            print('testing')
            asyncio.sleep(1)
            
    except (KeyboardInterrupt, SystemExit):
        # Let's cancel all running tasks:
        pending = asyncio.Task.all_tasks()
        for task in pending:
            task.cancel()
            # Now we should await task to execute it's cancellation.
            # Cancelled task raises asyncio.CancelledError that we can suppress:
            with suppress(asyncio.CancelledError):
                loop.run_until_complete(task)
            
    transport.close()
    loop.close()