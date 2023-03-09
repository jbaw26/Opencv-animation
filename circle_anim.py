import numpy as np
import cv2
import math



img = np.ones((760, 1500, 3), np.uint8) * 255




#############################################################################################################
circ_center = (200,200)
circ_radius = 150
circ_thick  = 12

def draw_arc(img, center, rad, angle, startAngle, endAngle, color, thickness, lineType, thick=1):
    for r in range(rad,rad + thickness):
        cv2.ellipse(img, center, (r, r), angle, startAngle, endAngle, color, thick, lineType)

def make_it_tourner(img, n):

    draw_arc(img, circ_center, circ_radius, 0, 0, 360, (0, 255, 0), circ_thick, cv2.LINE_AA)

    draw_arc(img, circ_center, circ_radius, 0,    0 + n,  50 + n, (255, 0, 0), circ_thick, cv2.LINE_AA)
    draw_arc(img, circ_center, circ_radius, 0,    100 + n, 150 + n, (0, 0, 0), circ_thick, cv2.LINE_AA)
    draw_arc(img, circ_center, circ_radius, 0,    200 + n, 250 + n, (0, 0, 0), circ_thick, cv2.LINE_AA)


###############################################################################################################


draw_arc(img, (600, 200), 145, 0, 0, 360, (242, 227, 243), 12, cv2.LINE_AA)
for n in range(0, 1200, 100):
    x = round(600 + circ_radius*math.cos(n))
    y = round(200 + circ_radius*math.sin(n))
    cv2.circle(img, (x , y), 5, (0, 0, 255), -1)








cv2.circle(img, (200, 600), 50, (255, 0, 0), 10)










n = 0
to_raise = 0
to_add = 0
while True:



    make_it_tourner(img, n)



    if 120 - to_raise > 5:
        cv2.circle(img, (900 , 200), 120 - to_raise, (0, 0, 255), 8)
    else:
        to_raise = 0







    if to_add < 50:
        cv2.circle(img, (1200 , 200), to_add, (0, 0, 255), 8)
    
    else:
        to_add = 0







    cv2.imshow("dazdaz", img)
    cv2.waitKey(1)


    if 120 - to_raise > 5:
        cv2.circle(img, (900 , 200), 120 - to_raise, (255, 255, 255), 8)


    if to_add < 50:
        cv2.circle(img, (1200 , 200), to_add, (255, 255, 255), 8)







    n += 1

    if n % 5 == 0:
        to_raise += 1

    if n % 5 == 0:
        to_add += 1









