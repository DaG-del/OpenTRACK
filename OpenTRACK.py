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

print(l.count(-1))

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
        r[j] = type[i]/R[i]
        j += 1



x = fine(total_length)

distance_step_vector = numpy.diff(x)
distance_step_vector = distance_step_vector.tolist()
distance_step_vector.append(distance_step_vector[-1])
number_of_mesh_points = len(x)

d = numpy.diff(x_coarse)

i = 0
for dee in d:
    if dee == 0:
        print(i)
    i += 1


r = scipy.interpolate.pchip_interpolate(x_coarse, r, x)
r = r.tolist()

print(r[25])

f = open("r.csv", "r")
f = f.readlines()
r_MATLAB = []
for ef in f:
    r_MATLAB.append(float(ef.strip()))

print(r_MATLAB[25])

for el in range(len(r)):
    if round(r_MATLAB[el] * 100)/100 != round(r[el] * 100)/100:
        print("",end="")
