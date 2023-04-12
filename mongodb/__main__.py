from pymongo import MongoClient
from configs import config


class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def __str__(self):
        return f"User id={self.id}, name={self.name}, email={self.email}"

    @staticmethod
    def connect():
        """ 
            Conecta ao servidor de banco de dados MongoDB.
        """
        try:
            params = config()
            client = MongoClient(params["host"], int(
                params["port"]), serverSelectionTimeoutMS=2000)
            print("Conectando ao banco de dados MongoDB...")
            db = client[params["database"]]
            print("Conexão bem-sucedida!")
            # client.close()
            #print("Conexão com o banco de dados fechada.")
            return db, client
        except Exception as error:
            print(error)

    @staticmethod
    def create_table():
        """
            Cria a Tabela Users no banco de dados MongoDB.
        """
        try:
            db, client = User.connect()

            if "users" in db.list_collection_names():
                print("A coleção Users já existe!")
                return
        
            users = db.users
            print("Criando coleção Users...")
            users.create_index([("id", 1)], unique=True)
            print("Coleção criada com sucesso!")
            client.close()
            print("Conexão com o banco de dados fechada.")
        except Exception as error:
            print(f"ERRO: {error}")

    @staticmethod
    def create_user(name, email):
        """
            Cria um usuário no banco de dados MongoDB.
        """
        db, client = User.connect()

        try:
            users = db.users
            new_id = users.count_documents({}) + 1
            new_user = {"id": new_id, "name": name, "email": email}
            result = users.insert_one(new_user)
            new_id = str(result.inserted_id)
            print("Usuário criado com sucesso!")
            client.close()
            print("Conexão com o banco de dados fechada.")
            return User(new_id, name, email)
            # return User(result, name, email)
        except Exception as error:
            print(f"ERRO: {error}")

    @staticmethod
    def get_all():
        """
            Pesquisa todos os usuários criados no banco de dados MongoDB.
        """
        db, client = User.connect()

        try:

            users = db.users.find()

            print(f"Resultado da pesquisa:")
            for user in users:
                print(user)

            client.close()
            return users
        except Exception as error:
            print(f"ERRO: {error}")
            client.close()


"""
    Estabelece a conexão com o banco de dados
"""
#User.connect()

"""
    Cria uma tabela user
"""
# User.create_table()

"""
    Cria um usuário
"""
#User.create_user("Fabio", "fabio@mail.com")

"""
    Busca todos os usuários com id 
"""
User.get_all()
