class TypeErrorException(Exception):
    def __init__(self):
        super().__init__('The parameter(s) has/have an inappropriate type.')


class AbsentObjectException(Exception):
    def __init__(self):
        super().__init__('There is not an object with this attribute.')


class UnavailableObjectException(Exception):
    def __init__(self):
        super().__init__('This object is unavailable.')


class EmptyListException(Exception):
    def __init__(self):
        super().__init__('The list is empty.')


class LoginFailException(Exception):
    def __init__(self) -> None:
        super().__init__('The username and/or the password are incorrect.')