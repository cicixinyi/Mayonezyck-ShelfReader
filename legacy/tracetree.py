#This tree class is used to track the status of the shelf and help find and relocate books.
#This tree is not necessarily a traditional tree with multiple branches and branches, it is a 
#low bush, with a lot of branches but in each branch there's only a single strand,
#maybe call it willow
import Book,BookList,readfile
class tracetree:
    
    def __init__(self):
        self.questionableBookList = []
        # filename = 'shelflist.xlsx'
        # bookList = readfile.readfile(filename)
        # self.questionableBookList.append(bookList)
        # self.questionableBookList.append(bookList)
        pass

    def __str__(self):
        result = "Questionable Book List\n"
        for branch in self.questionableBookList:
            for book in branch:
                result += (str(book.barcode) + '->')
            result += '||\n'
        return result

    def addBook(self,bookBarcode):
        found = False
        for branch in self.questionableBookList:
            if(branch.getHead().barcode == bookBarcode):
                return -1 #meaning the book is already in the first layer of the tree
        book_info = {
            'barcode': bookBarcode,
            'title': None,
            'call number': None,
            'version': None
            }
        newBookList =BookList.BookList(bookinfo[0])

        self.questionableBookList.append()

    
test = tracetree()
filename = 'shelflist.xlsx'
bookList = readfile.readfile(filename)
test.addBook(12355)
print('1')
print(test)

