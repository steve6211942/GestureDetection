from yibajiu import Ui_Form
import numpy as np
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, Qt
import cv2
import sys
import math

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
         
        self.defineGlobal() # init global variable as class member

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.label_camera_up.setScaledContents(True)
        self.ui.label_camera_down.setScaledContents(True)
        self.ui.label_roi_u.setScaledContents(True)
        self.ui.label_roi_d.setScaledContents(True)
        self.ui.label_cnt_u.setScaledContents(True)
        self.ui.label_cnt_d.setScaledContents(True)
        self.ui.label_text.setScaledContents(True)  
        #set image to fit label

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loopCode)
        self.timer.start(100)
        #set timer

    def defineGlobal(self):
        self.bg1 = None
        self.bg2 = None
        self.cap = cv2.VideoCapture(0)
        self.width = self.cap.get(3)
        self.height = self.cap.get(4)
        self.width -= 15
        self.height -= 15
        self.min_x_u = 0
        self.min_y_u = 0
        self.max_x_u = 100
        self.max_y_u = 100
        self.min_x_d = 0
        self.min_y_d = 0
        self.max_x_d = 100
        self.max_y_d = 100
        self.status = 0
        self.ok_num = 0
        self.frame_num = 0
        self.num_frames = 0
        self.aWeight = 0.5
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.leave_times = 1
        self.leave_num = 3
        self.square_flag = 0    


    def loopCode(self):
        ok_flag = False
        ret, frame = self.cap.read()
        # mirror the camera
        frame=cv2.flip(frame,1)
	# draw the range of image
        cv2.rectangle(frame, (self.min_x_u, self.min_y_u), (self.max_x_u, self.max_y_u), (0,255,0), 2)
        cv2.rectangle(frame, (self.min_x_d, self.min_y_d), (self.max_x_d, self.max_y_d), (0,255,0), 2)
        # define the range you interest
        roi_u = frame[self.min_y_u:self.max_y_u, self.min_x_u:self.max_x_u,:]
        roi_d = frame[self.min_y_d:self.max_y_d, self.min_x_d:self.max_x_d,:]

        key = cv2.waitKey(25) & 0xFF
        
        text = np.zeros((400,800,3), np.uint8)
        text.fill(255)
        
        if self.status == 0:
            if self.square_flag == 0:
                cv2.putText(text,'Press WASD to move the square(up)',(10,50), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
                cv2.putText(text,'Press QE to change square size',(10,100), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
                cv2.putText(text,'Press SPACE to check the position of the square',(10,150), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
            else:
                cv2.putText(text,'Press WASD to move the square(down)',(10,50), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
                cv2.putText(text,'Press QE to change square size',(10,100), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
                cv2.putText(text,'Press SPACE to check the position of the square',(10,150), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
            # select range mode
#            if key == ord('w'):
#                if self.square_flag == 0:
#                    if self.min_y_u >= 15:
#                        self.min_y_u -= 15
#                        self.max_y_u -= 15
#                else:
#                    if self.min_y_d >= 15:
#                        self.min_y_d -= 15
#                        self.max_y_d -= 15
#            elif key == ord('a'):
#                if self.square_flag == 0:
#                    if self.min_x_u >= 15:
#                        self.min_x_u -= 15
#                        self.max_x_u -= 15
#                else:
#                    if self.min_x_d >= 15:
#                        self.min_x_d -= 15
#                        self.max_x_d -= 15
            elif key == ord('s'):
                if self.square_flag == 0:
                    if self.max_y_u <= self.height:
                        self.min_y_u += 15
                        self.max_y_u += 15
                else:
                    if self.max_y_d >= 15:
                        self.min_y_d += 15
                        self.max_y_d += 15
            elif key == ord('d'):
                if self.square_flag == 0:
                    if self.max_x_u <= self.width:
                        self.min_x_u += 15
                        self.max_x_u += 15
                else:
                    if self.max_x_d <= self.width:
                        self.min_x_d += 15
                        self.max_x_d += 15
            elif key == ord('q'):
                if self.square_flag == 0:
                    if self.max_x_u <= self.width and self.max_y_u <= self.height and self.min_x_u >= 15 and self.min_y_u >= 15:
                        self.min_x_u -= 15
                        self.min_y_u -= 15
                        self.max_x_u += 15
                        self.max_y_u += 15
                else:
                    if self.max_x_d <= self.width and self.max_y_d <= self.height and self.min_x_d >= 15 and self.min_y_d >= 15:
                        self.min_x_d -= 15
                        self.min_y_d -= 15
                        self.max_x_d += 15
                        self.max_y_d += 15
            elif key == ord('e'):
                if self.square_flag == 0:
                    if self.max_x_u-self.min_x_u >= 100:
                        self.min_x_u += 15
                        self.min_y_u += 15
                        self.max_x_u -= 15
                        self.max_y_u -= 15
                else:
                    if self.max_x_d-self.min_x_d >= 100:
                        self.min_x_d += 15
                        self.min_y_d += 15
                        self.max_x_d -= 15
                        self.max_y_d -= 15
            elif key == 32:
                if self.square_flag == 0:
                    self.square_flag += 1
                else:
                    self.status += 1
        
        elif self.status == 1 or self.status == 2 or self.status == 3:
            roi_uc = roi_u.copy()
            roi_dc = roi_d.copy()
            QRoi_u = QImage(roi_uc.data,roi_uc.shape[1],roi_uc.shape[0],roi_uc.shape[1]*roi_uc.shape[2],QImage.Format_RGB888)
            QRoi_d = QImage(roi_dc.data,roi_dc.shape[1],roi_dc.shape[0],roi_dc.shape[1]*roi_dc.shape[2],QImage.Format_RGB888)
            self.ui.label_roi_u.setPixmap(QPixmap.fromImage(QRoi_u))
            self.ui.label_roi_d.setPixmap(QPixmap.fromImage(QRoi_d))
            #cv2.imshow("roi_u", roi_u)
            cv2.imshow("roi_d", roi_d)

            gray = cv2.cvtColor(roi_u, cv2.COLOR_BGR2GRAY)
            gray_d = cv2.cvtColor(roi_d, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7,7), 0)
            gray_d = cv2.GaussianBlur(gray_d, (7,7), 0)
            if self.num_frames < 100:
                if self.leave_times < 90:
                    if self.leave_times % 30 == 0:
                        self.leave_num -= 1
                    self.leave_times += 1
                    cv2.putText(text,'Leave the square',(10,50), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
                    cv2.putText(text,str(self.leave_num),(10,100), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
                else:
                    run_avg1(gray)
                    run_avg2(gray_d)
                    self.num_frames += 1
                    cv2.putText(text,'Waiting for running average of background',(10,50), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
                    cv2.putText(text,str(self.num_frames) + "%",(10,100), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
            else:
                cv2.putText(text,'Use your gesture to control the position of camera',(10,50), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
                hand = segment1(gray)
                hand_d = segment2(gray_d)
                l = 0
                if hand is not None:
                    (mask, cnt) = hand
                    mask_c = mask.copy()
                    QMask = QImage(mask_c.data,mask_c.shape[1],mask_c.shape[0],mask_c.shape[1]*mask_c.shape[2],QImage.Format_RGB888)
                    self.ui.label_mask,setPixmap(QPixmap.fromImage(QMask))
                    #cv2.imshow("mask", mask)
                    (mode, cX, cY, areacnt, arearatio) = select_mode(mask, cnt, roi_u, self.min_x_u, self.max_x_u, self.min_y_u, self.max_y_u, 'u')
                    cv2.circle(roi_u, (cX,cY), 3, [0,0,255], -1)
                    (l,roi_u) = draw_contours(cnt, roi_u)
            
                #print corresponding gestures which are in their ranges
                if l == 1:
                    if areacnt < 2000:
                        cv2.putText(frame,'Put hand in the box',(0,50), self.font, 2, (0,0,255), 3, cv2.LINE_AA)
                    else:
                        if arearatio < 12 and self.status == 3:
                            cv2.putText(frame,'O',(0,50), self.font, 2, (0,0,255), 3, cv2.LINE_AA)
                            self.status = 0
                        elif self.status == 1 or self.status == 3:
                            if self.status == 1:
                                cv2.putText(frame,mode,(0,50), self.font, 2, (0,0,255), 3, cv2.LINE_AA)
                                print(mode)
                            else:
                                if mode == 'up':
                                    cv2.putText(frame,'1',(0,50), self.font, 2, (0,0,255), 3, cv2.LINE_AA)
                                    self.status = 2
                elif l == 3:
                    cv2.putText(frame,'ok',(0,50), self.font, 2, (0,0,255), 3, cv2.LINE_AA)
                    ok_flag = True
                    self.ok_num += 1
                    self.frame_num = 0
                    print("ok")
                    if self.ok_num == 30:
                        self.status += 1
                        self.ok_num = 0
                else :
                    cv2.putText(frame,'reposition',(10,50), self.font, 2, (0,0,255), 3, cv2.LINE_AA)
                    #show the windows
                #cv2.imshow('mask',mask)
                if ok_flag == False:
                    self.frame_num += 1
                    if self.frame_num == 5:
                        self.ok_num = 0

#        if self.status == 4:
#            self.cap.release()
#            cv2.destroyAllWindows()
#            break
        #cv2.imshow('frame',frame)
        Qtext = QImage(text.data,text.shape[1],text.shape[0],text.shape[1]*text.shape[2],QImage.Format_RGB888)
        self.ui.label_text.setPixmap(QPixmap.fromImage(Qtext))
        #cv2.imshow("text", text)
        #cv2.imshow('roi', roi_u)
        #cv2.imshow('roi2', roi_d)
        #print(self.status)
        #print("frame: ",frame.data)
        #print("roi_u: ",roi_u.data)
        #print("roi_d: ",roi_d.data)
        Qframe = QImage(frame.data, frame.shape[1], frame.shape[0],frame.shape[1] *frame.shape[2],QImage.Format_RGB888)
        self.ui.label_camera_up.setPixmap(QPixmap.fromImage(Qframe))
        roi_uc = roi_u.copy()
        roi_dc = roi_d.copy()
        #print("roi_u_copy: ",roi_u.data)
        Qroi_u = QImage(roi_uc.data, roi_uc.shape[1], roi_uc.shape[0],roi_uc.shape[1] *roi_uc.shape[2],QImage.Format_RGB888)
        self.ui.label_roi_u.setPixmap(QPixmap.fromImage(Qroi_u))
        Qroi_d = QImage(roi_dc.data, roi_dc.shape[1], roi_dc.shape[0],roi_dc.shape[1] *roi_dc.shape[2],QImage.Format_RGB888)
        self.ui.label_roi_d.setPixmap(QPixmap.fromImage(Qroi_d))
#        if key == 27:
#            self.cap.release()
#            cv2.destroyAllWindows()
#            break

    def keyPressEvent(self,event):
        if event.key() == Qt_W:
            if self.square_flag == 0:
                if self.min_y_u >= 15:
                    self.min_y_u -= 15
                    self.max_y_u -= 15
            else:
                if self.min_y_d >= 15:
                    self.min_y_d -= 15
                    self.max_y_d -= 15
        elif event.key() == Qt_S:


        elif event.key() == Qt_A:

        elif event.key() == Qt_D:

        elif event.key() == Qt_Q:

        elif event.key() == Qt_E:


    def run_avg1(self,image):
        if self.bg1 is None:
            self.bg1 = image.copy().astype("float")
            return
        cv2.accumulateWeighted(image, self.bg1, self.aWeight)

    def run_avg2(self,image):
        if self.bg2 is None:
            self.bg2 = image.copy().astype("float")
            return
        cv2.accumulateWeighted(image, self.bg2, self.aWeight)


    def segment1(self,image, threshold = 25):
        diff = cv2.absdiff(self.bg1.astype("uint8"), image)
        thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((3,3), np.uint8)
        thresholded = cv2.dilate(thresholded, kernel, iterations = 3)
        thresholded = cv2.erode(thresholded, kernel, iterations = 3)
        thresholded = cv2.GaussianBlur(thresholded,(5,5),100)
        cnts,_ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) == 0:
            return
        else:
            cnt = max(cnts, key = lambda x: cv2.contourArea(x))
            return (thresholded, cnt)

    def segment2(self,image, threshold = 25):
        diff = cv2.absdiff(self.bg2.astype("uint8"), image)
        thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((3,3), np.uint8)
        thresholded = cv2.dilate(thresholded, kernel, iterations = 3)
        thresholded = cv2.erode(thresholded, kernel, iterations = 3)
        thresholded = cv2.GaussianBlur(thresholded,(5,5),100)
        cnts,_ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) == 0:
            return
        else:
            cnt = max(cnts, key = lambda x: cv2.contourArea(x))
            return (thresholded, cnt)

    def compare_area(self,roi1, roi2, cut_flag):
        cnts1,_ = cv2.findContours(roi1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts2,_ = cv2.findContours(roi2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts1) != 0:
            cnt1 = max(cnts1, key = lambda x:cv2.contourArea(x))
            areacnt1 = cv2.contourArea(cnt1)
        else:
            areacnt1 = 0
        if len(cnts2) != 0:
            cnt2 = max(cnts2, key = lambda x:cv2.contourArea(x))
            areacnt2 = cv2.contourArea(cnt2)
        else:
            areacnt2 = 0

        if cut_flag == 'u_d':
            if areacnt1 > areacnt2:
                return 'down'
            else:
                return 'up'
        elif cut_flag == 'l_r':
            if areacnt1 > areacnt2:
                return 'right'
            else:
                return 'left'
        else:
            return 'none'

    def select_mode(self,mask, cnt, roi, min_x, max_x, min_y, max_y, u_d):
        # make convex hull around hand
        hull = cv2.convexHull(cnt)
    
        #define area of hull and area of hane
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
    
        # find the percentage of area not covered by hand in convex hull
        arearatio = ((areahull-areacnt)/areacnt)*100

        # find the extreme point of hand
        extreme_top = tuple(hull[hull[:,:,1].argmin()][0])
        extreme_bottom = tuple(hull[hull[:,:,1].argmax()][0])
        extreme_left = tuple(hull[hull[:,:,0].argmin()][0])
        extreme_right = tuple(hull[hull[:,:,0].argmax()][0])

        cut_flag = '0'
        if (abs(int(extreme_bottom[1]-extreme_top[1])) > abs(int(extreme_right[0]-extreme_left[0]))):
            # find the center of top and bottom
            # case up and down
            cX = int((extreme_top[0] + extreme_bottom[0]) / 2)
            cY = int((extreme_top[1] + extreme_bottom[1]) / 2)
            cut_flag = 'u_d'
        else:
            # find the center of left and right
            # case left and right
            cX = int((extreme_left[0] + extreme_right[0]) / 2)
            cY = int((extreme_left[1] + extreme_right[1]) / 2)
            cut_flag = 'l_r'

        # cutting the contour by cX or cY an finding the smaller area
        mode = 'none'
        if u_d == 'u':
            if arearatio > 12:
                roi_x = max_x-min_x
                roi_y = max_y-min_y
                if cut_flag == 'u_d':
                    # case up and down, only cut cY
                    roi1 = mask[0:cY, 0:roi_x]
                    roi2 = mask[cY:roi_y, 0:roi_x]
                else:
                    # case left and right, only cut cX
                    roi1 = mask[0:roi_y, 0:cX]
                    roi2 = mask[0:roi_y, cX:roi_x]
                mode = compare_area(roi1, roi2, cut_flag)
    
        return (mode, cX, cY, areacnt, arearatio)

    def draw_contours(self,cnt, roi):
        # approx the contour a little
        epsilon = 0.0005*cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
    

        # l = no. of defects
        l = 0
    
        # code for finding no. of defects due to fingers

        if defects is not None:
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt= (100,180)

                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                s = (a+b+c)/2
                ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            
                #distance between point and convex hull
                d = (2*ar)/a

                # apply cosine rule here
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
    
                # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                if angle <= 90 and d>30:
                    l += 1
                    cv2.circle(roi, far, 3, [255,0,0], -1)

                #draw lines around hand
                cv2.line(roi,start, end, [0,255,0], 2)
            l += 1
        return (l, roi)


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
