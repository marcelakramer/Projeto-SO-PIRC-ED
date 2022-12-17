# Initial imports
from datetime import date, timedelta

# Class Loan
class Loan:
    def __init__(self, id: int, book: object) -> None:
        '''
        Method that initializes the loan instance with its attributes
        
        '''
        self.__id = id
        self.__book = book
        self.__date = date.today()
        self.__renewal = self.__date
        self.__devolution = self.__date + timedelta(days = 10) # sets the devolution date to 10 days after the current date
        self.__returned = None
        self.__status = 'ON TIME'

    
    @property
    def id(self) -> int:
        '''
        Method to access the id private attribute
        
        '''
        return self.__id
        
    @property
    def book(self) -> object:
        '''
        Method to access the book private attribute
        
        '''
        return self.__book

    @property
    def renewal(self) -> date:
        '''
        Method to access the renewal private attribute
        
        '''
        return self.__renewal

    @property
    def devolution(self) -> date:
        '''
        Method to access the devolution private attribute
        
        '''
        return self.__devolution

    @property
    def status(self) -> str:
        '''
        Method to access the status private attribute
        
        '''
        return self.__status


    @renewal.setter
    def renewal(self, new_renewal: date) -> None:
        '''
        Method to change the renewal private attribute
        
        '''
        self.__renewal = new_renewal


    @devolution.setter
    def devolution(self, new_devolution: date) -> None:
        '''
        Method to change the devolution private attribute
        
        '''
        self.__devolution = new_devolution


    @status.setter
    def status(self, new_status: date) -> None:
        '''
        Method to change the status private attribute
        
        '''
        self.__status = new_status
    

    def __str__(self) -> str:
        '''
        Method that creates a string representation for the loan

        Returns this string

        '''
        return f"""[ID: {self.__id} | Book: '{self.__book.title}' | Devolution Date: {self.__devolution} | Status: {self.__status}]\n"""

    
    def update_status(self) -> None:
        '''
        Method that update the loan status based on the difference between the loan date and the devolution date or on the 'returned' attribute

        Returns this string

        '''
        if self.__returned == None:
            delta = self.__devolution - self.__renewal
            print(delta)
            if delta.days > 10: # checks if more than 10 days have passed since the loan date
                self.__status = 'LATE'
            else:
                self.__status = 'ON TIME'
        else:
            self.__returned = True
            self.__status = 'RETURNED'