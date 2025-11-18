from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           database='chargerstore')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/findcustomer', methods=['GET', 'POST'])
def find_customer_form():
    if request.method == 'POST':
        search_type = request.form.get('search_type', 'number')
        search_value = request.form.get('search_value')

        conn = get_db_connection()
        cur = conn.cursor()

        if search_type == 'number':
            sql = "SELECT * FROM customers WHERE customerNumber = %s"
            cur.execute(sql, (search_value,))
            result = cur.fetchone()
        else:  # search by name
            sql = "SELECT * FROM customers WHERE customerName LIKE %s"
            cur.execute(sql, ('%' + search_value + '%',))
            results = cur.fetchall()
            result = results[0] if results else None

        cur.close()
        conn.close()

        if result:
            customer_data = {
                'number': result[0],
                'name': result[1],
                'contact_last': result[2],
                'contact_first': result[3],
                'phone': result[4],
                'address': result[5],
                'city': result[7],
                'country': result[10]
            }
            return render_template('result.html', customer=customer_data)
        else:
            return render_template('form.html', error="Customer not found")

    return render_template('form.html')


@app.route('/findcustomer/<num>')
def find_customer(num):
    conn = get_db_connection()

    cur = conn.cursor()
    sql = "SELECT * FROM customers WHERE customerNumber = %s"
    cur.execute(sql, (num,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return str(result)
    else:
        return "Customer not found"


@app.route('/customers')
def list_customers():
    conn = get_db_connection()
    cur = conn.cursor()

    sql = "SELECT customerNumber, customerName, contactLastName, contactFirstName, phone, city, country FROM customers ORDER BY customerNumber"
    cur.execute(sql)
    customers = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('customers_list.html', customers=customers)


if __name__ == '__main__':
    app.run(debug=True)
