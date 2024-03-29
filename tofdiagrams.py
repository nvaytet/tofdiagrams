import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def deg_to_rad(x):
    return x * np.pi / 180.0


class Chopper:

    def __init__(self, frequency=0, openings=None, distance=0, phase=0,
                 unit="rad", name=""):
        # openings is list. First entry is start angle of the first cut-out
        # second entry is end angle of first cut-out, etc.
        self.frequency = frequency
        self.openings = openings
        self.omega = 2.0 * np.pi * frequency
        self.distance = distance
        self.phase = phase
        if unit == "deg":
            self.openings = deg_to_rad(self.openings)
            self.phase = deg_to_rad(self.phase)
        self.name = name


choppers = dict()

choppers["WFM1"] = Chopper(frequency=70,
                           openings=np.array([83.71, 94.7, 140.49, 155.79,
                                               193.26, 212.56, 242.32, 265.33,
                                               287.91, 314.37, 330.3, 360.0]) + 15.0,
                           phase=47.10,
                           distance=6.6,
                           unit="deg",
                           name="WFM1")

choppers["WFM2"] = Chopper(frequency=70,
                           openings=np.array([65.04, 76.03, 126.1, 141.4, 182.88,
                                              202.18, 235.67, 254.97, 284.73,
                                              307.74, 330.00, 360.0]) + 15.0,
                           phase=76.76,
                           distance=7.1,
                           unit="deg",
                           name="WFM2")

choppers["FOL1"] = Chopper(frequency=56,
                           openings=np.array([74.6, 95.2, 139.6, 162.8, 194.3, 216.1, 245.3, 263.1, 294.8, 310.5, 347.2, 371.6]),
                           phase=62.40,
                           distance=8.8,
                           unit="deg",
                           name="Frame-overlap 1")

choppers["FOL2"] = Chopper(frequency=28,
                           openings=np.array([98., 134.6, 154., 190.06, 206.8, 237.01, 254., 280.88, 299., 323.56, 344.65, 373.76]),
                           phase=12.27,
                           distance=15.9,
                           unit="deg",
                           name="Frame-overlap 2")


# Conversion factors
microseconds = 1.0e6
v_to_lambda = 3956.0
v_to_mev = 437.0

# Number of frames
nframes = 6

# Length of pulse
pulse_length = 2.86e-03

# Position of detector
# detector_position = 28.98 # 32.4
detector_position = 28.42 # 32.4
# # Monitor
# detector_position = 25

# Midpoint between WFM choppers which acts as new source distance for stitched data
wfm_choppers_midpoint = 0.5 * (choppers["WFM1"].distance + choppers["WFM2"].distance)

# Frame colors
colors = ['b', 'k', 'g', 'r', 'cyan', 'magenta']

# Make figure
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
ax.grid(True, color='lightgray', linestyle="dotted")
ax.set_axisbelow(True)

