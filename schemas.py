from flask_marshmallow import Marshmallow
from models import Product, CartItem, User

ma = Marshmallow()

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('password_hash',) # ¡Importante! Nunca exponer el hash.

class CartItemSchema(ma.SQLAlchemyAutoSchema):
    product = ma.Nested(ProductSchema)
    class Meta:
        model = CartItem
        include_fk = True