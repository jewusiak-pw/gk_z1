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

box_borders_untouch = True

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
# polygons_untouching += tx.gen_box(-50, 25, 150, 150, 10, 150, True)
# polygons_untouching += tx.gen_box(-50, 0, 100, 150, 10, 150, True)
# polygons += tx.gen_box(100, 0, d1, 50, 120, 150, False)
# polygons += tx.gen_box(-150, 0, d1, 50, 120, 150, False)

for d1 in range(250, 501, 250):
    polygons_untouching += tx.gen_box(100, 0, d1, 50, 120, 150, True)
    polygons_untouching += tx.gen_box(-150, 0, d1, 50, 120, 150, True)
    polygons += tx.gen_box(100, 0, d1, 50, 120, 150, False)
    polygons += tx.gen_box(-150, 0, d1, 50, 120, 150, False)

d = 1000
d_orig = 1000
md = d * -1

tx.translate_xyz(polygons, 0, 60, 0)
tx.translate_xyz(polygons_untouching, 0, 60, 0)

coords = [0,0,0,0,0,0]

# polygons = tx.div_polygons(polygons, 2)
polygons_untouching = tx.div_polygons(polygons_untouching, 2)

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
    chg = [0, 0, 0, 0, 0, 0]
    # right/left
    if keys[pygame.K_LEFT]:
        chg[0] -= xyz_step
    if keys[pygame.K_RIGHT]:
        chg[0] += xyz_step
    # up/down
    if keys[pygame.K_UP]:
        chg[1] += xyz_step
    if keys[pygame.K_DOWN]:
        chg[1] -= xyz_step
    # fwd/bckwd
    if keys[pygame.K_PAGEUP]:
        chg[2] += xyz_step
    if keys[pygame.K_PAGEDOWN]:
        chg[2] -= xyz_step
    # roll
    if keys[pygame.K_a]:
        chg[3] -= deg_step
    if keys[pygame.K_d]:
        chg[3] += deg_step
    # pitch
    if keys[pygame.K_w]:
        chg[4] += deg_step
    if keys[pygame.K_s]:
        chg[4] -= deg_step    
    # yaw
    if keys[pygame.K_q]:
        chg[5] += deg_step
    if keys[pygame.K_e]:
        chg[5] -= deg_step
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
        chg = [trans_x, trans_y, trans_z, r_roll, r_pitch, r_yaw]
    # print loc
    if keys[pygame.K_F3]:
        print('location (x,y,z):', *coords[:3])
        print('location (roll, pitch, yaw):', *coords[3:6])
        time.sleep(0.1)
    # reset position
    if keys[pygame.K_F5]:
        polygons = tx.deep_copy(polygons_backup)
        d = d_orig
        coords = [0,0,0,0,0,0]
    # toggle walls
    if keys[pygame.K_F6]:
        walls_enabled = not walls_enabled
        time.sleep(0.1)
    # toggle box borders
    if keys[pygame.K_F7]:
        box_borders_untouch = not box_borders_untouch
        polygons = tx.deep_copy(polygons_unt_backup if box_borders_untouch else polygons_backup)
        time.sleep(0.1)

    # make changes
    if len(list(filter(lambda x: x != 0, chg))) != 0:
        tx.translate_xyz(polygons, *chg[:3])
        tx.rotate_z(polygons, chg[3])
        tx.rotate_x(polygons, chg[4])
        tx.rotate_y(polygons, chg[5])
        coords = [coords[i]+chg[i] for i in range(len(chg))]

    # sprawdzenie widoczności z>0
    proj_polygons = tx.visiblity(polygons)

    # nie projektujemy ścian niewidocznych (tylnich)
    # proj_polygons = tx.hide_hidden(proj_polygons, [0, 0, 0])

    # sortowanie po odległości od obserwatora
    # proj_polygons.sort(key=tx.calc_dist, reverse=True)
    proj_polygons.sort(key=tx.calc_dist_middlepoints, reverse=True)

    # projekcja
    proj_polygons = tx.project_points2(proj_polygons, d)

    # draw projected points
    # for polygon in proj_polygons:
    #     for point in polygon:
    #         if point['visibility'] == True:
    #             pygame.draw.circle(screen, "black", tx.to_pg_xyz(point['point'])[:2], 4)

    # draw polygons
    for polygon in proj_polygons:
        if sum([(1 if point['visibility'] == True else 0) for point in polygon]) == len(polygon) or True:
            if walls_enabled:
                pygame.draw.polygon(screen, "white", [tx.to_pg_xyz(point['point'][:2]) for point in polygon], 0)
            pygame.draw.polygon(screen, "black", [tx.to_pg_xyz(point['point'][:2]) for point in polygon], 2)

    pygame.display.update()  # Refresh on-screen display
    # clock.tick(240)  # wait until next frame (at 60 FPS)
