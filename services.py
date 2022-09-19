from email import message
import os
from tkinter import E
from peewee import DoesNotExist, IntegrityError
from models import Carreteiro, Endereco, Solicitante, Viagem, db
from dto import CarreteiroDTO, EnderecoDTO, SolicitanteDTO
from excecoes import CPFException, CancelamentoException, DirecaoException, LugarNaoEncontradoException, ViagemException
import geocoder
import requests


def simular_viagem(origem: EnderecoDTO, destino: EnderecoDTO, tipo_veiculo_nome):
    enderecoOrigem = origem.rua + " " + origem.numero + " " + origem.cidade
    enderecoDestino = destino.rua + " " + destino.numero + " " + destino.cidade
    try:
        g = geocoder.osm(enderecoOrigem)
        if g.ok is False:
            raise LugarNaoEncontradoException(lugar=enderecoOrigem)
        lonOrigem = g.osm['x']
        latOrigem = g.osm['y']

        g = geocoder.osm(enderecoDestino)

        if g.ok is False:
            raise LugarNaoEncontradoException(enderecoDestino)

        lonDestino = g.osm['x']
        latDestino = g.osm['y']
    except (ConnectionError, LugarNaoEncontradoException) as e:
        raise e

    api_key = os.environ['api-key']

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }

    request = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={lonOrigem},{latOrigem}&end={lonDestino},{latDestino}'
    try:
        call = requests.get(request, headers=headers)
        if call.status_code != 200:
            raise DirecaoException(
                codigo=call.status_code, message=call.reason)
    except (ConnectionError, DirecaoException) as e:
        raise e
    resposta = call.json()
    distancia = resposta["features"][0]["properties"]["summary"]["distance"]

    if tipo_veiculo_nome == 'moto':
        tipo_veiculo_value = 2.5
    elif tipo_veiculo_nome == 'carro':
        tipo_veiculo_value = 4.2
    else:
        tipo_veiculo_value = 7.3
    distancia = distancia/1000
    preco = distancia * tipo_veiculo_value
    return {
        'origem': enderecoOrigem,
        'destino': enderecoDestino,
        'preco': "{:.2f}".format(preco),
        'distancia': "{:.1f}".format(distancia),
        'veiculo': tipo_veiculo_nome
    }


def confirmar_viagem(origemDTO: EnderecoDTO, destinoDTO: EnderecoDTO, tipo_veiculo_nome: str, id_solicitante: int):
    try:
        solicitante = Solicitante.get_by_id(id_solicitante)
    except DoesNotExist as e:
        raise e
    try:
        json_viagem = simular_viagem(origemDTO, destinoDTO, tipo_veiculo_nome)
    except (ConnectionError, DirecaoException, LugarNaoEncontradoException) as e:
        raise e
    origem = Endereco.get_or_create(
        rua=origemDTO.rua, numero=origemDTO.numero, cidade=origemDTO.cidade)
    destino = Endereco.get_or_create(
        rua=destinoDTO.rua, numero=destinoDTO.numero, cidade=destinoDTO.cidade)
    preco = json_viagem['preco']
    viagem = Viagem(origem=origem[0], destino=destino[0], solicitante=solicitante,
                    tipo_veiculo=tipo_veiculo_nome, preco=float(preco))
    viagem.save()
    return viagem


def cadastrar_solicitante(solicitanteDTO: SolicitanteDTO):
    try:
        if len(solicitanteDTO.cpf) != 11 or solicitanteDTO.cpf.isdecimal() is False:
            raise CPFException
        solicitante = Solicitante(cpf=solicitanteDTO.cpf, nome=solicitanteDTO.nome,
                                  email=solicitanteDTO.email, telefone=solicitanteDTO.telefone)
        solicitante.save()
    except (IntegrityError, CPFException) as e:
        raise e
    return solicitante


