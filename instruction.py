#generate instruction based on matrix input
#Two matrices should be taken in. one is the Levenshtein matrix for the twenty books
#The other is a binary matrix that indicates the matching pairs of the Levenshtein matrix
#The output is supposed to be a list of strings, that the student should complete in order.
#
class instructionGenerate:
    def __init__(self, workingMatrix = None) -> None:
        self.workingMatrix = workingMatrix
        self.posx, self.posy = self.getSize()
        self.solutionStepCount = self.posx
        self.solutionDictionary = {}
        self.solutionIndex = []
        
    def __str__(self):
        result = "The Working Matrix is:\n"
        for each in self.workingMatrix:
            result += str(each) + "\n"
        return result
        
    def printMinSteps(self):
        print("It takes at least " + str(self.workingMatrix[-1][-1]) + " steps to reorder")

    def checkXY(self):
        return not( self.posx == 0 and self.posy == 0) 
    def printXY(self):
        print("The " + str(self.posx) +" and " + str(self.posy) + " were reached\n\tValue: " + str(self.workingMatrix[self.posx][self.posy]) + "\n")
        #return posx, posy
    def traceBack(self, posx, posy):
        if(posx == 0 and posy == 0):
            print("Debug: The top left node was reached")
            return -1, -1
        elif(posx == 0 and posy != 0):
            print("Book should be taken somewhere else and insert to here")
            self.solutionDictionary[str(posx)] = "-2"#TODO:fill
            self.solutionIndex.append(str(posx))
            return posx, posy-1
        elif(posx != 0 and posy == 0):
            print("Remove the book at the " + str(posx) + " position")
            self.solutionDictionary[str(posx)] = "-1"
            self.solutionIndex.append(str(posx))
            return posx-1, posy
        else:
            if(self.workingMatrix[posx-1][posy-1] == self.workingMatrix[posx][posy]-1): 
                print("Replace the book at the " + str(posx) + " with the book at " + str(posy) + " position in the correct list")
                self.solutionDictionary[str(posx)] = str(posy)
                self.solutionIndex.append(str(posx))
                return posx-1,posy-1
            else:
                left = self.workingMatrix[posx][posy-1]
                top = self.workingMatrix[posx-1][posy]
                topleft = self.workingMatrix[posx-1][posy-1]
                if left < top and left < topleft:
                    print("Book should be taken somewhere else and insert to here")
                    self.solutionDictionary[str(posx)] = "-2"#TODO:fill
                    self.solutionIndex.append(str(posx))
                    return posx, posy-1
                elif left > top and top < topleft:
                    print("Remove the book at the " + str(posx) + " position")
                    self.solutionDictionary[str(posx)] = "-1"
                    self.solutionIndex.append(str(posx))
                    return posx-1, posy
                elif left < topleft and top < topleft:
                    print("Remove the book at the " + str(posx) + "position")
                    self.solutionDictionary[str(posx)] = "-1"
                    self.solutionIndex.append(str(posx))
                    return posx-1, posy
                else:
                    print("this step can be omited because of matching elements")
                    self.solutionStepCount -= 1
                    return posx-1, posy-1
    def flipSolutionIndex(self):
        self.solutionIndex = self.solutionIndex[::-1]
    def getSize(self):
        return len(self.workingMatrix)-1 , len(self.workingMatrix[0])-1
    def getSolution(self):
        return self.solutionDictionary,self.solutionIndex
    def traceBackOnce(self):
        self.posx, self.posy = self.traceBack(self.posx,self.posy)
    def tracBackToTop(self):
        while(self.checkXY()):
            self.traceBackOnce()
            self.printXY()
