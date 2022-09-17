from enum import Enum
from peewee import Model, CharField, ForeignKeyField, DoubleField, BooleanKeyField

class BaseModel(Model):
    class Meta:
        database = db


class Endereco(BaseModel):
    rua = CharField()
    numero = CharField()
    cidade = CharField()


class TipoVeiculo(int, Enum):
    moto = "moto", 2
    carro = "carro", 3
    carreta = "carreta", 5

class Usuario(BaseModel):
    cpf = CharField()
    nome = CharField()
    email = CharField()
    telefone = CharField()

class Carreteiro(Usuario):
    placa = CharField()
    veiculo = ForeignKeyField(TipoVeiculo)

class Solicitante(Usuario):
    ehReceptor = BooleanKeyField()
    ehEmissor = BooleanKeyField()

class Viagem(BaseModel):
    origem = ForeignKeyField(Endereco)
    destino = ForeignKeyField(Endereco)
    carreteiro = ForeignKeyField(Carreteiro)
    preco = DoubleField()
    pagamento = CharField()

