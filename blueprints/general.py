from flask import Blueprint, render_template

from models.product import Product

app = Blueprint('general',__name__)

@app.route('/')
def main():
  product = Product.query.filter(Product.quantity > 0).all()
  return render_template('main.html', product=product)
  

@app.route('/product/<int:id>/<name>')
def product(id,name):
  product = Product.query.filter(Product.id == id)\
  .filter(Product.name == name).first_or_404()
  return render_template('product.html', product=product)

@app.route('/about')
def about():
  return render_template('about.html')

