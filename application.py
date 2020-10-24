import cv2
import tkinter as tk
import numpy as np
import pandas as pd
import datetime
import time
from tkinter import font as tkfont
from tkinter import messagebox, PhotoImage, filedialog
from PIL import Image, ImageTk
from helpers import no_accent_vietnamese
import os


filePathClass = ""
fileNameClass = ""
listStudentDataFrame = None

class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        width = 1000
        height = 600
        widthScreen = self.winfo_screenwidth()
        heightScreen = self.winfo_screenheight()
        x = (widthScreen/2) - (width/2)
        y = (heightScreen/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Điểm danh lớp học")
        self.resizable(False, False)
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for Frame in (StartPage, PageOne, PageTwo, PageFour):
            pageName = Frame.__name__
            frame = Frame(parent=container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame("StartPage")
        # self.protocol("WM_DELETE_WINDOW", self.on_closing);

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

    def saveExcel(self):
        writer = pd.ExcelWriter(filePathClass,engine='xlsxwriter')
        listStudentDataFrame.to_excel(writer, engine='xlsxwriter', index=False)
        writer.save()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        imageBg = ImageTk.PhotoImage(Image.open('./images-app/homepagepic.png').resize((300, 300)))
        backgroundLabel = tk.Label(self, image=imageBg, width=550, height=550)
        backgroundLabel.image = imageBg
        backgroundLabel.grid(row=0, column=0, rowspan=100,sticky="nsew")
        titleApp = tk.Label(self, text="Ứng dụng điểm danh sinh viên", font=self.controller.title_font,fg="#263942")
        titleApp.grid(row=20, column=1, sticky="nsew",columnspan=1000)
        fontNomal = tkfont.Font(family='Helvetica', size=13)
        fontNomalUnderLine = tkfont.Font(family='Helvetica', size=13)
        fontNomalUnderLine.configure(underline = True)
        labelNameListStudent = tk.Label(self, text="Danh sách lớp đang chọn: ", font=fontNomal)
        labelNameListStudent.grid(row=30, column=1, rowspan=1)
        nameListStudent = tk.Label(self, text="chưa chọn danh sách", font=fontNomalUnderLine)
        nameListStudent.grid(row=30, column=2, columnspan=10, rowspan=1)
        button2 = tk.Button(self, text="Chọn danh sách lớp", fg="#ffffff", bg="#007bff", height=2, font=fontNomal ,command = lambda:chooseFileClass(), width=30)
        button2.grid(row=40, column=1,columnspan=5, sticky="nsew", padx=50)
        button3 = tk.Button(self, text="Thêm vào sinh viên vào danh sách", fg="#ffffff", bg="#007bff", height=2, font=fontNomal, width=30,command=lambda:showFrameAddStudent())
        button3.grid(row=50, column=1,columnspan=5, sticky="nsew", padx=50)
        button4 = tk.Button(self, text="Thêm dữ liệu khuôn mặt sinh viên", fg="#ffffff", bg="#007bff", height=2, font=fontNomal, width=30, command=lambda:addDataTrainFace())
        button4.grid(row=60, column=1,columnspan=5, sticky="nsew", padx=50)
        button5 = tk.Button(self, text="Điểm danh", fg="#ffffff", bg="#007bff", height=2, font=fontNomal, width=30, command=lambda:attendanceStudent())
        button5.grid(row=70, column=1,columnspan=5, sticky="nsew", padx=50)
        button6 = tk.Button(self, text="Thoát", fg="#000000", bg="#ffffff", height=2, font=fontNomal, width=30, command=lambda: self.controller.destroy())
        button6.grid(row=80, column=1,columnspan=5, sticky="nsew", padx=50)

        def chooseFileClass():
            file = filedialog.askopenfile(mode ='r', filetypes =[("Excel files", "*.xlsx")]) 
            if file is not None: 
                global filePathClass, fileNameClass, listStudentDataFrame
                filePathClass = file.name
                fileNameFolder = file.name.split("/")
                fileName = fileNameFolder[len(fileNameFolder)-1]
                nameListStudent.config(text=fileName)
                fileNameClass = fileName
                listStudentDataFrame = pd.read_excel(filePathClass);
                checkColumnTrainData()
                checkColumnDate()
        
        def addDataTrainFace():
            if checkFileClass():
                numberSvTrain = len(listStudentDataFrame.loc[listStudentDataFrame['CV6'] <= 0]);
                if numberSvTrain == 0:
                    messagebox.showerror("Có lỗi xảy ra", "Tất cả sinh viên đã được thêm dữ liệu")
                    return
                self.controller.frames["PageTwo"].getListStudent()
                self.controller.showFrame("PageTwo")

        def checkFileClass():
            global filePathClass, fileNameClass, listStudentDataFrame
            if filePathClass == "":
                messagebox.showerror("Có lỗi xảy ra", "Vui lòng chọn danh sách lớp")
                return False
            if len(listStudentDataFrame) <= 0:
                messagebox.showerror("Có lỗi xảy ra", "Chưa có sinh viên trong danh sách")
                return False
            return True
        
        def showFrameAddStudent():
            if filePathClass != "":
                self.controller.showFrame("PageOne")
            else:
                messagebox.showerror("Có lỗi xảy ra", "Vui lòng chọn danh sách lớp")
                return
        
        def attendanceStudent():
            if checkFileClass():
                numberSvTrain = len(listStudentDataFrame.loc[listStudentDataFrame['CV6'] > 0]);
                if numberSvTrain == 0:
                    messagebox.showerror("Có lỗi xảy ra", "Chưa sinh viên nào được thêm dữ liệu")
                    return;
                else:
                    self.controller.frames["PageFour"].getListStudent()
                    checkColumnDate()
                    self.controller.showFrame("PageFour")

        def checkColumnDate():
            global filePathClass, fileNameClass, listStudentDataFrame
            ts = time.time()      
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            columnNames = set()
            for col in listStudentDataFrame.columns: 
                if isinstance(col,datetime.datetime):
                    columnNames.add(col.strftime('%Y-%m-%d'))
                else:
                    columnNames.add(col)
            isTodayInList = date in columnNames
            if not isTodayInList:
                listStudentDataFrame[date] = None
                self.controller.saveExcel()
        
        def checkColumnTrainData():
            columns = list(listStudentDataFrame.columns)
            checkColumn = "CV6" in columns
            if not checkColumn:
                listStudentDataFrame['CV6'] = None
                if len(listStudentDataFrame) > 0:
                    listStudentDataFrame['CV6'] = 0;
                self.controller.saveExcel()
            else:
                listStudentDataFrame.loc[listStudentDataFrame['CV6'] != 1, ['CV6']] = 0
                self.controller.saveExcel()
        

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        imageBg = ImageTk.PhotoImage(Image.open('./images-app/homepagepic.png').resize((300, 300)))
        backgroundLabel = tk.Label(self, image=imageBg, width=550, height=550)
        backgroundLabel.image = imageBg
        backgroundLabel.grid(row=0, column=0, rowspan=100,sticky="nsew")
        titleApp = tk.Label(self, text="Ứng dụng điểm danh sinh viên", font=self.controller.title_font,fg="#263942")
        titleApp.grid(row=20, column=1, sticky="nsew",columnspan=1000)
        fontNomal = tkfont.Font(family='Helvetica', size=13)
        fontNomalUnderLine = tkfont.Font(family='Helvetica', size=13)
        fontNomalUnderLine.configure(underline = True)

        tk.Label(self, text="Nhập tên sinh viên", font =('Helvetica', 18)).grid(row=29, column=1)
        self.newUserName = tk.Entry(self, borderwidth=0, bg="lightgrey", font =('Helvetica', 18), width=25,justify="center")
        self.newUserName.grid(row=30, column=1,  padx=50)

        button2 = tk.Button(self, text="Thêm vào sinh viên vào danh sách", fg="#ffffff", bg="#007bff", height=2, font=fontNomal, width=30, command=lambda: self.addStudent())
        button2.grid(row=40, column=1,columnspan=5, sticky="nsew", padx=50)
        # button2 = tk.Button(self, text="Thêm dữ liệu khuôn mặt sinh viên", fg="#ffffff", bg="#007bff", height=2, font=fontNomal, width=30)
        # button2.grid(row=50, column=1,columnspan=5, sticky="nsew", padx=50)
        button2 = tk.Button(self, text="Trang chủ", fg="#000000", bg="#ffffff", height=2, font=fontNomal, width=30,command=lambda: controller.showFrame("StartPage"))
        button2.grid(row=60, column=1,columnspan=5, sticky="nsew", padx=50)

    def checkUserName(self):
        if self.newUserName.get() == "None" or len(self.newUserName.get()) == 0:
            messagebox.showerror("Có lỗi xảy ra", "Tên không được để trống")
            return False
        numberSv = len(listStudentDataFrame.loc[listStudentDataFrame['Họ Và Tên'] == self.newUserName.get()]);
        if numberSv > 0:
            messagebox.showerror("Có lỗi xảy ra", "Tên sinh viên đã tồn tại")
            return False
        return True
    def addStudent(self):
        global filePathClass, fileNameClass, listStudentDataFrame
        if self.checkUserName():
            listStudentDataFrame.loc[len(listStudentDataFrame), ['Họ Và Tên', 'CV6']] = [self.newUserName.get()] + [0]
            self.controller.saveExcel()
            messagebox.showinfo("Thành công", "Thêm mới sinh viên thành công")
            self.newUserName.delete(0,len(self.newUserName.get()))

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        imageBg = ImageTk.PhotoImage(Image.open('./images-app/homepagepic.png').resize((300, 300)))
        self.backgroundLabel = tk.Label(self, image=imageBg, width=550, height=550)
        self.backgroundLabel.image = imageBg
        self.backgroundLabel.grid(row=0, column=0, rowspan=100,sticky="nsew")
        titleApp = tk.Label(self, text="Thêm dữ liệu khuôn mặt sinh viên", font=self.controller.title_font,fg="#263942")
        titleApp.grid(row=20, column=1, sticky="nsew",columnspan=1000)
        fontNomal = tkfont.Font(family='Helvetica', size=13)
        fontNomalUnderLine = tkfont.Font(family='Helvetica', size=13)
        fontNomalUnderLine.configure(underline = True)
        self.activeNameStudent = tk.StringVar(self)
        button2 = tk.Button(self, text="Thêm khuôn mặt", fg="#ffffff", bg="#007bff", height=2, font=fontNomal, width=30, command=lambda:self.startCapture())
        button2.grid(row=40, column=1,columnspan=5, sticky="nsew", padx=50)
        button2 = tk.Button(self, text="Train dữ liệu", fg="#ffffff", bg="#007bff", height=2, font=fontNomal, width=30, command=lambda:self.trainClassifer())
        button2.grid(row=50, column=1,columnspan=5, sticky="nsew", padx=50)
        button2 = tk.Button(self, text="Trang chủ", fg="#000000", bg="#ffffff", height=2, font=fontNomal, width=30,command=lambda: controller.showFrame("StartPage"))
        button2.grid(row=60, column=1,columnspan=5, sticky="nsew", padx=50)

    def getListStudent(self):
        global filePathClass, fileNameClass, listStudentDataFrame
        fontNomal = tkfont.Font(family='Helvetica', size=13)
        tk.Label(self, text="Chọn sinh viên", font =('Helvetica', 18)).grid(row=29, column=3)
        listStudent = listStudentDataFrame.loc[listStudentDataFrame['CV6'] == 0, ['Họ Và Tên']]['Họ Và Tên'].tolist()
        self.activeNameStudent.set(listStudent[0])
        self.dropdown = tk.OptionMenu(self, self.activeNameStudent, *listStudent)
        self.dropdown.config(bg="lightgrey", width=26, height=2, font=fontNomal)
        self.dropdown["menu"].config(bg="lightgrey", font=fontNomal)
        self.dropdown.grid(row=30, column=3)

    def startCapture(self):
        if self.activeNameStudent.get() == "None" or len(self.activeNameStudent.get()) == 0:
            messagebox.showerror("Lỗi", "Tên không được để trống")
            return
        nameStudent = no_accent_vietnamese(self.activeNameStudent.get()).replace(" ", "_");
        path = "./data/" + nameStudent;
        num_of_images = 0
        detector = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")
        print(path)
        try:
            os.makedirs(path)
        except:
            print('Directory Already Created')
        vid = cv2.VideoCapture(0)
        while True:
            ret, img = vid.read()
            new_img = None
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
            for x, y, w, h in face:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
                cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                cv2.putText(img, str(str(num_of_images)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                new_img = grayimg[y:y+h, x:x+w]
            cv2.imshow("FaceDetection", img)
            key = cv2.waitKey(1) & 0xFF
            try :
                cv2.imwrite(str(path+"/"+str(num_of_images)+'_'+nameStudent+".jpg"), new_img)
                num_of_images += 1
            except :
                pass
            if key == ord("q") or key == 27 or num_of_images > 299:
                break
        cv2.destroyAllWindows()
        messagebox.showinfo("Thành công", "Lấy dữ liệu khuôn mặt thành công")

    def trainClassifer(self):
        global filePathClass, fileNameClass, listStudentDataFrame
        nameStudent = no_accent_vietnamese(self.activeNameStudent.get()).replace(" ", "_");
        path = os.path.join(os.getcwd()+"/data/"+nameStudent+"/")

        faces = []
        ids = []
        labels = []
        pictures = {}
        for root,dirs,files in os.walk(path):
                pictures = files

        for pic in pictures :

                imgpath = path+pic
                img = Image.open(imgpath).convert('L')
                imageNp = np.array(img, 'uint8')
                id = int(pic.split("_")[0])
                #names[name].append(id)
                faces.append(imageNp)
                ids.append(id)

        ids = np.array(ids)
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("./data/"+nameStudent+"_classifier.xml")
        listStudentDataFrame.loc[listStudentDataFrame['Họ Và Tên'] == self.activeNameStudent.get(), ['CV6']] = [1];
        self.controller.saveExcel()
        messagebox.showinfo("Thành công", "Train dữ liệu thành công")
        self.controller.showFrame("StartPage")

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        imageBg = ImageTk.PhotoImage(Image.open('./images-app/homepagepic.png').resize((300, 300)))
        self.backgroundLabel = tk.Label(self, image=imageBg, width=550, height=550)
        self.backgroundLabel.image = imageBg
        self.backgroundLabel.grid(row=0, column=0, rowspan=100,sticky="nsew")
        titleApp = tk.Label(self, text="Điểm danh sinh viên", font=self.controller.title_font,fg="#263942")
        titleApp.grid(row=20, column=1, sticky="nsew",columnspan=1000)
        fontNomal = tkfont.Font(family='Helvetica', size=13)
        fontNomalUnderLine = tkfont.Font(family='Helvetica', size=13)
        fontNomalUnderLine.configure(underline = True)
        self.activeNameStudent = tk.StringVar(self)
        button2 = tk.Button(self, text="Điểm danh", fg="#ffffff", bg="#007bff", height=2, font=fontNomal, width=30,command=lambda: self.attendance())
        button2.grid(row=40, column=1,columnspan=5, sticky="nsew", padx=50)
        button2 = tk.Button(self, text="Trang chủ", fg="#000000", bg="#ffffff", height=2, font=fontNomal, width=30,command=lambda: controller.showFrame("StartPage"))
        button2.grid(row=60, column=1,columnspan=5, sticky="nsew", padx=50)
    def getListStudent(self):
        global filePathClass, fileNameClass, listStudentDataFrame
        fontNomal = tkfont.Font(family='Helvetica', size=13)
        tk.Label(self, text="Chọn sinh viên", font =('Helvetica', 18)).grid(row=29, column=3)
        listStudent = listStudentDataFrame.loc[listStudentDataFrame['CV6'] == 1, ['Họ Và Tên']]['Họ Và Tên'].tolist()
        self.activeNameStudent.set(listStudent[0])
        self.dropdown = tk.OptionMenu(self, self.activeNameStudent, *listStudent)
        self.dropdown.config(bg="lightgrey", width=26, height=2, font=fontNomal)
        self.dropdown["menu"].config(bg="lightgrey", font=fontNomal)
        self.dropdown.grid(row=30, column=3)
    
    def changeImage(self, image):
        self.backgroundLabel.image = image
        self.backgroundLabel.config(image=image)

    def attendance(self):
        global filePathClass, fileNameClass, listStudentDataFrame
        studentNameFolder = no_accent_vietnamese(self.activeNameStudent.get()).replace(" ", "_");
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(f"./data/{studentNameFolder}_classifier.xml")
        cap = cv2.VideoCapture(0)
        pred = 0

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
                print(id)
                if confidence > 50:
                    #if u want to print confidence level
                            #confidence = 100 - int(confidence)
                            pred += +1
                            text = no_accent_vietnamese(self.activeNameStudent.get()).upper();
                            font = cv2.FONT_HERSHEY_PLAIN
                            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                            ts = time.time()   
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d');
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            # attendance.loc[len(attendance)] = [name] + [date] + [timeStamp] + ['x'];
                            listStudentDataFrame.loc[listStudentDataFrame['Họ Và Tên'] == self.activeNameStudent.get() , [date]] = [1];
                else:   
                            pred += -1
                            text = "UnknownFace"
                            font = cv2.FONT_HERSHEY_PLAIN
                            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)
            cv2.imshow("image", frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        self.controller.saveExcel();  
        cap.release()
        cv2.destroyAllWindows()

app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='./images-app/icon.ico'))
app.mainloop()
