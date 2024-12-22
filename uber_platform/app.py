from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key


# Database configuration
db_config = {
    'user': 'root',  # Replace with your MySQL username
    'password': 'password',  # Replace with your MySQL password
    'host': '127.0.0.1',
    'database': 'uber'  # Replace with your database name
}

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Route: Merchant Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Hash the password before saving to the database
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO merchant (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, hashed_password))
            conn.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return jsonify({'error': str(err)})
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

# Route: Merchant Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM merchant WHERE email = %s", (email,))
        merchant = cursor.fetchone()
        cursor.close()
        conn.close()

        if merchant and check_password_hash(merchant['password'], password):
            session['merchant_id'] = merchant['id']
            session['merchant_name'] = merchant['name']
            return redirect(url_for('view_orders'))
        return jsonify({'error': 'Invalid email or password'})
    return render_template('login.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Route: View Orders
@app.route('/orders', methods=['GET'])
def view_orders():
    if 'merchant_id' not in session:
        return redirect(url_for('login'))

    merchant_id = session['merchant_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 查詢該商家所有訂單
    cursor.execute("""
        SELECT o.id AS order_id, o.status, o.delivery_address, o.total_price, o.created_at,
               c.name AS customer_name
        FROM `order` o
        JOIN customer c ON o.customer_id = c.id
        WHERE o.merchant_id = %s
        ORDER BY o.created_at DESC
    """, (merchant_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('orders.html', orders=orders)

# Route: Add Menu Item
@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
    if 'merchant_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        availability_status = request.form['availability_status']
        merchant_id = session['merchant_id']

        # Insert the menu item into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO menuitem (name, price, description, availability_status, merchant_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, price, description, availability_status, merchant_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('view_menu'))  # Redirect to view menu page

    return render_template('add_menu.html')


# Route: View Menu Items
@app.route('/view_menu', methods=['GET'])
def view_menu():
    if 'merchant_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    merchant_id = session['merchant_id']

    # Fetch all menu items for the merchant
    cursor.execute("SELECT * FROM menuitem WHERE merchant_id = %s", (merchant_id,))
    menu_items = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('view_menu.html', menu_items=menu_items)


# Route: Update Order Status
@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    if 'merchant_id' not in session:
        return redirect(url_for('login'))

    order_id = request.form['order_id']
    new_status = request.form['status']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE `order` SET status = %s WHERE id = %s AND merchant_id = %s
    """, (new_status, order_id, session['merchant_id']))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('view_orders'))
# Route: Home Page
@app.route('/', methods=['GET'])
def home():
    if 'merchant_id' not in session:
        return redirect(url_for('login'))  # 如果未登入，重定向到登入頁面
    return render_template('home.html')  # 渲染主頁模板

@app.route('/menu', methods=['GET', 'POST'])
def manage_menu():
    if 'merchant_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 處理刪除請求
    if request.method == 'GET' and 'delete_id' in request.args:
        delete_id = request.args.get('delete_id')
        merchant_id = session['merchant_id']

        # 刪除符合條件的菜單項目
        cursor.execute("DELETE FROM menuitem WHERE id = %s AND merchant_id = %s", (delete_id, merchant_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('manage_menu'))  # 刪除後重定向回菜單頁面

    # 處理新增或更新菜單項目
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        availability_status = request.form['availability_status']
        merchant_id = session['merchant_id']

        # 插入或更新菜單項目
        cursor.execute("""
            INSERT INTO menuitem (name, price, description, availability_status, merchant_id)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            price = VALUES(price),
            description = VALUES(description),
            availability_status = VALUES(availability_status)
        """, (name, price, description, availability_status, merchant_id))
        conn.commit()

    # 顯示所有菜單項目
    cursor.execute("SELECT * FROM menuitem WHERE merchant_id = %s", (session['merchant_id'],))
    menu_items = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('view_menu.html', menu_items=menu_items)


if __name__ == '__main__':
    app.run(debug=True)
