import serial
import sys
import cv2

cap = cv2.VideoCapture(0)
COM_PORT = '/dev/ttyUSB0'
BAUD_RATES = 9600
ser = serial.Serial(COM_PORT, BAUD_RATES)
prev = '0'
count = 0
non_status = 1
try:
	while True:
		ret, frame = cap.read()
		image_np = cv2.flip(frame, 1)
		cv2.imshow('camera', image_np)
		key = cv2.waitKey(25) & 0xFF
		if key == ord('q'):
#			count+=1;
#			if count % 2 == 0:
			if prev != 'q' or non_status == 1:
				ser.write(b'Q message\n')
				prev = 'q'
			count = 0
		elif key == ord('e'):
			if prev != 'e' or non_status == 1:
#			count+=1;
#			if count %2 == 0:
				ser.write(b'E message\n')
				prev = 'e'
			count = 0
		elif key == ord('a'):
			if prev != 'a' or non_status == 1:
				ser.write(b'A message\n')
				prev = 'a'
			count = 0
		elif key == ord('d'):
			if prev != 'd' or non_status == 1:
				ser.write(b'D message\n')
				prev = 'd'
			count = 0
		else:
			count += 1;
			if count == 2:
				ser.write(b'Non message\n');
		#		prev = 'n';
				count = 0
				non_status = 1


except KeyboardInterrupt:
	ser.close()
	print("bye")
