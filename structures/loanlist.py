class LoanListException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class Node:
    def __init__(self, loan: object):
        self.loan = loan
        self.next = None

    def __str__(self):
        return str(self.value)


class LoanList:
    def __init__(self):
        self.__start = None
        self.__length = 0

    
    def __str__(self) -> str:
        s = '{ '
        cursor = self.__start
        while(cursor != None):
            s += f'\n[{cursor.loan}\n]'
            cursor = cursor.next
        s += '}'
        return s

    
    def __len__(self) -> int:
        return self.__length


    def isEmpty(self) -> bool:
        return self.__start == None

    
    def search(self, id: int) -> bool:
        cursor = self.__start
        while(cursor != None):
            if cursor.loan.id == id:
                return True
            cursor = cursor.next
        return False

    
    def get(self, id: int) -> object:
        cursor = self.__start
        while(cursor != None):
            if cursor.loan.id == id:
                return cursor.loan
            cursor = cursor.next
        raise LoanListException(f'Loan with id "{id}" does not exist.')
    

    def insert(self, loan: object) -> None:

        new = Node(loan)
        # empty list
        if (self.isEmpty()):
            self.__start = new
            self.__length += 1
            return

        # not empty and inserting in the last position
        cursor = self.__start
        count = 1
        while ( (count < self.__length - 1) and (cursor != None)):
            cursor = cursor.next
            count += 1

        new.prox = cursor.next
        cursor.next = new
        self.__length += 1


    def remove(self, id:int) -> bool:
        try:
            if not self.search(id):
                raise LoanListException(f'There is not a loan with this id.')

            if self.isEmpty():
                raise LoanListException(f'Empty loan list.')

            cursor = self.__start

            while(cursor.loan.id != id) :
                previous = cursor
                cursor = cursor.next

            if( cursor == self.__start):
                self.__start = cursor.next
            else:
                previous.next = cursor.next

            self.__length -= 1
        
        except TypeError:
            raise LoanListException(f'The id must be an integer.')            