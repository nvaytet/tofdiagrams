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








# angles = [np.array([15.0, 98.71, 109.7, 155.49, 170.79, 208.26,
#                             227.56, 257.32, 280.33, 302.91, 329.37, 345.3]),
#                   np.array([15.0, 80.04, 91.03, 141.1 ,156.4 ,197.88,
#                             217.18, 250.67, 269.97, 299.73, 322.74, 345.])]




choppers = []





# choppers.append(Chopper(frequency=70,
#                         openings=np.array([15.0, 98.71, 109.7, 155.49, 170.79,
#                                            208.26, 227.56, 257.32, 280.33,
#                                            302.91, 329.37, 345.3]),
#                         distance=6.6))

# choppers.append(Chopper(frequency=70,
#                         openings=np.array([15.0, 80.04, 91.03, 141.1, 156.4,
#                                            197.88, 217.18, 250.67, 269.97,
#                                            299.73, 322.74, 345.0]),
#                         distance=7.1))


choppers.append(Chopper(frequency=70,
                        openings=np.array([83.71, 94.7, 140.49, 155.79,
                                            193.26, 212.56, 242.32, 265.33,
                                            287.91, 314.37, 330.3, 360.0]) + 15.0,
                        phase=17.2,
                        distance=6.6,
                        unit="deg",
                        name="WFM1"))

choppers.append(Chopper(frequency=70,
                        openings=np.array([65.04, 76.03, 126.1, 141.4, 182.88,
                                           202.18, 235.67, 254.97, 284.73,
                                           307.74, 330.00, 360.0]) + 15.0,
                        phase=46,
                        distance=7.1,
                        unit="deg",
                        name="WFM2"))

choppers.append(Chopper(frequency=56,
                        openings=np.array([ 74.6,  95.2, 139.6, 162.8, 194.3, 216.1, 245.3, 263.1, 294.8, 310.5, 347.2, 371.6]),
                        phase=32,
                        distance=8.8,
                        unit="deg",
                        name="Frame-overlap 1"))


# HZB_Chopper_FOL1 = DiscChopper(Name='HZB_Chopper_FOL1', Type='disc', Disk_Thickness=20.0, Radius=700.0, Speed=56,
#                                MaxSpeed=14.0, Source_Frequency=14.0,
#                                Sense_Of_Rotation='cw', FlightPath=30.5-21.7, Upstream_guide_opening=[25.0, 30.0], phase=32,
#                                delay=0.0,
#                                Downstream_guide_opening=[20, 20], Number_of_Cutouts=6, Cutout_depth=50.0,
#                                offset_from_TDC=[74.6,139.6,194.3,245.3,294.8,347.2], Cutout_sector_angle=[20.6,23.2,21.8,17.8,15.7,24.4])

# HZB_Chopper_DC2a = DiscChopper(Name='HZB_Chopper_DC2a', Type='disc', Disk_Thickness=20.0, Radius=700.0, Speed=14.0,
#                                MaxSpeed=14.0, Source_Frequency=14.0,
#                                Sense_Of_Rotation='cw', FlightPath=31.7-21.7, Upstream_guide_opening=[25.0, 30.0], phase=90,
#                                delay=0.0,
#                                Downstream_guide_opening=[20, 20], Number_of_Cutouts=1, Cutout_depth=50.0,
#                                offset_from_TDC=[70], Cutout_sector_angle=[140])

# HZB_Chopper_DC2b = DiscChopper(Name='HZB_Chopper_DC2b', Type='disc', Disk_Thickness=20.0, Radius=600.0, Speed=14.0,
#                                MaxSpeed=14.0, Source_Frequency=14.0,
#                                Sense_Of_Rotation='cw', FlightPath=32.3-21.7, Upstream_guide_opening=[25.0, 30.0], phase=90,
#                                delay=0.0,
#                                Downstream_guide_opening=[20, 20], Number_of_Cutouts=1, Cutout_depth=50.0,
#                                offset_from_TDC=[101], Cutout_sector_angle=[202])

# HZB_Chopper_FOL2 = DiscChopper(Name='HZB_Chopper_FOL2', Type='disc', Disk_Thickness=20.0, Radius=600.0, Speed=28,
#                                MaxSpeed=14.0, Source_Frequency=14,
#                                Sense_Of_Rotation='cw', FlightPath=37.6-21.7, Upstream_guide_opening=[25.0, 30.0], phase=20,
#                                delay=0.0,
#                                Downstream_guide_opening=[20, 20], Number_of_Cutouts=6, Cutout_depth=50.0,
#                                offset_from_TDC=[98,154,206.8,254,299,344.65], Cutout_sector_angle=[36.6,36.06,30.21,26.88,24.56,29.11])








