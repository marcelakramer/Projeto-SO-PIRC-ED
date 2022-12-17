
import sys
sys.path.append('./..')

from structures.exceptions import TypeErrorException, AbsentObjectException, EmptyListException, AlreadyExistingObjectException

class Node:
    def __init__(self, content: object):
        self.content = content
        self.next = None

    def __str__(self):
        return str(self.content)


class LinkedList:
    def __init__(self):
        self.__start = None
        self.__length = 0

    
    @property
    def length(self) -> int:
        return self.__length

    
    def __str__(self) -> str:
        s = ''
        cursor = self.__start
        while(cursor != None):
            s += f'{cursor.content}'
            cursor = cursor.next
        return s

    
    def __len__(self) -> int:
        return self.__length


    def isEmpty(self) -> bool:
        return self.__start == None

    
    def search(self, value: any) -> bool:
        cursor = self.__start
        while(cursor != None):
            if cursor.content.id == value:
                return True
            cursor = cursor.next
        return False

    
    def get(self, value: any) -> object:
        cursor = self.__start
        while(cursor != None):
            if cursor.content.id == value:
                return cursor.content
            cursor = cursor.next
        
        raise AbsentObjectException
            

    def insert(self, content: object) -> None:
        
        if self.search(content.id):
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


    def remove(self, id:int) -> bool:
        try:
            if not self.search(id):
                raise AbsentObjectException

            if self.isEmpty():
                raise EmptyListException

            cursor = self.__start

            while(cursor.content.id != id) :
                previous = cursor
                cursor = cursor.next

            if( cursor == self.__start):
                self.__start = cursor.next
            else:
                previous.next = cursor.next

            self.__length -= 1
        
        except TypeError:
            raise TypeErrorException            