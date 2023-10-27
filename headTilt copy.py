import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
import numpy as np
import tkinter as tk
import time
def initialize_board():
    params = BrainFlowInputParams()
    params.serial_port = 'COM3'
    board_id = brainflow.BoardIds.CYTON_BOARD.value
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    return board

def zero_gyroscope(board):
    time.sleep(2)
    data = board.get_current_board_data(num_samples=1)
    gyro_data = data[9:12, :]  # Assuming gyroscope channels are at indices 9, 10, and 11
    print(gyro_data)
    return gyro_data

def get_gyroscope_data(board, zero_point):
    data = board.get_current_board_data(num_samples=1)
    gyro_data = data[9:12, :]  # Assuming gyroscope channels are at indices 9, 10, and 11
    #gyro_data = gyro_data - zero_point.reshape(-1, 1)
    return gyro_data

def predict_tilt(gyro_data,zero_point):
    threshold = 0.5  # Adjust based on your requirements
    #thresholdValues = [abs(zero_point[0])+threshold,abs(zero_point[1])+threshold,abs(zero_point[2])+threshold]
    tilt_direction = {"left_right": "No left/right tilt", "forward_backward": "No forward/backward tilt"}
    if gyro_data[0] > zero_point[0]+threshold:
        tilt_direction["left_right"] = "Tilting right"
    elif gyro_data[0] < -zero_point[0]-threshold:
        tilt_direction["left_right"] = "Tilting left"
    if gyro_data[1] < zero_point[1]+threshold:
        tilt_direction["forward_backward"] = "Tilting backward"
    elif gyro_data[1] > -zero_point[1]-threshold:
        tilt_direction["forward_backward"] = "Tilting forward"
    return tilt_direction

def update_data():
    global board, zero_point
    gyro_data = get_gyroscope_data(board, zero_point)
    tilt_direction = predict_tilt(gyro_data,zero_point)
    gyro_label.config(text=f'Gyro Data: {gyro_data.ravel()}')
    tilt_label.config(text=f'Left/Right: {tilt_direction["left_right"]}, Forward/Backward: {tilt_direction["forward_backward"]}')
    root.after(200, update_data)  # Update every 200 ms

if __name__ == '__main__':
    board = initialize_board()
    zero_point = zero_gyroscope(board)
    
    root = tk.Tk()
    root.title('Gyroscope Data')
    root.geometry('400x400')  # Set the dimensions of the window to be a square
    
    gyro_label = tk.Label(root, text='Gyro Data: ')
    gyro_label.pack()
    
    tilt_label = tk.Label(root, text='Left/Right: , Forward/Backward: ')
    tilt_label.pack()
    
    root.after(200, update_data)  # Start updating data every 200 ms
    root.mainloop()
    board.stop_stream()
    board.release_session()
