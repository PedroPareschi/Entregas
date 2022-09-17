from enum import Enum
import traceback
from typing import Union
from pydantic import BaseModel
import services
from http.client import HTTPException
from fastapi import FastAPI

app = FastAPI()


class TipoVeiculo(str, Enum):
    moto = 'moto'
    carro = 'carro'
    carreta = 'carreta'


class Endereco(BaseModel):
    rua: str
    numero: str
    cidade: str


@app.post("/passageiro/{id_passageiro}/simular-viagem")
def simular_viagem(origem: Endereco, destino: Endereco, tipo_veiculo: TipoVeiculo, id_passageiro: int):
    return services.simular_viagem(origem, destino, tipo_veiculo.value, id_passageiro)
