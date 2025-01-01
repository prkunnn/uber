from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

#app = Flask(__name__)
app = Flask(__name__, static_folder='static',static_url_path='/')
app.secret_key = 'your_secret_key'  # Replace with a secure key


# Database configuration
db_config = {
    'user': 'root',  # Replace with your MySQL username
    'password': '',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'begin'  # Replace with your database name
}

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 路由：商家註冊
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # 如果請求方法是 POST，表示提交註冊表單
        name = request.form['name']  # 獲取表單中的商家名稱
        email = request.form['email']  # 獲取表單中的電子郵件
        password = request.form['password']  # 獲取表單中的密碼

        # 在儲存至資料庫之前對密碼進行雜湊處理
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()  # 獲取資料庫連線
        cursor = conn.cursor()
        try:
            # 插入商家資料到 merchant 資料表
            cursor.execute("INSERT INTO merchant (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, hashed_password))
            conn.commit()  # 提交變更
            return redirect(url_for('login'))  # 註冊成功後導向登入頁面
        except mysql.connector.Error as err:
            return jsonify({'error': str(err)})  # 捕捉並返回錯誤訊息
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')  # 渲染註冊頁面

# 路由：商家登入
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # 如果請求方法是 POST，表示提交登入表單
        email = request.form['email']  # 獲取表單中的電子郵件
        password = request.form['password']  # 獲取表單中的密碼

        conn = get_db_connection()  # 獲取資料庫連線
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM merchant WHERE email = %s", (email,))  # 查詢商家資料
        merchant = cursor.fetchone()  # 獲取查詢結果
        cursor.close()
        conn.close()

        if merchant and check_password_hash(merchant['password'], password):  # 驗證密碼是否正確
            session['merchant_id'] = merchant['id']  # 儲存商家 ID 到 session
            session['merchant_name'] = merchant['name']  # 儲存商家名稱到 session
            return redirect(url_for('view_orders'))  # 登入成功後導向查看訂單頁面
        else:
            return jsonify({'error': 'Invalid email or password!'})  # 返回錯誤訊息
    return render_template('login.html')  # 渲染登入頁面

# 路由：登出
@app.route('/logout')
def logout():
    session.clear()  # 清空 session 資料
    return redirect(url_for('frontPage'))  # 導向主頁面

# 路由：查看訂單
@app.route('/orders', methods=['GET'])
def view_orders():
    if 'merchant_id' not in session:  # 確認商家是否已登入
        return redirect(url_for('login'))

    merchant_id = session['merchant_id']  # 從 session 獲取商家 ID
    conn = get_db_connection()  # 獲取資料庫連線
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
    orders = cursor.fetchall()  # 獲取所有訂單
    cursor.close()
    conn.close()

    return render_template('orders.html', orders=orders)  # 渲染訂單頁面

# 路由：新增菜單項目
@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
    if 'merchant_id' not in session:  # 確認商家是否已登入
        return redirect(url_for('login'))

    if request.method == 'POST':  # 如果請求方法是 POST，表示提交新增表單
        name = request.form['name']  # 獲取菜單名稱
        price = request.form['price']  # 獲取菜單價格
        description = request.form['description']  # 獲取菜單描述
        availability_status = request.form['availability_status']  # 獲取菜單狀態
        merchant_id = session['merchant_id']  # 從 session 獲取商家 ID

        conn = get_db_connection()  # 獲取資料庫連線
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO menuitem (name, price, description, availability_status, merchant_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, price, description, availability_status, merchant_id)
        )
        conn.commit()  # 提交變更
        cursor.close()
        conn.close()

        return redirect(url_for('view_menu'))  # 重定向到查看菜單頁面

    return render_template('add_menu.html')  # 渲染新增菜單頁面

