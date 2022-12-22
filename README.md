# **KES PROTOCOL**

**Overview**

The KES is an application-level protocol created to be used in a specific client-server application that functions as a virtual library. It is stateful, simple and intuitive. KES allows data exchange between a server and multiple clients, embracing all necessary commands to the application functions properly.

After a connection is established between server and client, the last must send a line-command request according to KES rules — followed by its parameters if necessary — and the first will answer with a code informing the status of the response and other parameters if needed.

<hr>

## **Request Methods**

### **No login required**

-     REGISTER [ username ] [ password ]        Register a new user.

-     LOGIN [ username ] [ password ]           Login.

-     QUIT                                      Quit the connection.             


### **Login required**

-     CHECK [ book ISBN ]                       Check if a book is available for loan.

-     BOOKLIST                                  List all books.

-     LOAN [ book ISBN ]                        Loan a book.

-     INFO [ loan ID ]                          Check a loan’s information.

-     LIST                                      List a user's current loans.

-     RENEW [ loan ID ]                         Renew a loan.

-     RETURN [ loan ID ]                        Return a loan.


## **Response Codes**

### **Success**

-     +OK 20 [ username ]                             user registered successfully

-     +OK 21 [ username ]                             user logged in successfully

-     +OK 22 [ list of books ]                        book list accessed successfully 

-     +OK 23 [ book title ]                           book available for loan

-     +OK 24 [ loan ID ] [ book title ]               loan made successfully 

-     +OK 25 [ loan’s info ]                          loan info accessed successfully 

-     +OK 26 [ list of loans ]                        loan list accessed successfully 

-     +OK 27 [ loan ID ]                              loan renewed successfully

-     +OK 28 [ loan ID ]                              loan returned successfully

-     +OK 29                                          client disconnect request received successfully

### **Error**

-     -ERR 40 [ command ]                             invalid command

-     -ERR 41                                         session already initialized

-     -ERR 42                                         user already logged in

-     -ERR 43                                         user already registered

-     -ERR 44                                         the username or the password are incorrect

-     -ERR 45                                         book not registered on the bookshelf

-     -ERR 46                                         book unavailable for loan

-     -ERR 47                                         nonexistent loan for this user

-     -ERR 48                                         loan already late

-     -ERR 49                                         login required
