

import cv2
import numpy as np
import mediapipe as mp



def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results


def draw_styled_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)) 
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=2), mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=1)) 
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=2), mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=1)) 
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=1)) 


def extract_keypoints(results):

    return [[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]\
            if results.pose_landmarks else [(0, 0, 0)] * 33


def group_pts(nb_points, liste, image):

    return [( int(x * image.shape[1]), int(y * image.shape[0]) ) for (x, y, z) in liste]



class Animation_circle:
    """
        Animation. Display a gif, a line, a picture and another gif.
    """

    def __init__(self):

        path_loading = r"C:\Users\jb264\OneDrive\Bureau\modules\interface\animation\picture\load1\{}.png"
        path_loading2 = r"C:\Users\jb264\OneDrive\Bureau\modules\interface\animation\picture\load2\{}.png"
        path_slot = r"C:\Users\jb264\OneDrive\Bureau\modules\interface\animation\picture\slot\{}.png"
        
        # Gifs.
        self.loading1 = [cv2.resize( cv2.imread( path_loading.format(str(n)) ), (80, 45) ) for n in range(1, 24, 1)]
        self.loading2 = [cv2.resize( cv2.imread( path_loading2.format(str(n)) ), (200, 160) ) for n in range(1, 41, 1)]
        self.slot = [cv2.imread( path_slot.format(picture) ) for picture in ["b1", "b2", "b3", "b4", "b5"]]

        # 
        self.timer_first = 0
        self.counter_first_loader = 0
        self.line = 0

        self.active_display_line = False

        self.counter_activ_line = 0

        #
        self.fist_line = 11
        self.second_line = 25


        self.line_displayed = False

        self.counter_time = 0
        self.slot_counter = 0

        self.timer_seconde = 0
        self.counter_second_loader = 0

        self.stop_display_slot = False
        self.stop_counter_display_slot = False
        self.counter_displaying_slot = 0

        self.counter_before_undisplay_line = 0
        self.undisplay_line_is_active = False


        self.active_second_loader = False


    def setter_line(self):
        """

        """

        if not self.undisplay_line_is_active and self.line != self.second_line:
            self.line += 1
        else:
            if self.line != 0:
                self.line -= 1
                
            if self.line == 0:
                self.active_second_loader = True

    def setter_first_loader(self):
        """

        """
        
        self.counter_first_loader += 1

        if self.counter_first_loader >= len(self.loading1) - 1:
            self.counter_first_loader = 0



    def first_loader(self, frame, x_offset, y_offset):
        """

        """
        if self.active_second_loader is False:

            x_offset = x_offset - 40
            y_offset = y_offset - 20

            current_picture = self.loading1[self.counter_first_loader]

            height, width = current_picture.shape[:2]

            y1, y2 = y_offset, y_offset + height
            x1, x2 = x_offset, x_offset + width

            alpha_s = current_picture[:, :, 1] / 255.0
            alpha_l = 1.0 - alpha_s

            try:
                for c in range(0, 3):
                    frame[y1:y2, x1:x2, c] = (
                        alpha_s * current_picture[:, :, c] + alpha_l * frame[y1:y2, x1:x2, c])
            except:
                pass


    def second_loader(self, frame, x_offset, y_offset):

        if self.active_second_loader:
            x_offset = x_offset - 100
            y_offset = y_offset - 80

            current_picture = self.loading2[self.counter_second_loader]

            height, width = current_picture.shape[:2]

            y1, y2 = y_offset, y_offset + height
            x1, x2 = x_offset, x_offset + width

            alpha_s = current_picture[:, :, 1] / 255.0
            alpha_l = 1.0 - alpha_s

            try:
                for c in range(0, 3):
                    frame[y1:y2, x1:x2, c] = (
                        alpha_s * current_picture[:, :, c] + alpha_l * frame[y1:y2, x1:x2, c])
            except:
                pass


            self.timer_seconde += 1

            if self.timer_seconde % 3 == 0:
                self.counter_second_loader += 1

            if self.counter_second_loader >= len(self.loading2) - 1:
                self.counter_second_loader = 0
                self.timer_seconde = 0


    def new_coordinate_lines(self, x, y, line, operator):

        x1 = x + ( ( line * 5 ) * operator)
        y1 = y - ( line * 6 )

        return x1, y1


    def setter_counter_activ_line(self):

        if self.counter_activ_line < 50:
            self.counter_activ_line += 1

        elif self.counter_activ_line == 50:
            self.active_display_line = True

    def display_line(self, frame, x, y, operator):
        """

        """

        operator = -1 if operator == "-" else 1

        x2 = 0
        y1 = 0


        if self.line <= self.fist_line and self.active_display_line:

            x1, y1 = self.new_coordinate_lines(x, y, self.line, operator)
            cv2.line(frame, (x, y), (x1, y1), (121, 123, 64), 2)

        elif self.second_line > self.line > self.fist_line:

            x1, y1 = self.new_coordinate_lines(x, y, self.fist_line - 1,  operator)

            cv2.line(frame, (x, y), (x1, y1), (121, 123, 64), 2)

            x2 = x1 + ( self.line * 4 * operator )
            cv2.line(frame, (x1, y1), (x2, y1), (121, 123, 64), 2)


        elif self.line >= self.second_line and not self.undisplay_line_is_active:

            x1, y1 = self.new_coordinate_lines(x, y, self.fist_line - 1, operator)

            cv2.line(frame, (x, y), (x1, y1), (121, 123, 64), 2)

            x2 = x1 + ( (self.second_line - 1) * 4 * operator )
            cv2.line(frame, (x1, y1), (x2, y1), (121, 123, 64), 2)

            self.line_displayed = True

        return x2, y1


    def undisplay_line_function(self, frame, x, y, operator):



        if not self.slot_counter >= 0:

            if self.counter_before_undisplay_line != 10:
                self.counter_before_undisplay_line += 1

            if self.counter_before_undisplay_line == 10:

                operator = -1 if operator == "-" else 1

                self.undisplay_line_is_active = True

                if self.line <= self.fist_line:
                    x1, y1 = self.new_coordinate_lines(x, y, self.line, operator)
                    cv2.line(frame, (x, y), (x1, y1), (121, 123, 64), 2)

                elif self.second_line >= self.line > self.fist_line:
                    x1, y1 = self.new_coordinate_lines(x, y, self.fist_line - 1,  operator)

                    cv2.line(frame, (x, y), (x1, y1), (121, 123, 64), 2)

                    x2 = x1 + ( self.line * 4 * operator )
                    cv2.line(frame, (x1, y1), (x2, y1), (121, 123, 64), 2)








    def displaying_slots(self, frame, x, y, x1, x2):


        if self.line_displayed and self.slot_counter >= 0:

            to_reverse = True if x > x1 else False

            current_picture = self.slot[self.slot_counter]

            if to_reverse:
                current_picture = cv2.flip(current_picture, 1)
            
            
            height, width = current_picture.shape[:2]

            x2 = x1 + width
            y2 = y1 - height

            alpha_s = current_picture[:, :, 1] / 255.0
            alpha_l = 1.0 - alpha_s


            if 0 < y2 < frame.shape[0] and 0 < x2 < frame.shape[1]:

                if not to_reverse:

                    for c in range(0, 3):
                        frame[y2:y1, x1:x2, c] = (
                            alpha_s * current_picture[:, :, c] + alpha_l * frame[y2:y1, x1:x2, c])

                else:
                    x2 = x1 - width
                    for c in range(0, 3):
                        frame[y2:y1, x2:x1, c] = (
                            alpha_s * current_picture[:, :, c] + alpha_l * frame[y2:y1, x2:x1, c])


            self.counter_time += 1

            if not self.stop_display_slot:
                if self.counter_time % 5 == 0 and self.slot_counter < len(self.slot) - 1:
                    self.slot_counter += 1
                    self.stop_counter_display_slot = True
            else:
                if self.counter_time % 5 == 0:
                    self.slot_counter -= 1


    def setter_counter_display_slot(self):

        if self.stop_counter_display_slot:


            if self.counter_displaying_slot < 30:
                self.counter_displaying_slot += 1
            else:
                self.stop_display_slot = True
                self.slot_counter = len(self.slot) - 1
                self.stop_counter_display_slot = False










if __name__ == "__main__":


    anim = Animation_circle()

    animation_dispaly = 1

    mp_holistic = mp.solutions.holistic # Holistic model
    mp_drawing = mp.solutions.drawing_utils # Drawing utilities


    path = r"C:\Users\jb264\OneDrive\Bureau\hello\hello\data\video_jambe\b.mp4"
    capture_video = cv2.VideoCapture(path)

    holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    counter_skeltton = 0
    to_draw_skelleton = False

    

    while capture_video.isOpened():

        ret, frame = capture_video.read()

        if not ret:
            break


        copy_frame = frame.copy()

        image, results = mediapipe_detection(frame, holistic)


        if counter_skeltton % 30 == 0:
            to_draw_skelleton = False if to_draw_skelleton else True

        if to_draw_skelleton:
            draw_styled_landmarks(image, results)


        pose = extract_keypoints(results)
        pose = group_pts(3, pose, copy_frame)




        #################################################################
        genoux_right = pose[26]

        x_offset, y_offset = genoux_right
        anim.first_loader(image, x_offset, y_offset)
        x1, y1 = anim.display_line(image, x_offset, y_offset, operator="-")
        anim.displaying_slots(image, x_offset, y_offset, x1, y1)
        anim.undisplay_line_function(image, x_offset, y_offset, operator="-")
        anim.second_loader(image, x_offset, y_offset)

        #################################################################
        genoux_right = pose[13]

        x_offset, y_offset = genoux_right
        anim.first_loader(image, x_offset, y_offset)
        x1, y1 = anim.display_line(image, x_offset, y_offset, operator="+")
        anim.displaying_slots(image, x_offset, y_offset, x1, y1)
        anim.undisplay_line_function(image, x_offset, y_offset, operator="+")
        anim.second_loader(image, x_offset, y_offset)

        #################################################################
        genoux_right = pose[20]

        x_offset, y_offset = genoux_right
        anim.first_loader(image, x_offset, y_offset)
        x1, y1 = anim.display_line(image, x_offset, y_offset, operator="-")
        anim.displaying_slots(image, x_offset, y_offset, x1, y1)
        anim.undisplay_line_function(image, x_offset, y_offset, operator="-")
        anim.second_loader(image, x_offset, y_offset)


        #################################################################
        genoux_right = pose[0]

        x_offset, y_offset = genoux_right
        anim.first_loader(image, x_offset, y_offset)
        x1, y1 = anim.display_line(image, x_offset, y_offset, operator="-")
        anim.displaying_slots(image, x_offset, y_offset, x1, y1)
        anim.undisplay_line_function(image, x_offset, y_offset, operator="-")
        anim.second_loader(image, x_offset, y_offset)


        #################################################################
        genoux_right = pose[15]

        x_offset, y_offset = genoux_right
        anim.first_loader(image, x_offset, y_offset)
        x1, y1 = anim.display_line(image, x_offset, y_offset, operator="+")
        anim.displaying_slots(image, x_offset, y_offset, x1, y1)
        anim.undisplay_line_function(image, x_offset, y_offset, operator="+")
        anim.second_loader(image, x_offset, y_offset)
        
        #####################################################################

        genoux_right = pose[25]

        x_offset, y_offset = genoux_right

        



        #####################################################################

        genoux_right = pose[24]

        x_offset, y_offset = genoux_right




        #####################################################################

        genoux_right = pose[31]

        x_offset, y_offset = genoux_right





        #####################################################################

        genoux_right = pose[11]

        x_offset, y_offset = genoux_right


        


        anim.setter_line()
        anim.setter_first_loader()

        counter_skeltton += 1

        anim.setter_counter_display_slot()
        anim.setter_counter_activ_line()





        cv2.imshow('frame', image)


        press = cv2.waitKey(animation_dispaly)

        if press == ord('q'):
            break
        elif press == ord('a'):
            animation_dispaly = 0 if animation_dispaly == 50 else 50



    cap.release()
    cv2.destroyAllWindows()
