# 路由：查看菜單項目
@app.route('/view_menu', methods=['GET'])
def view_menu():
    if 'merchant_id' not in session:  # 確認商家是否已登入
        return redirect(url_for('login'))

    conn = get_db_connection()  # 獲取資料庫連線
    cursor = conn.cursor(dictionary=True)
    merchant_id = session['merchant_id']  # 從 session 獲取商家 ID

    # 查詢所有菜單項目
    cursor.execute("SELECT * FROM menuitem WHERE merchant_id = %s", (merchant_id,))
    menu_items = cursor.fetchall()  # 獲取菜單資料
    cursor.close()
    conn.close()

    return render_template('view_menu.html', menu_items=menu_items)  # 渲染菜單頁面

# 路由：更新訂單狀態
@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    if 'merchant_id' not in session:  # 確認商家是否已登入
        return redirect(url_for('login'))

    order_id = request.form['order_id']  # 獲取訂單 ID
    new_status = request.form['status']  # 獲取新狀態

    conn = get_db_connection()  # 獲取資料庫連線
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE `order` SET status = %s WHERE id = %s AND merchant_id = %s
    """, (new_status, order_id, session['merchant_id']))
    conn.commit()  # 提交變更
    cursor.close()
    conn.close()

    return redirect(url_for('view_orders'))  # 重定向到訂單頁面

# 路由：主頁
@app.route('/', methods=['GET'])
def home():
    if 'customer_id' not in session:  # 如果客戶未登入
        return redirect(url_for('frontPage'))  # 重定向到主頁
    elif 'merchant_id' not in session:  # 如果商家未登入
        return redirect(url_for('frontPage'))  # 重定向到登入頁面
    return render_template('home.html')  # 渲染主頁模板

# 路由：管理菜單
@app.route('/menu', methods=['GET', 'POST'])
def manage_menu():
    if 'merchant_id' not in session:  # 確認商家是否已登入
        return redirect(url_for('login'))

    conn = get_db_connection()  # 獲取資料庫連線
    cursor = conn.cursor(dictionary=True)

    # 處理刪除請求
    if request.method == 'GET' and 'delete_id' in request.args:
        delete_id = request.args.get('delete_id')  # 獲取刪除的菜單項目 ID
        merchant_id = session['merchant_id']  # 從 session 獲取商家 ID

        # 刪除符合條件的菜單項目
        cursor.execute("DELETE FROM menuitem WHERE id = %s AND merchant_id = %s", (delete_id, merchant_id))
        conn.commit()  # 提交變更
        cursor.close()
        conn.close()
        return redirect(url_for('manage_menu'))  # 刪除後重定向

    # 處理新增或更新菜單項目
    if request.method == 'POST':
        name = request.form['name']  # 獲取菜單名稱
        price = request.form['price']  # 獲取價格
        description = request.form['description']  # 獲取描述
        availability_status = request.form['availability_status']  # 獲取狀態
        merchant_id = session['merchant_id']  # 從 session 獲取商家 ID

        # 插入或更新菜單項目
        cursor.execute("""
            INSERT INTO menuitem (name, price, description, availability_status, merchant_id)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            price = VALUES(price),
            description = VALUES(description),
            availability_status = VALUES(availability_status)
        """, (name, price, description, availability_status, merchant_id))
        conn.commit()  # 提交變更

    # 顯示所有菜單項目
    cursor.execute("SELECT * FROM menuitem WHERE merchant_id = %s", (session['merchant_id'],))
    menu_items = cursor.fetchall()  # 獲取菜單資料
    cursor.close()
    conn.close()

    return render_template('view_menu.html', menu_items=menu_items)  # 渲染菜單頁面

#-------------------------------------------------------------------------------------------------------------

# Route: Front Page登入前主頁
@app.route("/frontPage")
def frontPage():
	#data = dat
	return render_template('index.html')

# Route: 客人 Register
@app.route('/customer_regi', methods=['GET', 'POST'])
def cusReg():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['pswd']

        # Hash the password before saving to the database
        # hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO customer (name, contact_info, password) VALUES (%s, %s, %s)",
                           (name, phone, password))
            conn.commit()
            return redirect(url_for('cusReg'))
        except mysql.connector.Error as err:
            return jsonify({'error': str(err)})
        finally:
            cursor.close()
            conn.close()
    return render_template('cusLogin.html')

# Route: 客人 Login
@app.route('/customer_login', methods=['GET', 'POST'])
def cuslogin():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['pswd']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer WHERE contact_info = %s", (phone,))
        customer = cursor.fetchone()
        #return jsonify(customer['password'], password)
        cursor.close()
        conn.close()
        #return jsonify(merchant['password'], password, hashed_password)
        #if check_password_hash(merchant['password'], password):
        if customer['password'] == password:
            #return jsonify(merchant['password'], password)
            session['customer_id'] = customer['id']
            session['customer_name'] = customer['name']
            session['customer_address'] = customer['address']
            return redirect(url_for('main_index'))
        else:
            return jsonify({'error': 'Invalid email or password!'})
    return render_template('cuslogin.html')

# Route: 平台主頁面
@app.route("/main_index")
def main_index():
    if 'customer_id' not in session:
        return redirect(url_for('cuslogin'))
    return render_template('main_index.html')

# Route:餐廳列表
@app.route("/restaurants")
def restaurants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    customer_id = session['customer_id']

    # Fetch all menu items for the merchant
    cursor.execute("SELECT * FROM merchant")
    menu_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('restaurants.html', menu_items=menu_items)

# Route: 購物車
@app.route("/entershoppingCart", methods=['POST'])
def chcekSC():
    if request.method == 'POST':
        merchant_id = request.form['merchant_id']
        items = []
        for key, value in request.form.items():
            if key.startswith('amount_'):
                item_id = key.split('_')[1]
                amount = value
                dish_id = request.form.get(f'dish_id_{item_id}')
                name = request.form.get(f'name_id_{item_id}')
                price = request.form.get(f'price_id_{item_id}')
                total_price = int(amount) * int(price)
                items.append({'dish_id': dish_id, 'amount': amount, 'name': name, 'price': price, 'total_price': total_price})
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    customer_id = session['customer_id']
    address = session['customer_address']
    sumprice = 0
    for item in items:
        sumprice += item['total_price']
    order = []
    # for item in items:
        # cursor.execute("SELECT * FROM menuitem WHERE id = %s", (item['dish_id'],))
        # order.append(cursor.fetchone())
        # cursor.execute("INSERT INTO orderitem (menu_item_id, quantity, price) VALUES (%s,%s,%s);", (item['dish_id'], item['amount'], item['total_price'],))
        # order.append(cursor.fetchone())
    # cursor.execute("INSERT INTO `order` (customer_id, merchant_id, delivery_address, total_price) VALUES (%s,%s,%s,%s);", (customer_id, merchant_id, address, sumprice,))
    conn.commit()
    cursor.close()
    conn.close()

    return render_template('shoppingCart.html', m_id = merchant_id, items=items)

# Route: 確認訂單
@app.route("/confirm_order", methods=['POST'])
def confirm_order():
    # loaded = False
    customer_id = session['customer_id']
    address = session['customer_address']
    if request.method == 'POST':
        merchant_id = request.form['m_id']
        total_price = request.form['total_price']
        # loaded = request.form['loaded']
        items = []
        
        for key, value in request.form.items():
            if key.startswith('amount_'):
                item_id = key.split('_')[1]
                amount = request.form.get(f'amount_{item_id}')
                dish_id = request.form.get(f'dish_id_{item_id}')
                price = request.form.get(f'sum_price_{item_id}')
                items.append({'dish_id': dish_id, 'amount': amount, 'price': price})

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # 检查是否已经存在相同的订单
        cursor.execute("SELECT id FROM `order` WHERE customer_id = %s AND merchant_id = %s AND delivery_address = %s AND total_price = %s ORDER BY created_at DESC LIMIT 1;", (customer_id, merchant_id, address, total_price))
        last_order = cursor.fetchone()
        # cursor.execute("SELECT id FROM `order` WHERE customer_id = %s ORDER BY created_at DESC LIMIT 1;", (customer_id,))
        # last_order = cursor.fetchone() #135
        cursor.execute("SELECT TIMESTAMPDIFF(SECOND,(SELECT created_at FROM `order` ORDER BY id DESC LIMIT 1 OFFSET 1), (SELECT created_at FROM `order` ORDER BY id DESC LIMIT 1 )) as timediff;")
        time_diff = cursor.fetchone()
        time_diff_str = str(time_diff)
        # return jsonify(last_order)
        if last_order:
            # 检查订单项是否相同
            cursor.execute("SELECT menu_item_id, quantity, price FROM `orderitem` WHERE order_id = %s", (last_order['id'],))
            existing_items = cursor.fetchall()
            existing_items_set = {(str(item['menu_item_id']), str(item['quantity']), str(item['price'])) for item in existing_items}
            new_items_set = {(item['dish_id'], item['amount'], item['price']) for item in items}
            # return jsonify(list(existing_items_set), list(new_items_set))
            # return jsonify(existing_items, items, existing_items_set)

            if existing_items_set == new_items_set:
                # 如果订单项相同，则不插入新的订单
                cursor.execute("SELECT  id, status, total_price, delivery_person_id FROM `order` WHERE customer_id = %s ORDER BY created_at DESC LIMIT 1;", (customer_id,))
                order = cursor.fetchall()
                cursor.execute("SELECT name FROM `deliveryperson` WHERE id = %s", (order[0]['delivery_person_id'],))
                deliver = cursor.fetchall()
                cursor.execute("SELECT orderitem.menu_item_id, orderitem.quantity, orderitem.price, menuitem.name FROM `orderitem`,`menuitem` WHERE order_id = %s AND menuitem.id=orderitem.menu_item_id", (order[0]['id'],))
                fitem = cursor.fetchall()
                conn.close()
                return render_template('cusOrder.html', order=order, fitem=fitem, deliver=deliver)

        # 插入新的訂單
        cursor.execute("INSERT INTO `order` (customer_id, merchant_id, delivery_address, total_price) VALUES (%s,%s,%s,%s);", (customer_id, merchant_id, address, total_price,))
        for item in items:
            cursor.execute("INSERT INTO `orderitem` (menu_item_id, quantity, price) VALUES (%s,%s,%s);", (item['dish_id'], item['amount'], item['price'],))
            cursor.fetchone()
            #order.append(cursor.fetchone())
        cursor.execute("UPDATE orderitem SET order_id = (SELECT id FROM `order` ORDER BY created_at DESC LIMIT 1) Where order_id IS NULL;")
        cursor.execute("SELECT id, status, total_price, delivery_person_id FROM `order` WHERE customer_id = %s ORDER BY created_at DESC LIMIT 1;", (customer_id,))
        order = cursor.fetchall()
        cursor.execute("SELECT name FROM `deliveryperson` WHERE id = %s", (order[0]['delivery_person_id'],))
        deliver = cursor.fetchall()
        cursor.execute("SELECT orderitem.menu_item_id, orderitem.quantity, orderitem.price, menuitem.name FROM `orderitem`,`menuitem` WHERE order_id = %s AND menuitem.id=orderitem.menu_item_id", (order[0]['id'],))
        fitem = cursor.fetchall()
        # return jsonify(order)
        # cursor.execute("SELECT * FROM `orderitem` WHERE order_id = %s", (item['dish_id'],))
        conn.commit()
        cursor.close()
        conn.close()

    return render_template('cusOrder.html', order=order, fitem=fitem, deliver=deliver)

# Route: 收貨
@app.route("/confirm_delivered", methods=['POST'])
def confirm_delivered():
    customer_id = session['customer_id']
    # 在这里处理确认收到订单的逻辑，例如更新订单状态
    if request.method == 'POST':
        order_id = request.form['o_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE `order` SET status = 'Received' WHERE customer_id = %s AND id = %s AND status = %s;", (customer_id, order_id, 'Delivered',))
    cursor.execute("UPDATE `deliveryperson` SET current_status = 'Idle' WHERE id = (SELECT delivery_person_id FROM `order` WHERE customer_id = %s AND id = %s AND status = 'Received');", (customer_id,order_id,))
    conn.commit()
    cursor.close()
    conn.close()
    # return redirect(url_for('home'))
    return redirect("/")

# Route: 訂單歷史
@app.route("/order_history")
def order_history():
    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `order` WHERE customer_id = %s ORDER BY created_at DESC LIMIT 30;", (customer_id,))
    orders = cursor.fetchall()
    order_details = []
    for order in orders:
        cursor.execute("SELECT orderitem.menu_item_id, orderitem.quantity, orderitem.price, menuitem.name FROM `orderitem` JOIN `menuitem` ON orderitem.menu_item_id = menuitem.id WHERE order_id = %s;", (order['id'],))
        order_items = cursor.fetchall()
        order['items'] = order_items
        
        #order_details.append(order)
    # return jsonify(orders.items().name)
    # for i in orders:
    #      return jsonify(i['items'][0]['name'])
    cursor.close()
    conn.close()
    return render_template('order_history.html', orders=orders, order_details=order_details)

@app.route('/check_single_order', methods=['POST'])
def check_order():
    customer_id = session['customer_id']
    address = session['customer_address']
    if request.method == 'POST':
        order_id = request.form['o_id']
        merchant_id = request.form['m_id']
        total_price = request.form['total_price']
        deliver_id = request.form['d_id']
    # return jsonify(items)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `order` WHERE id = %s", (order_id,))
    order = cursor.fetchall()
    cursor.execute("SELECT orderitem.menu_item_id, orderitem.quantity, orderitem.price, menuitem.name FROM `orderitem`,`menuitem` WHERE order_id = %s AND menuitem.id=orderitem.menu_item_id", (order_id,))
    fitem = cursor.fetchall()
    cursor.execute("SELECT name FROM `deliveryperson` WHERE id = %s", (deliver_id,))
    deliver = cursor.fetchone() or []
    cursor.close()
    conn.close()
    
    return render_template('cusOrder.html', order=order, fitem=fitem, deliver=deliver)

# Route: View Menu Items 查看各餐廳菜單
@app.route('/check_menu', methods=['GET'])
def check_menu():
    if 'customer_id' not in session:
        return redirect(url_for('login'))
    data = request.args.get('data')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    merchant_id = data
    customer_id = session['customer_id']
    # Fetch all menu items for the menuitem
    cursor.execute("SELECT name, img, id FROM merchant WHERE id = %s ", (merchant_id,))
    merchant_info = cursor.fetchall()
    cursor.execute("SELECT * FROM menuitem WHERE merchant_id = %s ", (merchant_id,))
    menu_items = cursor.fetchall()
    cursor.execute("SELECT customer.name as cName, merchant.name, feedback.feedback_text, feedback.rating, feedback.created_at FROM `customer`,`merchant`,`feedback` WHERE merchant.id = %s AND customer.id=feedback.customer_id AND merchant.id=feedback.target_id;", (merchant_id,))
    feedbacks = cursor.fetchall()
    #return jsonify(feedbacks)
    cursor.close()
    conn.close()
    
    return render_template('check_menu.html', merchant = merchant_info, menu_items =menu_items, feedbacks = feedbacks)

# Route: Feedback給評
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'customer_id' not in session:
        return redirect(url_for('cuslogin'))

    rating = request.form.get('star_count')
    print(f'Star count: {rating}')
    # 處理新增點評項目
    c_id = session['customer_id']
    if request.method == 'POST':
        if 'm_id' in request.form:
            target_id = request.form['m_id']
            feedback_text = request.form['feedback']
            rating = request.form['star_count']
        elif 'd_id' in request.form:
            target_id = int(request.form['d_id'])+10000
            feedback_text = request.form['feedback']
            rating = request.form['star_count']
            order_id = request.form['o_id']
            target_id = str(target_id)+'_'+str(order_id)
    else:
        target_id = "No target id provided"
        feedback_text = 'No feedback or rating provided'
    # return jsonify(feedback_text, target_id, rating)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO feedback (customer_id, target_id, feedback_text, rating, created_at) VALUES (%s, %s, %s, %s, NOW());", (c_id, target_id, feedback_text, rating,))
    conn.commit()
    # cursor.execute("""
    #         INSERT INTO feedback (feedback_text)
    #         VALUES (%s)
    #         ON DUPLICATE KEY UPDATE
    #         feedback_text = VALUES(feedback_text)
    #     """, (feedback_text,)
    feedbacks = cursor.fetchall()
    #return jsonify()
    cursor.close()
    conn.close()

    return redirect(url_for('restaurants'))

