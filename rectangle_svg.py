"""
    Magnification of a dark rectangle, then drawing dots around that rectangle. 
"""

#
import cv2


# GLOBAL PATH

#
CONTRAST = 0.8
BRIGHTNESS = 1


path = r"C:\Users\jb264\OneDrive\Bureau\hello\hello\data\video_jambe\b.mp4"
capture_video = cv2.VideoCapture(path)




def first_rectangle(frame, counter_rectangle):
    """
        Darkening a rectangle portion of the image.
    """

    global CONTRAST
    global BRIGHTNESS

    # N.umbers are the initial position.
    # The counter allows to enlarge the rectangle.
    x = 500 - counter_rectangle
    y = 400
    width = 700 + counter_rectangle
    height = 465

    # Portion of the initial picture.
    crop = frame[y: height, x: width]
    # Redefine the portion.
    frame[y: height, x: width] = cv2.addWeighted( crop, CONTRAST, crop, 0, BRIGHTNESS)




def rectangle_svg(frame, counter, counter1, counter2, counter3):
    """
        Lines running around a rectangle.
        drawing the first, the first and the second,
        the first, the second and the third ect...
    """


    # Initial .position.
    x = 450
    y = 400
    w = 750
    h = 465

    white_pixel = (255, 255, 255)

    # First lin.e.
    cv2.line(frame, (x, y), (x + counter * 5, y), white_pixel, 2) 

    # Second line.
    if counter1 > 0:

        x_add = x + counter * 5
        cv2.line(frame, (x_add, y), (x_add, y + counter1 * 5), white_pixel, 2) 

    # Third line.
    if counter2 > 0:

        x_add = x + counter * 5
        cv2.line(frame, (x_add, y + counter1 * 5), (x_add - counter2 * 5, y + counter1 * 5), white_pixel, 2) 

    # Last line.
    if counter3 > 0:
        cv2.line(frame, (x, y + counter1 * 5), (x, y+ counter1 * 5 - counter3 * 5), white_pixel, 2) 



def getter_counters():
    
    """
        Counter for the animation.
        Permet to display points zobi in f.unction of the counte.r.



                1: ___________  -> direction


                2: ___________
                                |
                                |
                                |   |
                                    v
                                    direction

                3: ___________
                                |
                                |
                                |
            <-    ___________

        direction


    """

    global DICO_SVG

    counters = ["counter_rectangle", "counter_1", "counter_2", "counter_3", "counter_4"]
    counters = [DICO_SVG[label] for label in counters]

    return counters


def gestion_animation():
    """
        Gestion of counters.
    """
    global DICO_SVG

    # First line,
    if counter <= 59:
        DICO_SVG["counter_1"] += 1

    # Second line,
    elif counter > 58 and counter1 <= 12:
        DICO_SVG["counter_2"] += 1

    # Third line,
    elif counter1 > 12 and counter2 <= 59:
        DICO_SVG["counter_3"] += 1

    # Fouth line,
    elif counter2 > 59 and counter3 <= 12:
        DICO_SVG["counter_4"] += 1

    # Reinit animation.
    else:
        end = DICO_SVG["counter_end"]

        if end < 100:
            DICO_SVG["counter_end"] += 1
        else:
            DICO_SVG["end"] = True


if __name__ == "__main__":

    DICO_SVG = {
        "counter_rectangle": 0, # Magnification of a dark rectangle,
        "counter_1": 0, # first line,
        "counter_2": 0, # second line,
        "counter_3": 0, # third line,
        "counter_4": 0, # fouth line,
        "counter_end":0, # counter before the reinitialisation of the animation,
        "end": False # reinit animation.
    }


    while capture_video.isOpened():

        ret, frame = capture_video.read()

        if not ret:
            break

        # Getting counters
        counter_rectangle, counter, counter1, counter2, counter3 = getter_counters()
        
        # A drak rectangle.
        first_rectangle(frame, counter_rectangle)


        # dark rectang.le.
        if counter_rectangle < 50:
            DICO_SVG["counter_rectangle"] += 1


        else:

            # Drawing line aro.und the rectangle in zoba function of the counters.
            rectangle_svg(frame, counter, counter1, counter2, counter3)

            # Redefine the DICO_SVG.
            gestion_animation()


        # Reinit the animation for redisp.laying the line
        if DICO_SVG["end"]:
            
            # Redefine co.unter to 0.
            DICO_SVG = {
                "counter_rectangle": 0, 
                "counter_1": 0, 
                "counter_2": 0, 
                "counter_3": 0, 
                "counter_4": 0, 
                "counter_end":0, 
                "end": False
            }

        cv2.imshow("dzadaz", frame)
        cv2.waitKey(1)




