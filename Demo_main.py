from ast import main
from asyncio.windows_events import NULL
from datetime import datetime
from ConnectionObject import Connection
from turtle import position
from types import CellType
import numpy as np
import cv2
import math
from PyQt5.QtWidgets import * 

#WINDOW = NULL
#Returns the average position of where the eye was looking

class EyeTracker():
    connection = NULL

    def __init__(self):
        print("Eye Tracker Creation Succesful_________")
        
    def Positions():
        CENTRE = [0, 0] #with +-2 error
        NUMBEROFITERATIONS = 0
        cap = cv2.VideoCapture(0) #initialize video capture
        left_counter=0  #counter for left movement
        right_counter=0	#counter for right movement

        th_value=5   #changeable threshold value 

        def thresholding( value ):  # function to threshold and give either left or right
            global left_counter
            global right_counter
        
            if (value<=54):   #check the paeter is less than equal or greater than range to 
                left_counter=left_counter+1		#increment left counter 

                if (left_counter>th_value):  #if left counter is greater than threshold value 
                    print ('RIGHT')  #the eye is left
                    left_counter=0   #reset the counter

            elif(value>=54):  # same procedure for right eye
                right_counter=right_counter+1

                if(right_counter>th_value):
                    print ('LEFT')
                    right_counter=0


        while True:
            ret, frame = cap.read()
            vid = frame
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            cv2.line(frame, (320,0), (320,480), (0,200,0), 2)
            cv2.line(frame, (0,200), (640,200), (0,200,0), 2)
            if ret==True:
                col=frame
            
                frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
                #cv2.imshow('Random', frameForThreshold)
                #ret,thresh = cv2.threshold(frameForThreshold,3,255,cv2.THRESH_BINARY)
                pupilFrame=frame
                clahe=frame
                blur=frame
                edges=frame
                eyes = cv2.CascadeClassifier('haarcascade_eye.xml')
                detected = eyes.detectMultiScale(frame, 1.3, 5)
                for (x,y,w,h) in detected: #similar to face detection
                    cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)	 #draw rectangle around eyes
                    cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)   #draw cross
                    cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
                    pupilFrame = cv2.equalizeHist(frame[int(y+(h*0.25)):(y+h), (x):(x+w)]) #using histogram equalization of better image. 
                    cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) #set grid size
                    clahe = cl1.apply(pupilFrame)  #clahe
                    blur = cv2.medianBlur(clahe, 7)  #median blur
                    centre = (int((x+w)/2), int((x-y)/2))
                    CENTRE[0] += int((x+w)/2)
                    CENTRE[1] += int((x-y)/2)
                    NUMBEROFITERATIONS+=  1
                    print(centre)
                    print("=============")
                    # in order to mask only one eye in the frame 
                    break



                retval, thresholded = cv2.threshold(pupilFrame, 80, 255, 0)
                cv2.imshow("threshold", thresholded)

                closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
                contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
                drawing = np.copy(pupilFrame)
                cv2.drawContours(drawing, contours, -1, (255, 0, 0), 2)

                for contour in contours:
                
                    area = cv2.contourArea(contour)
                
                    if area < 100:
                        continue
                    circumference = cv2.arcLength(contour,True)
                    circularity = circumference ** 2 / (4*math.pi*area)
                    if 1.3 > circularity  or circularity > 1.319:
                        continue
                    print(circularity)
                    contour = cv2.convexHull(contour)
                    bounding_box = cv2.boundingRect(contour)

                    extend = area / (bounding_box[2] * bounding_box[3])

                    # reject the contours with big extend
                    if extend > 0.8:
                        continue

                    # calculate countour center and draw a dot there
                    m = cv2.moments(contour)
                    if m['m00'] != 0:
                        center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                        cv2.circle(drawing, center, 3, (0, 255, 0), -1)

                    # fit an ellipse around the contour and draw it into the image
                    try:
                        ellipse = cv2.fitEllipse(contour)
                        cv2.ellipse(drawing, box=ellipse, color=(0, 255, 0))
                    except:
                        pass

            # show the frame
                cv2.imshow("Drawing", drawing)
                cv2.imshow('image',pupilFrame)  
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                


        cap.release()
        cv2.destroyAllWindows()
        print(CENTRE)
        print(NUMBEROFITERATIONS)
        CENTRE[0] = int(CENTRE[0]/NUMBEROFITERATIONS)
        CENTRE[1] = int(CENTRE[1]/NUMBEROFITERATIONS)
        print(CENTRE)
        return CENTRE

    #Track the movement of eye by the movement of x and y coordinate
    def EyePosition(self, centre):
        #Testing function which tells where the eye is looking
        def looking(x, y):
            if centre[0] -3 < x < centre[0] + 3:
                return "Centre"
            elif centre[0] < x:
                return "Left"
            elif centre[0] > x:
                return "Right"


        camera = cv2.VideoCapture(0)
        while True:
            ret, frame = camera.read()
            raw = frame
            centrre = (0, 0)
            vid = frame
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            cv2.line(frame, (320,0), (320,480), (0,200,0), 2)
            cv2.line(frame, (0,200), (640,200), (0,200,0), 2)
            if ret==True:
                col=frame
            
                frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
                pupilFrame=frame
                clahe=frame
                blur=frame
                edges=frame
                eyes = cv2.CascadeClassifier('haarcascade_eye.xml')
                detected = eyes.detectMultiScale(frame, 1.3, 5)
                for (x,y,w,h) in detected: #similar to face detection
                    print(x, y, w, h)
                    cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)	 #draw rectangle around eyes
                    cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)   #draw cross
                    cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
                    pupilFrame = cv2.equalizeHist(frame[int(y+(h*0.25)):(y+h), (x):(x+w)]) #using histogram equalization of better image. 
                    cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) #set grid size
                    clahe = cl1.apply(pupilFrame)  #clahe
                    blur = cv2.medianBlur(clahe, 7)  #median blur
                    centrre = (int((x+w)/2), int((x-y)/2))
                    print(centrre)
                    print("=============")
                    frameY, frameX = frame.shape[:2]
                    newFrameY, newFrameX = 1080, 1920
                    print(frameY, frameX)
                    x1, y1 = maskToPupil(x, y, int(frameX), int(frameY), newFrameX, newFrameY)
                    print(x1, y1)
                    #self.connection.putCoordinates((x1, y1))
                    
                    # in order to mask only one eye in the frame we break
                    break

                #Evaluating the position of the eye
                position = looking(centrre[0], centrre[1])

                retval, thresholded = cv2.threshold(pupilFrame, 80, 255, 0)
                cv2.imshow("threshold", thresholded)

                closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
                contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
                drawing = np.copy(pupilFrame)
                cv2.drawContours(drawing, contours, -1, (255, 0, 0), 2)

                for contour in contours:
                
                    area = cv2.contourArea(contour)
                
                    if area < 100:
                        continue
                    circumference = cv2.arcLength(contour,True)
                    circularity = circumference ** 2 / (4*math.pi*area)
                    if 1.3 > circularity  or circularity > 1.319:
                        continue
                    print(circularity)
                    contour = cv2.convexHull(contour)
                    bounding_box = cv2.boundingRect(contour)

                    extend = area / (bounding_box[2] * bounding_box[3])

                    # reject the contours with big extend
                    if extend > 0.8:
                        continue

                    # calculate countour center and draw a dot there
                    m = cv2.moments(contour)
                    if m['m00'] != 0:
                        center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                        cv2.circle(drawing, center, 3, (0, 255, 0), -1)

                    # fit an ellipse around the contour and draw it into the image
                    try:
                        ellipse = cv2.fitEllipse(contour)
                        cv2.ellipse(drawing, box=ellipse, color=(0, 255, 0))
                    except:
                        pass

            # show the frame
                color = (255,255, 0)
                cv2.putText(raw, position, centre,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                cv2.imshow("Drawing", frame)
                cv2.imshow("frame", raw)
                cv2.imshow('image',pupilFrame)  
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        camera.release()
        cv2.destroyAllWindows()


def maskToPupil(x , y, xFrame, yFrame, newXFrame, newYFrame):
    x1 = int((newXFrame * x)/xFrame)
    y1 = int((newYFrame*y)/yFrame)
    return x1,y1
    #Track the Screen with the help of the points tracked by EyeTracker
    #def TrackOnScreen(window, x, y):
    #window.paintEvent(x, y)

e = EyeTracker()
centre = EyeTracker.Positions()
e.EyePosition(centre=centre)