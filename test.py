#test file
import matrixgenerate, instruction

def findBookFromDic(somebook, dic, bookList):
    for key in dic:
        #print(somebook,bookList[int(dic[key])])
        if somebook == bookList[int(dic[key])]:
            return key
    return None
def findBookFromList(somebook, bookList):
    for i  in range(len(bookList)):
        if somebook == bookList[i]:
            return i 
    return -1

pseudoBookList = [None,"Book1", "Book2", "Book3", "Book4", "Book5", "Book6", "Book7"]#None acts as a padding component for empty string
pseudoShelfList = [None, "Book1", "Book3", "Book5", "Book2", "Book4", "Book6", "Book7"]#None acts as a padding component
mg = matrixgenerate.matrixgenerate(pseudoBookList,pseudoShelfList)
mg.generating(pseudoBookList,pseudoShelfList)
matrix = mg.getMatrix()
ig = instruction.instructionGenerate(matrix)
#print(ig)
ig.printMinSteps()
#print('')
#print(a.solutionStepCount)
#a.printXY()
ig.tracBackToTop()
ig.flipSolutionIndex()
solutionDic, solutionInd = ig.getSolution()
#print(solutionDic)

booksNeedRemoval = []
for step in solutionInd:
    #print(step)
    if(int(solutionDic[step]) == -1): 
        solutionInd.remove(step)
        del solutionDic[step]
        booksNeedRemoval.append(step)
#print(solutionDic)
#print("solutionIND" , solutionInd)
#print(booksNeedRemoval)
bookinHand = None
#bookinHand = pseudoBookList[int(solutionInd[0])]
while len(solutionInd) != 0 or len(booksNeedRemoval) != 0: 
    if len(booksNeedRemoval) != 0 and bookinHand == None:
        bookinHand = pseudoShelfList[int(booksNeedRemoval[0])]
        print("Remove " + bookinHand + " from the Shelf")
        del booksNeedRemoval[0]
    #print(bookinHand)
    
    #print(bookToDealWith)
    if bookinHand == None and len(solutionInd) != 0:
        bookinHand = pseudoShelfList[int(solutionInd[0])];
    if bookinHand == None and len(solutionInd) == 0:
        break
    bookToDealWith = findBookFromDic(bookinHand,solutionDic,pseudoBookList)

    if bookinHand and len(solutionInd) == 1:
        print("Put " + bookinHand + " in front of their Next Book")
        break
    if bookToDealWith is None:#TODO: figure out, if multiple books needs to be add in, how can we know which is which
        #print("BookINHAND", bookinHand)
        print("Add in " + bookinHand + " in front of  " + pseudoShelfList[findBookFromList(bookinHand,pseudoBookList)])
        #print("This solutionind", findBookFromList(bookinHand,pseudoBookList))
        #print('list', solutionInd)
        
        #solutionInd.remove(str(findBookFromList(bookinHand,pseudoBookList)))
        solutionInd.remove(str(0))
        bookinHand = None;

    elif (int(solutionDic[bookToDealWith]) == -2):#TODO:figure out why this elif is never used 
        print("when solution dic is -2 Add in " + bookinHand + " after " + pseudoShelfList[findBookFromList(bookinHand,pseudoBookList)])
        
        solutionInd.remove(bookToDealWith)
        bookinHand = None
    else:
        #print(int(bookToDealWith),int(bookinHand))
        #print(bookToDealWith)
        #print(bookinHand)
        print("Use " + bookinHand + " to replace " + pseudoShelfList[int(bookToDealWith)])
        solutionInd.remove(bookToDealWith)
        bookinHand = pseudoShelfList[int(bookToDealWith)]
    
    '''print("REACH")
    print(booksNeedRemoval)
    print(bookToDealWith)
    print('solutionInd',solutionInd)
    print(solutionDic)
    print(bookinHand)'''
#print(solutionInd)
#for step in solutionInd:
#    solutionInd.remove(step)
#bookInHand = pseudoShelfList[]



#print(solutionInd)


#TODO: Known problems: if somebook needs to be inserted at the front of the string, it cannot be handled well enough
#example :pseudoShelfList = [None, "Book2", "Book3", "Book5", "Book1", "Book4", "Book6", "Book7"]
#TODO: Known problems: if all the fixs needed are replacements, the last replacement instruction should be replaced with an insertion.
#example :pseudoShelfList = [None, "Book1", "Book3", "Book5", "Book2", "Book4", "Book6", "Book7"]