import numpy as np
import cv2
import imutils
from sklearn.metrics import pairwise

bg = None

def run_avg(image, aWeight):
	global bg
	# initialize the background
	if bg is None:
		bg = image.copy().astype("float")
		return
	# compute weighted average, accumulate it and update the background
	cv2.accumulateWeighted(image, bg, aWeight)

def segment(image, threshold=25):
	global bg
	# find the absolute difference between background and current frame
	diff = cv2.absdiff(bg.astype("uint8"), image)
	# threshold the diff image so that we get the foreground
	thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
	# get the contours in the thresholded image
	kernel = np.ones((3,3),np.uint8)
	thresholded = cv2.dilate(thresholded,kernel,iterations = 4)
	thresholded = cv2.GaussianBlur(thresholded,(5,5),100)
	cnts,_ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# return None, if no contours detected
	if len(cnts) == 0:
		return
	else:
		# based on contour area, get the maximum contour which is the hand
		segmented = max(cnts, key=cv2.contourArea)
		return (thresholded, segmented)

def count(thresholded, segmented):
	# find the convex hull of the segmented hand region
	chull = cv2.convexHull(segmented)
	
	# find the most extreme points in the convex hull
	extreme_top    = tuple(chull[chull[:, :, 1].argmin()][0])
	extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
	extreme_left   = tuple(chull[chull[:, :, 0].argmin()][0])
	extreme_right  = tuple(chull[chull[:, :, 0].argmax()][0])

	# find the maximum euclidean distance between the center of the palm
	# and the most extreme points of the convex hull
	distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
	maximum_distance = distance[distance.argmax()]
	
	# calculate the radius of the circle with 80% of the max euclidean distance obtained
	radius = int(0.8 * maximum_distance)

	# find the circumference of the circle
	circumference = (2 * np.pi * radius)

	# take out the circular region of interest which has 
	# the palm and the fingers
	circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
	
	# draw the circular ROI
	cv2.circle(circular_roi, (cX, cY), radius, 255, 1)

	# take bit-wise AND between thresholded hand using the circular ROI as the mask
	# which gives the cuts obtained using mask on the thresholded hand image
	circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

	# compute the contours in the circular ROI
	(_, cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# initalize the finger count
	count = 0

	# loop through the contours found
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)

        # increment the count of fingers only if -
        # 1. The contour region is not the wrist (bottom area)
        # 2. The number of points along the contour does not exceed
        #     25% of the circumference of the circular ROI
        if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
            count += 1

    return count	

if __name__ == "__main__":
	aWeight = 0.5
	num_frames = 0

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
		image_np = cv2.flip(frame,1)
		cv2.rectangle(image_np, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
		crop_img = image_np[min_y:max_y, min_x:max_x]
		key = cv2.waitKey(25) & 0xFF
		if status == 0:
			# select range
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
				status += 1;
		elif status == 1:
			(height, width) = frame.shape[:2]
			gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (7,7), 0)
			if num_frames < 30:
				run_avg(gray, aWeight)
			else:
				hand = segment(gray)
				if hand is not None:
					(thresholded, segmented) = hand
					cv2.drawContours(image_np, [segmented + (min_x, min_y)], -1, (0,0,255))
					cv2.imshow("Thersholded", thresholded)
			num_frames += 1
		if key == 27:
			cap.release()
			cv2.destroyAllWindows()
			break
		cv2.imshow('camera', image_np)
		cv2.imshow('crop', crop_img)


