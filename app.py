from flask import Flask, render_template, request, json
#from flaskext.mysql import MySQL
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'flask'
app.config['MYSQL_DATABASE_PASSWORD'] = 'svgSD#201'
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = '54.38.176.15'
mysql.init_app(app)



@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():

    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:

        conn = mysql.connect()
        cursor = conn.cursor()
        # Используйте модуль Werkzeug для создания хэшированного пароля.
        _hashed_password = generate_password_hash(_password)
        # Теперь вызываем процедуру sp_createUser:

        cursor.callproc('sp_createUser', (_name, _email, _hashed_password))

        # Если процедура выполнена успешно, мы зафиксируем изменения и вернем
        # сообщение об успешном завершении.

        data = cursor.fetchall()

        if (len(data) is 0):
            conn.commit()
            return(json.dumps({"message": "User created successfully "}))
        else:
            return(json.dumps({'error': str(data[0])}))
        # read the posted values from the UI

            #return (json.dumps({'html': '<span>All fields good !!</span>'}))
    else:
        return (json.dumps({'html': '<span>Enter the required fields</span>'}))

    cursor.close() 
    conn.close()




if __name__ == "__main__":
    app.run()
