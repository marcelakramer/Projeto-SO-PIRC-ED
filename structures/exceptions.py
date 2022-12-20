class TypeErrorException(Exception):
    '''
    Exception for when a data type of a parameter is inappropiate.

    '''
    def __init__(self):
        super().__init__('The parameter(s) has/have an inappropriate type.')


class AbsentObjectException(Exception):
    '''
    Exception for when there isn't a object with certain identificator attribute.

    '''
    def __init__(self):
        super().__init__('There is not an object with this attribute.')


class UnavailableObjectException(Exception):
    '''
    Exception for when a object is unavailable for a certain use.

    '''
    def __init__(self):
        super().__init__('This object is unavailable.')
        

class AlreadyExistingObjectException(Exception):
    '''
    Exception for when a object with certain identificator parameter already exists.

    '''
    def __init__(self):
        super().__init__('This object already exists.')


class EmptyListException(Exception):
    '''
    Exception for when a list of objects is empty.

    '''
    def __init__(self):
        super().__init__('The list is empty.')