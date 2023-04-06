#test file
import Book
import BookList
bl = BookList.BookList()
b = Book.Book('Off the record with F.D.R., 1942-1945 /','author',31840001105024,'E807 .H34')
c = Book.Book('Franklin D. Roosevelt, an informal biography,','author',31840001101684,'E807 .H35')
d = Book.Book('That man : an insider\'s portrait of Franklin D. Roosevelt /','author', 31840007137245,'E807 .J36 2003')
e = Book.Book('The juggler : Franklin Roosevelt as wartime statesman /','author',31840003303312,'E807 .K48 1991')
bl.addBook(b)
bl.addBook(c)
bl.addBook(d)
bl.addBook(e)
bl.printList()
b.printBook()