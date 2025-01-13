from app import (
    app,
    db,
    User,
    Order,
    Product,
    user_schema,
    users_schema,
    order_schema,
    orders_schema,
    product_schema,
    products_schema,
)
from flask import request, jsonify, render_template
from marshmallow import ValidationError
from sqlalchemy import select
# from sqlalchemy.orm.exc import StaleDataError
from sqlalchemy.exc import IntegrityError
import logging

''' An e-commerce app created using Python, SQL, SQLAlchemy, and Postman to 
create and manage the relationships between tables for users, orders, products 
and the order-product associations '''


@app.route('/')
def main():
  return render_template("index.html")


# Endpoints:

# --- MARK: USER SCHEMAS

# Route to ADD new user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json) # loads the JSON data with User schema
    
    except ValidationError as e:
        app.logger.error(e, exc_info=True)
        if "title" in e.messages and e.messages["title"] == "400 Bad Request":
            return jsonify({"message": "Invalid Entry"}), 400            
        return jsonify(e.messages), 400 # returns error msg for 400 = Bad Request
    
    existing_user = db.session.query(User).filter_by(email=user_data['email']).first()
    
    if existing_user:
        return jsonify({"message": "Duplicate email already exists"}), 409

    new_user = User(name=user_data['name'], address=user_data['address'], email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201 # request created successfully
    
    
# Route to GET all users
@app.route('/users', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    
    if not users:
        users = db.session.execute(query).all()
        return jsonify({"message": "No users found"}), 404
    return users_schema.jsonify(users), 200


# Route to GET a single user
@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    return user_schema.jsonify(user), 200


# Route to UPDATE a user
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    try:
        user_data = user_schema.load(request.json)
    
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user.name = user_data["name"]
    user.address = user_data["address"]
    user.email = user_data["email"]
    db.session.commit()
    return user_schema.jsonify(user), 200


# Route to DELETE a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"successfully deleted {user.name}"}), 200



# --- MARK: PRODUCT SCHEMAS

# Route to ADD new product
@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json) # loads the JSON data with Product schema

    except ValidationError as e:
        app.logger.error(e, exc_info=True) # research app.logger
        if "title" in e.messages and e.messages["title"] == "400 Bad Request":
            return jsonify({"message": "Invalid Entry"}), 400            
        return jsonify(e.messages), 400 # returns error msg for 400 = Bad Request

    existing_product = db.session.query(Product).filter_by(product_name=product_data['product_name']).first()
    
    if existing_product:   
        return jsonify({"message": "Duplicate product already exists"}), 409

    new_product = Product(product_name=product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201 # product created successfully and response returned


# Route to GET all products
@app.route('/products', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    
    if not products:
            # products = db.session.execute(query).all()
            return jsonify({"message": "No products found"}), 404
    return products_schema.jsonify(products), 200


# Route to GET a single product
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid Product ID"}), 400
    return product_schema.jsonify(product), 200


# Route to UPDATE a product
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid Product ID"}), 400
    try:
        product_data = product_schema.load(request.json)
    
    except ValidationError as e:
        return jsonify(e.messages), 400
        
    product.product_name = product_data["product_name"]
    product.price = product_data["price"]
    db.session.commit()
    return product_schema.jsonify(product), 200


# Route to DELETE a product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"successfully deleted {product.product_name}"}), 200



# --- MARK: ORDER SCHEMAS

# Route to ADD new order
@app.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = order_schema.load(request.json) # loads the JSON data with Order schema
    
    except ValidationError as e:
        app.logger.error(e, exc_info=True)
        if "title" in e.messages and e.messages["title"] == "400 Bad Request":
            return jsonify({"message": "Invalid Entry"}), 400            
        return jsonify(e.messages), 400 # returns error msg for 400 = Bad Request
    
    new_order = Order(user_id=order_data['user_id'])
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 201 # request created successfully


# Route to ADD products to order
@app.route('/orders/<int:order_id>/add_products', methods=['POST'])
def add_products(order_id):
    order = db.session.get(Order, order_id)
    
    if not order:
        return jsonify({"message": "Invalid Order ID"}), 400
    
    product_ids = request.json
    
    for id in product_ids['product_ids']:
        product = db.session.get(Product, id)
        if not product:
            return jsonify({"message": f"Invalid Product ID: {id}"}), 400
        if product in order.products:
            return jsonify({"message": f"Product already on Order"}), 409
        order.products.append(product)
    
    db.session.commit()
    return jsonify({"message": f"Products successfully added to Order: {order_id}!"}), 200


# Route to DELETE products from order
@app.route('/orders/<int:order_id>/remove_products', methods=['DELETE'])
def remove_products(order_id):
    order = db.session.get(Order, order_id)
    
    if not order:
        return jsonify({"message": f"Invalid Order ID: {id}"}), 400
    
    product_ids = request.json
    
    for id in product_ids['product_ids']:
        product = db.session.get(Product, id)
        if not product:
            return jsonify({"message": f"Invalid Product ID: {id}"}), 400
        if product not in order.products:
            return jsonify({"message": f"Product not on Order: {order_id}"}), 409
        order.products.remove(product)
    
    db.session.commit()
    return jsonify({"message": f"Products successfully deleted from Order: {order_id}!"}), 200


# Route to GET all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()
    
    if not orders:
            orders = db.session.execute(query).all()
            return jsonify({"message": "No orders found"}), 404
    
    return orders_schema.jsonify(orders), 200


# Route to GET single order by order ID
@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = db.session.get(Order, id)
        
    if not order:
        return jsonify({"message": "Invalid Order ID"}), 400
    
    return order_schema.jsonify(order), 200


# Route to GET all Orders by User ID
@app.route('/orders/user/<int:id>', methods=['GET'])
def get_user_orders(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": f"Invalid User ID: {id}"}), 400       
    elif not user.orders:
        return jsonify({"message": "No open orders exist for user"}), 404
    
    return orders_schema.jsonify(user.orders), 200


# Route to GET all Products by Order ID
@app.route('/products/order/<int:id>', methods=['GET'])
def get_order_products(id):
    order = db.session.get(Order, id)
    
    if not order:
        return jsonify({"message": f"Invalid Order ID: {id}"}), 400       
    elif not order.products:
        return jsonify({"message": "No products on Order "}), 404
    
    return orders_schema.jsonify(order.products), 200
    

# Route to DELETE an order (that has no products)
@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = db.session.get(Order, id)
    
    if not order:
        return jsonify({"message": "Invalid Order ID"}), 400
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted Order {order.order_id}"}), 200


# Run the app
app.run(debug=True)
