#checking_UI.py
from guizero import *
import readfile
import matrixgenerate, instruction

class checking_UI:
    def __init__(self):
        self.filename = 'shelflist.xlsx'
        self.shelfCheckWindow = App(title = "Shelf Checking is in Progress", width = 1000)
        self.bookList, self.bookDic = readfile.readfile(self.filename)
        self.currentBook = None
        self.BookTitle = None
        self.BookCallNum = None
        self.BookBarcode = None
        self.BookVersion = None
        self.ButtonBookFound = None #button number0
        self.ButtonSubmit = None #button number1
        self.barcodeBox = None
        self.reachlast = False
        self.NbooktracerReachLast = False
        self.startCounting = False
        self.theNthBookTracer = self.bookList.getHead()
        self.N = 7#this is heuristic value of N
        self.Noffset = 0
        self.desiredBookArray = []
        self.desiredBookDic = {}
        self.expandDesiredBookArray(self.N)
        self.actualBookArray = []
        self.lostBookDic = {}

    def destroyWindow(self):
        self.shelfCheckWindow.warn('Session Over', 'Your Session is over, congratulations')
        self.shelfCheckWindow.destroy()

    def expandDesiredBookArray(self, count = 1):
        if not self.NbooktracerReachLast:
            for i in range(count):
                self.desiredBookArray.append(self.theNthBookTracer)
                self.desiredBookDic[self.theNthBookTracer.barcode] = True
                self.theNthBookTracer = self.theNthBookTracer.next_book
                if self.theNthBookTracer is None:
                    self.NbooktracerReachLast = True

    def start(self, student = None):
        def toEnter():
            self.barcodeBox.value = ''
            self.barcodeBox.text_color='black'
        print(student)

        # def __str__():
        #      book_title = ''
        #      if len(self.currentBook.title) > 15:
        #         #  book_title.append(self.currentBook.title.split()[:10])
        #         #  book_title.append('\n')
        #         #  book_title.append(self.currentBook.title.split()[10:-1])
        #         book_title = " ".join(self.currentBook.title.split()[:10])
        #      else:
        #          book_title = self.currentBook.title
        #      return book_title
        #   #  self.currentBook.title = str(self.currentBook.title)
        #    # return self.currentBook.title.split()[:10] + '\n' + self.currentBook.title.split()[10:-1]

        while not self.reachlast:#the window should be destroyed already by the previous method
            self.currentBook = self.bookList.getHead()
            self.BookTitle = Text(self.shelfCheckWindow, text = self.currentBook.title, size = 30)
            self.BookCallNum = Text(self.shelfCheckWindow, text = self.currentBook.call_number, size = 20)
            self.BookVersion = Text(self.shelfCheckWindow, text= self.currentBook.version, size=20)
            self.barcodeBox = TextBox(self.shelfCheckWindow, text="scan in barcode if not found", width=25, align="top")
            self.barcodeBox.text_color = "grey"
            self.barcodeBox.when_clicked = toEnter
            self.ButtonBookFound = PushButton(self.shelfCheckWindow, text = 'Book Found', command = self.foundButtonPressed)
            self.ButtonSubmit = PushButton(self.shelfCheckWindow, text = 'Submit', command = self.submitButtonPressed)
            self.shelfCheckWindow.set_full_screen()
            self.shelfCheckWindow.display()
        
    def showNextBook(self):
        if self.currentBook is not None: 
            if self.currentBook.next_book is not None:
                #if self.currentBook.next_book.ifNeedsSkip():
                if self.desiredBookDic[int(self.currentBook.next_book.barcode)] is False:
                    print(self.currentBook.title,'skiped')
                    self.desiredBookDic[int(self.currentBook.next_book.barcode)] = True
                    self.currentBook = self.currentBook.next_book
                self.currentBook = self.currentBook.next_book
                if self.currentBook.ifneedsAnounce():
                    self.shelfCheckWindow.warn('Reshelf', 'This next book needs to be reshelved to the current position')
                self.BookTitle.clear()
                self.BookTitle.append(self.currentBook.title)
                self.BookCallNum.clear()
                self.BookCallNum.append(self.currentBook.call_number)
                self.BookVersion.clear()
                self.BookVersion.append(self.currentBook.version)
            else:
                self.reachlast = True

    def checkIfIsTimeToReorder(self):
        #A session should only stop when: startcounting is set
        #and
        #The size of actualBook became N
        if len(self.desiredBookArray) == len(self.actualBookArray) + self.Noffset:

            self.reorderLoop()
            print('End of one reorderLoop')
            self.actualBookArray = []
            self.desiredBookArray = []
            self.desiredBookDic.clear()
            self.Noffset = 0
            self.expandDesiredBookArray(self.N)
            self.startCounting = False
            
        pass

    def foundButtonPressed(self):
        #when the foundbutton has been pressed, check if the startCounting flag is on
        #The startCounting flag should be on when within a small session, the first "not in place" book was encountered.
        if not self.reachlast:
            if(self.startCounting):#this if and else block is used to do the shifitng of the N size block along the linked list
                self.actualBookArray.append(self.currentBook)
                self.desiredBookDic[int(self.currentBook.barcode)] = True
                self.checkIfIsTimeToReorder()
                pass
            else:
                del self.desiredBookDic[int(self.desiredBookArray[0].barcode)]
                self.desiredBookArray.remove(self.desiredBookArray[0])
                self.expandDesiredBookArray()
            
            self.showNextBook()
        else:
            #at the end of shelf, no more book to look at
            for eachBook in self.lostBookDic:
                thisBook = self.lostBookDic[eachBook]
                print('lost books', thisBook)
                if thisBook.ifneedsAnounce():
                    print('this book needs anounce')
                    nextBookAvailable = thisBook.next_book
                    while int(nextBookAvailable.barcode) in self.lostBookDic:
                        nextBookAvailable = nextBookAvailable.next_book
                        
                    reshelfInstruction = 'Place \n' + thisBook.title + ' in front of \n' + nextBookAvailable.title
                    self.shelfCheckWindow.warn('Reshelf',reshelfInstruction)
            self.destroyWindow()
            pass
        print(self.desiredBookDic)

    def submitButtonPressed(self):
        #this button press means a book doesn't match was found
        #When the first time in session when the button was pressed, the flag "StartCounting" should be set to True
        if self.barcodeBox.value is not None and self.barcodeBox.value != 'scan in barcode if not found':
            #The nextbook should sure be printed 
            #TODO:search the booklist and see if this book should be immediately pull out
            print(self.barcodeBox.value)#this is for debug
            if int(self.barcodeBox.value) in self.bookDic:#meaning, if this book is belong to the list
                shouldShow = True
                shouldStart = True
                if int(self.barcodeBox.value) in self.lostBookDic: #if this book is lost
                    shouldStart = False
                    shouldShow = False#shouldn't show the next book
                    self.shelfCheckWindow.warn('warning', 'Remove this book and put it on the cart, this will be reshelfed')
                
                if int(self.barcodeBox.value) in self.desiredBookDic:
                    if self.desiredBookDic[int(self.barcodeBox.value)] == True:
                        self.Noffset += 1 
                        self.desiredBookDic[int(self.barcodeBox.value)] = False
                        self.desiredBookDic[int(self.currentBook.barcode)] = False
                        print('within method', self.desiredBookDic)
                    else:
                        print('reached here')
                        self.Noffset -= 1
                        self.desiredBookDic[int(self.barcodeBox.value)] = True
                        shouldShow = False
                    #self.bookDic[int(self.barcodeBox.value)].needsSkip()
                else:
                    self.desiredBookDic[int(self.currentBook.barcode)] = False
                    self.bookDic[int(self.barcodeBox.value)].needsAnounce()
                    print(self.bookDic[int(self.barcodeBox.value)].title,'needs anounce')
                if (not self.startCounting) and shouldStart:
                        self.startCounting = True
                if shouldStart:
                    self.actualBookArray.append(self.bookDic[int(self.barcodeBox.value)])
                if shouldShow:
                    self.showNextBook()
                self.checkIfIsTimeToReorder()
            else:
                self.shelfCheckWindow.warn('warning', 'Remove this book and put it on the cart, this is gonna be returned to the desk')
            #reset the barcodebox
            self.barcodeBox.value = 'scan in barcode if not found'
            self.barcodeBox.text_color = "grey"
            
        else:
            self.shelfCheckWindow.warn('warning', 'Please put in barcode before hitting button')
        print(self.desiredBookDic)

    def reorderLoop(self): #this method initiates the reorder loop.
        def exitReshelf():
            print('pressedd')
            reorderWindow.destroy()
        def findBookToDealWith(handBook):
            ind = 0
            for book in actualBookArray:
                if book == handBook:
                    return ind
                ind += 1
            return -1
        def findIfCanInsert():
            handBook = actualBookArray[int(self.bookinHand)]
            for key in solutionDic:
                if solutionDic[key] == '-2':
                    if desiredBookArray[int(key)+1] == handBook:
                        return int(key)
            return -1
        def bookInHandRefresh():
            BookInHandText.clear()
            BookInHandText.append(actualBookArray[int(self.bookinHand)].title)
        def bookInHandClear():
            self.bookinHand = None
            BookInHandText.clear()
            BookInHandText.append('Nothing')
        def takeOutInstruction(theBook):
            InstructionLine1.clear()
            InstructionLine1.append('Take Out')
            InstructionLine2.clear()
            InstructionLine2.append(theBook.title)
            InstructionLine3.clear()
            InstructionLine3.append('From Shelf')
        def putAwayInstruction():
            InstructionLine1.clear()
            InstructionLine1.append('Put')
            InstructionLine2.clear()
            InstructionLine2.append('the book in your hand')
            InstructionLine3.clear()
            InstructionLine3.append('On the cart for future use')
        def replaceInstruction(theBook):
            InstructionLine1.clear()
            InstructionLine1.append('Replace')
            InstructionLine2.clear()
            InstructionLine2.append(theBook.title)
            InstructionLine3.clear()
            InstructionLine3.append('with the Book in Hand')
        def insertInstruction(theBook):
            InstructionLine1.clear()
            InstructionLine1.append('Put')
            InstructionLine2.clear()
            InstructionLine2.append('The book in hand')
            InstructionLine3.clear()
            done = False
            for book in desiredBookArray:
                if book is not None:
                    if book.next_book == theBook:
                        InstructionLine3.append('to the right of ' + book.title)
                        done = True
            if not done:
                if desiredBookArray[1] != theBook:
                    InstructionLine3.append(('to the left of ' + desiredBookArray[1].title))
                else:
                    InstructionLine3.append(('to the left of ' + desiredBookArray[2].title))
        def nextStepShow():
            if self.bookinHand is not None:
                bookInHandRefresh()
            else:
                bookInHandClear()

            if self.bookinHand is None:
                if len(booksNeedRemoval) > 0 :
                    takeOutInstruction(actualBookArray[int(booksNeedRemoval[0])])
                    self.bookinHand = booksNeedRemoval[0]
                    del booksNeedRemoval[0]
                    #bookInHandRefresh()
                else:
                    if len(solutionInd) > 0:
                        takeOutInstruction(actualBookArray[int(solutionInd[0])])
                        self.bookinHand = solutionInd[0]
                        if self.loophead == None:
                            self.loophead = actualBookArray[int(self.bookinHand)]
                            print('loophead', self.loophead)
                        del solutionInd[0]
                        #bookInHandRefresh()
                    else:
                        exitReshelf()
                    
            else:
                if self.bookinHand in solutionDic:
                    print('is it in solutiondic?')
                    situation = solutionDic[self.bookinHand]#situation can be -2: plugin -1: remove positive number:index 
                    print('situation',situation)
                    if situation == '-1':#if remove
                        insertPlace = findIfCanInsert()
                        if insertPlace != -1:
                            insertInstruction(actualBookArray[int(self.bookinHand)])
                            del solutionDic[self.bookinHand]
                            solutionInd.remove(str(insertPlace))
                            del solutionDic[str(insertPlace)]
                            self.bookinHand = None
                        else:
                            temp = None
                            bookHand = actualBookArray[int(self.bookinHand)]
                            print('bh',bookHand)
                            for key in solutionDic:
                                if desiredBookArray[int(solutionDic[key])] == bookHand:
                                    bookToReplace = actualBookArray[int(key)]
                                    temp = key
                                    replaceInstruction(bookToReplace)
                                    del solutionDic[self.bookinHand]

                                    self.bookinHand = temp
                                    del solutionDic[self.bookinHand]
                                    solutionInd.remove(self.bookinHand)
                                    break
                            '''for key in solutionDic:
                                if solutionDic[key] == self.bookinHand:
                                    bookToReplace = actualBookArray[int(key)]
                                    temp = key
                                    replaceInstruction(bookToReplace)
                                    del solutionDic[self.bookinHand]
                                    self.bookinHand = temp
                                    solutionInd.remove(self.bookinHand)'''
                    else:#if not remove, most times switching
                    #print('book', bookToDealWith)
                    #print(actualBookArray)
                        #ind = self.bookinHand
                        bookToReplace = desiredBookArray[int(self.bookinHand)]
                        if bookToReplace != self.loophead:
                            replaceInstruction(bookToReplace)
                            del solutionDic[self.bookinHand]
                            self.bookinHand = str(findBookToDealWith(bookToReplace))
                            solutionInd.remove(self.bookinHand)
                        else:
                            insertInstruction(actualBookArray[int(self.bookinHand)])
                            del solutionDic[self.bookinHand]
                            self.loophead = None
                            self.bookinHand = None
                        

                        '''del solutionDic[self.bookinHand]
                            if actualBookArray[ind] != self.loophead:
                                replaceInstruction(actualBookArray[ind])
                            else:
                                insertInstruction(ind)
                                self.loophead = None
                            self.bookInHand = None
                        if len(solutionInd) > 0:
                            ind = findBookToDealWith()
                            print('ind', ind)
                            if ind != -1:
                                del solutionDic[self.bookinHand]
                                replaceInstruction(actualBookArray[ind])
                                self.bookinHand = str(ind)
                                print('now solution',solutionInd)
                                print('now book', self.bookinHand)
                                solutionInd.remove(self.bookinHand)
                            else:
                                putAwayInstruction()  
                                bookInHandClear()     
                        else:
                            ind = findBookToDealWith()
                            insertInstruction(ind)
                            del solutionDic[self.bookinHand]
                            #solutionInd.remove(str(insertPlace))
                            self.bookinHand = None'''
                else:
                    inserted = False
                    for key in solutionDic:
                        if solutionDic[key] == '-2':
                            if desiredBookArray[int(key)+1] == actualBookArray[int(self.bookinHand)]:
                                insertInstruction(actualBookArray[int(self.bookinHand)])
                                #del solutionDic[self.bookinHand]
                                solutionInd.remove(key)
                                del solutionDic[key]
                                self.bookinHand = None
                                inserted = True
                                break
                    if not inserted:
                        putAwayInstruction()
                        bookInHandClear()
                
                print(booksNeedRemoval)
                print(solutionDic)
                print(solutionInd)
            pass
        #It takes in the actualBookArray and desiredBookArray, it will call the matrixgenerate.py
        #after getting the matrix back from the call, it will pass the matrix to the instruction.py
        #the instruction.py will have a solution dictionary and solution index passed back. 
        #Using the solution dictionary and solution index, the book reordering solution should be performed at this order
        #Create a temporary Book object, as "Book in the hand", its initial value should be the first book needed to be fixed on the shelf
        #The loop should be: use the "Book in the hand" as the key, find where it should fit, replace it, and the replaced book is the new
        #"Book in the hand" 
        #For the extra book in the list, it will point to "-1". We can let the student pull out all the books needed to be picked out first
        reorderWindow = Window(self.shelfCheckWindow, title="Reshelfing")
        titleBox = Box(reorderWindow)
        titleText = Text(titleBox, text = "Please wait until the solution is generated", size = 20, color="red", font="Arial")
        instructionBox = Box(reorderWindow)
        Text(instructionBox, text = "Book in Hand")
        BookInHandText = Text(instructionBox, text = "Nothing")
        InstructionLine1 = Text(instructionBox, text = "Instruction Line 1")
        InstructionLine2 = Text(instructionBox, text = "Instruction Line 2")
        InstructionLine3 = Text(instructionBox, text = "Instruction Line 3")
        finishButton = PushButton(titleBox, text="Finish",command = exitReshelf)
        nextStepButton = PushButton(instructionBox, text="Next Step", command = nextStepShow)
        
        desiredBookArray =[None]+self.desiredBookArray
        actualBookArray = [None]+self.actualBookArray
        
        for eachBook in self.desiredBookDic:
            #print('key',eachBook)
            #print('value',self.desiredBookDic[eachBook])
            if(self.desiredBookDic[eachBook] == False):
                desiredBookArray.remove(self.bookDic[eachBook])
                self.lostBookDic[eachBook] = self.bookDic[eachBook]#add this book to the lostBookDictionary
        print(self.desiredBookDic)
        print("desiredBook")
        for i in desiredBookArray:# this is for debugging#TODO:CLEAR THIS OUT WHEN PACK
            if i is not None:
                print(i.title + i.version)
        print('')
        print("CurrentBook")
        for i in actualBookArray:# this is for debugging#TODO:CLEAR THIS OUT WHEN PACK
            if i is not None:
                print(i.title + i.version)
        print('')

        #reorderWindow.full_screen = True
        #Calling matrix generation for desired list and actual list
        mg = matrixgenerate.matrixgenerate(desiredBookArray, actualBookArray)
        mg.generating()    
        matrix = mg.getMatrix()
        ig = instruction.instructionGenerate(matrix)
        ig.printMinSteps()
        ig.tracBackToTop()
        ig.flipSolutionIndex()
        solutionDic, solutionInd = ig.getSolution()
        print(solutionDic)
        print(solutionInd)
        booksNeedRemoval = []
        for step in solutionInd:
            if(int(solutionDic[step] == '-1')):
                solutionInd.remove(step)
                #del solutionDic[step]
                booksNeedRemoval.append(step)
        self.bookinHand = None
        self.loophead = None
        nextStepShow()
        #print(booksNeedRemoval)
        #print(solutionDic)
        #print(solutionInd)
        #print(self.lostBookDic)
        reorderWindow.show()
                   
        pass