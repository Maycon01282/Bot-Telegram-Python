from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# String de conexão MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost/bottelegram"

# Criação do engine e da sessão
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base do SQLAlchemy para os modelos
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
