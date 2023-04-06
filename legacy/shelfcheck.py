#this is the backend portal for the shelf chekcing process
from guizero import *
import Book
import BookList
import readfile
#What is the process of shelf checking
#Get the area of interest-> Fetch a list of book from Alma
#->compile a list of books based on the inputs
#this range of books should be generated using the analysis tool from Alma, and sorted by call number
#on top of that, if the call numbers were shared among books, the version number should be sorted.


def main():
    GUInterface_login()
    #this is non-graphical user interface
    print('------------------------------')
    print('Please input the first book on the shelf')
    #Getting the input here, save as firstBook
    print('Please input the last book from the shelf')
    #getting the input here, save as LastBOok
    #compare the two call numbers:
    #COMPARE module is needed here
    #if the first book should be somewhere later in the shelf, an error should be thrown
    #to handle this error, request the user to input one book ahead/one book after
    print('Generating the list')
    #
    
 
def GUInterface_login():
    loginWindow = App(title="Log in")
    Text(loginWindow, text="\nWelcome!\n", size=40)
    box=Box(loginWindow, height="fill")
    Text(box, text="User ID: ", width=15, align="left")
    userNameBox = TextBox(box,text="Please enter your ID number", width=25, align="left")
    PushButton(box, text = 'clear', command = clearTextBox, args = [userNameBox], align = "bottom")
    PushButton(loginWindow, text = 'OK', command = GUInterface_listGenerate, args = [loginWindow], align = "right")
    loginWindow.set_full_screen()
    loginWindow.display()

def clearTextBox(textBox):
    textBox.clear()

def textDestroy(text):
    text.destroy()

def GUInterface_listGenerate(previousWindow):
    appDestroy(previousWindow)
    shelfCheck = App(title = "list generate")
    Text(shelfCheck, text="\nWhere to Shelf Check\n", size=30)
    arrange = Box(shelfCheck, height='fill', width='fill')
    firstBarcode = TextBox(arrange,text="Scan in the barcode of the FIRST Book",height="fill", width="fill", align="top")
    PushButton(arrange, text = 'clear', command = clearTextBox, args = [firstBarcode])
    secondBarcode = TextBox(arrange,text="Scan in the barcode of the LAST Book",height="fill", width="fill", align="top")
    PushButton(arrange, text = 'clear', command = clearTextBox, args = [secondBarcode])
    PushButton(shelfCheck, text = 'OK', command = GUInterface_checkBooks, args = [shelfCheck], align = "right")
    shelfCheck.set_full_screen()
    shelfCheck.display()
    
def GUInterface_checkBooks(previousWindow):
    appDestroy(previousWindow)
    bookCheck = App(title = 'book Check')
    filename = 'shelflist.xlsx'
    BL = readfile.readfile(filename)
    #
    #Now that the Book list was initialized
    #Start from the first Book
    #
    #this listRunhrough method starts from the first book in the list, display required books one by one
    result = listRunThrough(BL,bookCheck)
    
    
    

def appDestroy(app):
    app.destroy()

def foundButtonPressed(barcodeBox,currentNode,result,buttons,GUI_window,textList):
    if(currentNode.next == None):
        GUI_window.warn(title = "Warning", text = "no more books in the list");
        return
    currentNode.next.value.GUI_printBook(GUI_window,textList)
    currentBarcode = currentNode.value.getBarcode()
    decisionMaking(currentBarcode,currentNode,result,buttons)
    currentNode = currentNode.next
    if(currentNode == None):
        GUI_window.warn(title = "Warning", text = "no more books in the list");
        return
    currentBarcode = currentNode.value.getBarcode()
    buttons[0].update_command(command = foundButtonPressed, args = [currentBarcode, currentNode,result,buttons,GUI_window,textList])
    buttons[1].update_command(command = submitButtonPressed, args = [barcodeBox, currentNode,result,buttons,GUI_window,textList])
    
def submitButtonPressed(barcodeBox, currentNode,result,buttons,GUI_window,textList):
    if(currentNode.next == None):
        GUI_window.warn(title = "Warning", text = "no more books in the list");
        return
    barcodeValue = int(barcodeBox.value)
    currentNode.next.value.GUI_printBook(GUI_window,textList)
    currentBarcode = currentNode.value.getBarcode()
    decisionMaking(barcodeValue, currentNode,result,buttons)
    currentNode = currentNode.next
    if(currentNode == None):
        GUI_window.warn(title = "Warning", text = "no more books in the list");
        return
    currentBarcode = currentNode.value.getBarcode()
    buttons[0].update_command(command = foundButtonPressed, args = [currentBarcode, currentNode,result,buttons,GUI_window,textList])
    buttons[1].update_command(command = submitButtonPressed, args = [barcodeBox, currentNode,result,buttons,GUI_window,textList])

