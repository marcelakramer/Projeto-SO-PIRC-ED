from datetime import date, timedelta

import threading
import time


mutex = threading.Semaphore(1)

import sys
sys.path.append('./..')

from src.user import User
from src.loan import Loan
from src.book import Book



from structures.bookshelf import AVLBookshelf
from structures.linkedlist import LinkedList
from structures.exceptions import LoginFailException, AbsentObjectException, UnavailableObjectException

class Library:
    def __init__(self) -> None:
        self.__loans = LinkedList()
        self.__users = LinkedList()
        self.__bookshelf = AVLBookshelf()
        self.__autoinc = 1


    @property
    def loans(self) -> object:
        return self.__loans

    @property
    def users(self) -> object:
        return self.__users

    @property
    def bookshelf(self) -> object:
        return self.__bookshelf
    

    def register_user(self, username: str, password: str) -> None:
        newUser = User(username, password)
        self.__users.insert(newUser)

    
    def login(self, username: str, password: str) -> bool:
        user = self.__users.get(username)
        if user.password != password:
            return False
        
        return True

    def register_book(self, book_isbn: int, book_title: str) -> None:
        newBook = Book(book_isbn, book_title)
        self.__bookshelf.insert(newBook)


    def check_book(self, book_isbn: int) -> bool:
        return self.__bookshelf.searchBook(book_isbn)

    
    def check_available(self, book_isbn: int) -> bool:
        return self.__bookshelf.isAvailable(book_isbn)

    
    def loan_book(self, book_isbn: int, username: str, password: str) -> bool:
        if not self.login(username, password):
            raise LoginFailException
        
        if not self.check_available(book_isbn):
            raise UnavailableObjectException

        user = self.__users.get(username)

        book = self.__bookshelf.getBook(book_isbn)

        mutex.acquire()

        book.update_status()

        newLoan = Loan(self.__autoinc, book)
        self.__autoinc += 1 
    
        self.loans.insert(newLoan)
        user.loans.insert(newLoan)

        mutex.release()

        return True, newLoan.id

    def check_loan_info(self, loan_id: int, username: str, password: str) -> str:
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username)

        if not user.loans.search(loan_id):
            raise AbsentObjectException

        loan = user.loans.get(loan_id)
        loan.update_status()
        return str(loan)

    
    def check_loan_list(self, username: str, password: str) -> str:
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username)
        for i in range(1, user.loans.length):
            user.loans.get(i).update_status()
        return str(user.loans)

    
    def renew_loan(self, loan_id: int, username: str, password: str) -> bool:
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username)

        if not user.loans.search(loan_id):
            raise AbsentObjectException

        loan = user.loans.get(loan_id)
        loan.update_status()
        if loan.status == 'LATE':
                raise UnavailableObjectException
        else:
            loan.renewal = date.today()
            loan.devolution = loan.renewal + timedelta(days = 10)

            return True

        
    def return_book(self, loan_id: int, username: str, password: str) -> None:
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username)

        if not user.loans.search(loan_id):
            raise AbsentObjectException

        loan = self.loans.get(loan_id)
        loan.status = 'RETURNED'
        book = loan.book
        book.update_status()
        user.loans.remove(loan_id)
        

    def bookList(self):
        return self.__bookshelf.InOrder()


    def delete_book(self, book_isbn: int) -> None:
        newBook = Book(book_isbn, book_title)
        self.__bookshelf.insert(newBook)
