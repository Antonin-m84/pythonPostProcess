from typing import List

import matplotlib.pyplot as plt
import numpy as np

import serial
import time

# Open the serial port
# ser.open()

tableau = [
    "0", "0", "0", "0",
    "0", "0", "0", "0",
    "0", "0", "0", "0",
    "0", "0", "0", "0"
]

current_table_index = 0


def loop():
    global current_table_index

    # create plot
    coordinates_x = [0, 1, 2, 3]
    coordinates_y = [0, 1, 2, 3]
    plt.ion()
    fig, ax = plt.subplots()

    plt.title("VL53L8CX 4X4 V1 GTX Turbo")
    plt.axis('off')

    texts = {}
    max_y = 3

    for y in range(4):
        for x in range(4):
            texts[f'{x}:{y}'] = ax.text(x, max_y - y, f'{tableau[y * 4 + x]}', color="black", ha="center", va="center")

    try:
        # Read and print the data from the serial port
        while True:
            # decode = convert raw signal (b'Zone;...' to encoded string ("Zone;...")
            line = ser.readline().decode("utf-8", errors="ignore")

            parse_line(line)

            if current_table_index >= len(tableau):
                # last line, update table
                # Convert the list of 16 elements to a matrix of 4x4 elements
                ax.pcolormesh(coordinates_x, coordinates_y, [
                    # Convert each element of the subset (from i to i+4) using map to int, wrapped as a list
                    list(map(int, tableau[i:i+4]))
                    # iterate from 0 to tableau length (16) step by 4
                    for i in range(0, len(tableau), 4)
                ][::-1],
                    vmin=0,
                    vmax=4500
                )

                for y in range(4):
                    for x in range(4):
                        texts[f'{x}:{y}'].set_text(f'{tableau[y * 4 + x]}')

                # re-drawing the figure
                fig.canvas.draw()

                # to flush the GUI events
                fig.canvas.flush_events()
                fig.tight_layout()

                # Print to the console (debug)
                print_table(tableau)

            # print(cc)
    except Exception as e:
        print(e)
    finally:
        ser.close()


def print_table(table: List[str]):
    print(table)

    for i in range(len(table)):
        print(f'{table[i]:^6}', end="|")
        if (i + 1) % 4 == 0:
            print("")


def parse_line(line):
    global tableau
    global current_table_index

    # check if 5 ; => valid line
    if line.count(";") == 5:
        if line.startswith("Zone"):
            # cas du header, ignore
            print("Got header -- Ignore")

        if len(line) < 8 and line.startswith(";;;;;"):
            # reset table index
            current_table_index = 0
            tableau = ["0"] * len(tableau)
        else:
            # line with data
            zone, nb_targets, ambient, target_status, distance, _ = line.split(";")

            tableau[current_table_index] = distance

            current_table_index += 1

    else:
        print("invalid line")


if __name__ == '__main__':
    # Create a serial object with the specified configuration
    ser = serial.Serial(
        port='COM3',
        baudrate=460800,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE
    )

    loop()