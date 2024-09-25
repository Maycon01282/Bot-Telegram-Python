from config import engine
from Model.BaseModel import Base
from Model.Client import Client
from Model.Category import Category
from Model.Product import Product

# Teste a conexão
try:
    connection = engine.connect()
    print("Conexão bem-sucedida!")
    connection.close()
except Exception as e:
    print(f"Erro de conexão: {e}")

# Cria as tabelas no banco de dados
try:
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas no banco de dados!")
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")

if __name__ == "__main__":
    print("Script executado!")
