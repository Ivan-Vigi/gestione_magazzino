from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    expiry_date = Column(DateTime, nullable=False)

# Connessione al database MySQL
DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/yourdatabase"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
