
"""


    dessine avec ta souris,
    reconnaissance de forme
    avec tkinter choisis si svg
    fais toi plaiz
    on redissine ta forme !


"""


import cv2
import numpy as np
import math

def bresenham_march(img, p1, p2):
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        #tests if any coordinate is outside the image
        if ( 
            x1 >= img.shape[1]
            or x2 >= img.shape[1]
            or y1 >= img.shape[0]
            or y2 >= img.shape[0]
        ): #tests if line is in image, necessary because some part of the line must be inside, it respects the case that the two points are outside
            
            return

        steep = math.fabs(y2 - y1) > math.fabs(x2 - x1)
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # takes left to right
        also_steep = x1 > x2
        if also_steep:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = math.fabs(y2 - y1)
        error = 0.0
        delta_error = 0.0
        # Default if dx is zero
        if dx != 0:
            delta_error = math.fabs(dy / dx)

        y_step = 1 if y1 < y2 else -1

        y = y1
        ret = []
        for x in range(x1, x2):
            p = (y, x) if steep else (x, y)
            if p[0] < img.shape[1] and p[1] < img.shape[0]:
                ret.append(p)
            error += delta_error
            if error >= 0.5:
                y += y_step
                error -= 1
        if also_steep:  # because we took the left to right instead
            ret.reverse()
        return ret

drawing=False
mode=True

coord = []


# mouse callback function
def paint_draw(event,former_x,former_y,flags,param):
    global coord
    global current_former_x,current_former_y,drawing, mode
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        coord += [(former_x, former_y)]
        current_former_x,current_former_y=former_x,former_y
        
    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if mode==True:
                coord += [(former_x, former_y)]






                #cv2.line(image,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),5)


                current_former_x, current_former_y
                former_x, former_y

                A = (current_former_x, current_former_y)
                B = (former_x, former_y)
                

                
                # being start and end two points (x1,y1), (x2,y2)
                discrete_line = bresenham_march(image, A, B)
                if discrete_line is not None:
                    for (x, y) in discrete_line:
                        if x >= 0 and y >= 0 and x <= image.shape[1] and y <= image.shape[0]:
                            image[y][x] = (0, 0, 255)
                            coord += [(x, y)]

                current_former_x = former_x
                current_former_y = former_y
                



    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode==True:
            cv2.line(image,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),5)


            current_former_x = former_x
            current_former_y = former_y
    return former_x,former_y


def gogogo_to_svg():

    global redrawing


    counter = 0
    coucou = 10
    while True:

        if counter % 2 == 0:
            coucou += 10
        
        if coucou > len(coord) - 1:
            break

        for n in range(coucou - 10, coucou):

            x, y = coord[n]
            try:
                redrawing[y][x] = (0, 255, 0)
            except:
                pass
        counter += 1

        cv2.imshow('redrawing',redrawing)
        cv2.waitKey(1)

def gestion_click(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        
        if 10 < x < 1000 and 50 < y < 150:
            print("1")

        if 10 < x < 1000 and 200 < y < 250:
            print("2")

        if 10 < x < 1000 and 300 < y < 350:
            print("3")


        if 10< x < 1000 and 500 <y <550:
            print("4")


            gogogo_to_svg()














    cv2.putText(image_button, "line", (10, 50), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(image_button, "rectangle", (10, 200), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(image_button, "cercle", (10, 300), font, 2, (0, 0, 255), 2, cv2.LINE_AA)

if __name__ == "__main__":

    image = np.ones((760, 500, 3), np.uint8) * 255
    cv2.namedWindow("OpenCV Paint Brush")
    cv2.setMouseCallback('OpenCV Paint Brush',paint_draw)


    image_button = np.ones((760, 500, 3), np.uint8) * 255
    cv2.namedWindow("OpenCV Paint dzada")
    cv2.setMouseCallback('OpenCV Paint dzada', gestion_click)

    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(image_button, "line", (10, 50), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(image_button, "rectangle", (10, 200), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(image_button, "cercle", (10, 300), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(image_button, "svg", (10, 500), font, 2, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.rectangle(image_button, (10, 50), (1000, 100), (0, 255, 0), 1)
    cv2.rectangle(image_button, (10, 200), (1000, 250), (0, 255, 0), 1)
    cv2.rectangle(image_button, (10, 300), (1000, 350), (0, 255, 0), 1)
    cv2.rectangle(image_button, (10, 500), (1000, 550), (0, 255, 0), 1)

    redrawing = np.ones((760, 500, 3), np.uint8) * 255

    while(1):
        cv2.imshow('OpenCV Paint Brush',image)
        cv2.imshow('OpenCV Paint dzada',image_button)
        cv2.imshow('redrawing',redrawing)






        k=cv2.waitKey(1)& 0xFF
        if k==27: #Escape KEY
            break


        cv2.imwrite(r"C:\Users\jb264\OneDrive\Bureau\modules\interface\animation\u_drawing\a.jpg",image)



    cv2.destroyAllWindows()

