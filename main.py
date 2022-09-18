from email import message
from enum import Enum
from typing import Union
from urllib import response
from dto import CarreteiroDTO, EnderecoDTO, SolicitanteDTO
from fastapi import FastAPI, HTTPException
from excecoes import CPFException, DirecaoException, LugarNaoEncontradoException
from pydantic import BaseModel
from peewee import DoesNotExist, IntegrityError
import services

app = FastAPI()


class TipoVeiculo(str, Enum):
    moto = 'moto'
    carro = 'carro'
    carreta = 'carreta'


class HTTPError(BaseModel):
    detail: str


@app.post("/simular-viagem", responses={
    502: {
        "model": HTTPError
    },
    404: {
        "model": HTTPError
    }
})
def simular_viagem(origem: EnderecoDTO, destino: EnderecoDTO, tipo_veiculo: TipoVeiculo):
    try:
        resposta = services.simular_viagem(origem, destino, tipo_veiculo.value)
    except ConnectionError as e:
        raise HTTPException(
            status_code=502, detail="Erro ao conectar com serviços de geolocalização, tente novamente mais tarde")
    except LugarNaoEncontradoException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DirecaoException as e:
        raise HTTPException(status_code=e.codigo,
                            detail="Erro ao buscar direção: " + e.message)
    return resposta


@app.post("/solicitante/{id_solicitante}/confirmar-viagem", responses={
    502: {
        "model": HTTPError
    },
    404: {
        "model": HTTPError
    }
})
def confirmar_viagem(id_solicitante: int, origem: EnderecoDTO, destino: EnderecoDTO, tipo_veiculo: TipoVeiculo):
    try:
        resposta = services.confirmar_viagem(
            origem, destino, tipo_veiculo.value, id_solicitante)
    except ConnectionError as e:
        raise HTTPException(
            status_code=502, detail="Erro ao conectar com serviços de geolocalização, tente novamente mais tarde")
    except LugarNaoEncontradoException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except DirecaoException as e:
        raise HTTPException(status_code=e.codigo,
                            detail="Erro ao buscar direção: " + e.message)
    return resposta


@app.post("/solicitante", responses={
    400: {
        "model": HTTPError
    }})
def cadastrar_solicitante(solicitante: SolicitanteDTO):
    try:
        resposta = services.cadastrar_solicitante(solicitante)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="CPF deve ser único")
    except CPFException as e:
        raise HTTPException(
            status_code=400, detail=e.message)
    return resposta


@app.post("/carreteiro", responses={
    400: {
        "model": HTTPError
    }})
def cadastrar_carreteiro(carreteiro: CarreteiroDTO, tipoVeiculo: TipoVeiculo):
    try:
        resposta = services.cadastrar_carreteiro(carreteiro, tipoVeiculo.value)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="CPF deve ser único")
    except CPFException as e:
        raise HTTPException(
            status_code=400, detail=e.message)
    return resposta


@app.get("/carreteiro/{carreteiro_id}/viagens")
def viagens_proximas(carreteiro_id: int):
    return services.viagens_proximas(carreteiro_id)


@app.post("/carreteiro/{carreteiro_id}/viagens/{viagem_id}/aceitar")
def aceitar_viagem(carreteiro_id: int, viagem_id: int):
    return services.aceitar_viagem(carreteiro_id, viagem_id)


@app.delete("/solicitante/{solicitante_id}/viagem/{viagem_id}")
def cancelar_viagem_solicitante(solicitante_id: int, viagem_id: int):
    return services.cancelar_viagem_solicitante(solicitante_id, viagem_id)


@app.delete("/carreteiro/{carreteiro_id}/viagens/{viagem_id}")
def cancelar_viagem_carreteiro(carreteiro_id: int, viagem_id: int):
    return services.cancelar_viagem_carreteiro(carreteiro_id, viagem_id)
