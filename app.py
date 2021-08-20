from sys import meta_path
from flask import Flask, render_template, request
from flask.helpers import url_for
import psycopg2
import psycopg2.extras
from werkzeug.utils import redirect


app = Flask(__name__)
DB_HOST = "localhost"
DB_NAME = "flask_crud"
DB_USER = "admin"
DB_PASS ="1234"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route("/")
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM employee ORDER BY id"
    cur.execute(s)
    list_employee =cur.fetchall()
    return render_template('index.html', list_employee = list_employee)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur.execute("INSERT INTO employee (fname, lname, email) VALUES (%s, %s, %s)", (fname, lname, email))
        conn.commit()
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM employee WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', employee = data[0])

@app.route('/update/<string:id>', methods=['POST'])
def update_employee(id):
    
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
        UPDATE employee 
            SET fname=%s, 
                lname=%s, 
                email=%s 
            WHERE id=%s
        """, (fname, lname, email,id))
        conn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM employee WHERE id = {0}'.format(id))
    conn.commit()
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)