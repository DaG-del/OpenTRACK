import scipy
import math
import numpy
import helper_lib
import matplotlib.pyplot as mlt

def center_points(l):
    sum = 0
    cumulative = []
    for el in l:
        sum += el
        cumulative.append(sum - el / 2)

    return cumulative


def end_points(l):
    sum = 0
    cumulative = []
    for el in l:
        sum += el
        cumulative.append(sum)

    return cumulative


def nos(R):
    n = 0
    for r in R:
        if r == float("inf"):
            n += 1

    return n


def fine(total_length):
    tl = total_length
    x_fine = []
    sum = 0
    while True:
        x_fine.append(sum)
        sum += _mesh_size
        if x_fine[-1] > math.floor(tl):
            x_fine.pop()
            x_fine.append(total_length)
            return x_fine


def min_custom(dh):
    dh_abs = []
    for d in dh:
        dh_abs.append(abs(d))
    return min(dh_abs)


_KAPPA = 10
_mesh_size = 0.1
f = open("track.txt", "r")
track = []
ip = f.readlines()

for l in ip:
    l = l[:-1]
    tup = tuple(l.split(","))
    track.append(tup)

track = tuple(track)

R = [float(t[2]) for t in track]
for r in range(len(R)):
    if R[r] == 0:
        R[r] = float("inf")

l = [float(t[1]) for t in track]
type = [-int(t[0]) for t in track]
total_length = sum(l)

track = [(type[i], l[i], R[i]) for i in range(len(track))]

angle_seg = [(l[i] / R[i]) * 180 / math.pi for i in range(len(track))]

R_injected = R
l_injected = l
type_injected = type

j = 0
for i in range(len(l)):
    if angle_seg[i] > _KAPPA:
        distance_of_injected_point_from_corner_entry_and_exit = min(l_injected[j] / 3, (_KAPPA * math.pi / 180) * R[i])
        temp = l_injected[0:j]
        temp.append(distance_of_injected_point_from_corner_entry_and_exit)
        temp.append(l_injected[j] - 2 * distance_of_injected_point_from_corner_entry_and_exit)
        temp.append(distance_of_injected_point_from_corner_entry_and_exit)
        temp.extend(l_injected[j + 1:])
        l_injected = temp

        temp = R_injected[0:j]
        temp.extend([R_injected[j]] * 3)
        temp.extend(R_injected[j + 1:])

        R_injected = temp

        temp = type_injected[0:j]
        temp.extend([type_injected[j]] * 3)
        temp.extend(type_injected[j + 1:])

        type_injected = temp

        del temp

        j += 3
    else:
        j += 1

R = R_injected
l = l_injected
type = type_injected

'''
for i=1:length(l)-1
    j = 1 ;
    while true
        if type(i+j)==0 && type(i)==0 && l(i)~=-1
            l(i) = l(i)+l(i+j) ;
            l(i+j) = -1 ;
        else
            break
        end
        j = j+1 ;
    end
end
R(l==-1) = [] ;
type(l==-1) = [] ;
l(l==-1) = [] ;
'''

for i in range(len(l) - 1):
    j = 1
    while True:
        if type[i + j] == 0 and type[i] == 0 and l[i] != -1:
            l[i] = l[i + j] + l[i]
            l[i + j] = -1
        else:
            break
        j += 1

temp = len(l) - 1
el = 0
while el < temp:
    if l[el] == -1:
        l.pop(el)
        R.pop(el)
        type.pop(el)
        temp -= 1
    el += 1

segment_end_point = end_points(l)

segment_center_point = center_points(l)

no_of_straights = nos(R)
x_coarse = [0] * (len(segment_end_point) + no_of_straights)
r = [0] * len(x_coarse)

j = 0
for i in range(len(segment_center_point)):
    if R[i] == float("inf"):
        x_coarse[j] = segment_end_point[i] - l[i]
        x_coarse[j + 1] = segment_end_point[i]
        j += 2
    else:
        x_coarse[j] = segment_center_point[i]
        r[j] = type[i] / R[i]
        j += 1

x = fine(total_length)

distance_step_vector = numpy.diff(x)
distance_step_vector = distance_step_vector.tolist()
distance_step_vector.append(distance_step_vector[-1])
number_of_mesh_points = len(x)

r = scipy.interpolate.pchip_interpolate(x_coarse, r, x)
r = r.tolist()

n = len(x)

X = [0] * n
Y = [0] * n

angle_seg = []
for d in range(len(distance_step_vector)):
    angle_seg.append((distance_step_vector[d] * r[d]) * (180 / math.pi))

angle_heading = numpy.cumsum(angle_seg)
angle_heading = list(angle_heading.tolist())

dh = []

temp = angle_heading[-1] % (360 * (abs(angle_heading[-1]) / angle_heading[-1]))
dh.append(temp)
temp = angle_heading[-1] - (360 * (abs(angle_heading[-1]) / angle_heading[-1]))
dh.append(temp)

dh = min(dh)

for ah in range(len(angle_heading)):
    angle_heading[ah] -= x[ah] / total_length * dh

angle_seg.clear()
angle_seg.append(angle_heading[0])
diff_as = numpy.diff(angle_heading)
diff_as = list(diff_as.tolist())
angle_seg.extend(diff_as)

temp = angle_heading[0]

for ah in range(len(angle_heading)):
    angle_heading[ah] -= temp

for i in range(1, len(x)):
    p = [X[i - 1], Y[i - 1]]

    xyz = helper_lib.rotz(angle_heading[i - 1], distance_step_vector[i - 1], p)

    X[i] = xyz[0]
    Y[i] = xyz[1]

r_abs = helper_lib.absol(r)
r_apex_indices = scipy.signal.find_peaks(r_abs)
r_apex_indices = r_apex_indices[0]
r_apex_indices = r_apex_indices.tolist()

r_apex = helper_lib.find(r_apex_indices, r)

X = helper_lib.calc_d(x, total_length, X)
Y = helper_lib.calc_d(x, total_length, Y)
Z = [0] * len(X)

X_matlab = helper_lib.read_csv("X.csv")
helper_lib.compare_floats(X, X_matlab, 0.1)

Y_matlab = helper_lib.read_csv("Y.csv")
helper_lib.compare_floats(Y, Y_matlab, 0.1)

mlt.plot(X, Y)
mlt.show()

