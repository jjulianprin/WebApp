from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#------------ DB Connection Settings --------------
app.config['MYSQL_HOST'] = 'dbserver.cmrj9j8ds9vf.us-west-2.rds.amazonaws.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'qa12pl09'
app.config['MYSQL_DB'] = 'usersnpets'
mysql = MySQL(app)

# -------------- Session configuration ------------------
app.secret_key = 'mysecretkey'

#---------------- Routes Definition ---------------------
@app.route ('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
#    print (data) #---- To know the indexes to use in HTML
    return render_template('index.html', users = data)

#---------------------USER NAME--------------------------
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        pet = request.form['pet']
#----------DB Connection Definition---------
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (name, color, pet) VALUES (%s,%s,%s)', (name, color, pet))
        mysql.connection.commit()
        flash('Thanks for your information')
#TestingPrintsOnConsole
#        print(name)
#        print(color)
#        print(pet)
        return redirect(url_for('Index'))

#---------------------------------

@app.route ('/edit_user/<name>')
def get_user(name):
    cur = mysql.connection.cursor()
    cur.execute('select * FROM users WHERE name = (%s)',(name,))
    data = cur.fetchall()
    return render_template ('edit-contact.html', user=data[0])
#    print (data[0])
#    return 'Acknowledged'

@app.route('/update/<name>', methods=['POST'])
def update_user(name):
    if request.method == 'POST':
        nameE = request.form['name'] #---NameEdited
        color = request.form['color']
        pet = request.form['pet']
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE users
        SET name = %s,
            color = %s,
            pet = %s
        Where name = %s        
        """, (nameE, color, pet, name))
        mysql.connection.commit()
        flash ('Update issued correctly')
        return redirect(url_for('Index'))
#---------------------------------

@app.route ('/delete_user/<string:name>')
def delete_user(name):
    cur = mysql.connection.cursor()
#    cur.execute('DELETE FROM users WHERE name = {0}',format(name)) ---NotWorking
    cur.execute('DELETE FROM users WHERE name = (%s)', (name,))
    mysql.connection.commit()
    flash ('Your contact has been correctly deleted')
    return redirect(url_for('Index'))


#-----------------------------------------------

if __name__ == '__main__':
    app.run(ssl_context='adhoc', host='0.0.0.0', port = 3000, debug = True)