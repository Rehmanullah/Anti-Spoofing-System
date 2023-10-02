from tkinter.font import BOLD
from tkinter import *
from tkinter import Button, Label, Tk, ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import pyttsx3
#from docx.enum.table import WD_TABLE_ALIGNMENT

class Student:
    def __init__(self,root):
        self.root=root
        w=self.root.winfo_screenwidth()
        h=self.root.winfo_screenheight()
        
        self.root.engine=pyttsx3.init('sapi5')
        voices=self.root.engine.getProperty('voices')
        self.root.engine.setProperty('voice',voices[1].id)
        
        self.root.geometry("%dx%d0+0+0" % (w,h))
        #self.root.resizable(0,0)
        self.root.title("face Recognition System")

        #===========make variables=============
        
        self.var_std_name=StringVar()
        self.var_std_id=StringVar()
        
        bg="bisque"
        fg="black"
        #bg image
        img3=Image.open("D:/facerecognitionsysteminpython/imagesforcreatingwindow/bg.jpg")
        img3=img3.resize((w,h),Image.ANTIALIAS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_image=Label(self.root,image=self.photoimg3)
        bg_image.place(x=0,y=0,width=w,height=h)

        #title on window
        title_lbl=Label(bg_image,text="Student Management System",font=("times new roman",35,"bold"),bg="white",fg="darkblue")
        title_lbl.place(x=0,y=0,width=w,height=75)

        #main frame
        main_frame=Frame(bg_image,bd=2,bg="black")
        main_frame.place(x=250,y=200,width=1340,height=570)

        #left label frame
        left_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,font=("times new roman",15,"bold"))
        left_frame.place(x=40,y=40,width=615,height=480)
       

        
        #current course information
       
        #class student information
        class_student_frame=LabelFrame(left_frame,bd=2,relief=RIDGE,font=("times new roman",15,"bold"))
        class_student_frame.place(x=5,y=10,width=602,height=240)
        #student id entry and label
        student_id_lbl=Label(class_student_frame,text="StudentID:",font=("times new roman",14,"bold"),bg="white")
        student_id_lbl.grid(row=0,column=0,padx=3,sticky=W)
        student_id_entry=ttk.Entry(class_student_frame,textvariable=self.var_std_id,width=20,font=("times new roman",12,"bold"))
        student_id_entry.grid(row=0,column=1,sticky=W,padx=5,pady=3)
        #student name entry and label
        student_name_lbl=Label(class_student_frame,text="Name:",font=("times new roman",14,"bold"),bg="white")
        student_name_lbl.grid(row=1,column=0,padx=3,sticky=W)
        student_name_entry=ttk.Entry(class_student_frame,textvariable=self.var_std_name,width=20,font=("times new roman",12,"bold"))
        student_name_entry.grid(row=1,column=1,sticky=W,padx=5,pady=3)
        
        
        #button frame
        btn_frame=Frame(class_student_frame,relief=RIDGE,bd=2)
        btn_frame.place(x=0,y=102,width=598,height=70)
        #save btn
        update_btn=Button(btn_frame,text="Update",command=self.update_data,font=("times new roman",12,"bold"),bg=bg,fg=fg)
        update_btn.grid(row=0,column=0,padx=3,pady=2)
        delete_btn=Button(btn_frame,text="Delete",command=self.delete_data,font=("times new roman",12,"bold"),bg=bg,fg=fg)
        delete_btn.grid(row=0,column=1,padx=3,pady=2)
        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data,font=("times new roman",12,"bold"),bg=bg,fg=fg)
        reset_btn.grid(row=0,column=2,padx=3,pady=2)
        show_dataset_btn=Button(btn_frame,text="Show Dataset",command=self.open_image,font=("times new roman",12,"bold"),bg=bg,fg=fg)
        show_dataset_btn.grid(row=0,column=3,padx=3,pady=2)
        

        
        exit_btn=Button(main_frame,text="Exit",command=self.exit_all,font=("times new roman",12,"bold"),bg=bg,fg=fg)
        exit_btn.place(x=150,y=240,width=250,height=50)



        #right label frame
        right_frame=LabelFrame(main_frame,bd=2,relief=RIDGE)
        right_frame.place(x=667,y=40,width=615,height=480)
       
        
        
        #table frame use to show data
        table_frame=Frame(right_frame,bd=2,relief=RIDGE)
        table_frame.place(x=5,y=10,width=600,height=340)
        #===make a scroll bar========================
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,columns=("id","name"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        self.student_table.alignment=WD_TABLE_ALIGNMENT.CENTER
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
      
        #=======show heading in table===========
        
        self.student_table.heading("id",text="ID")
        self.student_table.heading("name",text="Name")
        
        self.student_table["show"]="headings"
        self.student_table.pack(fill=BOTH,expand=1)
        #============set the width of headings============
       
        self.student_table.column("id",width=100)
        self.student_table.column("name",width=100)
       
        

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()

        #========function for add data===============
    
    #=======================fetch data==================
    
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",user="root",password="",database="facerecognition")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from student")
        data=my_cursor.fetchall()
        
        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()
        
    #======================get data================
    def get_cursor(self,event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]
        self.var_std_id.set(data[0]),
        self.var_std_name.set(data[1])
        
    #==================update data============
    def update_data(self):
        
        if self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","please fill all fields",parent=self.root)
      
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update student details",parent=self.root)
                
                
                if Update>0:
                    conn=mysql.connector.connect(host="localhost",user="root",password="",database="facerecognition")
                    my_cursor=conn.cursor()
                    my_cursor.execute("update student set Name=%s where id=%s",(
                                                                                                                                                                                                    
                        self.var_std_name.get(),
                                                                                                                                                                                                
                        self.var_std_id.get()
                ))
                    
                else:
                    if not Update:
                        return
                    
                self.reset_data()
                messagebox.showinfo("Sucess","Your data has been successfully update",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            
            except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}",parent=self.root)
    #===============delete function==============
    
    def delete_data(self):
       if self.var_std_id.get()=="":
           messagebox.showerror("Error","Student id must be required",parent=self.root)
       else:
           try:
               delete=messagebox.askyesno("Delete","Do you want to delete this student",parent=self.root)
               if delete>0:
                   conn=mysql.connector.connect(host="localhost",user="root",password="",database="facerecognition")
                   my_cursor=conn.cursor()
                   sql="delete from student where id=%s"
                   val=(self.var_std_id.get(),)
                   
                   my_cursor.execute(sql,val)
                   
                   path="images"
                   img_name=self.var_std_id.get()+'.jpg'
                   os.remove(path + '/' + img_name)
               else:
                   if not delete:
                       return
               conn.commit()
               self.fetch_data()
               conn.close()
               
               messagebox.showinfo("Success","successfully delete student details",parent=self.root)
               
           except Exception as es:
               messagebox.showerror("Error",f"Due to :{str(es)}",parent=self.root)
               
    #==============reset data=================
    
    def reset_data(self):
        
        self.var_std_id.set(""),
        self.var_std_name.set("")
        
    #===============back to main page============
    def exit_all(self):
        self.exit_all=messagebox.askyesno("Exit","Do you want to exit project")
        if self.exit_all>0:
            self.root.destroy()
        else:
            return    

    def open_image(self):
        os.startfile("images")


if __name__ == '__main__':
    root=Tk()
    obj=Student(root)
    root.mainloop()