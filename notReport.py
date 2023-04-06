# count number of tasks user done and time needed for each task

import Student 
import csv
import pandas as pd

class notReport(Student.Student):
    
    def __init__(self,ID = '0000000'):
        self.ID = ID
        self.filename = 'studentInfo.csv'
        self.student_list = []
        self.currentRow = 0
        self.taskNum = 0
        self.tempTimePosition = 0
        
    # find the row of this student with its id number
    def getPosition(self, id):
	    with open(self.filename, newline='') as csvfile:
                 rowreader = csv.reader(csvfile)
                 for row in rowreader:
                      if row[0] == str(id):
                           self.currentRow = rowreader.line_num
                           # print(self.currentRow)
                           for element in row:
                                 self.student_list.append(element)
                                 # print(self.student_list)
                           if self.student_list[1] == '':
                              self.taskNum = 0
                           else: 
                              self.taskNum = int(self.student_list[1])
                           return self.currentRow

    def task_time(self, start, end):  
         self.tempTimePosition = self.taskNum + 2    
         if self.student_list[self.tempTimePosition] != '':
              self.tempTimePosition = self.taskNum + 3
         self.student_list[self.tempTimePosition] = start
         # print(self.tempTimePosition, self.student_list[self.tempTimePosition],float(end - start))
         if end < 43200: # 12 hours
            self.student_list[self.tempTimePosition] = str(float(end - start))
         print(self.student_list)

    def updateTaskDoneNum(self,start):
         time = float(self.student_list[self.tempTimePosition])
         if time == start:
                   self.taskNum += 0
         else:
                   self.taskNum += 1
         self.student_list[1] = str(self.taskNum)
                
    def renewCSV(self):
        studentinfo = pd.read_csv(self.filename, encoding = 'utf-8')
        # print(self.currentRow-2, self.taskNum+2)
        print(self.student_list)
        x,y = self.currentRow-2, self.tempTimePosition
        studentinfo.iloc[x,1] = self.student_list[1]
        print(studentinfo.iloc[x,1])
        studentinfo.iloc[x,y] = self.student_list[y]
        print(studentinfo.iloc[x,y])
        studentinfo.to_csv(self.filename,index=False)
        print(studentinfo)

# report = notReport()
# report.getPosition('123456789')
# report.task_time(10, 100)
# report.updateTaskDoneNum(1)
# report.renewCSV()