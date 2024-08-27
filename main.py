import pickle as pkl
import matplotlib.pyplot as plt

#simulate on recorded data
can_data = pkl.load(open('data/steering.pkl', 'rb'))


can_data = can_data[2:]

# saving data in lists
brake_pressure = []
throttle_pedal = []
speeds = []
steering = []

for can_signal in can_data:
    can_signal = can_signal.decode('utf-8').split()
    if len(can_signal) < 3:
        continue
    can_id = can_signal[0]
    can_frame = can_signal[2:] # to remove id and length
    new_can_frame = ''
    for byte in can_frame:
        if len(byte) == 1:
            byte = '0' + byte
        new_can_frame += byte
    can_frame = [new_can_frame[i:i+2] for i in range(0, len(new_can_frame), 2)]
    if can_id == '610':
        value = int(''.join(can_frame[2]), 16)
        speeds.append(value)
    if can_id == '224':
        value_p = int(''.join(can_frame[4:5]), 16)
        brake_pressure.append(value_p)
    if can_id == '2C1':
        value = int(can_frame[6], 16)
        throttle_pedal.append(value)
    if can_id == '260':
        value = int(''.join(can_frame)[10:], 16)
        if value & 0x800000:  # 0x800000 is the 24th bit
            value -= 0x1000000
        steering.append(value)


# replay the thing

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Steering Wheel Simulation')

# List of steering values (example values)
# steering_values = [0, 15, 30, 45, 60, 75, 90, 75, 60, 45, 30, 15, 0, -15, -30, -45, -60, -75, -90, -75, -60, -45, -30, -15, 0]
steering_values = steering
print(len(steering_values))
print(steering_values)
assert False


# Function to draw a circle with a line indicating the steering angle
def draw_steering_wheel(surface, angle):
    import math
    center = (width // 2, height // 2)
    radius = 150
    pygame.draw.circle(surface, (0, 0, 0), center, radius, 5)
    end_pos = (
        center[0] + radius * math.cos(angle),
        center[1] - radius * math.sin(angle)
    )
    pygame.draw.line(surface, (0, 0, 0), center, end_pos, 5)

# Main loop
clock = pygame.time.Clock()
index = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear screen
    window.fill((255, 255, 255))

    # Get current steering value
    angle = steering_values[index]
    index = (index + 1) % len(steering_values)

    # Draw steering wheel
    draw_steering_wheel(window, angle)

    # Update display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(10)




