#login_UI.py

from guizero import *
import csv
import pandas as pd
import Student

class login_UI:
    def __init__(self) -> None:
        self.filename = 'studentInfo.csv'
        self.loginWindow = App(title="Log in")
        self.currentStudent = None

    def addStaff(self,id):
        student_table = pd.read_csv(self.filename, sep = ',')
        new_studnet = [id]
        col_num = len(student_table.columns) - 1
        for i in range(col_num):
            new_studnet.append('')
        student_table.loc[len(student_table)] = new_studnet
        student_table.to_csv(self.filename,index=False)
        print('added')
            
    def checkExist(self,id):
        with open(self.filename, 'r') as file:
            isExist = False
            csvreader = csv.reader(file)
            for row in csvreader:
                # print(row[0])
                # print(str(id))
                if str(id) == row[0]:   
                    isExist = True
            if isExist == False:
                self.addStaff(id)
        return Student.Student(id)
	
# make the user interface
    def login(self):
        def toEnter():
            UserIdBox.value = ''
            UserIdBox.text_color='black'

        Text(self.loginWindow, text="\nWelcome!", size=30)
        Text(self.loginWindow, text="   ID number: ", align="left", size=18)
        UserIdBox = TextBox(self.loginWindow, text="Please enter your ID number", width=25, align="left")
        UserIdBox.text_color = 'grey'
        UserIdBox.when_clicked = toEnter   # clear text in textbox when click on it
        arrange_box=Box(self.loginWindow, height="fill") 
        PushButton(arrange_box, text = 'OK', command = self.check, args = [UserIdBox], align = "right")  
        self.loginWindow.set_full_screen()
        self.loginWindow.display()  
             
    def getStudent(self):
        return self.currentStudent
	
    def killWindow(self):
        self.loginWindow.destroy()  

    def strToInt(self,id):
        try:
            int(id)
        except(ValueError):
            self.loginWindow.error('!!!', 'ID number cannot contain any letters, special symbols or spaces, nor be empty!')

    def check(self,idbox):
        id = int(idbox.value[:-1])
        if len('00'+str(id)) == 9 and 0 <= int(id) < 10000000:
            # print(len(id))
            self.currentStudent = self.checkExist(id)  
            self.killWindow()  
        elif int(id) < 0:
            self.loginWindow.error('!!!', 'ID number must larger or equal to 0!')
        else:    
            self.loginWindow.error('!!!', 'ID number must be 9 in length!')
