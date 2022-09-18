
from models import Carreteiro, Endereco, Solicitante, Viagem, db
from dto import CarreteiroDTO, EnderecoDTO, SolicitanteDTO
import geocoder
import requests


def simular_viagem(origem: EnderecoDTO, destino: EnderecoDTO, tipo_veiculo_nome):
    g = geocoder.osm(origem.rua + " " + origem.numero + " " + origem.cidade)
    lonOrigem = g.osm['x']
    latOrigem = g.osm['y']

    g = geocoder.osm(destino.rua + " " + destino.numero + " " + destino.cidade)

    lonDestino = g.osm['x']
    latDestino = g.osm['y']

    api_key = ''

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }

    request = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={lonOrigem},{latOrigem}&end={lonDestino},{latDestino}'

    call = requests.get(request, headers=headers)
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
        'origem': origem.rua + ' ' + origem.numero + ',' + origem.cidade,
        'destino': destino.rua + ' ' + destino.numero + ',' + destino.cidade,
        'preco': "{:.2f}".format(preco),
        'distancia': "{:.1f}".format(distancia),
        'veiculo': tipo_veiculo_nome
    }


def confirmar_viagem(origemDTO: EnderecoDTO, destinoDTO: EnderecoDTO, tipo_veiculo_nome: str, id_solicitante: int):
    json_viagem = simular_viagem(origemDTO, destinoDTO, tipo_veiculo_nome)
    origem = Endereco.get_or_create(
        rua=origemDTO.rua, numero=origemDTO.numero, cidade=origemDTO.cidade)
    destino = Endereco.get_or_create(
        rua=destinoDTO.rua, numero=destinoDTO.numero, cidade=destinoDTO.cidade)
    solicitante = Solicitante.get_by_id(id_solicitante)
    preco = json_viagem['preco']
    viagem = Viagem(origem=origem[0], destino=destino[0], solicitante=solicitante,
                    tipo_veiculo=tipo_veiculo_nome, preco=float(preco))
    return viagem.save()


def cadastrar_solicitante(solicitanteDTO: SolicitanteDTO):
    solicitante = Solicitante(cpf=solicitanteDTO.cpf, nome=solicitanteDTO.nome,
                              email=solicitanteDTO.email, telefone=solicitanteDTO.telefone)
    return solicitante.save()


def cadastrar_carreteiro(carreteiroDTO: CarreteiroDTO, tipoVeiculo: str):
    carreteiro = Carreteiro(cpf=carreteiroDTO.cpf, nome=carreteiroDTO.nome, email=carreteiroDTO.email,
                            telefone=carreteiroDTO.telefone, placa=carreteiroDTO.placa, cidade=carreteiroDTO.cidade, tipo_veiculo=tipoVeiculo)
    return carreteiro.save()


def viagens_proximas(carreteiro_id: int):
    carreteiro = Carreteiro.get_by_id(carreteiro_id)
    cursor = db.execute_sql('SELECT v.id, e.rua, v.preco, s.nome from viagem v left join endereco e on e.id = v.origem_id left join solicitante s on s.id = v.solicitante_id  WHERE v.tipo_veiculo = %s AND e.cidade = %s AND v.carreteiro_id is NULL', (carreteiro.tipo_veiculo, carreteiro.cidade))
    return cursor.fetchall()

def aceitar_viagens_proximas(carreteiro_id: int, viagem_id: int):
    q = Viagem.update({Viagem.carreteiro: carreteiro_id}
                      ).where(Viagem.id == viagem_id)

    return db.execute_sql('')


def cancelar_viagem(solicitante_id: int, viagem_id: int):
    q = Viagem.delete_by_id(viagem_id)
    return q.execute()
