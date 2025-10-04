from flask import Flask, request, jsonify, render_template
import json
from models import db, Product, CartItem, User
from schemas import ma, ProductSchema, CartItemSchema, UserSchema
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "tu-super-secreto-aqui"

db.init_app(app)
ma.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
user_schema = UserSchema()
cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)

# --- Rutas para Renderizar Vistas HTML ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cart-view')
def cart_view():
    return render_template('cart.html')
    
@app.route('/register-view')
def register_view():
    return render_template('register.html')

@app.route('/login-view')
def login_view():
    return render_template('login.html')

# --- Rutas de Autenticación ---

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "El correo electrónico ya está en uso"}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuario registrado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": "Error en el registro", "details": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity={'id': user.id, 'username': user.username})
            return jsonify(access_token=access_token)
        
        return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        return jsonify({"error": "Error en el inicio de sesión", "details": str(e)}), 500

@app.route('/profile', methods=['GET'])
@jwt_required() # Protege esta ruta
def profile():
    """
    Ruta de ejemplo para demostrar la protección.
    Para probarla, haz una petición GET a /profile con el header:
    Authorization: Bearer <tu_access_token>
    """
    current_user_identity = get_jwt_identity()
    user = User.query.get(current_user_identity['id'])
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    return user_schema.jsonify(user)
    
# --- Rutas de la API (para ser llamadas por JavaScript) ---

@app.route('/products', methods=['POST'])
def add_product():
    try:
        name = request.json['name']
        description = request.json.get('description', "")
        price = request.json['price']
        image = request.json.get('image', "")
        stock = request.json['stock']
        new_product = Product(name=name, description=description, price=price, image=image, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product), 201
    except Exception as e:
        return jsonify({"error": "Datos inválidos", "details": str(e)}), 400

@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    return product_schema.jsonify(product)

@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    try:
        product.name = request.json.get('name', product.name)
        product.description = request.json.get('description', product.description)
        product.price = request.json.get('price', product.price)
        product.stock = request.json.get('stock', product.stock)
        db.session.commit()
        return product_schema.jsonify(product)
    except Exception as e:
        return jsonify({"error": "Datos inválidos", "details": str(e)}), 400

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Producto eliminado correctamente"})

