from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import datetime
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
import pandas as pd
import datetime
import time
#from PIL import ImageTk, Image
#from gender_prediction import emotion,ageAndgender
names = set()


class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        # with open("./nameslist.txt", "r") as f:
        #     x = f.read()
        #     z = x.rstrip().split(" ")
        #     for i in z:
        #         names.add(i)
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d');
        attendance = pd.read_excel(".\Attendance\L06.xlsx");
        columnNames = attendance['Name'].tolist();
        if len(columnNames) == 0:
            names.add(" ");
        else:
            names = set(columnNames)
        w = 500
        h = 300
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.destroy()


class StartPage(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='./homepagepic.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font,fg="#263942")
            label.grid(row=0, sticky="ew")
            button1 = tk.Button(self, text="   Add a User  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
            button4 = tk.Button(self, text="   Train Data  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageFive"))
            button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
            button1.grid(row=1, column=0, ipady=2, ipadx=7)
            button4.grid(row=2, column=0, ipady=2, ipadx=7)
            button2.grid(row=3, column=0, ipady=2, ipadx=7)
            button3.grid(row=4, column=0, ipady=2, ipadx=7)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure start page?"):
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.new_user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.new_user_name.grid(row=0, column=1, pady=10, padx=10)

        # self.menuvar = tk.StringVar(self)
        # tk.Label(self, text="Select one name", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=0, pady=10, padx=5)
        # self.dropdown = tk.OptionMenu(self, self.user_name, *names)
        # self.dropdown.config(bg="lightgrey")
        # self.dropdown["menu"].config(bg="lightgrey")
        # self.dropdown.grid(row=1, column=1, ipadx=8, padx=10, pady=10)

        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=2, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=2, column=1, pady=10, ipadx=5, ipady=4)
    def start_training(self):
        global names
        if self.new_user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.new_user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.new_user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.new_user_name.get()
        names.add(name)
        attendance = pd.read_excel(".\Attendance\L06.xlsx");
        attendance.loc[len(attendance), ['Name', 'Train Data']] = [name] + [0];
        fileName=".\Attendance\L06.xlsx"
        writer = pd.ExcelWriter(fileName,engine='xlsxwriter');
        attendance.to_excel(writer, engine='xlsxwriter', index=False)
        writer.save();

        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        attendance = pd.read_excel(".\Attendance\L06.xlsx");
        userTrain = attendance.loc[attendance['Train Data'] == 1, ['Name']]['Name'].tolist();
        
        if len(userTrain) == 0:
            userTrain = [' ']

        # global names
        self.controller = controller
        date_object = datetime.date.today()
        label = tk.Label(self, text="Date :", fg="#263942" , font='Helvetica 12 bold').grid(row=0, column=2, padx=10, pady=10)
        labe2 = tk.Label(self, text= date_object, fg="#263942" , font='Helvetica 12 bold').grid(row=0, column=3, padx=10, pady=10)
        tk.Label(self, text="Select user", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *userTrain)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self ):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
       
        # if self.controller.num_of_images < 300:
        #     messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
        #     return
        train_classifer(self.controller.active_name)
        attendance = pd.read_excel(".\Attendance\L06.xlsx");
        attendance.loc[attendance['Name'] == self.controller.active_name, ['Train Data']] = [1];
        fileName=".\Attendance\L06.xlsx"
        writer = pd.ExcelWriter(fileName,engine='xlsxwriter');
        attendance.to_excel(writer, engine='xlsxwriter', index=False)
        writer.save();
        messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)
    #def gender_age_pred(self):
     #  ageAndgender()
    #def emot(self):
     #   emotion()

class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Train Data", font='Helvetica 16 bold')
        # self.new_user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        # self.new_user_name.grid(row=0, column=1, pady=10, padx=10)

        attendance = pd.read_excel(".\Attendance\L06.xlsx");
        userNoTrain = attendance.loc[attendance['Train Data'] == 0, ['Name']]['Name'].tolist();
        print(userNoTrain)
        if len(userNoTrain) == 0:
            userNoTrain = [" "]
        # fileName=".\Attendance\L06.xlsx"
        # writer = pd.ExcelWriter(fileName,engine='xlsxwriter');
        # attendance.to_excel(writer, engine='xlsxwriter', index=False)
        # writer.save();


        self.user_name = tk.StringVar(self)
        tk.Label(self, text="Select one name", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=0, pady=10, padx=5)
        self.dropdown = tk.OptionMenu(self, self.user_name, *userNoTrain)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.dropdown.grid(row=1, column=1, ipadx=8, padx=10, pady=10)

        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=2, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=2, column=1, pady=10, ipadx=5, ipady=4)
    def start_training(self):
        name = self.user_name.get()
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='./icon.ico'))
app.mainloop()

