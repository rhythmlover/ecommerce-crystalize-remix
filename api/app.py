from flask import request, Flask
from dotenv import load_dotenv
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)


load_dotenv('../.env')

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('RDS_HOST'),
        user=os.environ.get('RDS_USER'),
        password=os.environ.get('RDS_PASSWORD'),
        database= os.environ.get('RDS_DATABASE')
    )

# API Endpoints
# /GetAllItems (GET)
# /addItems[params:db_schema] (POST)
# /getBySellerID[parameter: Seller_ID] (GET)
# /getItemInformation[params: seller_id, item_id] (GET)
# /updateItemQty[params: seller_id, item_id, new_qty] (PUT)

@app.route('/GetAllItems')
def get_all_items():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Items_Catalogue')
        results = cursor.fetchall()
        return {'items': results}
    finally:
        connection.close()


@app.route('/addItems', methods=['POST'])
def add_items():
    connection = get_db_connection()  
    try:
        cursor = connection.cursor()
        data = request.json
   
        cursor.execute('''
            INSERT INTO Items_Catalogue (Seller_ID, Item_ID, Item_Name, Item_Price, Item_Qty, Item_Desc, Category)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data['Seller_ID'], data['Item_ID'], data['Item_Name'], data['Item_Price'], data['Item_Qty'], data['Item_Desc'], data['Category']))
        
        connection.commit()
        return {'status': 'Item added successfully'}
    
    except Exception as e:
        connection.rollback()
        return {'status': 'Failed to add item', 'error': str(e)}, 500
    finally:
        connection.close()

@app.route('/getBySellerID/<seller_id>')
def get_by_seller_id(seller_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        seller_id = seller_id
        cursor.execute('SELECT * FROM Items_Catalogue WHERE Seller_ID = %s', (seller_id))
        results = cursor.fetchall()
        return {'items': results}
    finally:
        connection.close()

@app.route('/getItemInformation/<seller_id>/<item_id>')
def get_item_information(seller_id, item_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        seller_id = seller_id
        item_id = item_id
        cursor.execute('SELECT * FROM Items_Catalogue WHERE Seller_ID = %s AND Item_ID = %s', (seller_id, item_id))
        results = cursor.fetchall()
        return {'items': results}
    finally:
        connection.close()

@app.route('/updateItemQty/<seller_id>/<item_id>/<new_qty>', methods=['PUT'])
def update_item_qty(seller_id, item_id, new_qty):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        seller_id = seller_id
        item_id = item_id
        new_qty = new_qty
        cursor.execute('UPDATE Items_Catalogue SET Item_Qty = %s WHERE Seller_ID = %s AND Item_ID = %s', (new_qty, seller_id, item_id))
        connection.commit()
        return {'status': 'Item quantity updated successfully'}
    except Exception as e:
        connection.rollback()
        return {'status': 'Failed to update item quantity', 'error': str(e)}, 500
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(port=5000, debug=True)