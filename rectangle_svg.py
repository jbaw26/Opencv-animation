



import cv2



def first_rectangle(frame, counter_rectangle):


    contrast = 0.8
    brightness = 1

    x, y, w, h = 500, 400, 700, 465

    add = 1
    
    crop = frame[y: h, x - counter_rectangle * add: w + counter_rectangle * add]

    frame[y: h, x - counter_rectangle * add: w + counter_rectangle * add] = cv2.addWeighted( crop, contrast, crop, 0, brightness)




def rectangle_svg(frame, counter, counter1, counter2, counter3):

    x, y, w, h = 450, 400, 750, 465

    cv2.line(frame, (x, y), (x + counter * 5, y), (255, 255, 255), 2) 

    if counter1 > 0:
        cv2.line(frame, (x + counter * 5, y), (x + counter * 5, y + counter1 * 5), (255, 255, 255), 2) 

    if counter2 > 0:
        cv2.line(frame, (x + counter * 5, y + counter1 * 5), (x + counter * 5 - counter2 * 5, y + counter1 * 5), (255, 255, 255), 2) 

    if counter3 > 0:
        cv2.line(frame, (x, y+ counter1 * 5), (x, y+ counter1 * 5 - counter3 * 5), (255, 255, 255), 2) 




path = r"C:\Users\jb264\OneDrive\Bureau\hello\hello\data\video_jambe\b.mp4"
capture_video = cv2.VideoCapture(path)





dico_svg = {
    "counter_rectangle": 0, "counter_1": 0, "counter_2": 0, "counter_3": 0, "counter_4": 0,  "counter_end":0, "end": False
}





while capture_video.isOpened():

    ret, frame = capture_video.read()

    if not ret:
        break




    counter_rectangle = dico_svg["counter_rectangle"]
    counter = dico_svg["counter_1"]
    counter1 = dico_svg["counter_2"]
    counter2 = dico_svg["counter_3"]
    counter3 = dico_svg["counter_4"]

    
    first_rectangle(frame, counter_rectangle)

    if counter_rectangle < 50:
        dico_svg["counter_rectangle"] += 1

    else:
        rectangle_svg(frame, counter, counter1, counter2, counter3)



        if counter <= 59:
            dico_svg["counter_1"] += 1

        elif counter > 58 and counter1 <= 12:
            dico_svg["counter_2"] += 1

        elif counter1 > 12 and counter2 <= 59:
            dico_svg["counter_3"] += 1

        elif counter2 > 59 and counter3 <= 12:
            dico_svg["counter_4"] += 1

        else:
            end = dico_svg["counter_end"]

            if end < 100:
                dico_svg["counter_end"] += 1
            else:
                dico_svg["end"] = True


    if dico_svg["end"]:
        dico_svg = {
            "counter_rectangle": 0, "counter_1": 0, "counter_2": 0, "counter_3": 0, "counter_4": 0, "counter_end":0, "end": False
        }



    cv2.imshow("dzadaz", frame)
    cv2.waitKey(1)














