from dataclasses import dataclass
from enum import unique
import os
from peewee import Model, CharField, ForeignKeyField, DoubleField, PostgresqlDatabase


db = PostgresqlDatabase(database=os.environ['database'],
                        user=os.environ['user'], password=os.environ['password'],
                        host=os.environ['host'], autorollback=True)


class BaseModel(Model):
    class Meta:
        database = db


class Endereco(BaseModel):
    rua = CharField()
    numero = CharField()
    cidade = CharField()


class Carreteiro(BaseModel):
    cpf = CharField(unique=True, max_length=11)
    nome = CharField()
    email = CharField()
    telefone = CharField()
    placa = CharField()
    tipo_veiculo = CharField()
    cidade = CharField()


class Solicitante(BaseModel):
    cpf = CharField(unique=True, max_length=11)
    nome = CharField()
    email = CharField()
    telefone = CharField()


class Viagem(BaseModel):
    origem = ForeignKeyField(Endereco)
    destino = ForeignKeyField(Endereco)
    solicitante = ForeignKeyField(Solicitante)
    carreteiro = ForeignKeyField(Carreteiro, null=True)
    tipo_veiculo = CharField()
    preco = DoubleField()


if db.table_exists('viagem') is not None:
    db.create_tables(BaseModel.__subclasses__())
