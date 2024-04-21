import random

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


def visiblity(polygons):
    outp = []
    for polygon in polygons:
        outp2 = []
        for j in range(len(polygon)):
            zp = polygon[j][2]

            visible = zp > 0

            outp2.append({"point": polygon[j], "visibility": visible})
        outp.append(outp2)
    return outp


def project_points2(polygons, d):
    outp = []
    for polygon in polygons:
        outp2 = []
        for j in range(len(polygon)):
            xp = polygon[j]['point'][0]
            yp = polygon[j]['point'][1]
            zp = polygon[j]['point'][2]
            zp = get_d_safe(zp)
            din = d

            norm_param = din / zp

            xout = xp * norm_param
            yout = yp * norm_param

            p = {'point': [xout, yout, din, 1], 'visibility': polygon[j]['visibility']}
            outp2.append(p)
        outp.append(outp2)
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


def translate_xyz(polygons, x, y, z):
    tm = gen_translation_mx(-x, -y, -z)
    for polygon in polygons:
        for point in polygon:
            point['point'] = np.dot(tm, point['point']).tolist()[0]


def rotate_x(polygons, deg):
    rad = 2 * math.pi * deg / 360
    rotM = np.matrix(
        [[1, 0, 0, 0], [0, math.cos(rad), -math.sin(rad), 0], [0, math.sin(rad), math.cos(rad), 0], [0, 0, 0, 1]])
    for i in range(len(polygons)):
        for j in range(len(polygons[i])):
            polygons[i][j] = np.dot(rotM, polygons[i][j]).tolist()[0]


def rotate_y(polygons, deg):
    rad = 2 * math.pi * deg / 360
    rotM = np.matrix(
        [[math.cos(rad), 0, math.sin(rad), 0], [0, 1, 0, 0], [-math.sin(rad), 0, math.cos(rad), 0], [0, 0, 0, 1]])
    for i in range(len(polygons)):
        for j in range(len(polygons[i])):
            polygons[i][j] = np.dot(rotM, polygons[i][j]).tolist()[0]


def rotate_z(polygons, deg):
    rad = 2 * math.pi * deg / 360
    rotM = np.matrix(
        [[math.cos(rad), -math.sin(rad), 0, 0], [math.sin(rad), math.cos(rad), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    for i in range(len(polygons)):
        for j in range(len(polygons[i])):
            polygons[i][j] = np.dot(rotM, polygons[i][j]).tolist()[0]


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

    s_btm = [p1, p2, p3, p4]
    s_top = [p5, p6, p7, p8]
    s_fwd = [p4, p3, p7, p8]
    s_bck = [p1, p2, p6, p5]
    s_left = [p1, p4, p8, p5]
    s_right = [p2, p3, p7, p6]

    return [s_btm, s_top, s_fwd, s_bck, s_left, s_right]


def intTryParse(value) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def cd(xyz1, xyz2):
    [x, y, z] = xyz1
    [x2, y2, z2] = xyz2
    return math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2 + (z2 - z) ** 2)


def gen_mid_point(xyz1, xyz2):
    [x1, y1, z1] = xyz1
    [x2, y2, z2] = xyz2
    x = x1 + x2 / 2
    y = y1 + y2 / 2
    z = z1 + z2 / 2
    return [x, y, z]


def gen_random(n, poly_pts):
    minx = min([pt[0] for pt in poly_pts])
    maxx = max([pt[0] for pt in poly_pts])
    miny = min([pt[1] for pt in poly_pts])
    maxy = max([pt[1] for pt in poly_pts])
    minz = min([pt[2] for pt in poly_pts])
    maxz = max([pt[2] for pt in poly_pts])

    out = []
    for i in range(n):
        out.append([random.uniform(minx, maxx), random.uniform(miny, maxy), random.uniform(minz, maxz)])
    return out


def calc_dist(polygon, cam_xyz, altern_enabled):
    # cam_xyz = [0, 0, 0]

    poly_pts = [point['point'][:3] for point in polygon]

    x = sum([point['point'][0] for point in polygon]) / len(polygon)
    y = sum([point['point'][1] for point in polygon]) / len(polygon)
    z = sum([point['point'][2] for point in polygon]) / len(polygon)

    points = [[x, y, z]]
    if altern_enabled:
        points += poly_pts
        points += [gen_mid_point(poly_pts[i], poly_pts[i + 1]) for i in range(len(poly_pts) - 1)]
        points.append(gen_mid_point(poly_pts[0], poly_pts[-1]))
        points += gen_random(1000, poly_pts)

    return min([cd(cam_xyz, point) for point in points])


def deep_copy(polygons):
    return [polygon.copy() for polygon in polygons]

def dist_p2p(p1,p2):
    return math.sqrt(sum([(p1[i]-p2[i])**2 for i in range(3)]))
