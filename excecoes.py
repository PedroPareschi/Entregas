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
