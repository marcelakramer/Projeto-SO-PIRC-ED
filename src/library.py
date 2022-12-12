from user import User
from loan import Loan
from book import Book
from structures.bookshelf import AVLBookshelf
from structures.linkedlist import LinkedList
from structures.exceptions import LoginFailException, AbsentObjectException, UnavailableObjectException
from time import timedelta


class Library:
    def __init__(self) -> None:
        self.__loans = LinkedList()
        self.__users = LinkedList()
        self.__bookshelf = AVLBookshelf()

    
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

        book = self.__bookshelf.get(book_isbn)
        book.update_status()

        newLoan = Loan(1, book)

        self.loans.insert(newLoan)
        user.loans.insert(newLoan)

    
    def check_loan_info(self, loan_id: int, username: str, password: str) -> str:
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username)

        if not user.loans.search(loan_id):
            raise AbsentObjectException

        loan = user.loans.get(loan_id)
        return str(loan)

    
    def check_loan_list(self, username: str, password: str) -> str:
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username)
        return str(user.loans)

    
    def renew_loan(self, loan_id: int, username: str, password: str) -> bool:
        if not self.login(username, password):
            raise LoginFailException

        user = self.__users.get(username)

        if not user.loans.search(loan_id):
            raise AbsentObjectException

        loan = user.loans.get(loan_id)
        if loan.status == 'LATE':
                return False # raise
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
        

        
