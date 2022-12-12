class Book:
    def __init__(self, isbn: int, title: str) -> None:
        self.__isbn = isbn
        self.__title = title
        self.__status = True # available

    @property
    def isbn(self) -> int:
        return self.__isbn

    @property
    def title(self) -> str:
        return self.__title

    @property
    def status(self) -> bool:
        return self.__status
    
    def __str__(self) -> str:
        return f'''
               BOOK INFO

        ISBN: {self.__isbn}
        Title: "{self.__title}"
        Status: {self.__status}
        '''

    def update_status(self) -> None:
        self.__status = False if self.__status == True else True
  