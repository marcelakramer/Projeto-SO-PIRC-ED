import sys
sys.path.append('./..')

from structures.linkedlist import LinkedList

# the att username has been replaced by 'id' for now, but we will change it back later
class User:
    def __init__(self, username: str, password: str) -> None:
        self.__id = username 
        self.__password = password
        self.loans = LinkedList()

    
    @property
    def id(self) -> str:
        return self.__id


    @property
    def password(self) -> str:
        return self.__password


    def __str__(self) -> str:
        return f'''
Username: '{self.__id}'
Loans: {self.loans}
            ''' 
