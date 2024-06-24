from flask_restful import Resource, reqparse
from model.cliente import ClienteModel
from sql_alchemy import banco

class Clientes(Resource):
    def get(self):
        clientes = ClienteModel.query.all()
        clientes_json = [cliente.json() for cliente in clientes]
        return {'clientes': clientes_json}

class Cliente(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('endereco')
    argumentos.add_argument('gostos')

 
    def get(self, cliente_id):
        cliente = ClienteModel.find_cliente(cliente_id)
        if cliente:
            return cliente.json()
        return {'message': 'Cliente não encontrado.'}, 404 # not found
                
    def post(self, cliente_id):
        if ClienteModel.find_cliente(cliente_id): # Verifica se já existe o cliete, caso existir não é criado
            return {"message":"Cliente '{}' já existe".format(cliente_id)}, 400 # bad request

        dados = Cliente.argumentos.parse_args()
        cliente_objeto = ClienteModel(cliente_id, **dados)

        # Adiciona uma nova instancia
        banco.session.add(cliente_objeto)

        # Faz as mudancas no banco de dados
        banco.session.commit()

        # Retorna em json a nova instancia
        novo_cliente = cliente_objeto.json()
        return novo_cliente, 200


    def put(self, cliente_id):
        dados = Cliente.argumentos.parse_args()
        novo_cliente = ClienteModel(cliente_id, **dados)
        cliente = ClienteModel.find_cliente(cliente_id)
        if cliente:
            # Atualiza os dados do cliente ja existente
            cliente.nome = novo_cliente.nome
            cliente.endereco = novo_cliente.endereco
            cliente.gostos = novo_cliente.gostos

            # Faz as mudancas no banco de dados
            banco.session.commit()

            return novo_cliente.json(), 200  # Cliente atualizado com sucesso
        else:
            # Envia uma msg de erro caso nao encontre o cliente
            return {"error":"Cliente não encontrado!"}, 404


    def delete(self, cliente_id):
        cliente = ClienteModel.find_cliente(cliente_id)
        if cliente:
            banco.session.delete(cliente)
            banco.session.commit()
            return {'message': f'Cliente {cliente_id} deletado com sucesso.'}, 200
        return {'message': 'Cliente não encontrado.'}, 404