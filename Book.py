#this class of book represents one single book object that is unique and have a barcode of its
#own
from guizero import *
#
class Book:
    def __init__(self, title = 'Something', barcode = '-1', call_number = '-1', version = '', next_book = None, pre_book = None):
        self.title = title
        self.barcode = barcode
        self.call_number = call_number
        self.version = version
        self.inPlace = False
        self.hasNote = False
        self.next_book = next_book
        self.pre_book = pre_book
        #self.skip = False
    
    def __str__(self):
        # book_title = ''
        # if len(self.title) > 15:
        #     book_title = " ".join(self.title.split()[:10])
        # else:
        #     book_title = self.title
        return self.title +'\t'+ str(self.call_number) + '\t'+ str(self.version) +'\t'+ str(self.barcode)
    def getBarcode(self):
        return self.barcode
    
    # def printBook(self):
    #     if(self.hasNote):
    #         print('!!!!!!!!!!!!!!')
    #         print('Action Needed')
    #     print('[Title]: \n\t' + self.title)
    #     print('[Call number]: \n\t' + self.call_number)
        

    '''def GUI_printBook(self, GUI_window,textList):
        if(self.hasNote == True):
            GUI_window.warn("Alert","Next Book was found before, place it back in")
        textList[0].clear()
        textList[0].append(self.title)
        textList[1].clear()
        textList[1].append(self.barcode)
        textList[2].clear()
        textList[2].append(self.call_number)'''
        
    def founD(self):
        self.inPlace = True
        
    def needsAnounce(self):
        self.hasNote = True
    
    def ifneedsAnounce(self):
        return self.hasNote
    '''def needsSkip(self):
        print(self.title,'need skip')
        self.skip = True
    
    def ifNeedsSkip(self):
        return self.skip'''