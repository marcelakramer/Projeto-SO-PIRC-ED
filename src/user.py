from structures.loanlist import LoanList

class User:
    def __init__(self, username: str, password: str) -> None:
        self.__username = username
        self.__password = password
        self.loans = LoanList()

    
    @property
    def username(self) -> str:
        return self.__username


    @property
    def password(self) -> str:
        return self.__password


    def __str__(self) -> str:
        return f'''
                USER INFO

            Username: {self.__username}
            Books loaned: {self.loans}'''
        