
import socket, sys, os, array, threading
from time import *
from fcntl import ioctl
from can2RNET import *
import sys
# Function to induce JSM error
def induce_JSM_error(cansocket):
    for i in range(0,3):
        cansend(cansocket,'0c000000#')

# Function to exploit JSM error
def RNET_JSMerror_exploit(cansocket):
    print("Waiting for JSM heartbeat")
    canwait(cansocket,"03C30F0F:1FFFFFFF")
    t = time() + 0.20

    print("Waiting for joy frame")
    joy_id = wait_rnet_joystick_frame(cansocket, t)
    print("Using joy frame: " + joy_id)

    induce_JSM_error(cansocket)
    print("3 x 0c000000# sent")

    return joy_id

# Function to wait for any frame containing a Joystick position
def wait_rnet_joystick_frame(can_socket, start_time):
    frameid = ''

    while frameid[0:3] != '020':
        cf, addr = can_socket.recvfrom(16)
        candump_frame = dissect_frame(cf)
        frameid = candump_frame.split('#')[0]
        if time() > start_time:
            print("JoyFrame wait timed out")
            return 'Err!'
    return frameid
def dec2hex(dec,hexlen):  #convert dec to hex with leading 0s and no '0x'
    h=hex(int(dec))[2:]
    l=len(h)
    if h[l-1]=="L":
        l-=1  #strip the 'L' that python int sticks on
    if h[l-2]=="x":
        h= '0'+hex(int(dec))[1:]
    return ('0'*hexlen+h)[l:l+hexlen]
# This creates a power level that is wheelchair readable only use is for forward or backward
def powerToCan(powerLevel):
    #TODO Convert -255 to 255 to a command
    pass
def RNETsetSpeedRange(cansocket,speed_range):
    if speed_range>=0 and speed_range<=0x64:
        cansend(cansocket,'0a040100#'+dec2hex(speed_range,2))
    else:
        print('Invalid RNET SpeedRange: ' + str(speed_range))
def drive_forward(seconds):
    can_socket = opencansocket(0)
    play_r2d2_noise(can_socket)     
    return

    start_time = time()
    stop_time = start_time + seconds
    RNETsetSpeedRange(can_socket,10)

    forward_frame = '02000000#'+dec2hex(0,2)+dec2hex(60,2)
    while time() < stop_time:
        cansend(can_socket, forward_frame)

    stop_frame = '02000000#0000'

    # Send the stop command
    cansend(can_socket, stop_frame)

    # Close the CAN socket

def play_r2d2_noise(can_socket):
    """
    Play an R2D2-like noise on the wheelchair using the can_socket.

    Args:
    - can_socket: a socket connected to the CAN network.
    """
    
    # Example sequence of notes with format (Duration, Note)
    r2d2_notes = [("10", "5a"), ("20", "5b"), ("10", "5c"), ("20", "5d")]
    can_data =""
    for duration, note in r2d2_notes:
        # Construct and send the CAN frame
        can_id = "181C0100"
        can_data = can_data+duration + note + "00000000"  # pad with zeros to make 8 bytes
    print(can_data)
    print(can_id+"#"+can_data)
    cansend(can_socket, f"{can_id}#{can_data}")
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python startingTest.py <seconds>")
        sys.exit(1)
    try:
        seconds = float(sys.argv[1])
    except ValueError:
        print("Error: Invalid input. Please enter a number.")
        sys.exit(1)
    #play_r2d2_noise()
    drive_forward(seconds)
