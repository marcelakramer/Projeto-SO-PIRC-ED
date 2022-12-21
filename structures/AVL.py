import sys
sys.path.append('./..')

from structures.exceptions import AbsentObjectException

# Class Node
class Node(object): 
    def __init__(self, content: object) -> None:
        '''
        Method that initializes the Node with a content and its attributes

        ''' 
        self.content = content 
        self.left = None
        self.right = None
        self.height = 1 # attribute that specifies the balance factor of the node
    
    def __str__(self) -> str:
        '''
        Method that creates a string representation for the node

        Returns this string

        '''
        return f'{self.content}'
  
# AVL tree class
class AVLTree(object): 
    def __init__(self, content: object = None) -> None:
        '''
        Method that initializes the AVL

        If method is initialized without any argument
        AVL is created with "None" at the root

        If the argument is given
        a node with the content is created
        
        '''
        if content is None:
            self.__root = None
        else:
            self.__root = self.insert(content)


    def isEmpty(self) -> bool:
        '''
        Returns if AVL is empty
        
        '''

        # Returns whether the root is empty or not
        return self.__root == None 


    def insert(self, content: object) -> None:
        '''
        Call a private method to insert a node with content in the tree

        Receives the content as an argument
        
        '''
        # Inserts in the root if AVL is empty
        if(self.__root == None):
            self.__root = Node(content)

        # Calls a recursive function to insert
        else:
            self.__root = self.__insert(self.__root, content)
  
  
    def __insert(self, root: Node, content: object) -> Node:
        '''
        Objectively insert the content in the AVL

        Receives the root and the content to be inserted as arguments
        
        '''

        # Performs a BST recursion to add the node
        if not root: 
            return Node(content) 
        elif content < root.content: 
            root.left = self.__insert(root.left, content) 
        else: 
            root.right = self.__insert(root.right, content) 
  
        # Update the height of ancestor node
        root.height = 1 + max(self.getHeight(root.left), 
                              self.getHeight(root.right)) 
  
        # Computes the balance factor 
        balance = self.getBalance(root) 
  
        # Checks if the node is unbalanced
        # Then, one of the following actions will be performed:

        # Right rotation
        if balance > 1 and content < root.left.content: 
            return self.__rightRotate(root) 
  
        # Left rotation
        if balance < -1 and content > root.right.content: 
            return self.__leftRotate(root) 
  
        # Double rotation: Left Right 
        if balance > 1 and content > root.left.content: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # Double rotation: Right Left 
        if balance < -1 and content < root.right.content: 
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
            return left + ' ' + str(root.content) + ' ' + right


    def delete(self, content: object):
        '''
        Deletes an instance calling a private method

        It must receive the content to be deleted as an argument

        '''
        if(self.__root is not None):
            self.__root = self.__delete(self.__root, content)
        

    def __delete(self, root: Node, content: object) -> Node:
        '''
        Private method to delete the content

        Receives the content to be deleted
        and the root

        '''
        # Perform standard BST delete 
        if not root: 
            return root   

        # Search for the content by analyzing the id
        elif content < root.content: 
            root.left = self.__delete(root.left, content)   
        elif content > root.content: 
            root.right = self.__delete(root.right, content)   
        else: 
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 
  
            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 
  
            temp = self.getMincontentNode(root.right) 
            root.content = temp.content 
            root.right = self.__delete(root.right, 
                                      temp.content) 
  
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

        
    def search(self, content_id: int) -> bool:
        '''
        Calls a recursive function to search for a content

        The content id must be passed
        
        '''

        return self.__search(content_id, self.__root)
    

    def __search(self, content_id: int, node: Node) -> bool:
        '''
        Properly looks for the content passed through the arguments

        Returns a boolean to inform whether it was possible
        to find it or not
        
 =      '''
        # Base case
        if node is None:
            return False

        # Found the content
        if ( content_id == node.content):
            return True

        # Search by the id
        elif ( content_id < node.content and node.left != None):
            return self.__search( content_id, node.left)
        elif ( content_id > node.content and node.right != None):
            return self.__search( content_id, node.right)
        else:
            return False


    def get(self, content_id: int) -> object:
        '''
        Returns an specific content based on the id
        Calls a private method

        Needs the id as an argument

        '''
        if not self.search(content_id):
            raise AbsentObjectException

        return self.__get(content_id, self.__root)

    
    def __get(self, content_id: int, node: Node) -> object:
        '''
        Private method of "getcontent"

        Receives the id and the root as the arguments

        '''
        if node is None:
            return 
        if ( content_id == node.content ):
            return node.content
        elif ( content_id < node.content and node.left != None):
            return self.__get( content_id, node.left)
        elif ( content_id > node.content and node.right != None):
            return self.__get( content_id, node.right)
        else:
            return 
