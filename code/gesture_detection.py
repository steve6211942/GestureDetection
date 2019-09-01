import cv2
import numpy as np
import math

if __name__ == "__main__":
	cap = cv2.VideoCapture(1)
	width = cap.get(3)
	height = cap.get(4)
	width -= 15
	height -= 15
	min_x = 0
	min_y = 0
	max_x = 100
	max_y = 100
	status = 0
	while True:
		ret, frame = cap.read()
		
		# mirror the camera
		frame=cv2.flip(frame,1)
		
		# draw the range of image
		cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0,255,0), 2)
		
		# define the range you interest
		roi = frame[min_y:max_y, min_x:max_x]
		key = cv2.waitKey(25) & 0xFF
		if status == 0:
			# select range mode
			if key == ord('w'):
				if min_y >= 15:
					min_y -= 15
					max_y -= 15
			elif key == ord('a'):
				if min_x >= 15:
					min_x -= 15
					max_x -= 15
			elif key == ord('s'):
				if max_y <= height:
					min_y += 15
					max_y += 15
			elif key == ord('d'):
				if max_x <= width:
					min_x += 15
					max_x += 15
			elif key == ord('q'):
				if max_x <= width and max_y <= height and min_x >= 15 and min_y >= 15:
					min_x -= 15
					min_y -= 15
					max_x += 15
					max_y += 15
			elif key == ord('e'):
				if max_x-min_x >= 100:
					min_x += 15
					min_y += 15
					max_x += 15
					max_y += 15
			elif key == 32:
				status += 1

		elif status == 1:
			cv2.imshow("roi", roi)

			# control the camera base on gesture
			kernel = np.ones((3,3),np.uint8)
			hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

			# define range of skin color in HSV
			lower_skin = np.array([0,20,70], dtype=np.uint8)
			upper_skin = np.array([20,255,255], dtype=np.uint8)

			#extract skin colur imagw  
			mask = cv2.inRange(hsv, lower_skin, upper_skin)

			#extrapolate the hand to fill dark spots within
			mask = cv2.dilate(mask,kernel,iterations = 4)
			
			#blur the image
			mask = cv2.GaussianBlur(mask,(5,5),100)         
			
			#find contours
			contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

			#find contour of max area(hand)
			if len(contours) == 0:
				continue
			cnt = max(contours, key = lambda x: cv2.contourArea(x))    

			#approx the contour a little
			epsilon = 0.0005*cv2.arcLength(cnt,True)
			approx= cv2.approxPolyDP(cnt,epsilon,True)

			#make convex hull around hand
			hull = cv2.convexHull(cnt)

			#define area of hull and area of hand
			areahull = cv2.contourArea(hull)
			areacnt = cv2.contourArea(cnt)

			#find the percentage of area not covered by hand in convex hull
			arearatio=((areahull-areacnt)/areacnt)*100

			# fubd the extreme point of hand
			extreme_top = tuple(hull[hull[:, :, 1].argmin()][0])
			extreme_bottom = tuple(hull[hull[:, :, 1].argmax()][0])
			extreme_left = tuple(hull[hull[:, :, 0].argmin()][0])
			extreme_right = tuple(hull[hull[:, :, 0].argmax()][0])

			# find the center of the palm and circle the center
			#cX = int((extreme_left[0] + extreme_right[0]) / 2)
			#cY = int((extreme_top[1] + extreme_bottom[1]) / 2)
			#cv2.circle(roi, (cX,cY), 3, [255,0,0], -1)
			a = '0'
			if (abs(int(extreme_bottom[1]-extreme_top[1])) > abs(int(extreme_right[0]-extreme_left[0]))):
				# find the center of top and bottom
				# case up and down
				cX = int((extreme_top[0] + extreme_bottom[0]) / 2)
				cY = int((extreme_top[1] + extreme_bottom[1]) / 2)
				a = '1'
			else:
				# find the center of left and right
				# case left and right
				cX = int((extreme_left[0] + extreme_right[0]) / 2)
				cY = int((extreme_left[1] + extreme_right[1]) / 2)
				a = '2'
			cv2.circle(roi, (cX,cY), 3, [0,0,255], -1)			
			print(a)
			print(int(extreme_left[1]))
			print(int(extreme_right[1]))
			# Cutting the contour by cX and cY and find two smaller area
			if arearatio > 12:
				roi1 = roi[0:cY, 0:cX]
				roi2 = roi[cY:max_y-min_y, 0:cX]
				roi3 = roi[0:cY, cX:max_x-min_x]
				roi4 = roi[cY:max_y-min_y, cX:max_x-min_x]
				hsv1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2HSV)
				hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)
				hsv3 = cv2.cvtColor(roi3, cv2.COLOR_BGR2HSV)
				hsv4 = cv2.cvtColor(roi4, cv2.COLOR_BGR2HSV)
				mask1 = cv2.inRange(hsv1, lower_skin, upper_skin)
				mask2 = cv2.inRange(hsv2, lower_skin, upper_skin)
				mask3 = cv2.inRange(hsv3, lower_skin, upper_skin)
				mask4 = cv2.inRange(hsv4, lower_skin, upper_skin)
				mask1 = cv2.dilate(mask1,kernel,iterations = 4)
				mask2 = cv2.dilate(mask2,kernel,iterations = 4)
				mask3 = cv2.dilate(mask3,kernel,iterations = 4)
				mask4 = cv2.dilate(mask4,kernel,iterations = 4)
				mask1 = cv2.GaussianBlur(mask1,(5,5),100)
				mask2 = cv2.GaussianBlur(mask2,(5,5),100)
				mask3 = cv2.GaussianBlur(mask3,(5,5),100)
				mask4 = cv2.GaussianBlur(mask4,(5,5),100)
				contours1,hierarchy= cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				contours2,hierarchy= cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				contours3,hierarchy= cv2.findContours(mask3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				contours4,hierarchy= cv2.findContours(mask4,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				if len(contours1) != 0:
					cnt1 = max(contours1, key = lambda x: cv2.contourArea(x))
					areacnt1 = cv2.contourArea(cnt1)
				else:
					areacnt1 = 0
				if len(contours2) != 0:
					cnt2 = max(contours2, key = lambda x: cv2.contourArea(x))
					areacnt2 = cv2.contourArea(cnt2)
				else:
					areacnt2 = 0
				if len(contours3) != 0:
					cnt3 = max(contours3, key = lambda x: cv2.contourArea(x))
					areacnt3 = cv2.contourArea(cnt3)
				else:
					areacnt3 = 0
				if len(contours4) != 0:
					cnt4 = max(contours4, key = lambda x: cv2.contourArea(x))
					areacnt4 = cv2.contourArea(cnt4)
				else:
					areacnt4 = 0
				
				mode = 'none'
				if areacnt1 > areacnt4 and areacnt3 > areacnt2:
					mode = 'down'
				elif areacnt1 > areacnt4 and areacnt2 > areacnt3:
					mode = 'right'
				elif areacnt4 > areacnt1 and areacnt2 > areacnt3:
					mode = 'up'
				elif areacnt4 > areacnt1 and areacnt3 > areacnt2:
					mode = 'left'
				else:
					mode = 'none'
					cv2.imshow('mask1',mask1)
					cv2.imshow('roi1',roi1)
					cv2.imshow('mask2', mask2)
					cv2.imshow('roi2',roi2)
					cv2.imshow('mask3',mask3)
					cv2.imshow('roi3',roi3)
					cv2.imshow('mask4',mask4)
					cv2.imshow('roi4',roi4)

			#find the defects in convex hull with respect to hand
			hull = cv2.convexHull(approx, returnPoints=False)
			defects = cv2.convexityDefects(approx, hull)

			# l = no. of defects
			l = 0

			#code for finding no. of defects due to fingers
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

			#print corresponding gestures which are in their ranges
			font = cv2.FONT_HERSHEY_SIMPLEX
			if l == 1:
				if areacnt < 2000:
					cv2.putText(frame,'Put hand in the box',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
				else:
					if arearatio < 12:
						cv2.putText(frame,'0',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
					else:
						cv2.putText(frame,mode,(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
			elif l == 3:
				cv2.putText(frame,'ok',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
			else :
				cv2.putText(frame,'reposition',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
			#show the windows
			cv2.imshow('mask',mask)
		cv2.imshow('frame',frame) 
		if key == 27:
			cap.release()
			cv2.destroyAllWindows()
			break
