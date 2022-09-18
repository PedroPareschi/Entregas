from pydantic import BaseModel


class EnderecoDTO(BaseModel):
    rua: str
    numero: str
    cidade: str


class SolicitanteDTO(BaseModel):
    cpf: str
    nome: str
    email: str
    telefone: str


class CarreteiroDTO(BaseModel):
    cpf: str
    nome: str
    email: str
    telefone: str
    placa: str
    tipo_veiculo: str