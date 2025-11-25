from flask import Flask, render_template, request, redirect, url_for
import pymysql
from contextlib import contextmanager

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           database='chargerstore')


@contextmanager
def db_cursor():
    """Context manager for database connections and cursors."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def extract_customer_form_data():
    """Extract customer form data from request."""
    return {
        'customerName': request.form.get('customerName'),
        'contactLastName': request.form.get('contactLastName'),
        'contactFirstName': request.form.get('contactFirstName'),
        'phone': request.form.get('phone'),
        'addressLine1': request.form.get('addressLine1'),
        'addressLine2': request.form.get('addressLine2') or None,
        'city': request.form.get('city'),
        'state': request.form.get('state') or None,
        'postalCode': request.form.get('postalCode') or None,
        'country': request.form.get('country'),
        'salesRepEmployeeNumber': request.form.get('salesRepEmployeeNumber') or None,
        'creditLimit': request.form.get('creditLimit') or None
    }


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/findcustomer', methods=['GET', 'POST'])
def find_customer_form():
    if request.method == 'GET':
        return redirect(url_for('home'))
    search_type = request.form.get('search_type', 'number')
    search_value = request.form.get('search_value')

    with db_cursor() as (conn, cur):
        if search_type == 'number':
            sql = "SELECT * FROM customers WHERE customerNumber = %s"
            cur.execute(sql, (search_value,))
            result = cur.fetchone()
        else:  # search by name
            sql = "SELECT * FROM customers WHERE customerName LIKE %s"
            cur.execute(sql, ('%' + search_value + '%',))
            results = cur.fetchall()
            result = results[0] if results else None

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
            return render_template('home.html', error="Customer not found")


@app.route('/findcustomer/<num>')
def find_customer(num):
    with db_cursor() as (conn, cur):
        sql = "SELECT * FROM customers WHERE customerNumber = %s"
        cur.execute(sql, (num,))
        result = cur.fetchone()

        if result:
            return str(result)
        else:
            return "Customer not found"


@app.route('/customers')
def list_customers():
    with db_cursor() as (conn, cur):
        sql = "SELECT customerNumber, customerName, contactLastName, contactFirstName, phone, city, country FROM customers ORDER BY customerNumber"
        cur.execute(sql)
        customers = cur.fetchall()

        return render_template('customers_list.html', customers=customers)


@app.route('/customer/create', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        customer_number = request.form.get('customerNumber')
        form_data = extract_customer_form_data()

        sql = """INSERT INTO customers
                 (customerNumber, customerName, contactLastName, contactFirstName,
                  phone, addressLine1, addressLine2, city, state, postalCode,
                  country, salesRepEmployeeNumber, creditLimit)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            with db_cursor() as (conn, cur):
                cur.execute(sql, (
                    customer_number,
                    form_data['customerName'],
                    form_data['contactLastName'],
                    form_data['contactFirstName'],
                    form_data['phone'],
                    form_data['addressLine1'],
                    form_data['addressLine2'],
                    form_data['city'],
                    form_data['state'],
                    form_data['postalCode'],
                    form_data['country'],
                    form_data['salesRepEmployeeNumber'],
                    form_data['creditLimit']
                ))
            return redirect(url_for('list_customers'))
        except Exception as e:
            return render_template('create_customer.html', error=str(e))

    return render_template('create_customer.html')


@app.route('/customer/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    if request.method == 'POST':
        form_data = extract_customer_form_data()

        sql = """UPDATE customers
                 SET customerName=%s, contactLastName=%s, contactFirstName=%s,
                     phone=%s, addressLine1=%s, addressLine2=%s, city=%s,
                     state=%s, postalCode=%s, country=%s,
                     salesRepEmployeeNumber=%s, creditLimit=%s
                 WHERE customerNumber=%s"""

        try:
            with db_cursor() as (conn, cur):
                cur.execute(sql, (
                    form_data['customerName'],
                    form_data['contactLastName'],
                    form_data['contactFirstName'],
                    form_data['phone'],
                    form_data['addressLine1'],
                    form_data['addressLine2'],
                    form_data['city'],
                    form_data['state'],
                    form_data['postalCode'],
                    form_data['country'],
                    form_data['salesRepEmployeeNumber'],
                    form_data['creditLimit'],
                    customer_id
                ))
            return redirect(url_for('list_customers'))
        except Exception as e:
            # Reload customer data and show error
            with db_cursor() as (conn, cur):
                cur.execute("SELECT * FROM customers WHERE customerNumber = %s", (customer_id,))
                customer = cur.fetchone()
            return render_template('edit_customer.html', customer=customer, error=str(e))

    # GET request - load customer data
    with db_cursor() as (conn, cur):
        cur.execute("SELECT * FROM customers WHERE customerNumber = %s", (customer_id,))
        customer = cur.fetchone()

    if customer:
        return render_template('edit_customer.html', customer=customer)
    else:
        return "Customer not found", 404


@app.route('/customer/delete/<int:customer_id>')
def delete_customer(customer_id):
    try:
        with db_cursor() as (conn, cur):
            sql = "DELETE FROM customers WHERE customerNumber = %s"
            cur.execute(sql, (customer_id,))
        return redirect(url_for('list_customers'))
    except Exception as e:
        return f"Error deleting customer: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
