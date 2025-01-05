from sqlalchemy import Float, Table, Column, Select, String, create_engine, ForeignKey, Integer, DateTime, func    
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, Session
from flask import Flask, app, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
import os
from typing import List
from datetime import datetime
import logging

#  - SQLAlchemy for working with the database.
#  - Marshmallow for object serialization/deserialization.
#  - create_engine, ForeignKey, Table, String, Column, Integer for defining database schema.

# Initialize Flask app
logging.basicConfig(filename='record.log', level=logging.DEBUG)
app = Flask(__name__)  

# MySQL database configuration
# engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://PASSWORD_HERE@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Define a base class for other DB tables to inherit
class Base(DeclarativeBase): 
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base) # Pass in the Base class to the SQLAlchemy constructor
db.init_app(app) # Initialize the SQLAlchemy object with the Flask app
ma = Marshmallow(app) # Initialize Marshmallow with the Flask app

#The association table between orders and products
order_product = Table(
	'order_product',
	Base.metadata,
	Column('order_id', ForeignKey('orders.order_id')),
	Column('product_id', ForeignKey('products.product_id')),
)

#The association table between users and orders
user_order = Table(
	'user_order',
	Base.metadata,
	Column('user_id', ForeignKey('users.user_id')),
	Column('order_id', ForeignKey('orders.order_id')),
)

# MARK: - Models/Tables
class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # One-to-Many relationship - one User to many Orders
    orders: Mapped[List['Order']] = relationship(secondary=user_order, back_populates='user')
    # orders: Mapped[List['Order']] = relationship(back_populates='user')

    # # one-to-many relationship - one Order to one User
    # user: Mapped['User'] = relationship(secondary=user_order, back_populates='user')
    
    
class Order(Base):
    __tablename__ = 'orders'
    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())  # Automatically sets at order creation
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    
    # one-to-many relationship - one Order to one User
    user: Mapped['User'] = relationship(secondary='user_order', back_populates='orders')    
    # user: Mapped['User'] = relationship(secondary='user_order', back_populates='orders')    

    # Many-to-Many relationship - one Order to many Products
    products: Mapped[List['Product']] = relationship(secondary='order_product', back_populates='orders')
    

class Product(Base):
    __tablename__ = 'products'
    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Many-to-Many relationship - one Product to many Orders
    orders: Mapped[List['Order']] = relationship(secondary='order_product', back_populates='products') 
  


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
    
