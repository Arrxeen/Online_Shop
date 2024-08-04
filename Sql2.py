import sqlite3

db = sqlite3.connect("shop.db")

db.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);
''')

db.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY, 
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE 
);
''')

db.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY, 
    customer_id INTEGER NOT NULL, 
    product_id INTEGER NOT NULL, 
    quantity INTEGER NOT NULL, 
    order_date DATE NOT NULL, 
    FOREIGN KEY (customer_id) 
           
REFERENCES customers(customer_id),
           FOREIGN KEY (product_id) 

REFERENCES products(product_id) );

''')

def add_products():
    name = input("Name:")
    category = input("Category:")
    price = float(input("Price:"))
    db.execute('''
    INSERT INTO products (name, category, price) 
    VALUES(?, ?, ?);''', (name, category, price))
    db.commit()

def add_customers():
    first_name = input("first_name:")
    last_name = input("last_name:")
    email = input("email:")
    db.execute('''
    INSERT INTO customers (first_name, last_name, email) 
    VALUES(?, ?, ?);''', (first_name, last_name, email))
    db.commit()

def order_products():
    customers_id = int(input("customers_id:"))
    products_id = int(input("products_id:"))
    quantity = int(input("quantity:"))
    db.execute('''
    INSERT INTO orders (customer_id,product_id,quantity,order_date ) 
    VALUES(?, ?, ?,CURRENT_TIMESTAMP)''', (customers_id,products_id,quantity))
    db.commit()

def sum_products():
    total = db.execute('''
    SELECT SUM(products.price * orders.quantity) AS total_bill
    FROM orders
    INNER JOIN products ON orders.order_id == products.product_id
    ''')
    print(total.fetchone())

def count():
    count = db.execute('''
    SELECT customers.first_name, COUNT(orders.order_id)
    FROM orders
    INNER JOIN customers ON orders.customer_id == customers.customer_id
    GROUP BY customers.first_name
    ''') 
    print(count.fetchall())  

def ag_count():
    ag = db.execute('''
    SELECT AVG(products.price * orders.quantity)
    FROM orders
    INNER JOIN products ON orders.order_id == products.product_id
    ''')
    print(ag.fetchone())

def update_price():
    db.execute('''
    UPDATE products 
    SET price = price * 1.1
    WHERE category = 'Smarthone'                           
    ''')
    db.commit()

while True:
    print('''
    Що ви хочете зробити?

    1 - Додавання продуктів:
    2 - Додавання клієнтів:
    3 - Замовлення товарів:
    4 - Сумарний обсяг продажів:
    5 - Кількість замовлень на кожного клієнта:
    6 - Середній чек замовлення:
    7 - Найбільш популярна категорія товарів:
    8 - Загальна кількість товарів кожної категорії:
    9 - Оновлення цін категорії на 10% більші:
    10 - Показати усіх користувачів
    11 - Показати усі продукти
    12 - Показати усі замовлення(Joined)
    0 - Вийти:''')
    command = input('')

    match command:
        case "1":
            add_products()
        case "2":
            add_customers()
        case "3":
            order_products()
        case "4":
            sum_products()
        case '5':
            count()
        case '6':
            ag_count()
        case '9':
            update_price()
        case "0":
            break