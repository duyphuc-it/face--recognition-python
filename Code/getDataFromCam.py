import cv2
import numpy as np 

# thư viện khuôn mặt mặc định của opencv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#Truy cập vào webcam 
cap = cv2.VideoCapture(0)

while(True):
# ret trả về true nếu truy cập thành công 
# frame trả về dữ liệu lấy từ webcam
	ret, frame = cap.read()
# chuyển ảnh về ảnh xám 
# cvtColor là convert to Color 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3,5)
# vẽ hình vuông bao quanh khuôn mặt xác định đc
	for(x, y, w, h) in faces:

		cv2.rectangle(frame, (x,y), (x+w, y+h) , (0,225,0), 2)

	cv2.imshow('DETECTING FACE', frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break

cap.release()
cv2.destroyAllWindows()		
