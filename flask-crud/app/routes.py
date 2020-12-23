from flask import render_template, request, redirect
from app import app, db
from app.models import Entry, Product, ProductVariants, Bundle, Property
import os

jedi = "ERROR HAPPENED"

UPLOAD_FOLDER = '/Users/ahmedmgh/WORK/NewsImgKarim/flask-crud/app/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/index')
def index():
    products = Product.query.all()
    bundles = Bundle.query.all()
    return render_template('home.html', products=products, bundles=bundles)



@app.route('/crud')
def crud():
    entries = Entry.query.all()
    products = Product.query.all()
    productVars = ProductVariants.query.all()
    bundles = Bundle.query.all()
    props = Property.query.all()
    return render_template('index.html', entries=entries, products=products, productvars=productVars, bundles=bundles, props=props)


@app.route('/buy/<int:id>')
def cruda(id):
    entries = Entry.query.all()
    products = Product.query.get(id)
    # pvs_ids = products.provarsids
    # pvs_ids = str(pvs_ids).split(',')
    pvs = db.session.query(ProductVariants).filter(ProductVariants.SKU==id)
    
    propsIn = []
    propsList = products.propsids.split(',')
    for p in propsList:
        propsIn.append(Property.query.get((p)))
    # print(propsList)
    return render_template('buy.html', entry=products, pvs=pvs, pv="", propsList=propsIn)  

@app.route('/buy/<int:id>/<int:vid>')
def crudas(id, vid):
    entries = Entry.query.all()
    products = Product.query.get(id)
    productv = ProductVariants.query.get(vid)
    pvs = db.session.query(ProductVariants).filter(ProductVariants.SKU==id)
    propsIn = []
    propsList = productv.propsids.split(',')
    for p in propsList:
        propsIn.append(Property.query.get((p)))
    return render_template('buy.html', entry=products, pv=productv, pvs=pvs, propsList=propsIn)

@app.route('/buyf/<int:id>/', defaults={'vid': None}) 
@app.route('/buyf/<int:id>/<int:vid>')
def crudaf(id, vid):
    # entries = Entry.query.all()
    if vid is not None:
        pv = ProductVariants.query.get(id)
        db.session.query(ProductVariants).filter(ProductVariants.id==vid).update({ProductVariants.stock: pv.stock-1})
        db.session.commit()
    else:
        p = Product.query.get(id)
        db.session.query(Product).filter(Product.id==id).update({Product.stock: p.stock-1})
        db.session.commit()
        
    return redirect('/')



@app.route('/buyBun/<int:id>')
def buyBun(id):
    bundle = Bundle.query.get(id)
    
    productsIn = []
    productsList = bundle.product_variant_id.split(',')
    for p in productsList:
        productsIn.append(ProductVariants.query.get(p))
    propsIn = []
    propsList = bundle.propsids.split(',')
    for p in propsList:
        propsIn.append(Property.query.get((p)))
    return render_template('buyBun.html', bundle=bundle, productsIn=productsIn, propsList=propsIn)


@app.route('/buybunf/<int:id>')
def buyBunf(id):
    bundle = Bundle.query.get(id)
    
    productsIn = []
    productsList = bundle.product_variant_id.split(',')
    for p in productsList:
        # productsIn.append(ProductVariants.query.get(p))
        print(p)
        pv = ProductVariants.query.get(int(p))
        db.session.query(ProductVariants).filter(ProductVariants.id==int(p)).update({ProductVariants.stock: pv.stock-1})
        
    db.session.commit()
    # return render_template('buyBun.html', bundle=bundle, productsIn=productsIn)
    return redirect('/')




# TODO PRODUCT









@app.route('/product/add', methods=['POST'])
def addP():
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        if name:
            if 'file1'  in request.files:
                # return 'there is no file1 in form!'
                file1 = request.files['file1']
                path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
                file1.save(path)
                entry = Product(name = name, photo=file1.filename, description=form.get('description'), price=float(form.get('price')),stock=form.get('stock'), propsids=form.get('propsids'))
            else:
                entry = Product(name = name, description=form.get('description'), price=float(form.get('price')),stock=form.get('stock'), propsids=form.get('propsids'))
            db.session.add(entry)
            db.session.commit()
            return redirect('/crud')

    return "ERROR HAPPENED"

@app.route('/product/update/<int:id>')
def updateRouteP(id):
    if not id or id != 0:
        entry = Product.query.get(id)
        if entry:
            return render_template('update_product.html', entry=entry, typeURL="/product")

    return "ERROR HAPPENED"

@app.route('/product/update/req/<int:id>', methods=['POST'])
def updateP(id):
    if not id or id != 0:
        entry = Product.query.get(id)
        if entry:
            db.session.query(Product).filter(Product.id==id).update({Product.name: request.form.get('name'), Product.stock: request.form.get('stock'), Product.description: request.form.get('description'), Product.propsids: request.form.get('propsids')})
            # Product.query.get(id).update({Product.name: request.form.get("name")})
            # newp = Product(name=entry['name'])
            # db.session.add(newp)
            # db.session.delete(entry)
            db.session.commit()
        return redirect('/crud')

    return "ERROR HAPPENED"



