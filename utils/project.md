# Functionalities

register [USERNAME] [PASSWORD] = register a new user
check [BOOK ISBN] = check if a book is available for loan
books = check all books in the library
loan [BOOK ISBN] [USERNAME] [PASSWORD] = loan a book
info [LOAN ID] = check loan's info
renew [LOAN ID] [USERNAME] [PASSWORD] = renew a book loan
return [LOAN ID] = return a book
quit = disconnect from server

# Error codes
+OK 20 [ username ] : user registered successfully
+OK 21 [ username ] : user logged in successfully 
+OK 22 [ list of books ] : book list accessed successfully 
+OK 23 [ book title ] : book available for loan 
+OK 24 [ loan ID ] [ book title ] : loan done successfully 
+OK 25 [ loan’s info ] : loan info accessed successfully 
+OK 26 [ list of loans ] : loan list accessed successfully
+OK 27 [ loan ID ] : loan renewed successfully
+OK 28 [ loan ID ] : loan returned successfully
+OK 29: client disconnect request received successfully



-ERR 40 = invalid command
-ERR 41 = user already registered
-ERR 42 = the username or the password are incorrect
-ERR 43 = book not registered on the bookshelf
-ERR 44 = book unavailable for loan
-ERR 45 = unexistent loan for this user
-ERR 46 = loan already late

