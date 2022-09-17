
from http import client
from models import Endereco
import geocoder
import requests


def simular_viagem(origem: Endereco, destino: Endereco, tipo_veiculo_nome: str, id_passageiro: int):
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
