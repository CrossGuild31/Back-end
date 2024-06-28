from flask import Flask
from flask_restful import Api
from sql_alchemy import banco  
from resources.cliente import Cliente, Clientes
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicia o Swagger
swagger = Swagger(app)

# Inicia o banco de dados - chamado banco - com o flask app
banco.init_app(app)

api = Api(app)

# Cria as tabelas no banco de dados
with app.app_context():
    banco.create_all()

# Adiciona a resources para a API
api.add_resource(Clientes, '/clientes')
api.add_resource(Cliente, '/clientes/<string:cliente_id>')

if __name__ == '__main__':
    app.run(debug=True)

