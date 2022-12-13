import sys
sys.path.append('./structures')

from linkedlist import LinkedList

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
                USER INFO

            Username: {self.__id}
            Books loaned: {self.loans}'''
        