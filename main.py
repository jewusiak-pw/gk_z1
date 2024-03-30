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

# 1st box def BEGIN
p1 = [0.11, 0, 0.4, 1]
p2 = [0.11, 0, 0, 1]
p3 = [0.253, 0, 0, 1]
p4 = [0.253, 0, 0.4, 1]
p5 = [0.11, 0.3, 0.4, 1]
p6 = [0.11, 0.3, 0, 1]
p7 = [0.253, 0.3, 0, 1]
p8 = [0.253, 0.3, 0.4, 1]

b1 = [p1, p2, p3, p4, p5, p6, p7, p8]

# 1st box def END

# 2nd box def BEGIN
p1 = [-0.11, 0, 0.4, 1]
p2 = [-0.11, 0, 0, 1]
p3 = [-0.253, 0, 0, 1]
p4 = [-0.253, 0, 0.4, 1]
p5 = [-0.11, 0.2, 0.4, 1]
p6 = [-0.11, 0.2, 0, 1]
p7 = [-0.253, 0.2, 0, 1]
p8 = [-0.253, 0.2, 0.4, 1]

b2 = [p1, p2, p3, p4, p5, p6, p7, p8]

# 2nd box def END

# 3rd box def BEGIN
p1 = [-0.11, 0, 1, 1]
p2 = [-0.11, 0, 0.6, 1]
p3 = [-0.253, 0, 0.6, 1]
p4 = [-0.253, 0, 1, 1]
p5 = [-0.11, 0.6, 1, 1]
p6 = [-0.11, 0.6, 0.6, 1]
p7 = [-0.253, 0.6, 0.6, 1]
p8 = [-0.253, 0.6, 1, 1]

b3 = [p1, p2, p3, p4, p5, p6, p7, p8]

# 3rd box def END

# 4th box def BEGIN
p1 = [0.11, 0, 1, 1]
p2 = [0.11, 0, 0.6, 1]
p3 = [0.253, 0, 0.6, 1]
p4 = [0.253, 0, 1, 1]
p5 = [0.11, 0.3, 1, 1]
p6 = [0.11, 0.3, 0.6, 1]
p7 = [0.253, 0.3, 0.6, 1]
p8 = [0.253, 0.3, 1, 1]

b4 = [p1, p2, p3, p4, p5, p6, p7, p8]

# 4th box def END


points = b1 + b2 + b3 + b4

d = 3
md = d * -1

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    screen.fill("white")  # Fill the display with a solid color

    # process keys

    xyz_step = 0.01
    deg_step = 3

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tx.translate_xyz(points, -xyz_step, 0, 0)
    if keys[pygame.K_RIGHT]:
        tx.translate_xyz(points, xyz_step, 0, 0)
    if keys[pygame.K_UP]:
        tx.translate_xyz(points, 0, xyz_step, 0)
    if keys[pygame.K_DOWN]:
        tx.translate_xyz(points, 0, -xyz_step, 0)
    if keys[pygame.K_PAGEUP]:
        tx.translate_xyz(points, 0, 0, xyz_step)
    if keys[pygame.K_PAGEDOWN]:
        tx.translate_xyz(points, 0, 0, -xyz_step)
    if keys[pygame.K_KP_8]:
        tx.rotate_x(points, deg_step)
    if keys[pygame.K_KP_2]:
        tx.rotate_x(points, -deg_step)
    if keys[pygame.K_KP_6]:
        tx.rotate_z(points, deg_step)
    if keys[pygame.K_KP_4]:
        tx.rotate_z(points, -deg_step)
    if keys[pygame.K_KP_7]:
        tx.rotate_y(points, deg_step)
    if keys[pygame.K_KP_9]:
        tx.rotate_y(points, -deg_step)

    proj_pts = tx.visiblity(points)

    proj_pts = tx.project_points2(proj_pts, d)

    # draw projected points
    i = 0
    for point in proj_pts:
        if point[1] == True:
            pygame.draw.circle(screen, "black", tx.to_pg_xyz(point[0])[:2], 4)
        print(point[0][0:2], i / 2)
        i += 2

    lines = tx.gen_lines_for_box(proj_pts)

    for line in lines:
        if line[0][1] == True and line[1][1] == True:
            pygame.draw.line(screen, (255, 0, 0), tx.to_pg_xyz(line[0][0][:2]), tx.to_pg_xyz(line[1][0][:2]), 2)

    pygame.display.update()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
