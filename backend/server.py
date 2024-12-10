from flask import Flask, render_template, request 
import sqlite3
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return "Hello world"

connect = sqlite3.connect('./database/database.db')
cursor = connect.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PARTICIPANTS (
        name TEXT,
        email TEXT,
        city TEXT,
        country TEXT,
        phone TEXT
    )
''')
connect.commit()
connect.close()

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']
        phone = request.form['phone']
        with sqlite3.connect("./database/database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO PARTICIPANTS (name,email,city,country,phone) VALUES (?,?,?,?,?)",(name, email, city, country, phone)) 
            users.commit()
        return "500 oke"
    else:
        return render_template('join.html')
@app.route('/participants')
def participants():
    connect = sqlite3.connect('./database/database.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM PARTICIPANTS')
    data = cursor.fetchall()
    return data
if __name__ == '__main__':
    app.run(debug=False)