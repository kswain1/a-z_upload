from flask import (
    Flask, render_template, redirect, url_for, request, session, g,
    flash)
import requests
import os
from werkzeug.utils import secure_filename
from parser import HomerTechniqueCSVReader as reader

UPLOAD_FOLDER = '~/'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xlsx'])
API_BASE_URL = 'https://a-zapi.herokuapp.com'

app = Flask(__name__)
app.secret_key = 'precious'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    username = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        login = dict(username=username, password=password)
        res = requests.post('%s/login/' % API_BASE_URL, data=login)
        if res.ok:
            session['access_token'] = res.json()['token']
            session['username'] = username
            return redirect(url_for('trainer'))
        else:
            error = 'Login failed, error code: %s' % res.status_code
    return render_template('login.html', error=error, username=username)


@app.route('/trainer', methods=['GET', 'POST'])
def trainer():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('trainer.html')


@app.route('/player', methods=['GET', 'POST'])
def players():
    if 'username' not in session:
        return redirect(url_for('login'))
    error = ''
    data = {
        'player_name': request.form.get('player', ''),
        'team_name': request.form.get('team', ''),
        'user_age': request.form.get('age', ''),
    }
    headers = {
        'Authorization': 'Token %s' % session['access_token'],
    }
    res = requests.get('%s/api/team/' % API_BASE_URL, headers=headers)
    teams = res.json()
    if request.method == 'POST':
        res = requests.post('%s/player/' % API_BASE_URL, data=data,
                            headers=headers)
        if res.ok:
            return redirect(url_for('trainer'))
        else:
            error = 'Error creating player, code: %s' % res.status_code
    return render_template('player.html', data=data, teams=teams, error=error)


@app.route('/sessionsummary', methods=['GET', ])
def sessionsummary():
    return 'Session Summary'


@app.route('/session', methods=['GET', 'POST'])
def sessions():
    if 'username' not in session:
        return redirect(url_for('login'))
    error = ''
    payload = {
        'player_profile': request.form.get('athlete_profile', ''),
        'peroneals_rle': request.form.get('peroneals_rle', ''),
        'peroneals_lle': request.form.get('peroneals_lle', ''),
        'med_gastro_rle': request.form.get('med_gastro_rle', ''),
        'med_gastro_lle': request.form.get('med_gastro_lle', ''),
        'tib_anterior_lle': request.form.get('tib_anterior_lle', ''),
        'tib_anterior_rle': request.form.get('tib_anterior_rle', ''),
        'lat_gastro_lle': request.form.get('lat_gastro_lle', ''),
        'lat_gastro_rle': request.form.get('lat_gastro_rle', ''),
        'assessment': request.form.get('assessment', ''),
        'treatment': request.form.get('treatment', ''),
    }
    headers = {
        'Authorization': 'Token %s' % session['access_token'],
    }
    res = requests.get('%s/api/player/' % API_BASE_URL, headers=headers)
    athlete_profiles = res.json()
    if request.method == 'POST':
        headers = {
            'Authorization': 'Token %s' % session['access_token'],
        }
        res = requests.post('%s/session/' % API_BASE_URL, data=payload,
                            headers=headers)
        if res.ok:
            return redirect(url_for('trainer'))
        else:
            error = 'Error creating session, code: %s' % res.status_code
    return render_template('session.html', data=payload,
                           athlete_profiles=athlete_profiles, error=error)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    # player_session = requests.get('%s/api/session')
    import player_data as s
    player_data = s.player_athlete()
    return render_template('dashboard.html', player_session=player_data)


@app.route('/athletes', methods=['GET', ])
def athletes():
    if 'username' not in session:
        return redirect(url_for('login'))
    headers = {
        'Authorization': 'Token %s' % session['access_token']
    }
    res = requests.get('%s/player/' % API_BASE_URL, headers=headers)
    if res.ok:
        athlete_profiles = res.json()
        print(athlete_profiles)
        error = ''
    else:
        error = 'Error fetching athletes, code: %s' % res.status_code
        athlete_profiles = []
    return render_template('athlete_profiles.html', data=athlete_profiles,
                           error=error)


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
        if 'csv' not in file.filename:
            flash('Only CSV Files ')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # s= requests.post("https://a-zapi.heorkuapp.com/api/hello-viewset/",data=filename)
            # print(s.status_code)
            file.save(os.path.join('uploads/', filename))
            #collect first payload
            s = reader.read_csv(os.path.join('uploads',filename))
            payload = reader.neuro_sum(s)

            #collect second payload
            s = reader.read_csv(os.path.join('uploads',filename))
            payload = reader.neuro_sum(s)
            payload.update(payload)
            #send session data to the backend
            #reques.post()
            return redirect(url_for('upload',
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
