from flask import  Flask, render_template, redirect, url_for, request, session
import requests


app = Flask(__name__)
app.secret_key = "precious"

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
            session['access_token']=token.json()['token']
            return redirect(url_for('athletes'))
    return render_template('login.html', error=error)


@app.route('/athletes', methods=['GET','POST'])
def athletes():
    return "List of Athletes Here or opportunity to create new athlete"



if __name__ == '__main__':
    app.run(debug=True)