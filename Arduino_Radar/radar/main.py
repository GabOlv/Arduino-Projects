import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Serial communication setup
ser = serial.Serial('COM7', 9600, timeout=2) # Must change this to the correct COM port

# Create figure and axis for the radar plot
fig = plt.figure(facecolor='#333333')
fig.canvas.toolbar.pack_forget()
fig.canvas.manager.set_window_title('Ultrasonic Radar')

radar = fig.add_subplot(1, 1, 1, projection='polar', facecolor='#006b70')
radar.tick_params(axis='both', colors='white')


radar_axix_max = 100
radar.set_ylim([0.0, radar_axix_max])
radar.set_xlim([0.0, np.pi])

radar.set_position([0.0, 0.0, 1.1, 1.05])
radar.set_rticks(np.linspace(0.0, radar_axix_max, 5))
radar.set_thetagrids(np.linspace(0.0, 180, 10))

# Adjust angular range for semicircle (0 to 180 degrees)
start_angle = 0
end_angle = 180
angles = np.linspace(start_angle, end_angle, end_angle - start_angle + 1) * (np.pi / 180)
dists = np.zeros_like(angles)

# Plot for the radar points and line
pols, = radar.plot([], linestyle='', marker='o', color='red',
                   markersize=5, alpha=0.75)  # Points for radar plot
line_1, = radar.plot([], color='white', linewidth=1.5)  # Line for current reading

# Function to update the radar plot
def update(frame):
    try:
        data = ser.readline().decode().strip()  # Read serial data
        angle, distance = map(float, data.split(','))  # Parse angle and distance

        # Adjust angle to match semicircle range (0 to 180 degrees)
        if 0 <= angle <= 180:
            angle_mapped = angle
        elif 180 < angle <= 270:
            angle_mapped = 360 - angle
        else:
            return

        # Update radar points (distance at corresponding angle)
        dists[int(angle_mapped)] = distance
        pols.set_data(angles, dists)

        # Update the line (from center to current distance at angle)
        line_1.set_data([0, angle_mapped * (np.pi / 180)], [0, distance])

    except ValueError:
        pass  # Ignore corrupted or incomplete data

    return pols, line_1

# Animation function
ani = FuncAnimation(fig, update, interval=50, blit=True)

# Customize the figure appearance
fig.set_facecolor('#333333')
radar.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.5)

# Start the radar plot
plt.show()

# Clean up
ser.close()
