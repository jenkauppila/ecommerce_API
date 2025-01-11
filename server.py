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
from sqlalchemy.orm.exc import StaleDataError
from sqlalchemy.exc import IntegrityError
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
    
    existing_product = db.session.query(Product).filter_by(product_name=product_data['product_name']).first()
    if existing_product:   
        return jsonify({"message": "Duplicate product already exists"}), 409
    
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
@app.route('/orders', methods=['POST'])
# @app.route('/users/<int:user_id>/create_order', methods=['POST'])
def create_order():
    order_data = request.json
    user = db.session.get(User, order_data['user_id'])
    # old below
    # user = db.session.get(User, order_data['user_id'])
    if not user:
        return jsonify({"message": "Invalid User ID"}), 400
    user.orders.append(order_data['user_id'])
    # Order(user.id for user in  =order_data['user_id'])
    # db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 200

    # try:
    #     order_data = order_schema.load(request.json) # loads the JSON data with Order schema
    # user_id = request.json
    # user.orders.append(user)
    # if user in user.user_id:
        

    # except ValidationError as e:
    #     app.logger.error(e, exc_info=True)
    #     if "title" in e.messages and e.messages["title"] == "400 Bad Request":
    #         return jsonify({"message": "Invalid Entry"}), 400            
    #     return jsonify(e.messages), 400 # returns error msg for 400 = Bad Request
    

# old version below:
# @app.route('/orders', methods=['POST'])
# def create_order():
#     try:
#         order_data = order_schema.load(request.json) # loads the JSON data with Order schema
#     except ValidationError as e:
#         app.logger.error(e, exc_info=True)
#         if "title" in e.messages and e.messages["title"] == "400 Bad Request":
#             return jsonify({"message": "Invalid Entry"}), 400            
#         return jsonify(e.messages), 400 # returns error msg for 400 = Bad Request
    
#     new_order = Order(user_id=order_data['user_id'])
#     db.session.add(new_order)
#     user = db.session.get(User, order_data['user_id'])
#     if not user:
#         return jsonify({"message": "Invalid User ID"}), 400
#     user.orders.append(new_order)
#     db.session.commit()    
#     return order_schema.jsonify(new_order), 200

# previous below:
# def create_order():
#     try:
#         order_data = order_schema.load(request.json) # loads the JSON data with Order schema
#     except ValidationError as e:
#         app.logger.error(e, exc_info=True)
#         if "title" in e.messages and e.messages["title"] == "400 Bad Request":
#             return jsonify({"message": "Invalid Entry"}), 400            
#         return jsonify(e.messages), 400 # returns error msg for 400 = Bad Request
    
#     new_order = Order(user_id=order_data['user_id'])
#     db.session.add(new_order)
#     user = db.session.get(User, order_data['user_id'])
#     if not user:
#         return jsonify({"message": "Invalid User ID"}), 400
#     user.orders.append(new_order)
#     db.session.commit()    
#     return order_schema.jsonify(new_order), 200

    # try:
    #     order_data = order_schema.load(request.json) # loads the JSON data with Order schema
    
    # except ValidationError as e:
    #     app.logger.error(e, exc_info=True) # research app.logger
    #     if "title" in e.messages and e.messages["title"] == "400 Bad Request":
    #         return jsonify({"message": "Invalid Entry"}), 400            
    #     return jsonify(e.messages), 400 # returns error msg for 400 = Bad Request
    
    # new_order = Order(user_id=order_data['user_id'])
    # db.session.add(new_order)



    # return order_schema.jsonify(new_order), 200

# OG create_order:
# @app.route('/orders', methods=['POST'])
# def create_order():
#     try:
#         order_data = order_schema.load(request.json) # loads the JSON data with Order schema
    
#     except ValidationError as e:
#         app.logger.error(e, exc_info=True) # research app.logger
#         if "title" in e.messages and e.messages["title"] == "400 Bad Request":
#             return jsonify({"message": "Invalid Entry"}), 400            
#         return jsonify(e.messages), 400 # returns error msg for 400 = Bad Request
    
#     new_order = Order(user_id=order_data['user_id'])
#     db.session.add(new_order)
#     user = db.session.get(User, order_data['user_id'])
#     if not user:
#         return jsonify({"message": "Invalid User ID"}), 400
#     user.orders.append(new_order)
#     db.session.commit()    
#     return order_schema.jsonify(new_order), 200

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
            return jsonify({"message": f"{product.product_name} already on Order"}), 409
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
            return jsonify({"message": f"{product.product_name} not on Order: {order_id}"}), 409
        order.products.remove(product)
    
    db.session.commit()
    db.session.commit() # should this be here twice?
    
    return jsonify({"message": f"Product successfully deleted from Order: {order_id}!"}), 200


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
        
    order_ids = [order.id for order in user.orders]
    if not order_ids:
        return jsonify({"message": "No open orders exist for customer"}), 404
    return jsonify({"user_id": user.id, "user_name": user.name, "order_ids": order_ids}), 200

# WRONG: Route to GET all Orders by User ID
# @app.route('/orders/user/<int:id>', methods=['GET'])
# def get_user_orders(id):
#     user = db.session.get(User, id)
#     if not user:
#         return jsonify({"message": f"Invalid User ID: {id}"}), 400
        
#     order_ids = [order.order_id for order in user.orders]
#     if not order_ids:
#         return jsonify({"message": "No open orders exist for customer"}), 404

#     return jsonify({"user_id": user.user_id, "user_name": user.name, "order_ids": order_ids}), 200

# Run the app
app.run(debug=True)
# if __name__ == "__main__":
#     app.run(debug=True)

