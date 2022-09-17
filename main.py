import traceback
import services
from http.client import HTTPException
from fastapi import FastAPI
from models import Endereco, TipoVeiculo

app = FastAPI()


@app.post("/passageiro/{id_passageiro}/")
def simular_viagem(origem: Endereco, destino: Endereco, carro: TipoVeiculo, id_passageiro: int):
    services.simular_viagem(origem, destino, carro, id_passageiro)
