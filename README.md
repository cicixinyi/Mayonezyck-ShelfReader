# ShelfReader  


-----------------------------------------

Spring semester notes:

***!! New Thought!!*** 



SSH in from office computer for file transfer.
Per launching of the program, load the booklist.csv and start right away.

Switch gear to using the "Shelf-Reading Tool" 
Download the file from shelf-reading tool and pre-process the file, load all data into book classes.

--------------------------------------------

New Approach on the shelf checking, inspired by professor Islam.
Professor Islam suggested that this problem seems like a perfect fit for looking in an ***"edit distance"*** way.

One Levenshtein matrix will be generated, based on the requried book list and the other matrix would be of the same size but binary,
indicating the matching items' locations in the Levenshtein matrix.

using these two matrices, instructions can be generated backwards from the matrix. the priority of proceeding the matrix is: current > replacing -> adding == removing

The current structure of the whole project contains the following several modules, which each of them needed to be coded out by the end of 
march.

The modules from the office side to the shelf side are:
the officer should be able to upload the files into the device: so there should be a program for file management and tranfer to 
the device using ssh/remote in, somehow. So this is the uppermost program(1) TODO

Once the device side get the file, it can read it in to be future use in the local program. This is the program which will be called at the
beginning(2)

When the student turn the device on, it should automatically start the program, and on the touchscreen it will require the student to scan 
their id card, in order to keep track on their works. This is the login_UI.py(3)

Of cource the student id will be stored in a csv, which is the database for keeping track of their total working time, jobs they have done, 
job logs and whatnot. The database should be collected by the client's side (1) everytime and should be updated and back-uped every time. (4)

Once we know who is doing the job, we should let the student see and make sure if the job shown on the device is what they are supposed to do. By showing them the last updated date and time of the job file and the name, they should be able to tell. (5)

Once the student is in the shelf, the job dispenser program should be chopping the whole list into small chunks. Let's say it is N books per chunk, this number is heuristically selected to be 20. I would think 20 being a fair number. It is still easy for student to find a certain book within 20 books, and it is not too small that makes the book easier to miss. By miss I mean, if one book is not belonging to one certain chunk, but belongs to the next chunk, we have no choice but to take the book out: there is no direct inter-chunk operation allowed. With that being said, the smaller a chunk is, it is more likely to have this situation happen. To avoid this situation, we have to make this 
N as big as possible but remain easy for students to find one certain book from these N books. Tunning is needed.(6)
***New Thought for this paragraph: the list of N books can be made starting from the first missing book, so that the scanning can move on smoothly***

Once each chunk of books are defined, the book checking should begin. The Graphic UI should show the name of the current book's title and call number. The student should be able to read them clearly from the touchscreen. The student will start by looking at the first book on the bookshelf and compare to see if they match, if they do match, move on; if the books don't match, the barcode is required to be scanned in. So there will be a list which has N books ,which is 20 here, in order. As soon as the first book that did not seems right in the list appears, the list of twenty books is created, starting from the first book that is out-of-order, called "desired string". If the newly scanned book belongs to this 20 books, put it in a stack which will be used as the "current string" later; if the newly scanned book doesn't belong to these 20 books, put this book in a new stack, which is "missing book". After the ”current string" stack reacehs N of length, we should have a desired string shorter than N in length. When the reordering of this section begins, only two kinds of action is allowed to make the current order into desired order. 1) take out book from the stack 2)insert book we took out into a certain position. The taking out book and reinserting is equivalent to "replacing the book". (7)

From the matrix generated, we can retrace the smallest number from the bottom right and get the instructions ready for the student to follow and reshelf the book. (8)

Repeat the step 7 and step 8 until we have no more books to do in this shelfreading session. 

The session will be done, timer stops, and a report should be generated. The report will be stored in one file that is retrievable by the client.



___________________- Legacy content, original idea is below.







