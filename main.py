import numpy as np
import pygame
import toolbox as tx

pygame.init()

screen = pygame.display.set_mode((tx.WIDTH, tx.HEIGHT))

clock = pygame.time.Clock()

# test box def BEGIN
p1 = [-1, 0, 4, 1]
p2 = [1.50, 0, 4, 1]
p3 = [1.50, 0, 3, 1]
p4 = [-1, 0, 3, 1]
p5 = [-1, 8, 4, 1]
p6 = [1.50, 8, 4, 1]
p7 = [1.50, 8, 3, 1]
p8 = [-1, 8, 3, 1]

b_test = [p1, p2, p3, p4, p5, p6, p7, p8]

# test box def END

# 1st box def 
b1 = tx.gen_box(100, 0, 250, 50, 120, 150)

# 2nd box def
b2 = tx.gen_box(-150, 0, 250, 50, 120, 150)

# 3rd box def 
b3 = tx.gen_box(-150, 0, 500, 50, 120, 150)

# 4th box def 
b4 = tx.gen_box(100, 0, 500, 50, 120, 150)

points = []
for d1 in range(250, 1001, 250):
    points += tx.gen_box(100, 0, d1, 50, 120, 150)
    points += tx.gen_box(-150, 0, d1, 50, 120, 150)

d = 1000
d_orig = 1000
md = d * -1

tx.translate_xyz(points, 0, 60, 0)

points_backup = points.copy()

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    screen.fill("white")  # Fill the display with a solid color

    # process keys

    xyz_step = 1
    deg_step = 2
    d_step = 5

    keys = pygame.key.get_pressed()
    # right/left
    if keys[pygame.K_LEFT]:
        tx.translate_xyz(points, -xyz_step, 0, 0)
    if keys[pygame.K_RIGHT]:
        tx.translate_xyz(points, xyz_step, 0, 0)
    # up/down
    if keys[pygame.K_UP]:
        tx.translate_xyz(points, 0, xyz_step, 0)
    if keys[pygame.K_DOWN]:
        tx.translate_xyz(points, 0, -xyz_step, 0)
    # fwd/bckwd
    if keys[pygame.K_PAGEUP]:
        tx.translate_xyz(points, 0, 0, xyz_step)
    if keys[pygame.K_PAGEDOWN]:
        tx.translate_xyz(points, 0, 0, -xyz_step)
    # pitch
    if keys[pygame.K_w]:
        tx.rotate_x(points, deg_step)
    if keys[pygame.K_s]:
        tx.rotate_x(points, -deg_step)
    # yaw
    if keys[pygame.K_a]:
        tx.rotate_z(points, deg_step)
    if keys[pygame.K_d]:
        tx.rotate_z(points, -deg_step)
    # roll
    if keys[pygame.K_q]:
        tx.rotate_y(points, deg_step)
    if keys[pygame.K_e]:
        tx.rotate_y(points, -deg_step)
    # zoom
    if keys[pygame.K_l] and d > 0.1:
        d -= d_step
    if keys[pygame.K_p]:
        d += d_step
    # manual change of position
    if keys[pygame.K_F2]:
        trans_x = tx.intTryParse(input("Translate X (+ right / left): "))
        trans_y = tx.intTryParse(input("Translate Y (+ up / down): "))
        trans_z = tx.intTryParse(input("Translate Z (+ fwd / bckwd):"))
        r_roll = tx.intTryParse(input("Roll rotation deg (+ CW): "))
        r_pitch = tx.intTryParse(input("Pitch rotation deg (+ UP): "))
        r_yaw = tx.intTryParse(input("Yaw rotation deg (+ LEFT): "))
        tx.translate_xyz(points, trans_x, trans_y, trans_z)
        tx.rotate_x(points, r_pitch)
        tx.rotate_y(points, r_yaw)
        tx.rotate_z(points, r_roll)
    # reset position
    if keys[pygame.K_F5]:
        points = points_backup.copy()
        d = d_orig

    proj_pts = tx.visiblity(points)

    proj_pts = tx.project_points2(proj_pts, d)

    # draw projected points
    i = 0
    for point in proj_pts:
        if point[1] == True:
            pygame.draw.circle(screen, "black", tx.to_pg_xyz(point[0])[:2], 4)
        # print(point[0][0:2], i / 2)
        i += 2

    lines = tx.gen_lines_for_box(proj_pts)

    for line in lines:
        if line[0][1] == True and line[1][1] == True:
            pygame.draw.line(screen, (255, 0, 0), tx.to_pg_xyz(line[0][0][:2]), tx.to_pg_xyz(line[1][0][:2]), 2)

    pygame.display.update()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
