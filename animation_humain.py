
"""
    With opencv,
    1) read a picture,
    2) display a picture,
    3) blit on a picture,
    4) define slot of a picture,
    5) flip the picture if necessary.
"""

# Import cv2 for picture treatment.
import cv2

# Import os for path direction
# and checking documents exists.
import os

# For a cool display (random emplacement).
import random


def get_picture_path():
    """
        Get the current work repository,
        verification of the picture path.
        In case of another environement, 
        allows you to change the path of the images without taking the lead.
        Get the picture path.
    """

    # Current repository work.
    PATH = os.getcwd()
    print("[INFO] Current path's {}\n".format(PATH))

    # Picture path.
    picture_path = "{}/picture/human/{}.png"

    path_picture_one = picture_path.format(PATH, "a")
    path_picture_two = picture_path.format(PATH, "b")

    # Cheking existence of images.
    check_first_picture = os.path.exists(path_picture_one)
    check_second_picture = os.path.exists(path_picture_two)
    
    print("[INFO] first path picture exists:", check_first_picture)
    print("[INFO] second path picture exists:", check_second_picture)

    # Break the program if picture path isn't ok.
    if not check_first_picture or not check_second_picture:
        print("[INFO] Picture of the first picture doesn't exist, verify path !")
        exit()

    return path_picture_one, path_picture_two


def blitting_a_gif_on_a_picture(position, reverse_picture, img1):
    """
        Blitting a transparent picture on another (background) picture.
    """

    position_on_x, position_on_y = position

    # Flip picture if parameter's reverse_picture.
    if reverse_picture:
        img1 = cv2.flip(img1, 1)

    # Emplacement of the picture to blit in function of the size.
    height_picture, width_picture = img1.shape[:2]

    y1 = position_on_y
    y2 = position_on_y + height_picture

    x1 = position_on_x
    x2 = position_on_x + width_picture

    # IDK
    alpha_s = img1[:, :, 1] / 255.0
    alpha_l = 1.0 - alpha_s

    for canal in range(0, 3):

        a = alpha_s * img1[:, :, canal]
        b = alpha_l * img[y1:y2, x1:x2, canal]

        img[y1:y2, x1:x2, canal] = a + b


def get_the_picture_emplacement_from_a_random_function():
    """
        Each 50 frames choice randomly picture to display.
    """

    # Random function.
    picture_to_display = [random.randint(1, 6) for _ in range(random.randint(0, 6))]


    # Recuperate info of the picture to display
    # from the dictionnary emplacement.

    displaying_emplacement = []

    for emplacement in picture_to_display:

        label = emplacement_to_blit_picture[emplacement]

        position = label["emplacement"]
        reversing = label["need_to_be_reverse"]

        displaying_emplacement += [( position, reversing )]

    return displaying_emplacement




if __name__ == "__main__":

    # Verification of the picture path.
    path_picture_one, path_picture_two = get_picture_path()

    # Reading picture.
    background = cv2.imread(path_picture_one)
    picture_to_blit = cv2.imread(path_picture_two)

    # Define urself the emplacement for blit the picture, and
    # if the picture need to be reverse.
    emplacement_to_blit_picture = {

        1: { "emplacement": (585, 230), "need_to_be_reverse": False, "label": "right_leg" },
        2: { "emplacement": (550, 385), "need_to_be_reverse": False, "label": "right_foot" },
        3: { "emplacement": (585, 100), "need_to_be_reverse": False, "label": "right_hand" },
        4: { "emplacement": (480, 0),   "need_to_be_reverse": False, "label": "head" },
        5: { "emplacement": (8, 220),   "need_to_be_reverse": True,  "label": "left_leg" },
        6: { "emplacement": (55, 415),  "need_to_be_reverse": True,  "label": "left_foot" },
        7: { "emplacement": (5, 90),    "need_to_be_reverse": True,  "label": "left_hand" },
 
    }


    counter_for_switch_emplacement = 0

    while True:

        # Each 50 frames update slots of picture.
        condition_for_swith_picture = counter_for_switch_emplacement % 50 == 0

        if condition_for_swith_picture:


            displaying_emplacement = get_the_picture_emplacement_from_a_random_function()

            img = background.copy()

            [
                blitting_a_gif_on_a_picture(position, reversing, picture_to_blit)
                for (position, reversing) in displaying_emplacement
            ]

        counter_for_switch_emplacement += 1


        cv2.imshow('Animation', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()













