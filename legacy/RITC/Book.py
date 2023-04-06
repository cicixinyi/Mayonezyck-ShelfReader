#this class of book represents one single book object that is unique and have a barcode of its
#own
from guizero import *
#
class Book:
    title = ''
    author = ''
    barcode = -1
    call_number = ''
    inPlace = False
    hasNote = False
    
    def __init__(self, title, author, barcode, call_number):
        self.title = title
        self.author = author
        self.barcode = barcode
        self.call_number = call_number
        self.inPlace = False
        
    def getBarcode(self):
        return self.barcode
    
    def printBook(self):
        if(self.hasNote):
            print('!!!!!!!!!!!!!!')
            print('Action Needed')
        print('[Title]: \n\t' + self.title)
        print('[Author]: \n\t' + self.author)
        print('[Call number]: \n\t' + self.call_number)
        
    def GUI_printBook(self, GUI_window,textList):
        if(self.hasNote == True):
            GUI_window.warn("Alert","error message")
        textList[0].clear()
        textList[0].append(self.title)
        textList[1].clear()
        textList[1].append(self.author)
        textList[2].clear()
        textList[2].append(self.barcode)
        textList[3].clear()
        textList[3].append(self.call_number)
    def founD(self):
        self.inPlace = True
        
    def needsAnounce(self):
        self.hasNote = True