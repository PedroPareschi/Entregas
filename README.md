# Aplicativo de Entregas de Encomentas

Link: http://54.174.10.44/docs

## O que é?

Aplicativo que funciona como aplicativo de motoristas, porém especializado em entregas. Solicitante coloca o caminho que deseja percorrer e o tipo de veiculo que deseja solicitar.
O aplicativo é capaz de automaticamente precificar a partir da distância e o tipo de veículo selecionado. 

## Como usar?



![Screenshot 2022-09-19 190108](https://user-images.githubusercontent.com/81632607/191127460-0ff3c139-92ba-47ec-b006-8c73b7389b48.png)

### Post /simular-viagem

Simula viagem entre dois pontos, o cliente coloca o endereço incluindo rua, número e cidade de origem e destino, colocando também o tipo de veículo desejado e o sistema retorna a seguinte resposta:

```json
{
  "origem": "",
  "destino": "",
  "preco": "9.05",
  "distancia": "3.6",
  "veiculo": "moto"
}
```
Indicando entretanto o preço e e a distância percorrida


### POST /solicitante/{id_solicitante}/confirmar-viagem

Similar ao processo anterior, mas agora o cliente confirma a viagem, devendo estar cadastrado. A viagem é persistida no banco de dados

### POST /solicitante e Post/carreteiro

Endpoints simulando o cadastro de novos clientes, sejam solicitantes e carreteiros. cpf deve ser validado e único, porém um mesmo cliente pode ser tanto solicitante quanto carreteiro

### GET /carreteiro/{carreteiro_id}/viagens

Endpoint em que o carreteiro vê a lista de viagens próximas, somente viagens na mesma cidade e usando o mesmo tipo de veículo podem ser visualizadas

Formato:
```json
[
  [
    2,
    "",
    7.56,
    "Pedro"
  ]
]
```

### POST /carreteiro/{carreteiro_id}/viagens/{viagem_id}/aceitar

Endpoint em que um carreteriro aceita uma viagem, persistindo no banco de dados

### DELETE /solicitante/{solicitante_id}/viagem/{viagem_id}

Solicitante cancela a viagem, apagando seu registro do banco de dados

### DELETE /carreteiro/{carreteiro_id}/viagens/{viagem_id}

Carreteiro cancela viagem, e esta volta a ficar disponível para o públic

## Como buildar localmente

Python 3.9 e PostgreSQL instalados na máquina

Rodar ```pip install -r requirements.txt```

Para rodar fastapi, rodar comando ```uvicorn main:app --host 0.0.0.0 --port 80```
