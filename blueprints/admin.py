from flask import Blueprint, abort, redirect, render_template, request, session, url_for

import config
from extentions import db
from models.product import Product

app = Blueprint('admin', __name__)

@app.before_request
def before_request():
    print(request.endpoint)
    if session.get("admin_login",None ) == None and request.endpoint != "admin.admin_login" :
        abort(403)
      
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
  if request.method == 'POST':
    username = request.form.get('username' ,None)
    password = request.form.get('password' ,None)
    if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
      session['admin_login'] = username
      return redirect ('/admin/dashboard')
    else:
      redirect('/admin/login')
  else:
    return render_template('admin/login.html')


@app.route('/admin/dashboard' , methods=["GET"])
def dashbord ():
    return render_template('admin/dashboard.html')

@app.route('/admin/dashboard/products' , methods=["GET", "POST"])
def product():
    if request.method == 'GET':
        product = Product.query.all()
        return render_template('admin/products.html' , product = product)
    else :
        name =request.form.get('name', None)
        description =request.form.get('description', None)
        price =request.form.get('price', None)
        quantity =request.form.get('quantity', None)
        file = request.files.get('cover', None)
        p = Product(name=name ,description=description , price = price , quantity =quantity)
        db.session.add(p)
        db.session.commit()

        file.save(f'static/cover/{p.id}.jpg')
        return "done"

@app.route('/admin/dashboard/edit-product/<id>' , methods=["POST","GET"])
def edit_product(id):
    product = Product.query.filter(Product.id==id).first_or_404()
    if request.method == "GET":
        return render_template('admin/edit-product.html', product =product )
    else :
        name =request.form.get('name', None)
        description =request.form.get('description', None)
        price =request.form.get('price', None)
        quantity =request.form.get('quantity', None)
        file = request.files.get('cover', None)

        product.name=name
        product.description=description
        product.price=price
        product.quantity=quantity
        db.session.commit()

        if file != None:
            file.save(f'static/cover/{product.id}.jpg')        
        return redirect(url_for('admin.edit_product',id = id))
    
@app.route('/admin/dashboard/delete-product/<id>' , methods=["POST"])
def delete_product(id):
    product = Product.query.filter(Product.id==id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin.product'))
  
