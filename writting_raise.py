
import cv2
import numpy as np
import string
import imutils
import pytesseract



# https://www.youtube.com/watch?v=a2XXkUBEQFQ&list=PLwW0TR1gIf7wKyAbKtoTPmbAqatODiJJH&index=3

# https://www.youtube.com/watch?v=GY0mGV5FCHE&list=PLwW0TR1gIf7wKyAbKtoTPmbAqatODiJJH&index=5
#26 sec

# https://www.youtube.com/watch?v=GY0mGV5FCHE&list=PLwW0TR1gIf7wKyAbKtoTPmbAqatODiJJH&index=5
# 46 sec

path = r"C:\Users\jb264\OneDrive\Bureau\hello\hello\data\video_jambe\a.mp4"
capture_video = cv2.VideoCapture(path)








dico_letter = {"upper":{}, "lower": {}, "number": {}}




def treatment(dico_letter, list, label):

    font = cv2.FONT_HERSHEY_SIMPLEX

    for i in list:

        picture = 255 * np.ones((100, 100, 3), np.uint8)
        cv2.putText(picture, i, (50, 50), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
        gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 200, 255,cv2.THRESH_BINARY_INV)[1]
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        _, _, w, h = cv2.boundingRect(c)

        dico_letter[label][i] = [w, h]


def mesuring_space(dico_letter):

    font = cv2.FONT_HERSHEY_SIMPLEX
    picture = 255 * np.ones((100, 100, 3), np.uint8)
    cv2.putText(picture, "A A", (50, 50), font, 1, (0, 0, 0), 1, cv2.LINE_AA)

    y = 49
    activate = False
    counter = 0
    for x in range(0, 100):

        #print(activate, counter, picture[y][x])

        if picture[y][x][0] != 255 and picture[y][x][1] != 255 and picture[y][x][2] != 255 and not activate:
            activate = True
        
        elif activate and picture[y][x][0] != 255 and picture[y][x][1] != 255 and picture[y][x][2] != 255:
            activate = False

        elif activate:
            counter += 1


        # picture[y][x] = (0, 0, 255)
        # cv2.imshow("dzadaz", picture)
        # cv2.waitKey(0)


    dico_letter["space"] = counter

 


def raise_alphabet(dico_letter):

    alphabet_lower = list(string.ascii_lowercase)
    alphabet_upper = list(string.ascii_uppercase)
    number = [str(i) for i in range(0, 10)]


    treatment(dico_letter, alphabet_lower, "lower")
    treatment(dico_letter, alphabet_upper, "upper")
    treatment(dico_letter, number, "number")





dico_writting = {
    "anim1": {
        "counter1": 0, 
        "text1": " H E L L O   U I ",
        "text2": "A N I M A T I O N",
        "text1_position": [],
        "text2_position": [],
        "counter_anim2": 0,
        "text2_animation": [
            [], 
            [(0, 1), (4, 1)], 
            [(7, 0), (5, 1)], 
            [(1, 1), (2, 1), (3, 1)],
            [(6, 1), (8, 0)]
            ],
        "is_movement_finish_2": False
    },

}



def counter_position(position_text_x, text, dico_letter):
    
    position = []

    for i in text:

        if i == " ":
            x = dico_letter["space"]

        elif i.isdigit():
            x, y = dico_letter[number][i]
        else:
            size = "upper" if i.isupper() else "lower"
            x, y = dico_letter[size][i]
        

        position += [(i, position_text_x, position_text_x + x)]

        position_text_x += x


    return position




def get_contours(picture):

    contours_list = []


    gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 255,cv2.THRESH_BINARY_INV)[1]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(picture, contours, -1, (0, 255, 0), 3)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        contours_list += [(x, y, w, h)]


    # cv2.imshow("dazdaz", picture)
    # cv2.waitKey(0)

    return contours_list





def animation_un(frame, dico_writting, dico_letter):


    text1 = dico_writting["anim1"]["text1"]
    text2 = dico_writting["anim1"]["text2"]

    x = 500
    font = cv2.FONT_HERSHEY_SIMPLEX

    dacdac =  frame.copy()

    cv2.putText(frame, text1, (x, x), font, 1, (0, 0, 0), 1, cv2.LINE_AA)

    if dico_writting["anim1"]["text1_position"] == []:
        position = get_contours(frame)
        dico_writting["anim1"]["text1_position"] = position

    cv2.putText(dacdac, text2, (x, 550), font, 1, (0, 0, 0), 1, cv2.LINE_AA)

    if dico_writting["anim1"]["text2_position"] == []:
        position = get_contours(dacdac)
        dico_writting["anim1"]["text2_position"] = position

    cv2.putText(frame, text2, (x, 550), font, 1, (0, 0, 0), 1, cv2.LINE_AA)




    counter = dico_writting["anim1"]["counter1"]

    couter_raise_2 = dico_writting["anim1"]["counter_anim2"]
    to_raise = dico_writting["anim1"]["text2_animation"]

    if counter > 0 and counter % 200 == 0 and couter_raise_2 < len(to_raise) - 1:
        dico_writting["anim1"]["counter_anim2"] += 1

    couter_raise_2 = dico_writting["anim1"]["counter_anim2"]

    text2_position = dico_writting["anim1"]["text2_position"]
    
    for (nb_letter, movement) in to_raise[couter_raise_2]:

        x, y, w, h = text2_position[nb_letter]
        frame[y-1:y+h+1, x-1:x+w+1] = (255, 255, 255)



    dico_writting["anim1"]["counter1"] += 1





raise_alphabet(dico_letter)
mesuring_space(dico_letter)

print(dico_letter)





while True:

    
    frame = 255 * np.ones((720, 1280, 3), np.uint8)
    




    animation_un(frame, dico_writting, dico_letter)









    cv2.imshow("dzadaz", frame)
    cv2.waitKey(1)















