from app import (
    app,
    db,
    User,
    Order,
    Product,
    user_schema,
    users_schema,
    order_schema,
    # orders_schema,
    product_schema,
    products_schema,
)
from flask import request, jsonify, render_template
from marshmallow import ValidationError
from sqlalchemy import select
import logging

@app.route('/')
def main():
#   app.logger.debug("Debug log level")
#   app.logger.info("Program running correctly")
#   app.logger.warning("Warning; low disk space!")
#   app.logger.error("Error!")
#   app.logger.critical("Program halt!")
  return render_template("index.html")
# return "logger levels!"


# Endpoints:
# --- MARK: User Schemas 

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


# --- MARK: Product Schemas

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
            products = db.session.execute(query).all()
            return jsonify({"message": "No products found"}), 404
    return products_schema.jsonify(products), 200

# Route to GET a single product
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    return product_schema.jsonify(product), 200

# Route to UPDATE a product
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
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


# --- MARK: Order Schemas 

# Route to ADD new order
# @app.route('/users/<int:user_id>/orders', methods=['POST'])
# @app.route('/orders/users/<int:user_id>', methods=['POST'])
# def create_order(user_id):
#     try:
#         order_data = order_schema.load(request.json) # loads the JSON data with Order schema
#         user_data = user_schema.load(request.json) # loads the JSON data with User schema
    
#     except ValidationError as e:
#         app.logger.error(e, exc_info=True) # research app.logger
#         if "title" in e.messages and e.messages["title"] == "400 Bad Request":
#             return jsonify({"message": "Invalid Entry"}), 400            
#         return jsonify(e.messages), 400 # returns error msg for 400 = Bad Request
    
#     user_id = request.json
#     user = db.session.get(User, user_id)
    
#     for id in user_id:
#         new_order = Order(order_date=order_data['order_date']), User(user_id=user_data['user_id'])
#         user_id = db.session.get(User, user_id)    
#         db.session.add(new_order)
#         db.session.commit()
    
#     return order_schema.jsonify(new_order), 201 # product created successfully and response returned

    # order_ids = request.json
    # for id in order_ids['order_ids']:
    #     order = db.session.get(Order, id)
    #     user.order.append(order)
    #     db.session.commit()
    # return jsonify({"message": f"Order added to {user.name}!"}), 200


# @app.route('/orders', methods=['POST'])
# def create_order():
#     try:
#         order_data = order_schema.load(request.json) # loads the JSON data with Order schema
#         user_data = user_schema.load(request.json) # loads the JSON data with User schema
    
#     new_order = Order(order_date=order_data['order_date']), User(user_id=user_data['user_id'])
#     db.session.add(new_order)
#     db.session.commit()
#     return order_schema.jsonify(new_order), 201 # product created successfully and response returned

# @app.route('/users/<int:user_id>/orders', methods=['POST'])
# def create_order(user_id):
#     user = db.session.get(User, user_id)    
#     order_ids = request.json
#     for id in order_ids['order_ids']:
#         order = db.session.get(Order, id)
#         user.order.append(order)
#         db.session.commit()
#     return jsonify({"message": f"Order added to {user.name}!"}), 200

    # existing_product = db.session.query(Product).filter_by(product_name=product_data['product_name']).first()
    # if existing_product:   
    #     return jsonify({"message": "Duplicate product already exists"}), 409


# Run the app
app.run(debug=True)