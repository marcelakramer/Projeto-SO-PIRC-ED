# Initial imports

from datetime import date, timedelta

import threading

import csv
import sys
sys.path.append('./..') # allows the /src and /strcutures files import

from src.user import User
from src.loan import Loan
from src.book import Book

from structures.bookshelf import AVLBookshelf
from structures.linkedlist import LinkedList
from structures.exceptions import LoginFailException, AbsentObjectException, UnavailableObjectException

# creates the semaphores 
mutex_loan = threading.Semaphore(1)
mutex_check = threading.Semaphore(1)

# Class Library that manages the library itself
class Library:
    '''
    Method that initializes the library instance with its attributes
    
    '''
    def __init__(self) -> None:
        self.__loans = LinkedList() # list of all the loans already made 
        self.__users = LinkedList() # list of all the users registered
        self.__load_users()
        self.__bookshelf = AVLBookshelf() # AVL Tree of all the books
        self.__autoinc = 1 # used for loan ID purposes


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
        newUser = User(username, password) # creates a new instance of User object
        self.__users.insert(newUser) # insert the object in the list
        with open('registered_users.csv', 'a+', newline='', encoding='utf8') as user_list:
            writer = csv.writer(user_list)
            print(user_list)
            writer.writerow([username,password])

    
    def login(self, username: str, password: str) -> bool:
        '''
        Method to perform the user login

        Returns either True or False based on the password validation
        
        '''
        user = self.__users.get(username) # gets the user object based in its username
        if user.password != password: # check the password
            return False
        
        return True

    def register_book(self, book_isbn: int, book_title: str) -> None:
        '''
        Method to register a new book on the bookshelf
        
        '''
        newBook = Book(book_isbn, book_title) # creates a new book object
        self.__bookshelf.insert(newBook) # inserts the object in the bookshelf


    def check_book(self, book_isbn: int) -> bool:
        '''
        Method to check if the book is registered on the bookshelf

        Returns either True or False
        
        '''
        return self.__bookshelf.searchBook(book_isbn) # checks if the book exists on the bookshelf and return the result

    
    def check_available(self, book_isbn: int) -> bool:
        '''
        Method to check if the book is available for loan

        Returns either True of False
        
        '''
        mutex_check.acquire() # 'up' on the semaphore

        is_available = self.__bookshelf.isAvailable(book_isbn) # get the book status 

        mutex_check.release() # 'down' on the semaphore

        return is_available # returns the book status

    
    def loan_book(self, book_isbn: int, username: str, password: str) -> bool:
        '''
        Method to loan a book

        Returns either True or False
        
        '''
        if not self.login(username, password): 
            raise LoginFailException
        

        if not self.check_available(book_isbn): # check if the book is available
            raise UnavailableObjectException

        user = self.__users.get(username) # gets the user based on its username

        book = self.__bookshelf.getBook(book_isbn) # gets the book based on its ISBN

        mutex_loan.acquire() # 'up' on the semaphore

        book.update_status() # updates the book status for 'False"

        newLoan = Loan(self.__autoinc, book) # creates a new loan instance for the book
        self.__autoinc += 1  
    
        self.loans.insert(newLoan) # inserts the loan on the library loan list
        user.loans.insert(newLoan) # inserts the loan on the user loan list

        mutex_loan.release() # 'down' on the semaphore

        return True, newLoan.id # returns the loan ID

    def check_loan_info(self, loan_id: int, username: str, password: str) -> str:
        '''
        Method to check a loan's information

        Returns a string with the loan information
        
        '''
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username) # gets the user based on its username

        if not user.loans.search(loan_id): # checks if the user has a loan with the ID provided
            raise AbsentObjectException

        loan = user.loans.get(loan_id) # gets the loan based on its ID
        loan.update_status() # updates the loan status before returning its information
        return str(loan) # returns the loan information as string

    
    def check_loan_list(self, username: str, password: str) -> str:
        '''
        Method to check a user's loan list

        Returns the loan list as a string
        
        '''
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username) # gets the user based on its username
        # updates all loans status 
        for i in range(1, user.loans.length):
            user.loans.get(i).update_status()
        return str(user.loans) # returns all the user's loan as a string

    
    def renew_loan(self, loan_id: int, username: str, password: str) -> bool:
        '''
        Method to renew a loan

        Returns either True or False
        
        '''
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username) # gets the user based on its username

        if not user.loans.search(loan_id): # checks if the user has a loan with the ID provided
            raise AbsentObjectException

        loan = user.loans.get(loan_id) # gets the loan based on its ID
        loan.update_status() # updates the loan status
        if loan.status == 'LATE': # checks if the loan is LATE
                raise UnavailableObjectException
        else:
            loan.renewal = date.today() # renews the loan
            loan.devolution = loan.renewal + timedelta(days = 10) # recalculates the devolution date

            return True

        
    def return_book(self, loan_id: int, username: str, password: str) -> None:
        '''
        Method to return a book
        
        '''
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username) # gets the user based on its username

        if not user.loans.search(loan_id): # checks if the user has a loan with the ID provided
            raise AbsentObjectException

        loan = self.loans.get(loan_id) # gets the loan based on its ID
        loan.status = 'RETURNED' # updates the loan status to RETURNED
        book = loan.book # gets the book from the loan
        book.update_status() # updates the book status
        user.loans.remove(loan_id) # removes the loan from the user current loans list


    def __load_users (self):
        with open('registered_users.csv', encoding='utf8') as registered_users:
            user_list = csv.reader(registered_users,delimiter=',')
            print(user_list)
            for user in user_list:
                print(user)
                new_user = User(user[0],user[1])
                self.__users.insert(new_user)
        

    def bookList(self) -> str:
        '''
        Method to check all the books on the library

        Returns all the books as a string
        
        '''
        return self.__bookshelf.InOrder() # returns all the books as a string ordered by their ISBN


    def delete_book(self, book_isbn: int) -> None:
        '''
        Method to delete a book from the bookshelf
        
        '''
        book = self.__bookshelf.getBook(book_isbn) # gets the book based on its ISBN
        self.__bookshelf.delete(book) # deletes the book from the bookshelf
