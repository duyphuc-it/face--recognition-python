import cv2
import numpy as np 
import sqlite3
import os

def insertOrupdate(id, name):
	conn = sqlite3.connect('D:\\Học tập\\Thực tập cơ sở chuyên ngành\\data.db')
	query = 'SELECT * FROM people WHERE ID='+ str(id)
	cusor = conn.execute(query)
	isRecordExist = 0
	for row in cusor:
		isRecordExist = 1
	if(isRecordExist == 0):
		query = "INSERT INTO people(ID,Name) VALUES("+str(id)+",'"+ str(name)+ "')"
	else :
		query = "UPDATE people SET Name ='"+str(name)+"' WHERE ID="+str(id)
	conn.execute(query)	
	conn.commit()
	conn.close()

# load tv 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)	

#insert to db
id = input("Enter your id: ")
name = input("Enter your Name: ")	
insertOrupdate(id, name)

sampleNum = 0

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

		if not os.path.exists('dataSet'):
			os.makedirs('dataSet')
		sampleNum +=1

		cv2.imwrite('dataSet\\User.'+str(id)+'.'+ str(sampleNum)+ '.jpg', gray[y: y+h, x: x+w])
	cv2.imshow('frame', frame)
	cv2.waitKey(1)	
	if sampleNum > 500 :
		break

cap.release()
cv2.destroyAllWindows()


