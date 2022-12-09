from datetime import date, timedelta
from book import Book


class UnavailableLoanRenewalError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class Loan:
    def __init__(self, id: int, book: Book) -> None:
        self.__id = id
        self.__book = book
        self.__date = date.today()
        self.__devolution = self.__date + timedelta(days = 10)
        self.__status = 'ON TIME'
 
    
    def __str__(self) -> str:
        return f'''
               LOAN INFO

        ID: {self.__id}
        Book: {self.__book.__title}
        Date: {self.__date}
        Devolution date: {self.__devolution}
        Status: {self.__status}
        '''

    
    def update_status(self) -> None:
        delta = self.__devolution - self.__date
        if delta.days > 10:
            self.__status == 'LATE'

        else:
            self.__status == 'ON TIME'

    
    def renew(self) -> bool:
        if self.__status == 'Late':
            raise UnavailableLoanRenewalError('The loan has already passed the date of devolution.')
        
        self.__devolution += timedelta(days = 10)
        return True
