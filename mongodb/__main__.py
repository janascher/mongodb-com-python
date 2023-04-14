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
    def create_colletion():
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
        finally:
            client.close()

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
        except Exception as error:
            print(f"ERRO: {error}")
        finally:
            client.close()

    @staticmethod
    def update_user(id, name, email):
        """
            Atualiza as informações de um usuário existente no banco de dados MongoDB.
        """
        db, client = User.connect()

        try:
            users = db.users

            result = users.update_one(
                {"id": id}, {"$set": {"name": name, "email": email}})

            if result.modified_count == 0:
                print("Nenhum usuário encontrado com o ID fornecido.")
            else:
                print("Usuário atualizado com sucesso!")
                user = users.find_one({"id": id})
                client.close()
                return User(user["id"], user["name"], user["email"])

        except Exception as error:
            print(f"ERRO: {error}")
            client.close()
        finally:
            client.close()

    @staticmethod
    def delete_user(id):
        """
            Exclui um usuário do banco de dados MongoDB.
        """
        db, client = User.connect()

        try:
            users = db.users

            result = users.delete_one({"id": id})

            if result.deleted_count == 0:
                print(f"Nenhum usuário encontrado com o ID {id}.")
            else:
                print("Usuário excluído com sucesso.")
        except Exception as error:
            print(f"ERRO: {error}")
        finally:
            client.close()

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
        finally:
            client.close()

    @staticmethod
    def get_all_with_colletion():
        """
            Pesquisa todos os usuários criados no banco de dados MongoDB.
        """
        db, client = User.connect()

        try:
            users = db.users.find()

            all_users = []
            for user in users:
                user_with_collection = user
                user_with_collection["collection"] = "users"
                all_users.append(user_with_collection)

            print(f"Resultado da pesquisa:")
            for user in all_users:
                print(user)

            client.close()
            return users
        except Exception as error:
            print(f"ERRO: {error}")
            client.close()
        finally:
            client.close()

    @staticmethod
    def get_user_by_id(id):
        """
            Pesquisa um usuário pelo ID no banco de dados MongoDB.
        """
        db, client = User.connect()

        try:
            users = db.users

            user = users.find_one({"id": id})

            if user is None:
                print(f"Nenhum usuário encontrado com o ID {id}.")
                return None
            else:
                print(f"Usuário encontrado: {user}")
                client.close()
                return User(user["id"], user["name"], user["email"])
        except Exception as error:
            print(f"ERRO: {error}")
            client.close()
        finally:
            client.close()

    @staticmethod
    def get_user_by_id_with_colletion(id):
        """
            Pesquisa um usuário pelo ID no banco de dados MongoDB.
        """
        db, client = User.connect()

        try:
            users = db.users
            user = users.find_one({"id": id})

            if user is None:
                print(f"Nenhum usuário encontrado com o ID {id}.")
                return None
            else:
                user["collection"] = "users"
                print(f"Usuário encontrado: {user}")
                client.close()
                return User(user["id"], user["name"], user["email"])
        except Exception as error:
            print(f"ERRO: {error}")
            client.close()
        finally:
            client.close()


"""
    Estabelece a conexão com o banco de dados
"""
# User.connect()

"""
    Cria uma coleção user
"""
# User.create_colletion()

"""
    Cria um usuário
"""
#User.create_user("Gabriel", "gabi@mail.com")

"""
    Atualiza o usuário criado com ID
"""
#User.update_user(4, "Bento", "bento.silveira@mail.com.br")

"""
    Deleta um usuário pelo ID
"""
#User.delete_user(4)

"""
    Busca todos os usuários
"""
#User.get_all()

"""
    Busca todos os usuários em suas respectivas coleções
"""
# User.get_all_with_colletion()

"""
    Busca o usuário pelo ID 
"""
User.get_user_by_id(4)

"""
    Busca o usuário pelo ID em sua respectiva coleção
"""
# User.get_user_by_id_with_colletion(5)
