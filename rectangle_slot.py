
import cv2
import numpy as np



def side_right(frame, x, y, counter):

    length_verti = 40
    length_hori = 65

    cv2.line(frame, (x + counter, y), (x + counter + length_verti, y), (255, 255, 255), 2) # verticale
    cv2.line(frame, (x + counter, y), (x + counter, y + length_hori), (255, 255, 255), 2) # horizontale

    max_x = x + counter + length_verti

    return frame, max_x


def side_left(frame, x, y, counter):

    length_verti = 40
    length_hori = 65

    cv2.line(frame, (x - counter - length_verti, y), (x - counter, y), (255, 255, 255), 2) # verticale
    cv2.line(frame, (x - counter, y), (x - counter, y - length_hori), (255, 255, 255), 2) # horizontale

    min_x = x - counter

    return frame, min_x



def display_first_rectangle(frame, dico_display):

    counter_rectangle = dico_display["rectangle"]["counter"]
    first_animation = dico_display["rectangle"]["first_animation"]


    if first_animation:

        frame, max_x = side_right(frame, 500, 400, counter_rectangle)
        frame, min_x = side_left(frame, 700, 465, counter_rectangle)

        if max_x == min_x:
            dico_display["rectangle"]["first_animation"] = False

        dico_display["rectangle"]["counter"] += 1



    else:
        counter_pause = dico_display["rectangle"]["pause_first_animation"]
        seoncd_anim = dico_display["rectangle"]["second_animation"]
        first_animation = dico_display["rectangle"]["first_animation"]

        if counter_pause == 5 and not seoncd_anim:
            dico_display["rectangle"]["second_animation"] = True
            dico_display["rectangle"]["counter"] = 0

        elif counter_pause != 5 and not seoncd_anim and not first_animation:
            dico_display["rectangle"]["pause_first_animation"] += 1
            frame, max_x = side_right(frame, 500, 400, counter_rectangle)
            frame, min_x = side_left(frame, 700, 465, counter_rectangle)


def side_right_1(frame, x, y, counter):

    length_verti = 40
    length_hori = 65

    cv2.line(frame, (x + counter, y), (x + counter + length_verti, y), (255, 255, 255), 2) # verticale
    cv2.line(frame, (x + counter, y + length_hori), (x + counter + length_verti, y + length_hori), (255, 255, 255), 2)

    cv2.line(frame, (x + counter, y), (x + counter, y + length_hori), (255, 255, 255), 2) # horizontale


    max_x = x + counter + length_verti

    return frame, max_x


def side_left_1(frame, x, y, counter):

    length_verti = 40
    length_hori = 65

    cv2.line(frame, (x - counter - length_verti, y), (x - counter, y), (255, 255, 255), 2) # verticale
    cv2.line(frame, (x - counter - length_verti, y - length_hori), (x - counter, y - length_hori), (255, 255, 255), 2) # verticale

    cv2.line(frame, (x - counter, y), (x - counter, y - length_hori), (255, 255, 255), 2) # horizontale

    min_x = x - counter

    return frame, min_x



def display_second_rectangle(frame, dico_display):

    second_animation = dico_display["rectangle"]["second_animation"]

    if second_animation:

        counter_rectangle = dico_display["rectangle"]["counter"]

        contrast = 0.8
        brightness = 1
        crop = frame[400: 465, 500 + counter_rectangle: 700 - counter_rectangle]
        frame[400: 465, 500 + counter_rectangle: 700 - counter_rectangle] = cv2.addWeighted( crop, contrast, crop, 0, brightness)

        if counter_rectangle >= -50:

            frame, max_x = side_right_1(frame, 500, 400, counter_rectangle)
            frame, min_x = side_left_1(frame, 700, 465, counter_rectangle)

            dico_display["rectangle"]["counter"] -= 1

        else:

            frame, max_x = side_right_1(frame, 500, 400, counter_rectangle)
            frame, min_x = side_left_1(frame, 700, 465, counter_rectangle)

            dico_display["rectangle"]["end"] = True


def main(dico_display):

    while True:

        frame = 100 * np.ones((820, 2080, 3), np.uint8)

        display_first_rectangle(frame, dico_display)
        display_second_rectangle(frame, dico_display)


        if dico_display["rectangle"]["end"] is True:


            counter = dico_display["rectangle"]["counter_end"]
            
            if counter > 100:

                dico_display = {
                    "rectangle":{
                        "counter": 0, "first_animation": True, "end_first_animation": False,
                        "pause_first_animation": 0, "second_animation": False, "counter_third": 0,
                        "end": False, "counter_end": 0
                    }
                }

            dico_display["rectangle"]["counter_end"] += 1

        cv2.imshow("dzadaz", frame)
        cv2.waitKey(1)


if __name__ == "__main__":


    dico_display = {
        "rectangle":{
            "counter": 0, "first_animation": True, "end_first_animation": False,
            "pause_first_animation": 0, "second_animation": False, "counter_third": 0,
            "end": False, "counter_end": 0
        }
    }


    main(dico_display)
