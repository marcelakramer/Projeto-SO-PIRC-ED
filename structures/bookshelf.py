import sys
sys.path.append('./..')

from structures.exceptions import AbsentObjectException
class Node(object): 
    def __init__(self, book: object): 
        self.book = book 
        self.left = None
        self.right = None
        self.height = 1 # attribute that specifies the balance factor of the node
    
    def __str__(self):
        return f'{self.book}'
  
# AVL tree class
class AVLBookshelf(object): 
    def __init__(self, book:object = None) -> None:
        '''
        If method is initialized without any argument
        AVL is created with "None" at the root

        If the argument is given
        a node with the book is created
        
        '''
        if book is None:
            self.__root = None
        else:
            self.__root = self.insert(book)


    def isEmpty(self) -> bool:
        '''
        Returns if AVL is empty
        
        '''

        # Returns whether the root is empty or not
        return self.__root == None 


    def insert(self, book:object) -> None:
        '''
        Call a private method to insert a book in the tree

        Receives one object as an argument
        
        '''

        # Inserts in the root if AVL is empty
        if(self.__root == None):
            self.__root = Node(book)

        # Calls a recursive function to insert
        else:
            self.__root = self.__insert(self.__root, book)
  
  
    def __insert(self, root, book) -> Node:
        '''
        Objectively insert the book in the AVL

        Receives the root and the book to be inserted as arguments
        
        '''

        # Performs a BST recursion to add the node
        if not root: 
            return Node(book) 
        elif book.isbn < root.book.isbn: 
            root.left = self.__insert(root.left, book) 
        else: 
            root.right = self.__insert(root.right, book) 
  
        # Update the height of ancestor node
        root.height = 1 + max(self.getHeight(root.left), 
                              self.getHeight(root.right)) 
  
        # Computes the balance factor 
        balance = self.getBalance(root) 
  
        # Checks if the node is unbalanced
        # Then, one of the following actions will be performed:

        # Right rotation
        if balance > 1 and book.isbn < root.left.book.isbn: 
            return self.__rightRotate(root) 
  
        # Left rotation
        if balance < -1 and book.isbn > root.right.book.isbn: 
            return self.__leftRotate(root) 
  
        # Double rotation: Left Right 
        if balance > 1 and book.isbn > root.left.book.isbn: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # Double rotation: Right Left 
        if balance < -1 and book.isbn < root.right.book.isbn: 
            root.right = self.__rightRotate(root.right) 
            return self.__leftRotate(root) 
  
        return root 
  

    def __leftRotate(self, p:Node) -> Node: 
        '''
        Rotates the tree to the left to keep it balanced

        Receives the Node to be rotated

        '''
        u = p.right 
        T2 = u.left 
  
        # Perform rotation 
        u.left = p 
        p.right = T2 
  
        # Update heights 
        p.height = 1 + max(self.getHeight(p.left), self.getHeight(p.right)) 
        u.height = 1 + max(self.getHeight(u.left), self.getHeight(u.right)) 
  
        # Return the new root "u" node 
        return u 
  

    def __rightRotate(self, p:Node) -> Node: 
        '''
        Rotates the tree to the right to keep it balanced

        Receives the Node to be rotated

        '''
        u = p.left 
        T2 = u.right 
  
        # Perform rotation 
        u.right = p 
        p.left = T2 
  
        # Update heights 
        p.height = 1 + max(self.getHeight(p.left), 
                        self.getHeight(p.right)) 
        u.height = 1 + max(self.getHeight(u.left), 
                        self.getHeight(u.right)) 
  
        # Return the new root ("u" node)
        return u 
  

    def getHeight(self, node:Node) -> int:
        '''
        Returns the height of passed Node

        '''
        if node is None: 
            return 0
  
        return node.height 
  

    def getBalance(self, node:Node) -> int: 
        '''
        Returns the balance of a specific node

        '''
        if not node: 
            return 0

        # Returns the height of node at left and node at right
        return self.getHeight(node.left) - self.getHeight(node.right) 
  

    def InOrder(self):
        '''
        Calls a private function that returns a string
        '''
        return self.__InOrder(self.__root)


    def __InOrder(self, root: Node): 
        '''
        Returns a formated string of all the items of the tree

        A node (root as default) to proceed is needed

        '''

        # Returns an empty string if there is no node
        if not root: 
            return ''


        if root is not None:
            left = self.__InOrder(root.left)
            right = self.__InOrder(root.right)

            # Returns a concatenated string of values of left and right nodes
            return left + ' ' + str(root.book) + ' ' + right


    def delete(self, book:object):
        '''
        Deletes an instance calling a private method

        It must receive the book to be deleted as an argument

        '''
        if(self.__root is not None):
            self.__root = self.__delete(self.__root, book)
        

    def __delete(self, root:Node, book:object) -> Node:
        '''
        Private method to delete the book

        Receives the book to be deleted
        and the root


        '''

        # Perform standard BST delete 
        if not root: 
            return root   

        # Search for the book by analyzing the ISBN
        elif book.isbn < root.book.isbn: 
            root.left = self.__delete(root.left, book)   
        elif book.isbn > root.book.isbn: 
            root.right = self.__delete(root.right, book)   
        else: 
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 
  
            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 
  
            temp = self.getMinbookNode(root.right) 
            root.book = temp.book 
            root.right = self.__delete(root.right, 
                                      temp.book) 
  
        # If the tree has only one node, 
        # simply return it 
        if root is None: 
            return root 
  
        # Update the height of the  
        # ancestor node 
        root.height = 1 + max(self.getHeight(root.left), 
                            self.getHeight(root.right)) 
  
        # Get the balance factor 
        balance = self.getBalance(root) 
  
        # If the node is unbalanced,  
        # then try out the 4 cases 
        
        # Left Left 
        if balance > 1 and self.getBalance(root.left) >= 0: 
            return self.__rightRotate(root) 
  
        # Right Right 
        if balance < -1 and self.getBalance(root.right) <= 0: 
            return self.__leftRotate(root) 
  
        # Left Right 
        if balance > 1 and self.getBalance(root.left) < 0: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # Right Left 
        if balance < -1 and self.getBalance(root.right) > 0: 
            root.right = self.__rightRotate(root.right) 
            return self.__leftRotate(root) 
  
        return root 

        
    def searchBook(self, book_isbn: int) -> bool:
        '''
        Calls a recursive function to search for a book

        The book isbn must be passed
        
        '''

        return self.__searchBook(book_isbn, self.__root)
    

    def __searchBook(self, book_isbn: int, node: Node) -> bool:
        '''
        Properly looks for the book passed through the arguments

        Returns a boolean to inform whether it was possible
        to find or not
        
 =      '''

        # Base case
        if node is None:
            return False

        # Found the book
        if ( book_isbn == node.book.isbn):
            return True

        # Search by the ISBN
        elif ( book_isbn < node.book.isbn and node.left != None):
            return self.__searchBook( book_isbn, node.left)
        elif ( book_isbn > node.book.isbn and node.right != None):
            return self.__searchBook( book_isbn, node.right)
        else:
            return False

    def getBook(self, book_isbn: int) -> object:
        '''
        Returns an specific book based on the ISBN
        Calls a private method

        Needs the ISBN as an argument

        '''

        if not self.searchBook(book_isbn):
            raise AbsentObjectException

        return self.__getBook(book_isbn, self.__root)

    
    def __getBook(self, book_isbn: int, node: Node) -> object:
        '''
        Private method of "getBook"

        Receives the ISBN and the root as the arguments

        '''
        if node is None:
            return 
        if ( book_isbn == node.book.isbn ):
            return node.book
        elif ( book_isbn < node.book.isbn and node.left != None):
            return self.__getBook( book_isbn, node.left)
        elif ( book_isbn > node.book.isbn and node.right != None):
            return self.__getBook( book_isbn, node.right)
        else:
            return 


    def isAvailable(self, book_isbn: int) -> bool:
        '''
        Check if a book is available for loan based on the ISBN

        Returns the book status

        '''
        if not self.searchBook(book_isbn):
            raise AbsentObjectException
        
        book = self.getBook(book_isbn)
        return book.status
