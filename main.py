import time

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

box_borders_untouch = False

# test box def END

# 1st box def 
b1 = tx.gen_box(100, 0, 250, 50, 120, 150, box_borders_untouch)

# 2nd box def
b2 = tx.gen_box(-150, 0, 250, 50, 120, 150, box_borders_untouch)

# 3rd box def 
b3 = tx.gen_box(-150, 0, 500, 50, 120, 150, box_borders_untouch)

# 4th box def 
b4 = tx.gen_box(100, 0, 500, 50, 120, 150, box_borders_untouch)

polygons = []
polygons_untouching = []
for d1 in range(250, 1001, 250):
    polygons_untouching += tx.gen_box(100, 0, d1, 50, 120, 150, True)
    polygons_untouching += tx.gen_box(-150, 0, d1, 50, 120, 150, True)
    polygons += tx.gen_box(100, 0, d1, 50, 120, 150, False)
    polygons += tx.gen_box(-150, 0, d1, 50, 120, 150, False)

d = 1000
d_orig = 1000
md = d * -1

tx.translate_xyz(polygons, 0, 60, 0)
tx.translate_xyz(polygons_untouching, 0, 60, 0)

polygons_backup = tx.deep_copy(polygons)
polygons_unt_backup = tx.deep_copy(polygons_untouching)
if box_borders_untouch:
    polygons = tx.deep_copy(polygons_unt_backup)

walls_enabled = True

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
        tx.translate_xyz(polygons, -xyz_step, 0, 0)
    if keys[pygame.K_RIGHT]:
        tx.translate_xyz(polygons, xyz_step, 0, 0)
    # up/down
    if keys[pygame.K_UP]:
        tx.translate_xyz(polygons, 0, xyz_step, 0)
    if keys[pygame.K_DOWN]:
        tx.translate_xyz(polygons, 0, -xyz_step, 0)
    # fwd/bckwd
    if keys[pygame.K_PAGEUP]:
        tx.translate_xyz(polygons, 0, 0, xyz_step)
    if keys[pygame.K_PAGEDOWN]:
        tx.translate_xyz(polygons, 0, 0, -xyz_step)
    # pitch
    if keys[pygame.K_w]:
        tx.rotate_x(polygons, deg_step)
    if keys[pygame.K_s]:
        tx.rotate_x(polygons, -deg_step)
    # yaw
    if keys[pygame.K_a]:
        tx.rotate_z(polygons, deg_step)
    if keys[pygame.K_d]:
        tx.rotate_z(polygons, -deg_step)
    # roll
    if keys[pygame.K_q]:
        tx.rotate_y(polygons, deg_step)
    if keys[pygame.K_e]:
        tx.rotate_y(polygons, -deg_step)
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
        tx.translate_xyz(polygons, trans_x, trans_y, trans_z)
        tx.rotate_x(polygons, r_pitch)
        tx.rotate_y(polygons, r_yaw)
        tx.rotate_z(polygons, r_roll)
    # reset position
    if keys[pygame.K_F5]:
        polygons = tx.deep_copy(polygons_backup)
        d = d_orig
    # toggle walls
    if keys[pygame.K_F6]:
        walls_enabled = not walls_enabled
        time.sleep(0.1)
    # toggle box borders
    if keys[pygame.K_F7]:
        box_borders_untouch = not box_borders_untouch
        polygons = tx.deep_copy(polygons_unt_backup if box_borders_untouch else  polygons_backup)
        time.sleep(0.1)



    # sprawdzenie widoczności z>0
    proj_polygons = tx.visiblity(polygons)

    # nie projektujemy ścian niewidocznych (tylnich)
    proj_polygons = tx.hide_hidden(proj_polygons, [0,0,0])

    # sortowanie po odległości od obserwatora
    proj_polygons.sort(key=tx.calc_dist, reverse=True)

    # projekcja
    proj_polygons = tx.project_points2(proj_polygons, d)

    # draw projected points
    for polygon in proj_polygons:
        for point in polygon:
            if point['visibility'] == True:
                pygame.draw.circle(screen, "black", tx.to_pg_xyz(point['point'])[:2], 4)

    # draw polygons
    for polygon in proj_polygons:
        if sum([(1 if point['visibility'] == True else 0) for point in polygon]) == 4:
            if walls_enabled:
                pygame.draw.polygon(screen, "white", [tx.to_pg_xyz(point['point'][:2]) for point in polygon], 0)
            pygame.draw.polygon(screen, "black", [tx.to_pg_xyz(point['point'][:2]) for point in polygon], 2)


    pygame.display.update()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
