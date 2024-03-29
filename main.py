import numpy as np
import pygame
import toolbox as tx

pygame.init()

screen = pygame.display.set_mode((tx.WIDTH, tx.HEIGHT))

clock = pygame.time.Clock()

# 1st box def BEGIN
p1 = [-100, 0, 400, 1]
p2 = [150, 0, 400, 1]
p3 = [150, 0, 300, 1]
p4 = [-100, 0, 300, 1]
p5 = [-100, 800, 400, 1]
p6 = [150, 800, 400, 1]
p7 = [150, 800, 300, 1]
p8 = [-100, 800, 300, 1]

b1 = [p1, p2, p3, p4, p5, p6, p7, p8]

# 1st box def END

points = b1

d = 1500
md = d * -1

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    screen.fill("white")  # Fill the display with a solid color

    # process keys

    xyz_step = 0.1
    deg_step = 1

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
    if keys[pygame.K_KP_4]:
        tx.rotate_z(points, deg_step)
    if keys[pygame.K_KP_6]:
        tx.rotate_z(points, -deg_step)
    if keys[pygame.K_KP_9]:
        tx.rotate_y(points, deg_step)
    if keys[pygame.K_KP_7]:
        tx.rotate_y(points, -deg_step)

    proj_pts = tx.project_points(points, d)

    # draw projected points
    i = 0
    for point in proj_pts:
        pygame.draw.circle(screen, "magenta", tx.to_pg_xyz(point)[:2], 2 + i)
        print(point[0:2], i / 2)
        i += 2

    lines = tx.gen_lines_for_box(proj_pts)

    for line in lines:
        pygame.draw.line(screen, (255, 0, 0), tx.to_pg_xyz(line[0][:2]), tx.to_pg_xyz(line[1][:2]))

    pygame.display.update()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
