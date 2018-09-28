from flask import  Flask, render_template, redirect, url_for, request, session, g
import requests
import os 
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '~/'
ALLOWED_EXTENSIONS = set(['txt','csv','xlsx'])

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
            session['user'] = username
            return redirect(url_for('athletes'))
    return render_template('login.html', error=error)

@app.route('/trainer', methods=['GET','POST'])
def trainer():
    error = None
    return render_template('trainer.html',error=error)

#setting up to make sure that the user has an active session before they enter this session
@app.route('/athletes', methods=['GET','POST'])
def athletes():
    if g.user: 
        athlete_profile = requests.get("https://a-zapi.herokuapp.com/api/profile")
        print(athlete_profile.status_code)
        athlete_profile.json()
        return athlete_profile.json()
    else: 
        return redirect(url_for('login'))

# @app.before_request
# def before_request():
#     g.user = None
#     if 'user' in session:
#         return session['user']
#
#     return 'Not logged in!'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #check if the post request has the file change 
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser alse
        #submit an empty part without filename 
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # s= requests.post("https://a-zapi.heorkuapp.com/api/hello-viewset/",data=filename)
            # print(s.status_code)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                        filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



if __name__ == '__main__':
    app.run(debug=True)