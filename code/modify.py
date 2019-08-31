import cv2
import numpy as np
import math

bg = None

def run_avg(image, aWeight):
	global bg
	if bg is None:
		bg = image.copy().astype("float")
		return
	cv2.accumulateWeighted(image, bg, aWeight)

def segment(image, threshold = 25):
	global bg
	diff = cv2.absdiff(bg.astype("uint8"), image)
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

def compare_area(roi1, roi2, cut_flag):
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

if __name__ == "__main__":
	cap = cv2.VideoCapture(0)
	width = cap.get(3)
	height = cap.get(4)
	width -= 15
	height -= 15
	min_x = 0
	min_y = 0
	max_x = 100
	max_y = 100
	status = 0
	ok_num = 0
	frame_num = 0
	num_frames = 0
	aWeight = 0.5
	font = cv2.FONT_HERSHEY_SIMPLEX
	leave_times = 1
	leave_num = 3
	while True:
		ok_flag = False
		ret, frame = cap.read()
		
		# mirror the camera
		frame=cv2.flip(frame,1)
		
		# draw the range of image
		cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0,255,0), 2)
		
		# define the range you interest
		roi = frame[min_y:max_y, min_x:max_x]
		key = cv2.waitKey(25) & 0xFF
		
		text = np.zeros((400,800,3), np.uint8)
		text.fill(255)
		
		if status == 0:
			cv2.putText(text,'Press WASD to move the square',(10,50), font, 1, (0,0,255), 2, cv2.LINE_AA)
			cv2.putText(text,'Press QE to change square size',(10,100), font, 1, (0,0,255), 2, cv2.LINE_AA)
			cv2.putText(text,'Press SPACE to check the position of the square',(10,150), font, 1, (0,0,255), 2, cv2.LINE_AA)
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
					max_x -= 15
					max_y -= 15
			elif key == 32:
				status += 1

		elif status == 1 or status == 2 or status == 3:
			cv2.imshow("roi", roi)

			gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (7,7), 0)
			if num_frames < 100:
				if leave_times < 90:
					if leave_times % 30 == 0:
						leave_num -= 1
					leave_times += 1
					cv2.putText(text,'Leave the square',(10,50), font, 1, (0,0,255), 2, cv2.LINE_AA)
					cv2.putText(text,str(leave_num),(10,100), font, 1, (0,0,255), 2, cv2.LINE_AA)
				else:
					run_avg(gray, aWeight)
					num_frames += 1
					cv2.putText(text,'Waiting for running average of background',(10,50), font, 1, (0,0,255), 2, cv2.LINE_AA)
					cv2.putText(text,str(num_frames) + "%",(10,100), font, 1, (0,0,255), 2, cv2.LINE_AA)
			else:
				cv2.putText(text,'Use your gesture to control the position of camera',(10,50), font, 1, (0,0,255), 2, cv2.LINE_AA)
				hand = segment(gray)
				if hand is not None:
					(mask, cnt) = hand

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
					cv2.circle(roi, (cX,cY), 3, [0,0,255], -1)			
					# Cutting the contour by cX and cY and find two smaller area
					mode = 'none'
					if arearatio > 12:
						mode = 'none'
						roi_x = max_x-min_x
						roi_y = max_y-min_y
						if cut_flag == 'u_d':
						# case up and down, only cut cY
							roi1 = mask[0:cY, 0:roi_x]
							roi2 = mask[cY:roi_y, 0:roi_x]
						elif cut_flag == 'l_r':
							# case left and right, only cut cX
							roi1 = mask[0:roi_y, 0:cX]
							roi2 = mask[0:roi_y, cX:roi_x]
						mode = compare_area(roi1, roi2, cut_flag)
						cv2.imshow('roi1',roi1)
						cv2.imshow('roi2',roi2)
		
					#find the defects in convex hull with respect to hand
					hull = cv2.convexHull(approx, returnPoints=False)
					defects = cv2.convexityDefects(approx, hull)
		
					# l = no. of defects
					l = 0
		
					#code for finding no. of defects due to fingers
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
			
						#print corresponding gestures which are in their ranges
						if l == 1:
							if areacnt < 2000:
								cv2.putText(frame,'Put hand in the box',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
							else:
								if arearatio < 12 and status == 3:
									cv2.putText(frame,'O',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
									status = 0
								elif status == 1 or status == 3:
									if status == 1:
										cv2.putText(frame,mode,(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
										print(mode)
									else:
										if mode == 'up':
											cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
											status = 2
						elif l == 3:
							cv2.putText(frame,'ok',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
							ok_flag = True
							ok_num += 1
							frame_num = 0
							print("ok")
							if ok_num == 30:
								status += 1
								ok_num = 0
						else :
							cv2.putText(frame,'reposition',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
						#show the windows
						cv2.imshow('mask',mask)
						if ok_flag == False:
							frame_num += 1
							if frame_num == 5:
								ok_num = 0
		elif status == 4:
			cap.release()
			cv2.destroyAllWindows()
			break
		cv2.imshow('frame',frame)
		cv2.imshow("text", text)
		print(status)	
		if key == 27:
			cap.release()
			cv2.destroyAllWindows()
			break
