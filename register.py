from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'austen'
app.config['MYSQL_DATABASE_PASSWORD'] = 'alam5sql'
app.config['MYSQL_DATABASE_DB'] = 'tqm_register'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    if request.method == 'POST':
        try:
            _name = request.form['inputName']
            _email = request.form['inputEmail']
            _password = request.form['inputPassword']

            # validate the received values

            if _name and _email and _password:

                # All Good, let's call MySQL
                _hashed_password = generate_password_hash(_password)


                conn = mysql.connect()

                with conn.cursor() as cursor:

                    check = cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
                    data = cursor.fetchall()


                if len(data) is 0:
                    conn.commit()
                    conn.close()
                    return json.dumps({'message':'User created successfully !'})

                else:
                    app.logger.info(data)
                    conn.close()

                    return json.dumps({'error':str(data[0])})


            else:
                return json.dumps({'html':'<span>Enter the required fields</span>'})



        except Exception as e:
                return json.dumps({'error':str(e)})

    else:
        return render_template('signUp.html')

if __name__ == "__main__":
    app.run()
