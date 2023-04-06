# this class of student represents each studnet object that is unique

class Student:
	def __init__(self,ID = '0000000000'):
		self.ID = ID
		self.isStaff = False

	def __str__(self):
		return str(self.ID)
	
	def getID(self):
		return self.ID