nframes = 6


pulse_length = 2.86e-03

lambda_min = 2.0 # angstroms
lambda_max = 10.0 # angstroms

# Neutron speed from wavelength
vmin = 3956.0 / lambda_min # vmin is actually the highest velocity
vmax = 3956.0 / lambda_max # vmax is actually the lowest velocity

print("vmin, vmax", vmin, vmax)

colors = ['b', 'k', 'g', 'r', 'cyan', 'magenta']

fig, ax = plt.subplots(1, 1)
ax.grid(True, color='lightgray', linestyle="dotted")
ax.set_axisbelow(True)






for ch in choppers:
    dist = [ch.distance, ch.distance]
    for i in range(0, len(ch.openings), 2):
        t1 = (ch.openings[i] + ch.phase) / ch.omega
        t2 = (ch.openings[i+1] + ch.phase) / ch.omega
        ax.plot([t1, t2], dist, color=colors[i//2])


ch = choppers[1]

x0 = 0.0
x1 = pulse_length
y0 = 0.0
y1 = 0.0





detector_position = 32.4


psize = detector_position/50.0
# Pulse
rect = Rectangle((x0, y0), x1, -psize, lw=1, fc='grey', ec='k')
ax.add_patch(rect)
ax.text(0.5*(x0+x1), -psize, "2.86 ms", ha="center", va="top", fontsize=4)

for i in range(nframes):
# for i in range(0, len(ch.openings), 2):

    slope_min = 1.0e30
    slope_max = -1.0e30
    for ch in choppers:
        xmin = (ch.openings[i*2] + ch.phase) / ch.omega
        xmax = (ch.openings[i*2+1] + ch.phase) / ch.omega
        slope1 = (ch.distance - y1) / (xmin - x1)
        slope2 = (ch.distance - y0) / (xmax - x0)
        
        if slope_min > slope1:
            x2 = xmin
            y2 = ch.distance
            slope_min = slope1
        if slope_max < slope2:
            x3 = xmax
            y3 = ch.distance
            slope2 = slope_max
        
        # x2 = min(x2, (ch.openings[i] + ch.phase) / ch.omega)
        # x3 = max(x3, (ch.openings[i+1] + ch.phase) / ch.omega)


    # x2 = (ch.openings[i] + ch.phase) / ch.omega
    # y2 = ch.distance
    # x3 = (ch.openings[i+1] + ch.phase) / ch.omega
    # y3 = ch.distance
    a1 = (y3 - y0) / (x3 - x0)
    a2 = (y2 - y1) / (x2 - x1)
    b1 = y0 - a1 * x0
    b2 = y1 - a2 * x1
    x5 = (detector_position - b1)/a1
    x4 = (detector_position - b2)/a2
    
    ax.plot([x0, x3, x5], [y0, y3, detector_position], color=colors[i], lw=1)
    ax.plot([x1, x2, x4], [y1, y2, detector_position], color=colors[i], lw=1)






# t1 = (ch.openings[0] + ch.phase) / ch.omega
# ax.plot([pulse_length, t1], [0, ch.distance])


# t1 = (ch.openings[1] + ch.phase) / ch.omega
# ax.plot([0, t1], [0, ch.distance])



# # # line1
# # t1 = (ch.openings[0] + ch.phase) / ch.omega
# # b = ch.distance - vmin * t1
# # t0 = -b / vmin
# # ax.plot([t0, t1], [0, ch.distance])


# # # line2
# # b = - vmin*pulse_length
# # t2 = (ch.distance - b) / vmin
# # ax.plot([pulse_length, t2], [0, ch.distance])



# # # line3
# # t1 = (ch.openings[1] + ch.phase) / ch.omega
# # b = ch.distance - vmax * t1
# # t0 = -b / vmax
# # ax.plot([t0, t1], [0, ch.distance])


# # # line4
# # b = 0.0
# # t2 = (ch.distance - b) / vmax
# # ax.plot([0.0, t2], [0, ch.distance])





# ax.set_ylim(0, 20.0)

fig.savefig("chops.pdf", bbox_inches="tight")

