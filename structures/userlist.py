class UserListException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class Node:
    def __init__(self,  user: object):
        self.user = user
        self.next = None

    def __str__(self):
        return str(self.value)


class UserList:
    def __init__(self):
        self.__start = None
        self.__length = 0

    
    def __str__(self) -> str:
        s = '{ '
        cursor = self.__start
        while(cursor != None):
            s += f'\n[{cursor.user}\n]'
            cursor = cursor.next
        s += '}'
        return s

    
    def __len__(self) -> int:
        return self.__length


    def isEmpty(self) -> bool:
        return self.__start == None

    
    def search(self, username: str) -> bool:
        cursor = self.__start
        while(cursor != None):
            if cursor.user.username == username:
                return True
            cursor = cursor.next
        return False

    
    def get(self, username: str) -> object:
        cursor = self.__start
        while(cursor != None):
            if cursor.user.username == username:
                return cursor.user
            cursor = cursor.next
        raise UserListException(f'User with username "{username}" does not exist.')
    

    def insert(self, user: object) -> None:

        new = Node(user)
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


    def remove(self, usename: str) -> bool:
        try:
            if not self.search():
                raise UserListException(f'There is not an user with this username.')

            if self.isEmpty():
                raise UserListException(f'Empty user list.')

            cursor = self.__start

            while(cursor.loan.__id != id) :
                previous = cursor
                cursor = cursor.next

            if( cursor == self.__start):
                self.__start = cursor.next
            else:
                previous.next = cursor.next

            self.__length -= 1
        
        except TypeError:
            raise UserListException(f'The id must be an integer.')

    
    def login(self, username: str, password: str) -> True:
        try:
            if not self.search(username):
                raise UserListException(f'There is not an user with this username.')

            if self.isEmpty():
                raise UserListException(f'Empty user list.')

            user = self.get(username)
            if user.password == password:
                return True
            else:
                return False
        
        except TypeError:
            raise UserListException(f'The id must be an integer.')