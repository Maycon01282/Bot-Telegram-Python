from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import validates
from Model.BaseModel import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, Sequence('categories_id_seq', start=1), primary_key=True)
    name = Column(String(255), nullable=False)

    # Relacionamento com Product
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Fill in the name")
        if len(value) > 255:
            raise ValueError("Category name too long (more than 255 characters)")
        return value
