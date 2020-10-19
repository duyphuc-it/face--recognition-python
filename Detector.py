import cv2
from time import sleep
from PIL import Image 
import pandas as pd
import datetime
import time
from helpers import no_accent_vietnamese

def main_app(name):
        new_name = no_accent_vietnamese(name).replace(" ", "_");
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(f".\\data\\{new_name}_classifier.xml")
        cap = cv2.VideoCapture(0)
        pred = 0
        # col_names =  ['Name','Date','Time']
        # attendance = pd.DataFrame(columns = list(col_names))    
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d');
        attendance = pd.read_excel(".\Attendance\L06.xlsx");
        
        columnNames = set();
        for col in attendance.columns: 
            if isinstance(col,datetime.datetime):
                columnNames.add(col.strftime('%Y-%m-%d'));
            else:
                columnNames.add(col)
        isTodayInList = date in columnNames;

        if not isTodayInList:
            attendance[date] = None;



        while True:
            ret, frame = cap.read()
            #default_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5)
           
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]

                id,confidence = recognizer.predict(roi_gray)
                confidence = 100 - int(confidence)
                pred = 0
                if confidence > 50:
                    #if u want to print confidence level
                            #confidence = 100 - int(confidence)
                            pred += +1
                            text = no_accent_vietnamese(name).upper();
                            font = cv2.FONT_HERSHEY_PLAIN
                            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                            ts = time.time()   
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d');
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            # attendance.loc[len(attendance)] = [name] + [date] + [timeStamp] + ['x'];
                            attendance.loc[attendance['Name'] == name , [date]] = [1];
                else:   
                            pred += -1
                            text = "UnknownFace"
                            font = cv2.FONT_HERSHEY_PLAIN
                            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)
            cv2.imshow("image", frame)


            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName=".\Attendance\L06.xlsx"
        writer = pd.ExcelWriter(fileName,engine='xlsxwriter');
        attendance.to_excel(writer, engine='xlsxwriter', index=False)
        writer.save()
        cap.release()
        cv2.destroyAllWindows()
        
