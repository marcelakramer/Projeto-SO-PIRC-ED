class LoanListException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class Node:
    def __init__(self, value: any):
        self.value = value
        self.next = None

    def __str__(self):
        return str(self.value)


class LoanList:
    def __init__(self):
        self.__start = None
        self.__length = 0


    def isEmpty(self)->bool:
        return self.__start == None


    def len(self)->int:
        return self.__length


    def __len__(self)->int:
        return self.__length

    
    def search(self, id:any)->int:
        cursor = self.__start
        count = 1
        while(cursor != None):
            if cursor.value == id:
                return  count
            count += 1
            cursor = cursor.next
        raise  LoanListException(f'Loan with id "{id}" does not exist.', 1)

    def modify(self, position:int, value: any):
        try:
            assert position > 0 and position <= self.__length
            count = 1
            cursor = self.__start
            while( count < position):
                cursor = cursor.prox
                count += 1

            cursor.carga = value
        except AssertionError:
            raise LoanListException(f'Invalid position for the current loan list with {self.__length} elementos')

    
    def insert(self, book: object):

        new = Node(book)
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


    def remove(self, position:int)->any:
        try:
            assert position > 0 and position <= self.__length

            if( self.isEmpty() ):
                raise LoanListException(f'Não é possível remover de uma lista vazia')

            cursor = self.__start
            count = 1

            while( count <= position-1 ) :
                previous = cursor
                cursor = cursor.next
                count+=1

            value = cursor.value

            if( position == 1):
                self.__start = cursor.next
            else:
                previous.next = cursor.next

            self.__length -= 1
            return value
        
        except TypeError:
            raise LoanListException(f'A posição deve ser um número inteiro')            
        except AssertionError:
            raise LoanListException(f'A position deve ser um número entre 1 e {self.__length}')
        except:
            raise

    
    def __str__(self):
        s = '[ '
        cursor = self.__start
        while(cursor != None):
            s += f'{cursor.value} '
            cursor = cursor.near
        s += ']'
        return s