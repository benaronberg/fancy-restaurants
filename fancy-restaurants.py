from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Restaurant, Base, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	items = session.query(MenuItem).all()
	return render_template('restaurants.html', restaurants=restaurants, items=items)


@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		#flash("New restaurant created! Fancy!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		#flash("Restaurant modified! Fancy!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editrestaurant.html',restaurant = editedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one() 
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		#flash("Restaurant deleted!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleterestaurant.html', restaurant = restaurantToDelete)



@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu', methods=['GET','POST'])
def showMenu(restaurant_id, methods=['GET','POST']):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return render_template('menu.html',restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		#flash("New menu item created!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		return render_template('newmenuitem.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.name = request.form['description']
		if request.form['price']:
			editedItem.name = request.form['price']
		if request.form['course']:
			editedItem.name = request.form['course']
		session.add(editedItem)
		session.commit()
		flash("Menu item modified!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html',restaurant=restaurant,item=editedItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		#flash("New menu item deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html', item = itemToDelete, restaurant=restaurant)


@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurant=[r.serialize for r in restaurants])


@app.route('/restaurant/<int:restaurant_id>/JSON')
def menuJSON(restaurant_id):
	menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in menu])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem = menuItem.serialize)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)