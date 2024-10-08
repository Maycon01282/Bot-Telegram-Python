from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurações do banco de dados
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/bottelegram"

# Criação do engine
engine = create_engine(DATABASE_URL)

# Criação da base declarativa
Base = declarative_base()

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
