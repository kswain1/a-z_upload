from flask import  Flask, render_template, redirect, url_for, request
import requests


app = Flask(__name__)

#use decorators
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login = dict(username=username,password=password)
        token = requests.post("https://a-zapi.herokuapp.com/login/",data=login)
        if token.status_code != 200:
            return "error " + str(token.status_code)
        else:
            return "You have successfully logged in"
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)