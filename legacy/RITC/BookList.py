#BookList starts with one book object and start building up.
#One booklist
import llist
from llist import sllist, sllistnode

class BookList:
    book_list = None
    def __init__(self):
        self.book_list = sllist([])
    
    def addBook(self,theBook):
        self.book_list.append(theBook)
        
    def printList(self):
        print(self.book_list)
        
    def printLength(self):
        print(self.book_list.size)
        
    def getFirstNode(self):
        return self.book_list.first
    
    def printFirst(self):
        book = self.book_list.first.value
        book.printBook()
    