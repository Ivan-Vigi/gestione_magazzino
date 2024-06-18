from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/yourdatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ProductSchema(BaseModel):
    name: str
    quantity: int
    price: float
    expiry_date: datetime

class ProductUpdateSchema(BaseModel):
    name: str = None
    quantity: int = None
    price: float = None
    expiry_date: datetime = None

@app.post("/products/")
def create_product(product: ProductSchema):
    db = SessionLocal()
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product

@app.get("/products/")
def read_products(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    products = db.query(Product).offset(skip).limit(limit).all()
    db.close()
    return products

@app.get("/products/{product_id}")
def read_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdateSchema):
    db = SessionLocal()
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    db.close()
    return {"detail": "Product deleted"}