Legacy files can be found in the legacy folder 
#book finding logic 2.X  
Say: we are looking for Book A.  
Book should be in the ABCDEFGHI order  
Actually, Books are in AFEBDCHI order, meaning, a total mess  
-Construct a tree  
-Display on the screen the first book, and looking for the first book, A  
-A is in place, move to the second book  
-Display on the screen, looking for the book, B  
-F is in the place of B's  
-B and F doesn't match, throw both in the tree with their next nodes  
-raise the flag of F's 'hasNote', making it notify when reached  
-instruct the user to take out the book F from shelf.  
+tree{  
[B-C]  
[F-G]  
}  
+shelf{AEBDCHI}  
-move forward, looking for the book, C  
-C and E doesn't match, throw both in the tree with their next nodes  
-raise the flag of E's 'hasNote', making it notify when reached  
-instruct the user to take out the book E from shelf.  
add the C into tree, the first level, and add D to every C node  
+tree{  
[B-C-D]  
[F-G]  
[C-D]  
}  
add the E into tree, the first level, and add F to every E node  
+tree{  
[B-C-D]  
[F-G]  
[C-D]  
[E-F]  
}  
+shelf{ABDCHI}  
-move forward, looking for the book, D  
-next book on the shelf is B, which is in the tree, and doesn't appear in any node after D,  
-We first take a look at B branch in the tree, the bottom node is D, D doesn't appear in the tree's first row,  
-Meaning we can leave B at where it is and its position should be right  
+shelf{ABDCHI}  
-update the tree by deleting every children of every B node  
+tree{  
[B]  
[F-G]  
[C-D]  
[E-F]  
}  
-and add D to the tree's first row, add child E to every D node  
+tree{  
[B]  
[F-G]  
[C-D-E]  
[E-F]  
[D-E]  
}  
-still check for D  
-next book on the shelf is D  
-D is D  
-update the tree by deleting every children of every D node  
+tree{  
[B]  
[F-G]  
[C-D]  
[E-F]  
[D]  
}  
+shelf{ABDCHI}  
-move forward, looking for the book, E  
-E has a 'hasNote' flag and it will show a alert window on the screen  
-The user is required to take E and put it back on current location on the shelf.  
-update the tree by deleting every children of every E node  
+tree{  
[B]  
[F-G]  
[C-D]  
[E]  
[D]  
}  
+shelf{ABDECHI}  
-move forward, looking for the book, F    
-F has a 'hasNote' flag and it will show  a alert window on the screen  
-The user is required to take F and put it back on current location on the shelf.  
-update the tree by deleting every children of every F node  
+tree{  
[B]  
[F]  
[C-D]  
[E]  
[D]  
}  
+shelf{ABDEFCHI}  
-move forward, looking for the book, G  
-next book on the shelf is C, which is in the tree, and doesn't appear in any node after G,  
-We first take a look at C branch in the tree, the bottom node is D, D appears in the tree's first row,  
-Meaning we can instruct the user to place C before D  
+shelf{ABCDEFHI}  
-update the tree by deleting every children of every C node  
-and add G and its child to the tree  
+tree{  
[B]  
[F]  
[C]  
[E]  
[D]  
[G-H]  
}  
-still check for G  
-next book on the shelf is H  
-throw both into the tree, update evey G/H node with their child if they don't already have one  
+tree{  
[B]  
[F]  
[C]  
[E]  
[D]  
[G-H-I]  
[H-I]  
}  
+shelf{ABCDEFI}  
-move forward, looking for the book, H  
-H has a 'hasNote' flag and it will show a alert window on the screen  
-The user is required to take H and put it back on current location on the shelf.  
-update the tree by deleting every children of every H node  
+tree{  
[B]  
[F]  
[C]  
[E]  
[D]  
[G-H]  
[H]  
}  
+shelf{ABCDEFHI}  
+move forward, looking for the book, I  
-I is I   
  
  
  
Generate a report by the tree contents  
every node in the first level that doesn't have a child is misplaced  
every node in the first level that do have one+ child is missing  
every node that doesn't appear in the first level of the tree is correctly placed  
The number of misplaced item seems can be compensated by removing the number of missing items' depth in tree(needs more experiment)  

