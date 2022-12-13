from datetime import timedelta

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

        print(1)
        user = self.__users.get(username)

        print(2)
        book = self.__bookshelf.getBook(book_isbn)

        print(3)
        book.update_status()



        print(4)
        newLoan = Loan(self.__autoinc, book)

        print(5)
        self.__autoinc += 1 # check autoincrement


        print(6)
        self.loans.insert(newLoan)

        print(7)
        user.loans.insert(newLoan)


        print(8)

        return True

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

        # falta achar um jeito de colocar o loan.update aqui
        user = self.__users.get(username)
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
            loan.devolution += timedelta(days = 10)
            self.loans.get(loan_id).devolution += timedelta(days = 10)
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
        

        
