from sqlalchemy import Column, Integer, String, Boolean, Sequence
from Model.BaseModel import Base

class Client(Base):
    __tablename__ = 'clients'

    # Definindo o ID com uma sequence
    id = Column(Integer, Sequence('clients_id_seq', start=1), primary_key=True)

    chat_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(255))
    phone_number = Column(String(255))
    city = Column(String(255))
    address = Column(String(255))
    active = Column(Boolean, nullable=False, default=True)

    def __init__(self, chat_id, name=None, phone_number=None, city=None, address=None, active=True):
        self.chat_id = chat_id
        self.name = name
        self.phone_number = phone_number
        self.city = city
        self.address = address
        self.active = active

    def __repr__(self):
        return f"<Client(id={self.id}, chat_id={self.chat_id}, name={self.name}, phone_number={self.phone_number}, city={self.city}, address={self.address}, active={self.active})>"
