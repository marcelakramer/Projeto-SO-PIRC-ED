# Initial imports

import sys
sys.path.append('./..') # allows the /strcutures files import

from structures.linkedlist import LinkedList

# Class User
class User:
    def __init__(self, username: str, password: str) -> None:
        '''
        Method that initializes the user instance with its attributes
        
        ''' 
        self.__id = username 
        self.__password = password
        self.loans = LinkedList()

    
    @property
    def id(self) -> str:
        '''
        Method to access the id private attribute
        
        '''
        return self.__id


    @property
    def password(self) -> str:
        '''
        Method to access the password private attribute
        
        '''
        return self.__password


    def __str__(self) -> str:
        '''
        Method that creates a string representation for the user

        Returns this string

        '''
        return f'''
Username: '{self.__id}'
Loans: {self.loans}
            ''' 

    def __eq__(self, other: int) -> bool:
        return self.__id == other

    def __ne__(self, other: int) -> bool:
        return self.__id != other

    def __gt__(self, other: int) -> bool:
        return self.__id > other

    def __lt__(self, other: int) -> bool:
        return self.__id < other
