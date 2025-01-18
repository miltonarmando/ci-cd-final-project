from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy(app)

# Modelo de dados para representar produtos
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    name = db.Column(db.String(80), nullable=False)  # Nome do produto
    category = db.Column(db.String(80), nullable=False)  # Categoria do produto
    price = db.Column(db.Float, nullable=False)  # Preço do produto
    availability = db.Column(db.Boolean)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "availability": self.availability,
        }

# Garante que as tabelas sejam criadas antes de rodar o app
with app.app_context():
    db.create_all()

@app.route("/products/<int:product_id>", methods=["GET"])
def read_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.serialize())

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    product.name = data.get("name", product.name)
    product.category = data.get("category", product.category)
    product.price = data.get("price", product.price)
    product.availability = data.get("availability", product.availability)
    db.session.commit()
    return jsonify(product.serialize())

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return "", 204

@app.route("/products", methods=["GET"])
def list_products():
    filters = {}
    if "name" in request.args:
        filters["name"] = request.args["name"]
    if "category" in request.args:
        filters["category"] = request.args["category"]
    if "availability" in request.args:
        filters["availability"] = request.args.get("availability") == "true"
    products = Product.query.filter_by(**filters).all()
    return jsonify([product.serialize() for product in products])

@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    new_product = Product(
        name=data["name"],
        category=data["category"],
        price=data["price"],
        availability=data["availability"]
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.serialize()), 201

if __name__ == "__main__":
    app.run(debug=True)

