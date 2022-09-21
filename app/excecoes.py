class LugarNaoEncontradoException(Exception):
    def __init__(self, lugar, message="Lugar não encontrado"):
        self.lugar = lugar
        self.message = message
        super().__init__(self.message)


class DirecaoException(Exception):
    def __init__(self, codigo, message):
        self.codigo = codigo
        self.message = message
        super().__init__(self.message)


class CPFException(Exception):
    def __init__(self, message="CPF deve ser apenas numérico e conter 11 caracteres"):
        self.message = message
        super().__init__(self.message)


class ViagemException(Exception):
    def __init__(self, codigo, message):
        self.codigo = codigo
        self.message = message
        super().__init__(self.message)

class CancelamentoException(Exception):
    def __init__(self, codigo, message):
        self.codigo = codigo
        self.message = message
        super().__init__(self.message)
