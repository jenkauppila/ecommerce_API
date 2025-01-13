from sqlalchemy import Float, Table, Column, String, ForeignKey, Integer, DateTime, func    
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from typing import List
from datetime import datetime
from settings import dotenv
import os
from dotenv import load_dotenv

''' An e-commerce app created using Python, SQL, SQLAlchemy, and Postman to 
create and manage the relationships between tables for users, orders, products 
and the order-product associations '''


#  - SQLAlchemy for working with the database
#  - Marshmallow for object serialization/deserialization

load_dotenv()

# Initialize Flask app
app = Flask(__name__)  

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{dotenv.DB_PW}@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Define a base class for other DB tables to inherit
class Base(DeclarativeBase): 
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base) # Pass in the Base class to the SQLAlchemy constructor
db.init_app(app) # Initialize the SQLAlchemy object with the Flask app
ma = Marshmallow(app) # Initialize Marshmallow with the Flask app


# MARK: - MODULES/TABLES

#The association table between orders and products
order_product = Table(
    'order_product',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.product_id', ondelete='CASCADE'), primary_key=True)
)

    
# class User(Base):
class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # One-to-Many relationship - one User to many Orders
    orders: Mapped[List['Order']] = relationship('Order', back_populates='user')

    
# class Order(Base):
class Order(Base):
    __tablename__ = 'orders'
    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())  # Automatically sets at order creation
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    
    # One-to-Many relationship - one Order to one User
    user: Mapped[List['User']] = relationship('User', back_populates='orders')

    # Many-to-Many relationship - one Order to many Products
    products: Mapped[List['Product']] = relationship('Product', secondary=order_product, back_populates='orders')
    

# class Product(Base):
class Product(Base):
    __tablename__ = 'products'
    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Many-to-Many relationship - one Product to many Orders
    orders: Mapped[List['Order']] = relationship('Order', secondary=order_product, back_populates='products')
    
    

# MARK: - Schemas - Marshmallow
# Defines the schema for serializing User object (singular and plural)
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Defines the schema for serializing Order object (singular and plural)
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
    user_id=fields.Integer()
    product_id=fields.Integer()

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


# Defines the schema for serializing Product object (singular and plural)
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


with app.app_context():
    db.create_all()  # Create all tables in the database
    
