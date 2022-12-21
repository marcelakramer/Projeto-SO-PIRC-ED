# Class Book
class Book:
    def __init__(self, isbn: int, title: str) -> None:
        '''
        Method that initializes the book instance with its attributes
        
        '''
        self.__id = isbn
        self.__title = title
        self.__status = True # available


    @property
    def id(self) -> int:
        '''
        Method to access the isbn private attribute
        
        '''
        return self.__id


    @property
    def title(self) -> str:
        '''
        Method to access the title private attribute
        
        '''
        return self.__title

    @property
    def status(self) -> bool:
        '''
        Method to access the status private attribute
        
        '''
        return self.__status
    
    def __str__(self) -> str:
        '''
        Method that creates a string representation for the book

        Returns this string

        '''
        return f"""[ISBN: {self.__id} | Title: '{self.__title}' |  Status: {'AVAILABLE' if self.__status else 'LOANED'}]\n"""

    def update_status(self) -> None:
        '''
        Method that reverses the book's current status

        '''
        self.__status = not self.__status
        
        
    def __eq__(self, other: object) -> bool:
        return self.__id == other