
import sys
sys.path.append('./..')

from structures.exceptions import TypeErrorException, AbsentObjectException, EmptyListException, AlreadyExistingObjectException

# class Node
class Node:
    def __init__(self, content: object):
        '''
        Method that initializes the Node with a content and its attributes
        
        ''' 
        self.content = content
        self.next = None

    def __str__(self):
        '''
        Method that creates a string representation for the node

        Returns this string

        '''
        return str(self.content)

# class LinkedList
class LinkedList:
    def __init__(self):
        '''
        Method that initializes the list with its attributes

        '''
        self.__start = None
        self.__length = 0

    
    @property
    def length(self) -> int:
        '''
        Method to access the length private attribute
        
        '''
        return self.__length

    
    def __str__(self) -> str:
        '''
        Method that creates a string representation for the list

        Returns this string

        '''
        s = ''
        cursor = self.__start
        while(cursor != None):
            s += f'{cursor.content}'
            cursor = cursor.next
        return s

    
    def __len__(self) -> int:
        '''
        Method that returns the length of the list

        '''
        return self.__length


    def isEmpty(self) -> bool:
        '''
        Returns if linked list is empty
        
        '''
        return self.__start == None

    
    def search(self, value: any) -> bool:
        '''
        Method that searchs for a value

        Returns either True or False
        
        '''
        cursor = self.__start
        while(cursor != None):
            if cursor.content == value:
                return True
            cursor = cursor.next
        return False

    
    def get(self, value: any) -> object:
        '''
        Method that gets a node's content based on its value

        Returns the content
        
        '''
        cursor = self.__start
        while(cursor != None):
            if cursor.content== value:
                return cursor.content
            cursor = cursor.next
        
        raise AbsentObjectException
            

    def insert(self, content: object) -> None:
        '''
        Method that inserts a node with a content into the list
        
        '''
        
        if self.search(content):
            raise AlreadyExistingObjectException

        new = Node(content)

        # empty list
        if (self.isEmpty()):
            self.__start = new
            self.__length += 1
            return

        # not empty and inserting in the last position
        cursor = self.__start
        count = 1
        while ( (count < self.__length)):
            cursor = cursor.next
            count += 1

        cursor.next = new
        self.__length += 1


    def remove(self, id: int) -> bool:
        '''
        Method that removes a node from the list based on the node's content id
        
        '''

        try:
            if not self.search(id):
                raise AbsentObjectException # absent content

            if self.isEmpty():
                raise EmptyListException # empty list

            cursor = self.__start

            while(cursor.content != id) :
                previous = cursor
                cursor = cursor.next

            if( cursor == self.__start):
                self.__start = cursor.next
            else:
                previous.next = cursor.next

            self.__length -= 1
        
        except TypeError:
            raise TypeErrorException  # argument's type error          