# Plot the chopper openings
for key, ch in choppers.items():
    dist = [ch.distance, ch.distance]
    for i in range(0, len(ch.openings), 2):
        t1 = (ch.openings[i] + ch.phase) / ch.omega * microseconds
        t2 = (ch.openings[i+1] + ch.phase) / ch.omega * microseconds
        ax.plot([t1, t2], dist, color=colors[i//2])
    ax.text(t2 + (t2-t1), ch.distance, ch.name, ha="left", va="center")


# Define and draw source pulse
x0 = 0.0
x1 = pulse_length * microseconds
y0 = 0.0
y1 = 0.0
psize = detector_position/50.0
rect = Rectangle((x0, y0), x1, -psize, lw=1, fc='orange', ec='k', hatch="////", zorder=10)
ax.add_patch(rect)
ax.text(x0, -psize, "Source pulse (2.86 ms)", ha="left", va="top", fontsize=6)

# Now find frame boundaries and draw frames
frame_boundaries = []
frame_shifts = []
frame_velocities = []

for i in range(nframes):

    # Find the minimum and maximum slopes that are allowed through each frame
    slope_min = 1.0e30
    slope_max = -1.0e30
    for key, ch in choppers.items():

        # For now, ignore Wavelength band double chopper
        if len(ch.openings) == nframes * 2:

            xmin = (ch.openings[i*2] + ch.phase) / ch.omega * microseconds
            xmax = (ch.openings[i*2+1] + ch.phase) / ch.omega * microseconds
            slope1 = (ch.distance - y1) / (xmin - x1)
            slope2 = (ch.distance - y0) / (xmax - x0)

            if slope_min > slope1:
                x2 = xmin
                y2 = ch.distance
                slope_min = slope1
            if slope_max < slope2:
                x3 = xmax
                y3 = ch.distance
                slope_max = slope2

    # Compute line equation parameters y = a*x + b
    a1 = (y3 - y0) / (x3 - x0)
    a2 = (y2 - y1) / (x2 - x1)
    b1 = y0 - a1 * x0
    b2 = y1 - a2 * x1
    # This is the neutron velocities
    frame_velocities.append([a1 * microseconds, a2 * microseconds])

    y4 = detector_position
    y5 = detector_position

    # This is the frame boundaries
    x5 = (y5 - b1)/a1
    x4 = (y4 - b2)/a2
    frame_boundaries.append([x4, x5])

    # Compute frame shifts from fastest neutrons in frame
    frame_shifts.append((wfm_choppers_midpoint - b2)/a2)

    ax.fill([x0, x1, x4, x5], [y0, y1, y4, y5], alpha=0.3, color=colors[i])
    ax.plot([x0, x5], [y0, y5], color=colors[i], lw=1)
    ax.plot([x1, x4], [y1, y4], color=colors[i], lw=1)
    ax.text(0.5*(x4+x5), detector_position, "Frame {}".format(i+1), ha="center", va="top")


# Plot detector location
ax.plot([0, np.amax(frame_boundaries)], [detector_position, detector_position], lw=3, color='grey')
ax.text(0.0, detector_position, "Detector", va="bottom", ha="left")
# Plot WFM choppers mid-point
ax.plot([0, np.amax(frame_boundaries)], [wfm_choppers_midpoint, wfm_choppers_midpoint], lw=1, color='grey', ls="dashed")
ax.text(np.amax(frame_boundaries), wfm_choppers_midpoint, "WFM chopper mid-point", va="bottom", ha="right")

# Print results as a table:
output = "=================================================================================================\n"
output += "                     "
for i in range(nframes):
    output += "Frame {}      ".format(i+1)
output += "\nLeft boundary [us]:  "
for i in range(nframes):
    output += "{:.5e}  ".format(frame_boundaries[i][0])
output += "\nRight boundary [us]: "
for i in range(nframes):
    output += "{:.5e}  ".format(frame_boundaries[i][1])
output += "\nFrame shift [us]:    "
for i in range(nframes):
    output += "{:.5e}  ".format(frame_shifts[i])
output += "\nMin speed [m/s]:     "
for i in range(nframes):
    output += "{:.5e}  ".format(frame_velocities[i][0])
output += "\nMax speed [m/s]:     "
for i in range(nframes):
    output += "{:.5e}  ".format(frame_velocities[i][1])
output += "\nMin wavelength [AA]: "
for i in range(nframes):
    output += "{:.5e}  ".format(v_to_lambda / frame_velocities[i][1])
output += "\nMax wavelength [AA]: "
for i in range(nframes):
    output += "{:.5e}  ".format(v_to_lambda / frame_velocities[i][0])
output += "\nMin energy [meV]:    "
for i in range(nframes):
    output += "{:.5e}  ".format((frame_velocities[i][0]/v_to_mev)**2)
output += "\nMax energy [meV]:    "
for i in range(nframes):
    output += "{:.5e}  ".format((frame_velocities[i][1]/v_to_mev)**2)
output += "\n================================================================================================="
print(output)

# Save the figure
ax.set_xlabel("Time [microseconds]")
ax.set_ylabel("Distance [m]")
fig.savefig("tof_diagram.pdf", bbox_inches="tight")
