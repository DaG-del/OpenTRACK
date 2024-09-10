import math

_KAPPA = 10

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
type = [int(t[0]) for t in track]
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

