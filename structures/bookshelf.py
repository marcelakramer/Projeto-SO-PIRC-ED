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
    def __init__(self, book:object = None):
        if book is None:
            self.__root = None
        else:
            self.__root = self.insert(book)


    def isEmpty(self)->bool:
        return self.__root == None


    def insert(self, book:object):
        # Inserts in the root if AVL is empty
        if(self.__root == None):
            self.__root = Node(book)

        # Calls a recursive function to insert
        else:
            self.__root = self.__insert(self.__root, book)
  
  
    def __insert(self, root, book):
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
        if node is None: 
            return 0
  
        return node.height 
  

    def getBalance(self, node:Node) -> int: 
        if not node: 
            return 0

        # Returns the height of node at left and node at right
        return self.getHeight(node.left) - self.getHeight(node.right) 
  

    def InOrder(self):
        return self.__InOrder(self.__root)


    def __InOrder(self, root: Node): 
        # Returns an empty string if there is no node
        if not root: 
            return ''


        if root is not None:
            left = self.__InOrder(root.left)
            right = self.__InOrder(root.right)

            # Returns a concatenated string of values of left and right nodes
            return left + ' ' + str(root.book) + ' ' + right


    def delete(self, book:object):
        if(self.__root is not None):
            self.__root = self.__delete(self.__root, book)
        

    def __delete(self, root:Node, book:object) -> Node: 
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
        return self.__searchBook(book_isbn, self.__root)
    

    def __searchBook(self, book_isbn: int, node: Node) -> bool:
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
        if not self.searchBook(book_isbn):
            raise AbsentObjectException
        return self.__getBook(book_isbn, self.__root)

    
    def __getBook(self, book_isbn: int, node: Node) -> object:
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
        if not self.searchBook(book_isbn):
            raise AbsentObjectException
        
        book = self.getBook(book_isbn)
        return book.status
