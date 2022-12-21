# Initial imports

from tempfile import NamedTemporaryFile
import shutil

from datetime import date, timedelta

import threading

import csv
import sys
sys.path.append('./..') # allows the /src and /strcutures files import

from src.user import User
from src.loan import Loan
from src.book import Book

from structures.AVL import AVLTree
from structures.linkedlist import LinkedList
from structures.exceptions import AbsentObjectException, UnavailableObjectException

# creates the semaphores 
mutex_loan = threading.Semaphore(1)
mutex_check = threading.Semaphore(1)
mutex_register = threading.Semaphore(1)
mutex_booklist = threading.Semaphore(1)

# Class Library that manages the library itself
class Library:
    '''
    Method that initializes the library instance with its attributes
    
    '''
    def __init__(self) -> None:
        self.__loans = LinkedList() # list of all the loans already made 
        self.__users = LinkedList() # list of all the users registered
        self.__bookshelf = AVLTree() # AVL Tree of all the books
        self.__autoinc = 1 # used for loan ID purposes
        self.__load_books()
        self.__load_users()
        self.__load_lib_loans()
        

    @property
    def loans(self) -> object:
        '''
        Method to access the loans private attribute
        
        '''
        return self.__loans

    @property
    def users(self) -> object:
        '''
        Method to access the users private attribute
        
        '''
        return self.__users

    @property
    def bookshelf(self) -> object:
        '''
        Method to access the bookshelf private attribute
        
        '''
        return self.__bookshelf
    

    def register_user(self, username: str, password: str) -> None:
        '''
        Method to register a new user with its username(id) and password
        
        '''
        mutex_register.acquire() # up

        newUser = User(username, password) # creates a new instance of User object
        self.__users.insert(newUser) # insert the object in the list

        
        mutex_register.release() # down
        
        
        """
        with open('registered_users.csv', 'a+', newline='', encoding='utf8') as user_list:
            writer = csv.writer(user_list)
            print(user_list)
            writer.writerow([username,password])"""

    
    def register_book(self, book_isbn: int, book_title: str) -> None:
        '''
        Method to register a new book on the bookshelf
        
        '''
        newBook = Book(book_isbn, book_title) # creates a new book object
        self.__bookshelf.insert(newBook) # inserts the object in the bookshelf

    
    def login(self, username: str, password: str) -> bool:
        '''
        Method to perform the user login

        Returns either True or False based on the password validation
        
        '''
        user = self.__users.get(username) # gets the user object based in its username

        if user.password != password: # check the password
            return False
        
        return True


    def check_book(self, book_isbn: int) -> bool:
        '''
        Method to check if the book is registered on the bookshelf

        Returns either True or False
        
        '''
        return self.__bookshelf.search(book_isbn) # checks if the book exists on the bookshelf and return the result

    
    def check_available(self, book_isbn: int) -> bool:
        '''
        Method to check if the book is available for loan

        Returns either True of False
        
        '''
        mutex_check.acquire() # 'up' on the semaphore
        
        if not self.check_book(book_isbn): # checks if the book exists on the bookshelf
            raise AbsentObjectException
        
        book = self.__bookshelf.get(book_isbn) # gets the book based on its isbn
    
        is_available = book.status # get the book status 

        mutex_check.release() # 'down' on the semaphore

        return is_available # returns the book status

    
    def loan_book(self, book_isbn: int, username: str) -> bool:
        '''
        Method to loan a book

        Returns either True or False
        
        '''
        
        if not self.check_available(book_isbn): # check if the book is available
            raise UnavailableObjectException

        user = self.__users.get(username) # gets the user based on its username

        book = self.__bookshelf.get(book_isbn) # gets the book based on its ISBN

        mutex_loan.acquire() # 'up' on the semaphore

        book.update_status() # updates the book status for 'False"

        newLoan = Loan(self.__autoinc, book, username) # creates a new loan instance for the book
        self.__autoinc += 1  
    
        self.loans.insert(newLoan) # inserts the loan on the library loan list
        user.loans.insert(newLoan) # inserts the loan on the user loan list

        """with open('library_loans.csv', 'a+', newline='', encoding='utf8') as lib_loans:
            writer = csv.writer(lib_loans)
            print(lib_loans)
            writer.writerow([newLoan.id, book_isbn, newLoan.date, newLoan.renewal,newLoan.devolution,newLoan.returned,newLoan.status, newLoan.username])"""
    

        mutex_loan.release() # 'down' on the semaphore

        return True, newLoan.id # returns the loan ID

    def check_loan_info(self, loan_id: int, username: str) -> str:
        '''
        Method to check a loan's information

        Returns a string with the loan information
        
        '''
        user = self.__users.get(username) # gets the user based on its username

        if not user.loans.search(loan_id): # checks if the user has a loan with the ID provided
            raise AbsentObjectException

        loan = user.loans.get(loan_id) # gets the loan based on its ID
        loan.update_status(loan_id) # updates the loan status before returning its information
        return str(loan) # returns the loan information as string

    
    def check_loan_list(self, username: str) -> str:
        '''
        Method to check a user's loan list

        Returns the loan list as a string
        
        '''
        user = self.__users.get(username) # gets the user based on its username
        
        self.update_loans() # updates all loans status 
        
        list = ''

        # This for loop will look at all the loans in the library_loans list
        for i in range(1, self.__loans.length + 1):
            print(self.__loans.get(i).returned)
            try:
                loan = user.loans.get(i)
                list += str(loan)

            except AbsentObjectException:
                pass # a loan with this ID does not exist, so it must not be considered

        return list # returns all the user's loan as a string
    
    
    def update_loans(self):
        '''
        Method to update the status of all loans
        
        '''
        for i in range(1, self.__loans.length + 1):
            loan = self.__loans.get(i)
            loan.update_status(i)
        
    
    def renew_loan(self, loan_id: int, username: str) -> bool:
        '''
        Method to renew a loan

        Returns either True or False
        
        '''
        user = self.__users.get(username) # gets the user based on its username

        if not user.loans.search(loan_id): # checks if the user has a loan with the ID provided
            raise AbsentObjectException

        loan = user.loans.get(loan_id) # gets the loan based on its ID
        loan.update_status(loan_id) # updates the loan status
        if loan.status == 'LATE': # checks if the loan is LATE
            raise UnavailableObjectException
        else:
            loan.renewal = date.today() # renews the loan
            loan.devolution = loan.renewal + timedelta(days = 10) # recalculates the devolution date

            """            tempfile = NamedTemporaryFile(mode="w", delete=False)


            with open("library_loans.csv", "r") as lib_loans, tempfile:
                reader = csv.reader(lib_loans, delimiter=',')
                writer = csv.writer(tempfile)

                for row in reader:
                    print(row)

                    if (row[0]) == str(loan_id):
                        row[3] = loan.renewal
                        row[4] = loan.devolution


                            
                        
                    writer.writerow(row)
            
            shutil.move(tempfile.name, "library_loans.csv")"""

            return True

        
    def return_book(self, loan_id: int, username: str) -> None:
        '''
        Method to return a book
        
        '''
        user = self.__users.get(username) # gets the user based on its username

        if not user.loans.search(loan_id): # checks if the user has a loan with the ID provided
            raise AbsentObjectException

        loan = self.__loans.get(loan_id) # gets the loan based on its ID
        loan.returned = True # updates the loan status to RETURNED
        loan.update_status(loan_id)

        book = loan.book # gets the book from the loan
        book.update_status() # updates the book status
        user.loans.remove(loan_id) # removes the loan from the user current loans list
        """
        tempfile = NamedTemporaryFile(mode="w", delete=False)


        with open("library_loans.csv", "r") as lib_loans, tempfile:
            reader = csv.reader(lib_loans, delimiter=',')
            writer = csv.writer(tempfile)

            for row in reader:
                print(row)

                if (row[0]) == str(loan_id):
                    row[5] = loan.returned
                    row[6] = loan.status


                        
                    
                writer.writerow(row)
        
        shutil.move(tempfile.name, "library_loans.csv")"""



    def __load_users (self):
        with open('registered_users.csv', encoding='utf8') as registered_users:
            user_list = csv.reader(registered_users,delimiter=',')

            for user in user_list:
                new_user = User(user[0],user[1])
                self.__users.insert(new_user)

    def __load_lib_loans(self):
        with open('library_loans.csv', encoding='utf8') as lib_loans:
            loans = csv.reader(lib_loans,delimiter=',')
            for loan in loans:
                user = self.__users.get(loan[-1])
                book = self.__bookshelf.get(int(loan[1]))
                mutex_loan.acquire()
                book.update_status()
                newLoan = Loan(int(loan[0]),book,loan[-1])
                newLoan.date = date.fromisoformat(loan[2])
                newLoan.renewal = date.fromisoformat(loan[3])
                newLoan.devolution = date.fromisoformat(loan[4])
                self.__autoinc = int(loan[0]) + 1
                self.loans.insert(newLoan)
                user.loans.insert(newLoan)
                mutex_loan.release()
    
    def __load_books(self):
        with open('registered_books.csv', encoding='utf8') as book_list:
            books = csv.reader(book_list,delimiter=',')
            for book in books:
                self.register_book(int(book[0]),book[1])
            


    def bookList(self) -> str:
        '''
        Method to check all the books on the library

        Returns all the books as a string
        
        '''
        mutex_booklist.acquire() #up

        booklist = self.__bookshelf.InOrder() # returns all the books as a string ordered by their ISBN

        mutex_booklist.release() #down
        
        return booklist
