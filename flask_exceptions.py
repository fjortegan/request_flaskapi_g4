class UserPasswordNotFoundException(Exception):
    """Una excepción personalizada para casos específicos."""
    def __init__(self, mensaje, codigo_error=None):
        super().__init__(mensaje)
        self.codigo_error = codigo_error

class InvalidCredentialsException(Exception):
    """Una excepción personalizada para casos específicos."""
    def __init__(self, mensaje, codigo_error=None):
        super().__init__(mensaje)
        self.codigo_error = codigo_error