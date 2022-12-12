class Node(object): 
    '''Class used to create a generic tree node instance in memory'''
    def __init__(self, book: object): 
        self.book = book 
        self.left = None
        self.right = None
        self.height = 1 # attribute that specifies the balance factor of the node
    
    def __str__(self):
        return f'{self.book}'
  
# Classe AVL tree 
class AVLBookshelf(object): 
    """ Class that creates a AVL tree in memory. AVL tree is a self-balancing
        Binary Search Tree (BST) where the difference between heights
        of left and right subtrees cannot be more than one for all nodes. 
    """

    def __init__(self, book:object = None):
        """ Constructor of the AVL tree object
            Arguments
            ----------------
            book (object): the content to be added to AVL tree. If a book
                            is not provided, the tree initializes "empty".
                            Otherwise, the root node will be the node created
                            to the "Book" object.
        """
        if book is None:
            self.__root = None
        else:
            self.__root = self.insert(book)


    def isEmpty(self)->bool:
        '''Method that verifies the AVL Tree is empty or not.

        Returns
        ---------
        True: AVL Tree is empty
        False: AVL Tree is not empty, i.e., there is at least a root node.
        '''
        return self.__root == None

    def insert(self, book:object):
        ''' Insert a new node in AVL Tree recursively from root. The node will be created with
            "book" as content.
        '''
        if(self.__root == None):
            self.__root = Node(book)
        else:
            self.__root = self.__insert(self.__root, book)
  
    def __insert(self, root, book):
        # Step 1 - Performs a BST recursion to add the node
        if not root: 
            return Node(book) 
        elif book.isbn < root.book.isbn: 
            root.left = self.__insert(root.left, book) 
        else: 
            root.right = self.__insert(root.right, book) 
  
        # Step 2 - Update the height of ancestor node
        root.height = 1 + max(self.getHeight(root.left), 
                              self.getHeight(root.right)) 
  
        # Step 3 - Computes the balance factor 
        balance = self.getBalance(root) 
  
        # Step 4 - Checks if the node is unbalanced
        # Then, one of the following actions will be performed:

        # CASE 1 - Right rotation
        if balance > 1 and book.isbn < root.left.book.isbn: 
            return self.__rightRotate(root) 
  
        # CASE 2 - Left rotation
        if balance < -1 and book.isbn > root.right.book.isbn: 
            return self.__leftRotate(root) 
  
        # CASE 3 - Double rotation: Left Right 
        if balance > 1 and book.isbn > root.left.book.isbn: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # CASE 4 - Double rotation: Right Left 
        if balance < -1 and book.isbn < root.right.book.isbn: 
            root.right = self.__rightRotate(root.right) 
            return self.__leftRotate(root) 
  
        return root 
  
    def __leftRotate(self, p:Node) -> Node: 
        """
        Performs the 'left' rotation taking the no 'p' as a base
        to make 'u' as new root     
        """
 
        u = p.right 
        T2 = u.left 
  
        # Perform rotation 
        u.left = p 
        p.right = T2 
  
        # Update heights 
        p.height = 1 + max(self.getHeight(p.left), 
                         self.getHeight(p.right)) 
        u.height = 1 + max(self.getHeight(u.left), 
                         self.getHeight(u.right)) 
  
        # Return the new root "u" node 
        return u 
  
    def __rightRotate(self, p:Node)->Node: 
        """ Performs the rotation to the right taking the no "p" as a base
             to make "u" as new root
        """
  
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
  
    def getHeight(self, node:Node)->int: 
        """ Gets the height relative to the node passed as an argument
             Arguments:
             🇧🇷
             node (Node): the node of the tree where you want to query the height
            
             Return
             🇧🇷
             Returns an integer representing the height of the tree
             represented by the node "node". The book 0 means that the "node"
             not an in-memory object
        """
        if node is None: 
            return 0
  
        return node.height 
  
    def getBalance(self, node:Node)->int: 
        """
        Calculates the balancing factor of the node passed as an argument.

         Arguments:
         🇧🇷
         node (object): the tree node on which you want to determine the
                        balancing
            
         Return
         🇧🇷
         Returns the balancing factor for the given node.
         A book of 0, +1, or -1 indicates that the node is balanced
        """
        if not node: 
            return 0
  
        return self.getHeight(node.left) - self.getHeight(node.right) 
  
    def InOrder(self):
        self.__InOrder(self.__root)

    def __InOrder(self, root): 
        if not root: 
            return
  
        self.__InOrder(root.left)
        print("{0} ".format(root.book), end="")  
        self.__InOrder(root.right) 

    def delete(self, book:object):
        if(self.__root is not None):
            self.__root = self.__delete(self.__root, book)
        

    def __delete(self, root:Node, book:object)->Node: 
        """
        Recursive function to delete a node with given book from subtree
        with given root.

        Retorno
        --------------
        It returns root of the modified subtree.
        """
        # Step 1 - Perform standard BST delete 
        if not root: 
            return root   
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
  
        # Step 2 - Update the height of the  
        # ancestor node 
        root.height = 1 + max(self.getHeight(root.left), 
                            self.getHeight(root.right)) 
  
        # Step 3 - Get the balance factor 
        balance = self.getBalance(root) 
  
        # Step 4 - If the node is unbalanced,  
        # then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and self.getBalance(root.left) >= 0: 
            return self.__rightRotate(root) 
  
        # Case 2 - Right Right 
        if balance < -1 and self.getBalance(root.right) <= 0: 
            return self.__leftRotate(root) 
  
        # Case 3 - Left Right 
        if balance > 1 and self.getBalance(root.left) < 0: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # Case 4 - Right Left 
        if balance < -1 and self.getBalance(root.right) > 0: 
            root.right = self.__rightRotate(root.right) 
            return self.__leftRotate(root) 
  
        return root 

        
    def searchBook(self, book_isbn:any ):
        return self.__searchBook(book_isbn, self.__root)
    
    def __searchBook(self, book_isbn, node:Node):
        if node is None:
            return False
        if ( book_isbn == node.book.isbn):
            return True
        elif ( book_isbn < node.book.isbn and node.left != None):
            return self.__searchBook( book_isbn, node.left)
        elif ( book_isbn > node.book.isbn and node.right != None):
            return self.__searchBook( book_isbn, node.right)
        else:
            return False 