# Route: About關於我們頁面
@app.route("/about")
def about():
	#data = dat
	return render_template('about.html')

# Route: News最新消息, Blog頁面
@app.route("/news")
def news():
	#data = dat
	return render_template('news.html')
#-------------------------------------------------------------------------------------------------------------


# Route: Deliver Registration
@app.route('/deliver_regi', methods=['GET', 'POST'])
def deliver_regi():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Hash the password before saving to the database
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("INSERT INTO deliveryperson (name, contact_info, password) VALUES (%s, %s, %s)",
                           (name, email, password))
            conn.commit()
            return redirect(url_for('deliver_login'))
        except mysql.connector.Error as err:
            return jsonify({'error': str(err)})
        finally:
            cursor.close()
            conn.close()
    return render_template('deliverRegister.html')

# Route: Deliver Login
@app.route('/deliver_login', methods=['GET', 'POST'])
def deliver_login():
    if request.method == 'POST':
        phone = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM deliveryperson WHERE contact_info = %s", (phone,))
        deliver = cursor.fetchone()
        cursor.close()
        conn.close()
        # return jsonify(deliver['password'], password)

        # if deliver and check_password_hash(deliver['password'], password):
        if deliver['password'] == int(password):
            session['deliver_id'] = deliver['id']
            session['deliver_name'] = deliver['name']
            return redirect(url_for('deliverHome'))
        else:
            return jsonify({'error': 'Invalid email or password'})
    return render_template('deliveryLogin.html', merchant_login=True)

