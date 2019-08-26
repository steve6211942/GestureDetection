import numpy as np
import cv2
import imutils

bg = None

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
	start = 0
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
			if start == 0:
				first = crop_img
				second = crop_img
				start = 1
			else:
				second = crop_img
			diff = cv2.absdiff(first, second)
			gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (5,5), 0)
			ret2,thresh1 = cv2.threshold(gray,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
			cv2.imshow('threshold', thresh1)
			first = crop_img
		if key == 27:
			cap.release()
			cv2.destroyAllWindows()
			break
		cv2.imshow('camera', image_np)
		cv2.imshow('crop', crop_img)