@app.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user_id = get_jwt_identity()['id']
    product_id = request.json['product_id']
    quantity = request.json.get('quantity', 1)

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    if product.stock < quantity:
        return jsonify({"error": "Stock insuficiente"}), 400

    cart_item = CartItem.query.filter_by(user_id=current_user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return cart_item_schema.jsonify(cart_item), 201

@app.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    current_user_id = get_jwt_identity()['id']
    cart_items = CartItem.query.filter_by(user_id=current_user_id).all()
    return cart_items_schema.jsonify(cart_items)

@app.route('/cart/<item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    current_user_id = get_jwt_identity()['id']
    cart_item = CartItem.query.get(item_id)
    if not cart_item or cart_item.user_id != current_user_id:
        return jsonify({"error": "Item no encontrado en el carrito"}), 404
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Item eliminado del carrito"})

@app.route('/cart/checkout', methods=['POST'])
@jwt_required()
def checkout():
    current_user_id = get_jwt_identity()['id']
    cart_items = CartItem.query.filter_by(user_id=current_user_id).all()
    if not cart_items:
        return jsonify({"error": "El carrito está vacío"}), 400
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product.stock < item.quantity:
            return jsonify({"error": f"Stock insuficiente para el producto '{product.name}'"}), 400
        product.stock -= item.quantity
        db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Compra realizada con éxito. El carrito ha sido vaciado."})

def seed_data():
    """Carga datos iniciales en la base de datos si está vacía."""
    if Product.query.count() > 0:
        return

    products_data = [
        { "id": 1, "name": "Smartphone X100", "description": "Smartphone de alta gama con cámara de 108MP y pantalla OLED.", "price": 3199900, "image": "https://i.imgur.com/H2a5I3G.jpeg", "stock": 20 },
        { "id": 2, "name": "Laptop UltraPro", "description": "Laptop ultradelgada con procesador Intel i7 y 16GB de RAM.", "price": 5999900, "image": "https://i.imgur.com/4XE4927.jpeg", "stock": 15 },
        { "id": 3, "name": "Auriculares Bose", "description": "Auriculares con cancelación de ruido y sonido envolvente.", "price": 1199900, "image": "https://i.imgur.com/I5b55G5.jpeg", "stock": 30 },
        { "id": 4, "name": "Smartwatch ZFit", "description": "Reloj inteligente con monitoreo de salud y GPS integrado.", "price": 799900, "image": "https://i.imgur.com/E1zXyBC.jpeg", "stock": 25 },
        { "id": 5, "name": "Cámara Digital Nikon D7500", "description": "Cámara DSLR con sensor de 20.9MP y grabación en 4K.", "price": 4799900, "image": "https://i.imgur.com/sJz9tZg.jpeg", "stock": 10 },
        { "id": 6, "name": "Tablet ProTab 10", "description": "Tablet con pantalla de 10 pulgadas y 128GB de almacenamiento.", "price": 1399900, "image": "https://i.imgur.com/gJ5O4dC.jpeg", "stock": 18 },
        { "id": 7, "name": "Altavoces JBL Flip 5", "description": "Altavoces portátiles a prueba de agua con sonido potente.", "price": 519900, "image": "https://i.imgur.com/vJm2Sif.jpeg", "stock": 40 },
        { "id": 8, "name": "Teclado Mecánico Razer", "description": "Teclado con teclas mecánicas y retroiluminación RGB.", "price": 479900, "image": "https://i.imgur.com/hB2zWJ1.jpeg", "stock": 22 },
        { "id": 9, "name": "Ratón Logitech G502", "description": "Ratón gaming con 11 botones programables y sensor de 16K DPI.", "price": 239900, "image": "https://i.imgur.com/s3G2V3G.png", "stock": 50 },
        { "id": 10, "name": "Impresora HP DeskJet", "description": "Impresora multifuncional de inyección de tinta con Wi-Fi.", "price": 319900, "image": "https://i.imgur.com/5nLYJd3.jpeg", "stock": 12 },
        { "id": 11, "name": "Monitor LG 32UK550", "description": "Monitor 4K de 32 pulgadas con HDR y tecnología IPS.", "price": 1999900, "image": "https://i.imgur.com/gCq4V2a.jpeg", "stock": 8 },
        { "id": 12, "name": "Cafetera Nespresso", "description": "Cafetera de cápsulas Nespresso con sistema de preparación rápido.", "price": 599900, "image": "https://i.imgur.com/tVqYw2j.png", "stock": 35 },
        { "id": 13, "name": "Mochila North Face", "description": "Mochila resistente al agua con compartimentos para laptop.", "price": 359900, "image": "https://i.imgur.com/INf34rS.jpeg", "stock": 45 },
        { "id": 14, "name": "Silla Ergonómica DXRacer", "description": "Silla de oficina ergonómica para largas sesiones de trabajo.", "price": 1199900, "image": "https://i.imgur.com/b2gA25A.jpeg", "stock": 9 },
        { "id": 15, "name": "Tenedor Eléctrico Oster", "description": "Tenedor eléctrico con motor de alta potencia para carnes.", "price": 159900, "image": "https://i.imgur.com/yOq2gM4.jpeg", "stock": 15 },
        { "id": 16, "name": "Proyector Epson 1080p", "description": "Proyector de alta definición para cine en casa.", "price": 1999900, "image": "https://i.imgur.com/jNix1sF.jpeg", "stock": 7 },
        { "id": 17, "name": "Microondas Samsung", "description": "Microondas con tecnología inverter para una cocción uniforme.", "price": 599900, "image": "https://i.imgur.com/0z4zYjH.png", "stock": 14 },
        { "id": 18, "name": "Lámpara de Escritorio LED", "description": "Lámpara LED regulable para oficina con puerto USB.", "price": 119900, "image": "https://i.imgur.com/jB4g3fA.jpeg", "stock": 60 },
        { "id": 19, "name": "Cargador Inalámbrico Anker", "description": "Cargador inalámbrico rápido para smartphones.", "price": 159900, "image": "https://i.imgur.com/G4gL8bV.jpeg", "stock": 100 },
        { "id": 20, "name": "Horno Tostador Oster", "description": "Horno tostador compacto con función de gratinado.", "price": 279900, "image": "https://i.imgur.com/sW3dZ3Y.jpeg", "stock": 25 }
    ]

    for prod_data in products_data:
        new_product = Product(**prod_data)
        db.session.add(new_product)
    
    db.session.commit()
    print("¡Base de datos cargada con productos iniciales!")
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)
