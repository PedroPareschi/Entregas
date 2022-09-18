from enum import Enum
from typing import Union
from dto import CarreteiroDTO, EnderecoDTO, SolicitanteDTO
from http.client import HTTPException
from fastapi import FastAPI
import services

app = FastAPI()


class TipoVeiculo(str, Enum):
    moto = 'moto'
    carro = 'carro'
    carreta = 'carreta'


@app.post("/simular-viagem")
def simular_viagem(origem: EnderecoDTO, destino: EnderecoDTO, tipo_veiculo: TipoVeiculo):
    return services.simular_viagem(origem, destino, tipo_veiculo.value)


@app.post("/solicitante/{id_solicitante}/confirmar-viagem")
def confirmar_viagem(id_solicitante: int, origem: EnderecoDTO, destino: EnderecoDTO, tipo_veiculo: TipoVeiculo):
    return services.confirmar_viagem(origem, destino, tipo_veiculo.value, id_solicitante)


@app.post("/solicitante")
def cadastrar_solicitante(solicitante: SolicitanteDTO):
    return services.cadastrar_solicitante(solicitante)


@app.post("/carreteiro")
def cadastrar_carreteiro(carreteiro: CarreteiroDTO, tipoVeiculo: TipoVeiculo):
    return services.cadastrar_carreteiro(carreteiro, tipoVeiculo.value)


@app.get("/carreteiro/{carreteiro_id}/viagens-proximas")
def viagens_proximas(carreteiro_id: int):
    return services.viagens_proximas(carreteiro_id)


@app.post("/carreteiro/{carreteiro_id}/viagens-proximas/{viagem_id}/aceitar")
def aceitar_viagem(carreteiro_id: int, viagem_id: int):
    return services.aceitar_viagem(carreteiro_id, viagem_id)


@app.delete("solicitante/{solicitante_id}/viagem/{viagem_id}")
def cancelar_viagem(solicitante_id: int, viagem_id: int):
    return services.cancelar_viagem(solicitante_id, viagem_id)