@app.route('/product/delete/<int:id>')
def deleteP(id):
    if not id or id != 0:
        entry = Product.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/crud')

    return "ERROR HAPPENED"




# TODO PRODUCT VARIANT









@app.route('/productVar/add', methods=['POST'])
def addPV():
    if request.method == 'POST':
        form = request.form
        sku = form.get('SKU')
        name = form.get('name')
        price = form.get('price')
        stock = form.get('stock')
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        entry = ProductVariants(SKU = sku, name=name, price=price, stock=stock, photo=file1.filename, propsids=form.get('propsids'))
        db.session.add(entry)
        db.session.commit()
        return redirect('/crud')

# return "ERROR HAPPENED"

@app.route('/productVar/update/<int:id>')
def updateRoutePV(id):
    if not id or id != 0:
        entry = ProductVariants.query.get(id)
        if entry:
            return render_template('update_product_variant.html', entry=entry, typeURL="/product")

    return "ERROR HAPPENED"

@app.route('/productVar/update/req/<int:id>', methods=['POST'])
def updatePV(id):
    if not id or id != 0:
        entry = ProductVariants.query.get(id)
        if entry:
            db.session.query(ProductVariants).filter(ProductVariants.id==id).update({ProductVariants.SKU: request.form.get('SKU'), ProductVariants.name: request.form.get('name'), ProductVariants.price: request.form.get('price'), ProductVariants.stock: request.form.get('stock'), ProductVariants.propsids: request.form.get('propsids')})
            # Product.query.get(id).update({Product.name: request.form.get("name")})
            # newp = Product(name=entry['name'])
            # db.session.add(newp)
            # db.session.delete(entry)
            db.session.commit()
        return redirect('/crud')

    return "ERROR HAPPENED"



@app.route('/productVar/delete/<int:id>')
def deletePV(id):
    if not id or id != 0:
        entry = ProductVariants.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/crud')

    return "ERROR HAPPENED"











# TODO PROPERTY









@app.route('/prop/add', methods=['POST'])
def addPR():
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        if name:
            entry = Property(name = name, value=form.get('value'))
            db.session.add(entry)
            db.session.commit()
            return redirect('/crud')

    return "ERROR HAPPENED"

@app.route('/prop/update/<int:id>')
def updateRoutePR(id):
    if not id or id != 0:
        entry = Property.query.get(id)
        if entry:
            return render_template('update_product_property.html', entry=entry, typeURL="/product")

    return "ERROR HAPPENED"

@app.route('/prop/update/req/<int:id>', methods=['POST'])
def updatePR(id):
    if not id or id != 0:
        entry = Property.query.get(id)
        if entry:
            db.session.query(Property).filter(Property.id==id).update({Property.name: request.form.get('name')})
            # Product.query.get(id).update({Product.name: request.form.get("name")})
            # newp = Product(name=entry['name'])
            # db.session.add(newp)
            # db.session.delete(entry)
            db.session.commit()
        return redirect('/crud')

    return "ERROR HAPPENED"



@app.route('/prop/delete/<int:id>')
def deletePR(id):
    if not id or id != 0:
        entry = Property.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/crud')

    return "ERROR HAPPENED"



















# TODO PROPERTY









@app.route('/bundle/add', methods=['POST'])
def addB():
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        product_variant_id = form.get('product_variant_id')
        price = form.get('price')
        if name:
            file1 = request.files['file1']
            path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
            file1.save(path)
            entry = Bundle(name = name, product_variant_id=product_variant_id, price=price, photo=file1.filename, propsids=form.get('propsids'))
            
            db.session.add(entry)
            db.session.commit()
            return redirect('/crud')

    return "ERROR HAPPENED"

@app.route('/bundle/update/<int:id>')
def updateRouteB(id):
    if not id or id != 0:
        entry = Bundle.query.get(id)
        if entry:
            return render_template('update_product_bundle.html', entry=entry, typeURL="/product")

    return "ERROR HAPPENED"

@app.route('/bundle/update/req/<int:id>', methods=['POST'])
def updateB(id):
    if not id or id != 0:
        entry = Bundle.query.get(id)
        if entry:
            db.session.query(Bundle).filter(Bundle.id==id).update({Bundle.name: request.form.get('name'), Bundle.product_variant_id: request.form.get('product_variant_id'), Bundle.price: request.form.get('price'), Bundle.propsids: request.form.get('propsids')})
            # Product.query.get(id).update({Product.name: request.form.get("name")})
            # newp = Product(name=entry['name'])
            # db.session.add(newp)
            # db.session.delete(entry)
            db.session.commit()
        return redirect('/crud')

    return "ERROR HAPPENED"



@app.route('/bundle/delete/<int:id>')
def deleteB(id):
    if not id or id != 0:
        entry = Bundle.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/crud')

    return "ERROR HAPPENED"

