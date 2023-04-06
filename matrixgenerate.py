#matrixgenerate.py
#This class returns the matching matrix which will then be used in the instruction.py

class matrixgenerate:
    def __init__(self,desiredBookArray = None, actualBookArray = None) -> None:
        if desiredBookArray is None:
            self.result = [[0,1,2,3,4,5,6,7],[1,0,1,2,3,4,5,6],[2,1,1,2,3,4,5,5],[3,2,1,2,3,4,5,6],[4,3,2,1,2,3,4,5]
                              ,[5,4,3,2,1,2,3,4],[6,5,4,3,2,1,2,3],[7,6,5,4,3,2,1,2]]
        else:    
            self.result = []
            temp = 0
            self.desiredBookArray = desiredBookArray
            self.actualBookArray = actualBookArray
            for i in range(len(self.actualBookArray)):
                self.result.append([temp])
                temp += 1
            for i in range(1,len(self.desiredBookArray)):
                self.result[0].append(i)
        print(self.result[0])
    
    def A_Match_D(self,a,b,c):
        return min(a,b,c) + 0

    def A_notMatch_D(self,a,b,c):
        return min(a,b,c) + 1
    
    def generating(self):
        d_length = len(self.desiredBookArray)
        a_length = len(self.actualBookArray)
        for i_aBook in range(1,a_length):
            for i_dBook in range(1,d_length):   
                up_left = self.result[i_aBook-1][i_dBook-1]
                #print("lOoking for row ", i_dBook-1, "col", i_aBook)
                up_right = self.result[i_aBook-1][i_dBook]    
                down_left = self.result[i_aBook][i_dBook-1]
                #print(up_left, up_right, down_left)
                if self.actualBookArray[i_aBook] == self.desiredBookArray[i_dBook]:
                     no_action = self.A_Match_D(up_left,up_right,down_left)
                     self.result[i_aBook].append(no_action) 
                else:
                     do_oneStep = self.A_notMatch_D(up_left,up_right,down_left)
                     self.result[i_aBook].append(do_oneStep)
                #print(self.result[i_dBook][i_aBook])
            print(self.result[i_aBook])

    def getMatrix(self):
        return self.result
    
