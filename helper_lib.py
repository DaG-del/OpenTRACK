import math
import numpy


def compare_floats(a, b, error):
    a_rounded = []
    for ay in a:
        a_rounded.append(round(ay, 2))
    b_rounded = []
    for by in b:
        b_rounded.append(round(by, 2))

    if len(b_rounded) != len(a_rounded):
        print("Unequal length!")
        return

    errors = {}
    for x in range(len(a_rounded)):
        if a_rounded[x] - b_rounded[x] > error:
            errors[x] = [a_rounded[x], b_rounded[x]]

    for e in errors:
        print(e, end = " : ")
        print(errors[e])


def read_csv(filename):
    f = open(filename, "r")
    ret = []
    ip = f.readlines()
    for i in ip:
        ret.append(float(i))

    return ret


def rotz(angle, dsv, p):
    angle *= math.pi/180
    x = dsv*math.cos(angle) + p[0]
    y = dsv*math.sin(angle) + p[1]

    return [x, y]


def absol(r: list):
    r_abs = []
    for aar in r:
        r_abs.append(abs(aar))
    return r_abs


def find(r_apex_indices, r):
    ret = []
    for aar in r_apex_indices:
        ret.append(r[aar])
    return ret


def calc_d(x, total_length, Y):
    '''
    % linear correction vectors
    DX = x/L*(X(1)-X(end)) ;
    DY = x/L*(Y(1)-Y(end)) ;
    DZ = x/L*(Z(1)-Z(end)) ;
    % adding correction
    X = X+DX ;
    Y = Y+DY ;
    Z = Z+DZ ;
    '''
    ret = []
    DX = []
    for el in range(len(x)):
        DX.append(x[el] / total_length * (Y[0] - Y[-1]))

    for el in range(len(DX)):
        ret.append(Y[el] + DX[el])

    return ret