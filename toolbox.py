import numpy as np
import math

HEIGHT = 720
WIDTH = 1280


def get_d_safe(din):
    return (0 + 1e-10) if din == 0 else din


def gen_Mpp(din):
    return np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1 / get_d_safe(din), 0]])


def gen_translation_mx(x, y, z):
    return np.matrix([[1, 0, 0, x],
                      [0, 1, 0, y],
                      [0, 0, 1, z],
                      [0, 0, 0, 1]])


def normalize_vect(v):
    v3 = get_d_safe(v[3])
    return [v[0] / v3, v[1] / v3, v[2] / v3, 1]


def project_points(points, d):
    outp = []
    for point in points:
        xp = point[0]
        yp = point[1]
        zp = point[2]
        din = get_d_safe(d)

        norm_param = din / (zp + din)

        xout = xp * norm_param
        yout = yp * norm_param

        p = [xout, yout, 0, 1]

        outp.append(p)
    return outp


def project_points2(points, d):
    outp = []
    for point in points:
        xp = point[0][0]
        yp = point[0][1]
        zp = point[0][2]
        zp = get_d_safe(zp)
        din = d

        norm_param = din / zp

        xout = xp * norm_param
        yout = yp * norm_param

        p = ([xout, yout, din, 1], point[1])

        outp.append(p)
    return outp


def gen_lines_for_box(ps):
    po = []
    n = math.floor(len(ps) / 8)
    for i in range(n):
        offset = i * 8
        # top lines
        lines = [(ps[i + offset], ps[i + 1 + offset]) for i in range(3)]
        lines.append((ps[0 + offset], ps[3 + offset]))

        # bottom lines
        lines += [(ps[i + offset], ps[i + 1 + offset]) for i in range(4, 7)]
        lines.append((ps[4 + offset], ps[7 + offset]))

        # vertical lines
        lines += [(ps[i + offset], ps[i + 4 + offset]) for i in range(4)]
        po += lines
    return po


def to_pg_xyz(point):
    return [point[0] + WIDTH / 2, HEIGHT / 2 - point[1]]
    # return [p0,p1]


# see - inversed as per camera coords
def translate_xyz(points, x, y, z):
    tm = gen_translation_mx(-x, -y, -z)
    for i in range(len(points)):
        points[i] = np.dot(tm, points[i]).tolist()[0]


def rotate_x(points, deg):
    rad = 2 * math.pi * deg / 360
    rotM = np.matrix(
        [[1, 0, 0, 0], [0, math.cos(rad), -math.sin(rad), 0], [0, math.sin(rad), math.cos(rad), 0], [0, 0, 0, 1]])
    for i in range(len(points)):
        points[i] = np.dot(rotM, points[i]).tolist()[0]


def rotate_y(points, deg):
    rad = 2 * math.pi * deg / 360
    rotM = np.matrix(
        [[math.cos(rad), 0, math.sin(rad), 0], [0, 1, 0, 0], [-math.sin(rad), 0, math.cos(rad), 0], [0, 0, 0, 1]])
    for i in range(len(points)):
        points[i] = np.dot(rotM, points[i]).tolist()[0]


def rotate_z(points, deg):
    rad = 2 * math.pi * deg / 360
    rotM = np.matrix(
        [[math.cos(rad), -math.sin(rad), 0, 0], [math.sin(rad), math.cos(rad), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    for i in range(len(points)):
        points[i] = np.dot(rotM, points[i]).tolist()[0]


def visiblity(points):
    outp = []
    for point in points:
        zp = point[2]

        visible = zp > 0

        outp.append((point, visible))
    return outp


# gen box starting with bottom near left corner
def gen_box(x, y, z, x_l, y_l, z_l):
    p1 = [x, y, z, 1]
    p2 = [x + x_l, y, z, 1]
    p3 = [x + x_l, y, z + z_l, 1]
    p4 = [x, y, z + z_l, 1]
    p5 = [x, y + y_l, z, 1]
    p6 = [x + x_l, y + y_l, z, 1]
    p7 = [x + x_l, y + y_l, z + z_l, 1]
    p8 = [x, y + y_l, z + z_l, 1]

    return [p1, p2, p3, p4, p5, p6, p7, p8]
