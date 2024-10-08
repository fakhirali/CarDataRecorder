import pickle as pkl
import matplotlib.pyplot as plt

#simulate on recorded data
can_data = pkl.load(open('data/steering.pkl', 'rb'))


can_data = can_data[2:]

speed = []
steering = []
brake = []
gas = []


for can_signal in can_data:
    can_signal = can_signal.decode('utf-8').split()
    if len(can_signal) < 3:
        continue
    can_id = int(can_signal[0], 16)
    can_length = int(can_signal[1])
    can_frame = can_signal[2:]  # to remove id and length
    new_can_frame = ''
    for byte in can_frame:
        if len(byte) == 1:
            byte = '0' + byte
        new_can_frame += byte
    can_frame = [new_can_frame[i:i + 2] for i in range(0, len(new_can_frame), 2)]
    if can_id == 180:  # SPEED
        bit_start = 47
        bit_start = ((bit_start // 8) * 8) + (7 - (bit_start % 8))
        length = 16
        scale = 0.01
        bin_str = bin(int(''.join(can_frame), 16))[2:].zfill(64)
        bin_data = bin_str[bit_start:bit_start + length]
        value = int(bin_data, 2) * scale
        speed.append(value)
    if can_id == 37:  # STEERING ANGLE
        signed = True
        bit_start = 2
        bit_start = ((bit_start // 8) * 8) + (7 - (bit_start % 8))
        length = 11
        scale = 1
        bin_str = bin(int(''.join(can_frame), 16))[2:].zfill(64)
        bin_data = bin_str[bit_start:bit_start + length]
        value = int(bin_data, 2)
        if value >= 2 ** (length - 1) and signed:
            value -= 2 ** length
        value = value * scale
        steering.append(value)
    if can_id == 548:  # BRAKE PRESSURE
        signed = False
        bit_start = 39
        length = 16
        scale = 1

        bit_start = ((bit_start // 8) * 8) + (7 - (bit_start % 8))
        bin_str = bin(int(''.join(can_frame), 16))[2:].zfill(64)
        bin_data = bin_str[bit_start:bit_start + length]
        value = int(bin_data, 2)
        if value >= 2 ** (length - 1) and signed:
            value -= 2 ** length
        value = value * scale
        brake.append(value)
    if can_id == 705:  # GAS PEDAL PRESSURE
        signed = False
        bit_start = 55
        length = 8
        scale = 1

        bit_start = ((bit_start // 8) * 8) + (7 - (bit_start % 8))
        bin_str = bin(int(''.join(can_frame), 16))[2:].zfill(64)
        bin_data = bin_str[bit_start:bit_start + length]
        value = int(bin_data, 2)
        if value >= 2 ** (length - 1) and signed:
            value -= 2 ** length
        value = value * scale
        gas.append(value)
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


def draw_steering_wheel(surface, angle_degrees):
    import math
    angle_radians = math.radians(angle_degrees + 90)
    center = (width // 2, height // 2)
    radius = 150
    pygame.draw.circle(surface, (0, 0, 0), center, radius, 5)
    end_pos = (
        center[0] + radius * math.cos(angle_radians),
        center[1] - radius * math.sin(angle_radians)
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




