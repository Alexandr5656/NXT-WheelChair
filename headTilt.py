import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter

# Initialize parameters for the synthetic board
params = BrainFlowInputParams()
params.serial_port = 'COM3'  # replace with your serial port
board_id = -1  # board_id for synthetic board

# Create BoardShim object
board = BoardShim(board_id, params)

# Prepare the board for data streaming
board.prepare_session()

# Start streaming data
board.start_stream()

# Read data for a certain amount of time (e.g., 10 seconds)
data = board.get_board_data()  # replace with appropriate method to read data

# Stop data streaming
board.stop_stream()
board.release_session()

# Assuming accelerometer channels are at indices 0, 1, and 2
# And the data is in the format of [Ax, Ay, Az]
ax_data = data[0, :]
ay_data = data[1, :]
az_data = data[2, :]

# Calculate tilt angles in the X and Y directions
# Assuming ax_data, ay_data, and az_data are the data from accelerometer
tilt_x = DataFilter.get_inclination_angle(ax_data, ay_data)
tilt_y = DataFilter.get_inclination_angle(ax_data, az_data)

print(f'Tilt in X direction: {tilt_x} degrees')
print(f'Tilt in Y direction: {tilt_y} degrees')
