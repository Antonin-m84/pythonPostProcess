import time

import matplotlib.pyplot as plt

tableau = ['3036', '2896', '2772', '2', '3023', '2887', '2771', '2660', '3008', '2879', '2766', '2666', '1413',
           '1376', '13', '2655']

Z = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
coordinates_x = [0, 1, 2, 3]
coordinates_y = [0, 1, 2, 3]

plt.ion()

# creating subplot and figure
fig, ax = plt.subplots()
# setting labels
plt.title("Updating plot...")
plt.axis('off')

max_y = 3

texts = {}

for y in range(4):
    for x in range(4):
        texts[f'{x}:{y}'] = ax.text(x, max_y - y, f'{tableau[y * 4 + x]}', color="black", ha="center", va="center")

print(tableau)

for i in range(len(tableau)):
    print(f'{tableau[i]:^6}', end="|")
    if (i + 1) % 4 == 0:
        print("")

# looping
for i in range(150):
    vals = [
        # Convert each element of the subset (from i to i+4) using map to int, wrapped as a list
        list(map(int, tableau[i:i + 4]))
        # iterate from 0 to tableau length (16) step by 4
        for i in range(0, len(tableau), 4)
    ][::-1]

    print(vals)

    ax.pcolormesh(coordinates_x, coordinates_y, vals,
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
    time.sleep(0.5)
