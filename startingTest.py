
import sys
from can2RNET import cansend
from time import sleep
import socket

def drive_forward(seconds):
    # Initialize CAN socket
    print("Starting")
    s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    s.bind(("can0",))

    # CAN frame to move the wheelchair forward (using arbitrary values, these will need to be determined experimentally)
    forward_frame = '020#000080'  # This frame is a placeholder and likely incorrect
    # Send the forward command
    cansend(s, forward_frame)

    # Wait for the specified amount of time
    sleep(seconds)

    # CAN frame to stop the wheelchair (using arbitrary values, these will need to be determined experimentally)
    stop_frame = '020#000000'  # This frame is a placeholder and likely incorrect
    # Send the stop command
    cansend(s, stop_frame)

    # Close the CAN socket
    s.close()

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
