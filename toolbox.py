import numpy as np
import math

HEIGHT = 720
WIDTH = 1280


def get_d_safe(din):
    return (0 + 1e-10) if din == 0 else din


def gen_Mpp(din):
    return np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 1 / get_d_safe(din), 1]])


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


def gen_lines_for_box(ps):
    # top lines
    lines = [(ps[i], ps[i + 1]) for i in range(3)]
    lines.append((ps[0], ps[3]))

    # bottom lines
    lines += [(ps[i], ps[i + 1]) for i in range(4, 7)]
    lines.append((ps[4], ps[7]))

    # vertical lines
    lines += [(ps[i], ps[i + 4]) for i in range(4)]

    return lines


def to_pg_xyz(point):
    return [point[0] + WIDTH / 2, HEIGHT - point[1] + HEIGHT / 2]


# see - inversed as per camera coords
def translate_xyz(points, x, y, z):
    for i in range(len(points)):
        points[i][0] -= x
        points[i][1] -= y
        points[i][2] -= z


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
