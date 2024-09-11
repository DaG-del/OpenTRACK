import scipy
import math
import numpy


def center_points(l):
    sum = 0
    cumulative = []
    for el in l:
        sum += el
        cumulative.append(sum - el/2)

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
    total_length = math.ceil(total_length)
    x_fine = []
    sum = 0
    while True:
        sum += _mesh_size
        x_fine.append(sum)

        if x_fine[-1] > tl:
            x_fine.pop()
            x_fine[-1] = tl
            return x_fine


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

angle_seg = [(l[i]/R[i])*180/math.pi for i in range(len(track))]

R_injected = R
l_injected = l
type_injected = type

j = 0
for i in range(len(l)):
    if angle_seg[i] > _KAPPA:
        distance_of_injected_point_from_corner_entry_and_exit = min(l_injected[j]/3, (_KAPPA*math.pi/180) * R[i])
        temp = l_injected[0:j]
        temp.append(distance_of_injected_point_from_corner_entry_and_exit)
        temp.append(l_injected[j] - 2*distance_of_injected_point_from_corner_entry_and_exit)
        temp.append(distance_of_injected_point_from_corner_entry_and_exit)
        temp.extend(l_injected[j+1:])
        l_injected = temp

        temp = R_injected[0:j]
        temp.extend([R_injected[j]] * 3)
        temp.extend(R_injected[j+1:])

        R_injected = temp

        temp = type_injected[0:j]
        temp.extend([type_injected[j]] * 3)
        temp.extend(type_injected[j+1:])

        type_injected = temp

        del temp

        j += 3
    else:
        j += 1

R = R_injected
l = l_injected
type = type_injected

to_be_removed = []

for i in range(len(l) - 1):
    if type[i] == 0 and type[i + 1] == 0:
        l[i + 1] = l[i] + l[i + 1]
        to_be_removed.append(i)

for tbr in to_be_removed:
    R.pop(tbr)
    l.pop(tbr)
    type.pop(tbr)

f = open("l.csv", "r")
f = f.readlines()
l_MATLAB = []
for ef in f:
    l_MATLAB.append(float(ef.strip()))

for el in range(len(l)):
    if round(l_MATLAB[el] * 100)/100 != round(l[el] * 100)/100:
        print(el)

print(l[143])
print(l_MATLAB[143])

print(l[222:224])
print(l_MATLAB[222:224])


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
        r[j] = type[i]/R[i]
        j += 1

x = fine(total_length)

distance_step_vector = numpy.diff(x)
distance_step_vector = distance_step_vector.tolist()
distance_step_vector.append(distance_step_vector[-1])
number_of_mesh_points = len(x)

d = scipy.diff(x_coarse)

i = 0
for dee in d:
    if dee == 0:
        print(i)
    i += 1

print(x_coarse[245:300])

r = scipy.interpolate.pchip_interpolate(x_coarse, r, x)
print(r)