import numpy as np
import math
from shapely import Point, Polygon

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
    for i in range(len(polygons)):
        for j in range(len(polygons[i])):
            polygons[i][j] = np.dot(tm, polygons[i][j]).tolist()[0]


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
def gen_box(x, y, z, x_l, y_l, z_l, box_borders_untouch):
    diff_margin = 0.05 if box_borders_untouch else 0
    p1 = [x, y, z, 1]
    p2 = [x + x_l, y, z, 1]
    p3 = [x + x_l, y, z + z_l, 1]
    p4 = [x, y, z + z_l, 1]
    p5 = [x, y + y_l, z, 1]
    p6 = [x + x_l, y + y_l, z, 1]
    p7 = [x + x_l, y + y_l, z + z_l, 1]
    p8 = [x, y + y_l, z + z_l, 1]

    s_btm = md([p1, p2, p3, p4], 0, -diff_margin,0)
    s_top = md([p5, p6, p7, p8], 0, diff_margin, 0)
    s_fwd = md([p4, p3, p7, p8], 0, 0, diff_margin)
    s_bck = md([p1, p2, p6, p5], 0, 0, -diff_margin)
    s_left = md([p1, p4, p8, p5], -diff_margin, 0, 0)
    s_right = md([p2, p3, p7, p6], diff_margin, 0, 0)

    return [s_btm, s_top, s_fwd, s_bck, s_left, s_right]

def md(ps,x,y,z):
    return [[p[0]+x, p[1]+y, p[2]+z, *p[3:]] for p in ps]


def intTryParse(value) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def is_in_polygon(proj_cam, poly_pts):
    oxz_plane = [[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1]]

    poly_proj_pts = [project_point_onto_plane(pp, oxz_plane) for pp in poly_pts]
    poly_proj_pts = [[p[0], p[2]] for p in poly_proj_pts]
    [oxz_cam_pos_x, _, oxz_cam_pos_z] = project_point_onto_plane(proj_cam, oxz_plane)
    oxz_cam_pos = [oxz_cam_pos_x, oxz_cam_pos_z]

    poly = Polygon(poly_proj_pts)
    poi = Point(oxz_cam_pos)

    return poly.contains(poi)


def isbtw(a, b, c):
    return a <= b and b <= c;


def plane_point_dist(cam_xyz, poly_pts):
    [a, b, c, d] = equation_plane(*poly_pts[:3])
    [x, y, z] = cam_xyz[:3]
    top = abs(a * x + b * y + c * z + d)
    btm = math.sqrt(a * a + b * b + c * c)
    return top / btm


def line_point_dist(line_points, point):
    a = lineseg_dist(point, line_points[0], line_points[1])
    return a


def lineseg_dist(p, a, b):
    p = np.array(p)
    a = np.array(a)
    b = np.array(b)

    # normalized tangent vector
    d = np.divide(b - a, np.linalg.norm(b - a))

    # signed parallel distance components
    s = np.dot(a - p, d)
    t = np.dot(p - b, d)

    # clamped parallel distance
    h = np.maximum.reduce([s, t, 0])

    # perpendicular distance component
    c = np.cross(p - a, d)

    return np.hypot(h, np.linalg.norm(c))


def poly_border_point_dist(cam_xyz, poly_pts):
    points_dists = [dist_p2p(cam_xyz, p) for p in poly_pts]
    lines_dists = [line_point_dist([poly_pts[i], poly_pts[i + 1]], cam_xyz) for i in range(len(poly_pts) - 1)]
    lines_dists.append(line_point_dist([poly_pts[0], poly_pts[-1]], cam_xyz))
    points_dists += lines_dists
    return min(points_dists)


def dist_p2p(p1, p2):
    return math.sqrt(sum([(p1[i] - p2[i]) ** 2 for i in range(3)]))


def calc_dist(polygon):
    cam_xyz = [0, 0, 0]
    poly_pts = [point['point'][:3] for point in polygon]

    proj_cam = project_point_onto_plane(cam_xyz, poly_pts)

    if is_in_polygon(proj_cam, poly_pts):
        # use perpendicular to plane
        return plane_point_dist(cam_xyz, poly_pts)
    else:
        # use dist to poly
        return poly_border_point_dist(cam_xyz, poly_pts)


def deep_copy(polygons):
    return [polygon.copy() for polygon in polygons]


def equation_plane(p1, p2, p3):
    [x1, y1, z1] = p1
    [x2, y2, z2] = p2
    [x3, y3, z3] = p3
    a1 = x2 - x1
    b1 = y2 - y1
    c1 = z2 - z1
    a2 = x3 - x1
    b2 = y3 - y1
    c2 = z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * x1 - b * y1 - c * z1)
    return (a, b, c, d)


def project_point_onto_plane(point, plane_pts):
    v1 = (plane_pts[1][0] - plane_pts[0][0], plane_pts[1][1] - plane_pts[0][1], plane_pts[1][2] - plane_pts[0][2])
    v2 = (plane_pts[2][0] - plane_pts[0][0], plane_pts[2][1] - plane_pts[0][1], plane_pts[2][2] - plane_pts[0][2])
    [a, b, c] = np.cross(v1, v2).tolist()
    [d, e, f] = plane_pts[0][:3]
    [x, y, z] = point
    t = (a * d - a * x + b * e - b * y + c * f - c * z) / (a ** 2 + b ** 2 + c ** 2)
    return [x + t * a, y + t * b, z + t * c]