def cadastrar_carreteiro(carreteiroDTO: CarreteiroDTO, tipoVeiculo: str):
    try:
        if len(carreteiroDTO.cpf) != 11 or carreteiroDTO.cpf.isdecimal() is False:
            raise CPFException
        carreteiro = Carreteiro(cpf=carreteiroDTO.cpf, nome=carreteiroDTO.nome, email=carreteiroDTO.email,
                                telefone=carreteiroDTO.telefone, placa=carreteiroDTO.placa, cidade=carreteiroDTO.cidade, tipo_veiculo=tipoVeiculo)
        carreteiro.save()
    except (IntegrityError, CPFException) as e:
        raise e
    return carreteiro


def viagens_proximas(carreteiro_id: int):
    try:
        carreteiro = Carreteiro.get_by_id(carreteiro_id)
    except DoesNotExist as e:
        raise e
    cursor = db.execute_sql('SELECT v.id, e.rua, v.preco, s.nome from viagem v \
        left join endereco e on e.id = v.origem_id \
        left join solicitante s on s.id = v.solicitante_id \
        WHERE v.tipo_veiculo = %s AND e.cidade = %s AND v.carreteiro_id is NULL',
                            (carreteiro.tipo_veiculo, carreteiro.cidade))
    return cursor.fetchall()


def aceitar_viagem(carreteiro_id: int, viagem_id: int):
    try:
        viagem = Viagem.get_by_id(viagem_id)
        if viagem.carreteiro is not None:
            raise ViagemException(
                codigo=400, message="Viagem já aceita por outro motorista")
    except DoesNotExist:
        raise ViagemException(codigo=404, message="Viagem inexistente")
    except ViagemException as e:
        raise e
    try:
        carreteiro = Carreteiro.get_by_id(carreteiro_id)
        if carreteiro.tipo_veiculo != viagem.tipo_veiculo:
            raise ViagemException(
                codigo=400, message="Carreteiro com veículo incompatível")
    except DoesNotExist:
        raise ViagemException(codigo=404, message="Carreteiro não encontrado")
    except ViagemException as e:
        raise e

    cursor = db.execute_sql('with v as (UPDATE viagem SET carreteiro_id = %s WHERE id = %s returning *) \
        select v.preco, s.nome, s.telefone, o.rua as origem_rua, o.numero as origem_numero, \
        o.cidade as origem_cidade, d.rua as destino_rua, d.numero as destino_numero, \
        d.cidade as destino_cidade from v inner join solicitante s on s.id = v.solicitante_id \
        inner join endereco o ON o.id = v.origem_id inner join endereco d on d.id = v.destino_id',
                            (carreteiro_id, viagem_id))

    return cursor.fetchall()


def cancelar_viagem_solicitante(solicitante_id: int, viagem_id: int):
    try:
        viagem = Viagem.get_by_id(viagem_id)
    except DoesNotExist as e:
        raise CancelamentoException(codigo=404, message="Viagem não existe")
    try:
        solicitante = Solicitante.get_by_id(solicitante_id)
        if viagem.solicitante.id != solicitante.id:
            raise CancelamentoException(
                codigo=400, message="Viagem não pertence ao solicitante")
    except (DoesNotExist, CancelamentoException):
        raise CancelamentoException(
            codigo=400, message="Viagem não pertence ao solicitante")
    Viagem.delete_by_id(viagem_id)


def cancelar_viagem_carreteiro(carreteiro_id: int, viagem_id: int):
    try:
        viagem = Viagem.get_by_id(viagem_id)
    except DoesNotExist as e:
        raise CancelamentoException(codigo=404, message="Viagem não existe")
    try:
        carreteiro = Carreteiro.get_by_id(carreteiro_id)
        if viagem.carreteiro is None or viagem.carreteiro.id != carreteiro.id:
            raise CancelamentoException(
                codigo=400, message="Carreteiro não é motorista da viagem")
    except (DoesNotExist, CancelamentoException):
        raise CancelamentoException(
            codigo=400, message="Carreteiro não é motorista da viagem")
    db.execute_sql(
        'UPDATE viagem SET carreteiro_id = NULL WHERE id = %s', [viagem_id])
