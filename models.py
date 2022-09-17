from peewee import Model, CharField, ForeignKeyField, DoubleField, PostgresqlDatabase


db = PostgresqlDatabase(database='truckdriver', user='postgres', password='1234')


class BaseModel(Model):
    class Meta:
        database = db


class Endereco(BaseModel):
    rua = CharField()
    numero = CharField()
    cidade = CharField()


class Carreteiro(BaseModel):
    cpf = CharField()
    nome = CharField()
    email = CharField()
    telefone = CharField()
    placa = CharField()
    veiculo_preco = DoubleField()


class Solicitante(BaseModel):
    cpf = CharField()
    nome = CharField()
    email = CharField()
    telefone = CharField()


class Viagem(BaseModel):
    origem = ForeignKeyField(Endereco)
    destino = ForeignKeyField(Endereco)
    carreteiro = ForeignKeyField(Carreteiro)
    preco = DoubleField()
    pagamento = CharField()


if db.table_exists('viagem') is not None:
    db.create_tables(BaseModel.__subclasses__())
