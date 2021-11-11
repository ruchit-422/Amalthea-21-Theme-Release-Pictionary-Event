import numpy as np
import cv2
from collections import deque
import math

#default trackbar function 
def setValues(x):
   print("")

cv2.namedWindow('Tracking', cv2.WINDOW_NORMAL)
cv2.namedWindow('Paint', cv2.WINDOW_NORMAL)
cv2.namedWindow("Thickness")


cv2.createTrackbar("Thickness", "Thickness", 10, 50, setValues)
# Creating trackbars needed to adjust the marker colour
cv2.namedWindow("Color detectors")

cv2.createTrackbar("Upper Hue", "Color detectors", 40, 180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 25, 180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 76, 255,setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 95, 255,setValues)

cv2.namedWindow("Color detectorsrub")

cv2.createTrackbar("Upper Hue", "Color detectorsrub", 0, 180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectorsrub", 255, 255,setValues)
cv2.createTrackbar("Upper Value", "Color detectorsrub", 255, 255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectorsrub", 0, 180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectorsrub", 80, 255,setValues)
cv2.createTrackbar("Lower Value", "Color detectorsrub", 80, 255,setValues)


# Giving different arrays for handling colour points of different colours
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
wpoints = [deque(maxlen=1024)]

# These indexes shall be used to mark the points in particular arrays of specific colours
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0
white_index = 0

#The kernel to be used for dilation purpose 
kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0),(255,255,255)]
colorIndex = 0

#Code for Canvas setup
paintWindow = np.zeros((471,636,3)) + 255

paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (20,406), (120,470), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "ERASER", (40, 442), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)


# webcam of PC.
cap = cv2.VideoCapture(1)

# Keep looping
while True:
    # Reading the frame
    ret, frame = cap.read()
    #Flipping the frame to see same side of yours
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    rad = cv2.getTrackbarPos("Thickness", "Thickness")

    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([u_hue,u_saturation,u_value])
    Lower_hsv = np.array([l_hue,l_saturation,l_value])
    
    u_hue1 = cv2.getTrackbarPos("Upper Hue", "Color detectorsrub")
    u_saturation1 = cv2.getTrackbarPos("Upper Saturation", "Color detectorsrub")
    u_value1 = cv2.getTrackbarPos("Upper Value", "Color detectorsrub")
    l_hue1 = cv2.getTrackbarPos("Lower Hue", "Color detectorsrub")
    l_saturation1 = cv2.getTrackbarPos("Lower Saturation", "Color detectorsrub")
    l_value1 = cv2.getTrackbarPos("Lower Value", "Color detectorsrub")
    Upper_hsv1 = np.array([u_hue1,u_saturation1,u_value1])
    Lower_hsv1 = np.array([l_hue1,l_saturation1,l_value1])
    
    # Adding the colour buttons to the live frame for colour access
    frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (20,406), (120,470), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "ERASER", (40, 442), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)


    # Identify the pointer by making its mask
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)
    
    Mask1 = cv2.inRange(hsv, Lower_hsv1, Upper_hsv1)
    Mask1 = cv2.erode(Mask1, kernel, iterations=1)
    Mask1 = cv2.morphologyEx(Mask1, cv2.MORPH_OPEN, kernel)
    Mask1 = cv2.dilate(Mask1, kernel, iterations=1)
    
    # Find contours for the pointer after idetifying it
    cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    center = None

    cnts1,_ = cv2.findContours(Mask1.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    center1 = None

    # If the contours are formed
    if len(cnts) > 0:
    	#sorting the contours to find biggest 
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        #Get the radius of enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw  circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        paintWindow = np.zeros((471,636,3)) + 255
        paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
        paintWindow = cv2.rectangle(paintWindow, (20,406), (120,470), (0,0,0), 2)
        paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
        paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
        paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
        paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

        cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "ERASER", (40, 442), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.circle(paintWindow, (int(x), int(y)), int(13), (0, 0, 0), 2)
        # Calculating center of the detected contour
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        # Checking if the user wants to click on any button above the screen
        if center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear Button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                wpoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0
                white_index = 0

                paintWindow = np.zeros((471,636,3)) + 255
                paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
                paintWindow = cv2.rectangle(paintWindow, (20,406), (120,470), (0,0,0), 2)
                paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
                paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
                paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
                paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

                cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(paintWindow, "ERASER", (40, 442), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(paintWindow, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
 
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # Blue
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # Green
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # Red
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # Yellow
        elif center[1] >= 406:
            if  20 <= center[0] <= 120:
                    colorIndex = 4 #Erase
        else :
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)

            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)

            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

            elif colorIndex == 4:
                for j in bpoints:
                    b = []
                    for i in j:
                        if math.hypot(i[0]-center[0], i[1]-center[1]) <= 50:
                            b.append(i)
                    for i1 in b:
                        j.remove(i1)
                for j in gpoints:
                    g = []
                    for i in j:
                        if math.hypot(i[0]-center[0], i[1]-center[1]) <= 50:
                            g.append(i)
                    for i1 in g:
                        j.remove(i1)
                for j in rpoints:
                    r = []
                    for i in j:
                        if math.hypot(i[0]-center[0], i[1]-center[1]) <= 50:
                            r.append(i)
                    for i1 in r:
                        j.remove(i1)
                for j in ypoints:
                    y = []
                    for i in j:
                        if math.hypot(i[0]-center[0], i[1]-center[1]) <= 50:
                            y.append(i)
                    for i1 in y:                        
                        j.remove(i1)

    # when nothing is detected,  to avoid messing up, we append the next deques 
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1
    
    if len(cnts1) > 0:
    	# sorting the contours to find biggest 
        cnt1 = sorted(cnts1, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x1, y1), radius1) = cv2.minEnclosingCircle(cnt1)
        # Draw the circle around the contour
        cv2.circle(frame, (int(x1), int(y1)), int(radius1), (0, 255, 255), 2)
        # Calculating the center of the detected contour
        M1 = cv2.moments(cnt1)
        center1 = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))

        paintWindow = np.zeros((471,636,3)) + 255
        paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
        paintWindow = cv2.rectangle(paintWindow, (20,406), (120,470), (0,0,0), 2)
        paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
        paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
        paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
        paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

        cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "ERASER", (40, 442), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.circle(paintWindow, (int(x1), int(y1)), int(13), (0, 0, 0), 2)

    # Draw lines of all the colors on the canvas and frame 
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                try:
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], rad)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], rad)
                except:
                    True

    # Show all the windows
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("mask",Mask)

	# If the 'q' key is pressed then stop the application 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()