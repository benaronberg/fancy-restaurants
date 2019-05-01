from flask import Flask
	
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	output = '<html><body>This page will show all my restaurants</body></html>'
	return output


@app.route('/restaurant/new')
def newRestaurant():
	output = '<html><body>This page will be for making a new restaurant</body></html>'
	return output


@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	output = '<html><body>This page will be for editing restaurant %s</body></html>' % restaurant_id
	return output


@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	output = '<html><body>This page will be for deleting restaurant %s</body></html>' % restaurant_id
	return output


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	output = '<html><body>This page is the menu for restaurant %s</body></html>' % restaurant_id
	return output


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	output = '<html><body>This page will be for making a new menu item for restaurant %s</body></html>' % restaurant_id
	return output


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	output = '<html><body>This page will be for editing menu item %s for restaurant %s</body></html>' % (menu_id, restaurant_id)
	return output


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	output = '<html><body>This page will be for deleting menu item %s for restaurant %s</body></html>' % (menu_id, restaurant_id)
	return output

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)