def printBreakingLine():
    print('------------------------------')#this method simply organize the UI by inserting breaking lines of the same length

def printAnouncements(something):#similarly, this method organize the a UI by printing things with Breaking lines Surrounding 
    printBreakingLine()
    print(something)
    printBreakingLine()
    
def decisionMaking(barCode, currentNode,result,buttons):
    #print(barCode, '+', currentNode)
    if(barCode == currentNode.value.getBarcode()):
        print('book Found')
        result[0] = result[0]+1
        print(result)
        currentNode = currentNode.next
        return 0#return True if the barcodes match thus indicating the book in place
    else:
        compareBook = currentNode.next#get the next Node to compare
        while(compareBook != None):#if it is not the end of the list
            compareBarcode = compareBook.value.getBarcode()#get the barcode of next book
            if(compareBarcode == barCode):#if they match
                print('Book out of place but still in the list')
                compareBook.value.needsAnounce()#mark the book who needs action, return false
                result[1] = result[1]+1
                print(result)
                currentNode = currentNode.next
                if(currentNode == None):
                    printAnouncements('You\'ve reached the end of the list, please wait until the report to generate')
                return 1
            compareBook = compareBook.next#move to the next book
            if(currentNode == None):
                printAnouncements('You\'ve reached the end of the list, please wait until the report to generate')
        print('Book does not belong to this list')
        result[2] = result[2]+1
        print(result)
        currentNode = currentNode.next
        if(currentNode == None):
            printAnouncements('You\'ve reached the end of the list, please wait until the report to generate')
        return -1#move to another book
def terminate(GUI_window):
    GUI_window.info('notice','You have decided to quit.')
    GUI_window.destroy()

def listRunThrough(bookList,GUI_window):
    Text(GUI_window, text="\nBook info\n", size=30)
    inPlace = 0
    notInPlace = 0
    missing = 0
    result = [0,0,0]#inplace,notInplace, missing item
    currentNode = bookList.getHead()
    currentBook = bookList.head
    reachLast = False#this flag counts if the list reaches the last element
    
    while(reachLast == False):
        BookTitle = Text(GUI_window,size = 20)
        BookAuthor = Text(GUI_window,size = 15)
        BookBarcode = Text(GUI_window,size = 15)
        BookCallNumber = Text(GUI_window,size = 13)
        textList = [BookTitle, BookAuthor, BookBarcode, BookCallNumber]
        currentBook.GUI_printBook(GUI_window,textList)
        currentBarcode = currentBook.barcode
        boxText = Text(GUI_window, text="Please scan the barcode")
        barcodeBox = TextBox(GUI_window,text = '123',width = 16)
        PushButton(GUI_window, text =' Clear', command = clearTextBox, args = [barcodeBox])        
        checkButton = PushButton(GUI_window, text =' Book Found')
        submitButton = PushButton(GUI_window, text =' Submit')
        buttons = [checkButton, submitButton]
        checkButton.update_command(command = foundButtonPressed, args = [barcodeBox, currentNode,result,buttons,GUI_window,textList])
        submitButton.update_command(command = submitButtonPressed, args = [barcodeBox, currentNode,result,buttons,GUI_window,textList])
        terminateButton = PushButton(GUI_window, text ='That\'s it!', command = terminate, args = [GUI_window]);
        GUI_window.set_full_screen()
        GUI_window.display()
        #printBreakingLine()
        #currentBook.printBook()
        #printBreakingLine()
        #currentBarcode = currentBook.barcode
        #print('[1] In place | [2] Missing | ')
        #response = int(input())
        #if(response == 1):
         #   result = decisionMaking(currentBarcode,currentNode)
        #else:
        #    result = decisionMaking(response, currentNode)
    
        #if(result == 0):
        #    inPlace+=1
        #elif(result == -1):
        #    missing+=1
        #else:
        #    notInPlace+=1
        #currentNode = currentNode.next
        #if(currentNode == None):
            #printAnouncements('You\'ve reached the end of the list, please wait until the report to generate')
        #    app.info("Notice", "You\'ve reached the end of the list, please wait until the report to generate")
        #    reachLast = True
        #else:    
         #   currentBook = currentNode.value

    
    
    
main()