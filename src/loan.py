from datetime import date, timedelta

class Loan:
    def __init__(self, id: int, book: object) -> None:
        self.__id = id
        self.__book = book
        self.__date = date.today()
        self.__renewal = self.__date
        self.__devolution = self.__date + timedelta(days = 10)
        self.__returned = None
        self.__status = 'ON TIME'

    
    @property
    def id(self) -> int:
        return self.__id
        
    @property
    def book(self) -> object:
        return self.__book

    @property
    def renewal(self) -> date:
        return self.__renewal

    @property
    def devolution(self) -> date:
        return self.__devolution

    @property
    def status(self) -> str:
        return self.__status
 
    @devolution.setter
    def devolution(self, new_devolution: date) -> None:
        self.__devolution = new_devolution

    @renewal.setter
    def renewal(self, new_renewal: date) -> None:
        self.__renewal = new_renewal

    @status.setter
    def status(self, new_status: date) -> None:
        self.__status = new_status
    

    def __str__(self) -> str:
        return f"""[ID: {self.__id} | Book: '{self.__book.title}' | Devolution Date: {self.__devolution} | Status: {self.__status}]\n"""

    
    def update_status(self) -> None:
        if self.__returned == None:
            delta = self.__devolution - self.__renewal
            print(delta)
            if delta.days > 10:
                self.__status = 'LATE'
            else:
                self.__status = 'ON TIME'
        else:
            self.__returned = True
            self.__status = 'RETURNED'