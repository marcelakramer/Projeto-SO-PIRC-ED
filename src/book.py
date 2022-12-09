class UnavailableBookError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class Book:
    def __init__(self, isbn: int, title: str, copies: int = 1) -> None:
        self.__isbn = isbn
        self.__title = title
        self.__copies = copies
        self.__status = 'AVAILABLE'

    
    @property
    def title(self) -> str:
        return self.__title

    
    def __str__(self) -> str:
        return f'''
               BOOK INFO

        ISBN: {self.__isbn}
        Title: "{self.__title}"
        Number of available copies: {self.__copies}
        Status: {self.__status}
        '''

    def update_status(self) -> None:
        if self.__copies == 0:
            self.__status = 'UNAVAILABLE'
        else:
            self.__status == 'AVAILABLE'


    def loan_copy(self) -> bool:
        if self.__status == 'UNAVAILABLE':
            raise UnavailableBookError('This book is not available for loan.')
        
        self.__copies -= 1
        self.update_status()
        return True


    def return_copy(self) -> None:
        self.__copies += 1
        self.update_status()    