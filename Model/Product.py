from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from Model.BaseModel import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('products_id_seq', start=1), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)  # ForeignKey para a categoria
    category = relationship("Category", back_populates="products")  # Relacionamento bidirecional
    
    photo_url = Column(String(255), nullable=False)  # URL da foto
    name = Column(String(255), nullable=False)  # Nome do produto
    description = Column(String(2550), nullable=False)  # Descrição do produto
    price = Column(Float, nullable=False)  # Preço do produto

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Fill in the name")
        if len(value) > 255:
            raise ValueError("Product name too long (more than 255 characters)")
        return value

    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Fill in the description")
        if len(value) > 2550:
            raise ValueError("Product description too long (more than 2550 characters)")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if value is None or value < 1:
            raise ValueError("Fill in the price. Minimum price is 1 $")
        return value

    def __repr__(self):
        return (f"<Product(id={self.id}, category_id={self.category_id}, photo_url={self.photo_url}, "
                f"name={self.name}, description={self.description}, price={self.price})>")

    def __eq__(self, other):
        if isinstance(other, Product):
            return (self.id == other.id and
                    self.category_id == other.category_id and
                    self.photo_url == other.photo_url and
                    self.name == other.name and
                    self.description == other.description and
                    self.price == other.price)
        return False

    def __hash__(self):
        return hash((self.id, self.category_id, self.photo_url, self.name, self.description, self.price))
