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
        num = request.form.get('num1')

        conn = get_db_connection()
        cur = conn.cursor()
        sql = "SELECT * FROM customers WHERE customerNumber = %s"
        cur.execute(sql, (num,))
        result = cur.fetchone()

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


if __name__ == '__main__':
    app.run(debug=True)
