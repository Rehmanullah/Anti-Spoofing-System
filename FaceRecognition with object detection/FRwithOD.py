import cv2
import face_recognition
import numpy as np
import os
import time
# import matplotlib.pyplot as plt
from tkinter.font import BOLD
from tkinter import *
import pywhatkit as pwk
from student import Student
from tkinter import Button, Label, Toplevel, Tk, ttk
from PIL import Image, ImageTk
from tkinter import messagebox

from datetime import datetime
from PIL import Image, ImageDraw

import mysql.connector

import pyttsx3
from ultralytics import YOLO
import cvzone
import math
# from sort import *

class Face_Recognition_Class:
    def __init__(self, root):
        self.root = root
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()

        self.root.geometry("%dx%d0+0+0" % (w, h))

        self.root.engine = pyttsx3.init('sapi5')
        voices = self.root.engine.getProperty('voices')
        self.root.engine.setProperty('voice', voices[0].id)

        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()

        self.root.geometry("%dx%d0+0+0" % (w, h))
        # self.root.resizable(0,0)
        self.root.title("Face Recognition System")
        bg = "bisque"
        fg = "black"
        # bg image
        img3 = Image.open("bg.jpg")
        #img3 = img3.resize((w, h), Image.ANTIALIAS)
        img3 = img3.resize((w, h), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_image = Label(self.root, image=self.photoimg3)
        bg_image.place(x=0, y=80, width=w, height=h)

        self.root.engine.say("welcome to face recognition system")
        self.root.engine.runAndWait()

        self.root.var_std_name = StringVar()
        self.root.var_std_id = StringVar()

        # title on window
        title_lbl = Label(self.root, text="Anti-Spoofing System using Facial Recognition", font=("Helvetica", 35, "bold"),
                          bg="#000011", fg="white")
        title_lbl.place(x=0, y=0, width=w, height=70)

        Train_btn = Button(self.root, text="HOG", command=self.face_recog_hog, font=("times new roman", 30, "bold"),
                           bg=bg, fg=fg, cursor="hand1")
        Train_btn.place(x=950, y=500, width=250, height=70)

        Train_btn = Button(self.root, text="CNN", command=self.face_recog_cnn, font=("times new roman", 30, "bold"),
                           bg=bg, fg=fg)
        Train_btn.place(x=1250, y=500, width=250, height=70)

        reset_btn = Button(self.root, text="Reset", command=self.reset_data, font=("times new roman", 30, "bold"),
                           bg=bg, fg=fg)
        reset_btn.place(x=1150, y=700, width=250, height=70)

        exit_btn = Button(self.root, text="Exit", command=self.exit_all, font=("times new roman", 30, "bold"), bg=bg,
                          fg=fg)
        exit_btn.place(x=1150, y=800, width=250, height=70)

        #show_data_base = Button(self.root, text="DataSet", command=self.student_details,
                                #font=("times new roman", 30, "bold"), bg=bg, fg=fg)
        #show_data_base.place(x=1150, y=500, width=300, height=70)

        save = Button(self.root, text="Save", command=self.add_data, font=("times new roman", 30, "bold"), bg=bg, fg=fg)
        save.place(x=1150, y=600, width=250, height=70)

        student_name_lbl = Label(self.root, text="Enter the Name in the input field",
                                 font=("times new roman", 14, "bold"), bg=bg, fg=fg)
        student_name_lbl.place(x=600, y=150, width=600, height=70)
        student_name_entry = ttk.Entry(self.root, textvariable=self.root.var_std_name, width=20,
                                       font=("times new roman", 12, "bold"))
        student_name_entry.place(x=1250, y=150, width=600, height=70)

        student_id_lbl = Label(self.root, text="Enter the id in the input field", font=("times new roman", 14, "bold"),
                               bg=bg, fg=fg)
        student_id_lbl.place(x=600, y=300, width=600, height=70)
        student_id_entry = ttk.Entry(self.root, textvariable=self.root.var_std_id, width=20,
                                     font=("times new roman", 12, "bold"))
        student_id_entry.place(x=1250, y=300, width=600, height=70)


    def face_recog_hog(self):
        cam = cv2.VideoCapture(0)

        ## for mobile detection
        model = YOLO('../Yolo-weights/yolov8l.pt')


        path = "images"
        images = []
        classNames = []
        myList = os.listdir(path)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])

        def findEncoding(image):
            encodeList = []
            for img in image:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        known_face_encoding = findEncoding(images)

        all_face_locations = []
        all_face_encoding = []

        while True:
            classNameso = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                          "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                          "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
                          "umbrella",
                          "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
                          "baseball bat",
                          "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                          "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                          "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                          "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                          "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                          "teddy bear", "hair drier", "toothbrush"
                          ]
            ret, current_frame = cam.read()
            results = model(current_frame, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1

                    conf = math.ceil(box.conf[0] * 100) / 100
                    cls = int(box.cls[0])
                    currentClass = classNameso[cls]
                    if currentClass in ["cell phone", "laptop"]:
                        cvzone.cornerRect(current_frame, (x1, y1, w, h))

                        messagebox.showerror("Error", "Please don't use phone or laptop ", parent=self.root)
                        self.send_message_obj(current_frame, "this one use a mobile")
                        cam.release()
                        cv2.destroyAllWindows()
                    else:
                        pass
                        # cvzone.putTextRect(current_frame, f'{classNameso[int(cls)]} {conf}', (max(0, x1), max(35, y1)), scale=2,
                        #                thickness=2)


            current_frame_small = cv2.resize(current_frame, (0, 0), fx=0.25, fy=0.25)
            # current_frame_small=cv2.cvtColor(current_frame_small,cv2.COLOR_BGR2GRAY)

            all_face_locations = face_recognition.face_locations(current_frame_small, number_of_times_to_upsample=2,
                                                                 model="hog")

            all_face_encoding = face_recognition.face_encodings(current_frame_small, all_face_locations)

            for current_face_location, current_face_encoding in zip(all_face_locations, all_face_encoding):
                top, right, bottom, left = current_face_location
                top = top * 4
                right = right * 4
                bottom = bottom * 4
                left = left * 4
                all_matches = face_recognition.compare_faces(known_face_encoding, current_face_encoding)
                face_Dist = face_recognition.face_distance(known_face_encoding, current_face_encoding)
                name_of_person = "unknown person"

                if True in all_matches:
                    first_match_index = all_matches.index(True)
                    name_of_person = classNames[first_match_index].upper()

                    conn = mysql.connector.connect(host="localhost", user="root", password="",
                                                   database="facerecognition")
                    my_cursor = conn.cursor()

                    my_cursor.execute("select name from student where id=" + name_of_person)
                    name_of_person = my_cursor.fetchone()
                    name_of_person = '*'.join(name_of_person)

                cv2.rectangle(current_frame, (left, top), (right, bottom + 20), (255, 0, 0), 2)

                cv2.putText(current_frame, str(name_of_person), (left, bottom), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 2)

            cv2.putText(current_frame, str(face_Dist), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
            cv2.imshow('Person Identified', current_frame)



            if name_of_person == 'unknown person':
                self.send_message(current_frame, name_of_person)
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()



    def face_recog_cnn(self):

        cam = cv2.VideoCapture(0)
        model = YOLO('../Yolo-weights/yolov8l.pt')
        path = "images"
        images = []
        classNames = []
        myList = os.listdir(path)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])

        def findEncoding(image):
            encodeList = []
            for img in image:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        known_face_encoding = findEncoding(images)

        all_face_locations = []
        all_face_encoding = []

        while True:
            classNameso = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                           "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                           "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
                           "umbrella",
                           "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
                           "baseball bat",
                           "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                           "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                           "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                           "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                           "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                           "teddy bear", "hair drier", "toothbrush"
                           ]

            ret, current_frame = cam.read()
            results = model(current_frame, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1

                    conf = math.ceil(box.conf[0] * 100) / 10
                    cls = int(box.cls[0])
                    currentClass = classNameso[cls]
                    if currentClass in ["cell phone", "laptop"]:
                        cvzone.cornerRect(current_frame, (x1, y1, w, h))

                        messagebox.showerror("Error", "Please don't use phone or laptop ", parent=self.root)
                        self.send_message_obj(current_frame, "This person is using mobile")
                        cam.release()
                        cv2.destroyAllWindows()
                    else:
                        pass

            current_frame_small = cv2.resize(current_frame, (0, 0), fx=0.25, fy=0.25)
            # current_frame_small=cv2.cvtColor(current_frame_small,cv2.COLOR_BGR2GRAY)

            all_face_locations = face_recognition.face_locations(current_frame_small, number_of_times_to_upsample=2,
                                                                 model="cnn")

            all_face_encoding = face_recognition.face_encodings(current_frame_small, all_face_locations)

            for current_face_location, current_face_encoding in zip(all_face_locations, all_face_encoding):
                top, right, bottom, left = current_face_location
                top = top * 4
                right = right * 4
                bottom = bottom * 4
                left = left * 4
                all_matches = face_recognition.compare_faces(known_face_encoding, current_face_encoding)
                face_Dist = face_recognition.face_distance(known_face_encoding, current_face_encoding)
                name_of_person = "unknown person"

                if True in all_matches:
                    first_match_index = all_matches.index(True)
                    name_of_person = classNames[first_match_index].upper()

                    conn = mysql.connector.connect(host="localhost", user="root", password="",
                                                   database="facerecognition")
                    my_cursor = conn.cursor()

                    my_cursor.execute("select name from student where id=" + name_of_person)
                    name_of_person = my_cursor.fetchone()
                    name_of_person = '*'.join(name_of_person)

                cv2.rectangle(current_frame, (left, top), (right, bottom), (255, 0, 0), 2)

                cv2.putText(current_frame, str(name_of_person), (left, bottom), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 2)

            cv2.putText(current_frame, str(face_Dist), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
            cv2.imshow('Person Identified', current_frame)

            if name_of_person == 'unknown person':
                self.send_message(current_frame, name_of_person)
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        cam.release()
        cv2.destroyAllWindows()

    def send_message(self, current_frame, name):

        condition = messagebox.askyesno("save or not", "Do you want to save this student", parent=self.root)
        if condition > 0:
            self.add_data()
        else:
            d = 0

            cv2.imwrite("imagesk/file_%d.jpg" % d, current_frame)

            nameimage = []
            path = "imagesk"
            myListc = os.listdir(path)
            for nameofimage in myListc:
                nameimage.append(os.path.splitext(nameofimage)[0])
                n = nameimage[0] + ".jpg"
                pwk.sendwhats_image("+60168510954", "imagesk/" + n, name)
    def send_message_obj(self, current_frame, name):
        d = 0
        cv2.imwrite("imageswo/file_%d.jpg" % d, current_frame)

        nameimage = []
        path = "imageswo"
        myListc = os.listdir(path)
        for nameofimage in myListc:
            nameimage.append(os.path.splitext(nameofimage)[0])
            n = nameimage[0] + ".jpg"
           # pwk.sendwhats_image("+923176034358", "imageswo/" + n, name)
            pwk.sendwhats_image("+60168510954", "imageswo/" + n, name)

    def save(self):

        self.sid = self.root.var_std_id.get()

        cam = cv2.VideoCapture(0)

        while True:
            ret, frame = cam.read()

            cv2.imshow("webcam", frame)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                cv2.imwrite("images/" + str(self.sid) + ".jpg", frame)
                messagebox.showinfo('Success', 'image saved', parent=self.root)
                break

            # elif cv2.waitKey(1) & 0xFF == ord('q'):
            #   break

        cam.release()
        cv2.destroyAllWindows()

    def add_data(self):

        if self.root.var_std_name.get() == "" or self.root.var_std_id.get() == "":
            messagebox.showerror("Error", "please fill all fields", parent=self.root)

        else:
            try:

                conn = mysql.connector.connect(host="localhost", user="root", password="",
                                               database="facerecognition")
                my_cursor = conn.cursor()

                my_cursor.execute("insert into student values(%s,%s)", (
                    self.root.var_std_id.get(),
                    self.root.var_std_name.get()
                ))
                conn.commit()
                conn.close()

                self.save()
                self.reset_data()
                messagebox.showinfo("Success", "Student details has been added successfully", parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Due to :{str(es)}", parent=self.root)

    def exit_all(self):
        self.exit_all = messagebox.askyesno("Exit", "Do you want to exit project")
        if self.exit_all > 0:
            self.root.destroy()
        else:
            return

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    # ======= Save unknown person data==================

    def reset_data(self):

        self.root.var_std_id.set(""),
        self.root.var_std_name.set("")


if __name__ == '__main__':
    root = Tk()
    obj = Face_Recognition_Class(root)
    root.mainloop()