# Route: Deliver Home
@app.route('/driverHome', methods=['GET'])
def deliverHome():
    if 'deliver_id' not in session:
        return redirect(url_for('deliver_login'))
    deliver_name = session['deliver_name']
    deliver_id = session['deliver_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, status FROM `order` WHERE delivery_person_id = %s AND status = %s or status =  %s", (deliver_id,'Accepted', 'PickedUp'))
    order_id = cursor.fetchall()

    # cursor.fetchall()
    cursor.close()
    conn.close()
    # return jsonify(order_id)
    return render_template('driver_home.html', deliver_name=deliver_name, order_id=order_id)


# Route: View Assigned Orders
@app.route('/assigned_orders', methods=['GET'])
def assigned_orders():
    if 'deliver_id' not in session:
        return redirect(url_for('deliver_login'))
    # return render_template('assigned_orders.html')

    deliver_id = session['deliver_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 查詢該商家所有訂單
    cursor.execute("""
        SELECT o.id AS order_id, o.status, o.delivery_address, o.total_price, o.created_at,
               c.name AS customer_name, m.name AS merchant_name, m.contact_info 
        FROM `merchant` m, `order` o
        JOIN customer c ON o.customer_id = c.id
        WHERE o.status = "Pending"
        AND o.merchant_id = m.id
        ORDER BY o.created_at ASC
    """)
    orders = cursor.fetchall()
    cursor.execute("SELECT current_status FROM `deliveryperson` WHERE id = %s", (deliver_id,))
    status = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('assigned_orders.html', orders=orders, status=status)

# Route: Update Order Status
@app.route('/upd_order_status', methods=['POST'])
def upd_order_status():
    if 'deliver_id' not in session:
        return redirect(url_for('deliver_login'))

    order_id = request.form['order_id']
    new_status = request.form['status']
    deliver_id = session['deliver_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE `order` SET status = %s, delivery_person_id = %s WHERE id = %s 
    """, (new_status,  deliver_id, order_id),)
    conn.commit()
    cursor.execute("""
        UPDATE `deliveryperson` SET current_status = %s WHERE id = %s 
    """, (new_status, deliver_id),)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('deliverHome'))

if __name__ == '__main__':
    app.run(debug=True)