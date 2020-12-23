from app import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(120), index=True, nullable=False)
    status = db.Column(db.Boolean, default=False)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(64), index=True)
    stock = db.Column(db.Integer, index=True, default=0)
    photo = db.Column(db.String(640), index=True, default="empty")
    price= db.Column(db.Numeric, index=True, nullable=False)
    provarsids = db.Column(db.Text)
    propsids = db.Column(db.Text)

class ProductVariants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SKU = db.Column(db.String(64), index=True, nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False)
    stock = db.Column(db.Integer, index=True, default=0)
    price = db.Column(db.Numeric, index=True, default=0)
    photo = db.Column(db.String(640), index=True, default="empty")
    propsids = db.Column(db.Text)
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    value = db.Column(db.String(64), index=True, nullable=False)

class Bundle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    product_variant_id = db.Column(db.String(64), index=True, nullable=False)
    price = db.Column(db.String(64), index=True, nullable=False)
    photo = db.Column(db.String(640), index=True, nullable=False)
    propsids = db.Column(db.Text)