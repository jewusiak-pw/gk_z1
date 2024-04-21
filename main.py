import time

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
for d1 in range(250, 1001, 250):
    polygons += tx.gen_box(100, 0, d1, 50, 120, 150, box_borders_untouch)
    polygons += tx.gen_box(-150, 0, d1, 50, 120, 150, box_borders_untouch)

d = 1000
d_orig = 1000
md = d * -1

# tx.translate_xyz(polygons, 0, 60, 0)

polygons_backup = tx.deep_copy(polygons)

walls_enabled = True

act_pos = [0, 60, 0, 0, 0, 0]
pos_backup = [0, 60, 0, 0, 0, 0]

proj = True
altern_enabled = True


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
        act_pos[0] = act_pos[0] - xyz_step
        proj = True
    if keys[pygame.K_RIGHT]:
        tx.translate_xyz(polygons, xyz_step, 0, 0)
        act_pos[0] = act_pos[0] + xyz_step
        proj = True
    # up/down
    if keys[pygame.K_UP]:
        tx.translate_xyz(polygons, 0, xyz_step, 0)
        act_pos[1] = act_pos[1] + xyz_step
        proj = True
    if keys[pygame.K_DOWN]:
        tx.translate_xyz(polygons, 0, -xyz_step, 0)
        act_pos[1] = act_pos[1] - xyz_step
        proj = True
    # fwd/bckwd
    if keys[pygame.K_PAGEUP]:
        tx.translate_xyz(polygons, 0, 0, xyz_step)
        act_pos[2] = act_pos[2] + xyz_step
        proj = True
    if keys[pygame.K_PAGEDOWN]:
        tx.translate_xyz(polygons, 0, 0, -xyz_step)
        act_pos[2] = act_pos[2] - xyz_step
        proj = True
    # pitch
    if keys[pygame.K_w]:
        tx.rotate_x(polygons, deg_step)
        act_pos[4] = act_pos[4] + deg_step
        proj = True
    if keys[pygame.K_s]:
        tx.rotate_x(polygons, -deg_step)
        act_pos[4] = act_pos[4] - deg_step
        proj = True
    # yaw
    if keys[pygame.K_a]:
        tx.rotate_z(polygons, deg_step)
        act_pos[5] = act_pos[5] + deg_step
        proj = True
    if keys[pygame.K_d]:
        tx.rotate_z(polygons, -deg_step)
        act_pos[5] = act_pos[5] - deg_step
        proj = True
    # roll
    if keys[pygame.K_q]:
        tx.rotate_y(polygons, deg_step)
        act_pos[3] = act_pos[3] + deg_step
        proj = True
    if keys[pygame.K_e]:
        tx.rotate_y(polygons, -deg_step)
        act_pos[3] = act_pos[3] - deg_step
        proj = True
    # zoom
    if keys[pygame.K_l] and d > 0.1:
        d -= d_step
        proj = True
    if keys[pygame.K_p]:
        d += d_step
        proj = True
    if keys[pygame.K_F3]:
        print("act pos (x,y,z):", act_pos[:3])
        print("act pos (roll, pitch, yaw):", act_pos[3:])
        print("act zoom:", d)

        p1 = [-125, 0, 325]
        p2 = [-100, 60, 325]
        dp1 = tx.dist_p2p(p1, act_pos)
        dp2 = tx.dist_p2p(p2, act_pos)

        print('dist btm', p1, ' d =', dp1, ' dist right', p2, ' d =', dp2, ' is the moment?', dp1 < dp2)

        time.sleep(0.1)
    # manual change of position
    if keys[pygame.K_F2]:
        time.sleep(0.1)
        trans_x = tx.intTryParse(input("Translate X (+ right / left): "))
        trans_y = tx.intTryParse(input("Translate Y (+ up / down): "))
        trans_z = tx.intTryParse(input("Translate Z (+ fwd / bckwd):"))
        r_roll = tx.intTryParse(input("Roll rotation deg (+ CW): "))
        r_pitch = tx.intTryParse(input("Pitch rotation deg (+ UP): "))
        r_yaw = tx.intTryParse(input("Yaw rotation deg (+ LEFT): "))
        # tx.translate_xyz(polygons, trans_x, trans_y, trans_z)
        tx.rotate_x(polygons, r_pitch)
        tx.rotate_y(polygons, r_yaw)
        tx.rotate_z(polygons, r_roll)
        txs = [trans_x, trans_y, trans_z, r_roll, r_pitch, r_yaw]
        act_pos = [(act_pos[i] + txs[i]) for i in range(len(act_pos))]
        proj = True
    # reset position
    if keys[pygame.K_F5]:
        act_pos = pos_backup.copy()
        polygons = tx.deep_copy(polygons_backup)
        d = d_orig
        proj = True
    # toggle walls
    if keys[pygame.K_F6]:
        walls_enabled = not walls_enabled
        proj = True
        time.sleep(0.1)
    # toggle alternative sort
    if keys[pygame.K_F7]:
        altern_enabled = not altern_enabled
        proj = True
        time.sleep(0.1)

    if proj or True:
        proj_polygons = tx.visiblity(polygons)
        ref_pos = [0,0,0] # act_pos[:3]
        if walls_enabled:
            # sorted_p = list(zip(proj_polygons, [ [{"point" : pbb, 'visibility': True} for pbb in pb] for pb in polygons_backup]))
            # sorted_p.sort(key=lambda p: tx.calc_dist(p[1], ref_pos, altern_enabled), reverse=True)
            # proj_polygons = [sp[0] for sp in sorted_p] 
            proj_polygons.sort(key=lambda p: tx.calc_dist(p, ref_pos, altern_enabled), reverse=True)

        # tx.translate_xyz(proj_polygons, act_pos[0], act_pos[1], act_pos[2])
        # tx.rotate_z(proj_polygons, act_pos[3])
        # tx.rotate_x(proj_polygons, act_pos[4])
        # tx.rotate_y(proj_polygons, act_pos[5])

        proj_polygons = tx.project_points2(proj_polygons, d)

        # draw projected points
        # for polygon in proj_polygons:
        #     for point in polygon:
        #         if point['visibility'] == True:
        #             pygame.draw.circle(screen, "black", tx.to_pg_xyz(point['point'])[:2], 4)

        # draw polygons
        for polygon in proj_polygons:
            if sum([(1 if point['visibility'] == True else 0) for point in polygon]) == 4:
                if walls_enabled:
                    pygame.draw.polygon(screen, "white", [tx.to_pg_xyz(point['point'][:2]) for point in polygon], 0)
                pygame.draw.polygon(screen, "black", [tx.to_pg_xyz(point['point'][:2]) for point in polygon], 2)

        pygame.display.update()  # Refresh on-screen display
        proj = False
        # polygons = tx.deep_copy(polygons_backup)
    clock.tick(60)  # wait until next frame (at 60 FPS)
