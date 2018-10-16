from flask import (
    Flask, render_template, redirect, url_for, request, session, g,
    flash)
import requests
import os
from werkzeug.utils import secure_filename
from parser import HomerTechniqueCSVReader as reader
import json

UPLOAD_FOLDER = '~/'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xlsx'])
API_BASE_URL = 'https://a-zapi.herokuapp.com'
# API_BASE_URL = 'http://localhost:8000'

app = Flask(__name__)
app.secret_key = 'precious'

@app.route('/')
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

@app.route('/playerprofile', methods=['GET','POST'])
def playerprofile():
    return render_template('user.html')

@app.route('/player', methods=['GET', 'POST'])
def players():
    if 'username' not in session:
        return redirect(url_for('login'))
    error = ''
    data = {
        'player_name': request.form.get('player', ''),
        'team_id': request.form.get('team', ''),
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


@app.route('/sessionsummary/<player_id>', methods=['GET', ])
def sessionsummary(player_id):
    s = requests.get('%s/session/?search=%s' % (API_BASE_URL,player_id))
    error = ''
    if s.ok:
        session = s.json()[0]
        print(s.json())
        jsonDec = json.decoder.JSONDecoder()
        for i in session:
            if i != 'id' and i != 'trainer_profile' and i != 'player_profile' and i != 'created_on' and i != 'assessment' and i != 'treatment':
                # session[i] = jsonDec.decode(session[i])
                session[i] = [float(item) for item in eval(session[i])]
                # for item in eval(session[i]):
                #     temp = []
                #     temp.append(float(item))
                # session[i] = temp
    else:
        return(s.text)
    player = requests.get('%s/player/%s' % (API_BASE_URL, player_id))
    return render_template('dashboard.html',data=session, player=player.json(), error=error)

@app.route('/reportsummary/<player_id>', methods=['GET','POST'])
def reportsummmary(player_id):
    s = requests.get('%s/session/?search=%s' % (API_BASE_URL, player_id))
    if s.ok:
        session = s.json()[0]
        print(s.json())
        jsonDec = json.decoder.JSONDecoder()

        for i in session:
            if i != 'id' and i != 'trainer_profile' and i != 'player_profile' and i != 'created_on' and i != 'assessment' and i != 'treatment':
                # session[i] = jsonDec.decode(session[i])
                session[i] = [float(item) for item in eval(session[i])]
                # for item in eval(session[i]):
                #     temp = []
                #     temp.append(float(item))
                # session[i] = temp
    else:
        return (s.text)
    update = request.form.get('assessment')
    if request.method == 'POST':
        data = request
        print(request.form.get('assessment',''))
        print(update)

    print(update)
    player = requests.get('%s/player/%s' % (API_BASE_URL, player_id))

    return render_template('report.html', data=session, player=player.json(), update = update)

@app.route('/composite/<player_id>', methods=['GET','POST'])
def composite(player_id):
    s = requests.get('%s/session/?search=%s' % (API_BASE_URL, player_id))
    return render_template('composite.html', player=player_id)

@app.route('/createcomposite', methods=['GET','POST'])
def createcomposite():
    error = ""
    if 'username' not in session:
        return redirect(url_for('login'))
    headers = {
        'Authorization': 'Token %s' % session['access_token'],
    }

    s = requests.get('%s/composite/' % API_BASE_URL)
    payload = {
        'player_profile': request.form.get('athlete_profile', ''),
        'risk_area':request.form.get('injuries',),
        'post_medial_direction_rle': request.form.get('peroneals_rle', ''),
        'post_medial_direction_lle': request.form.get('peroneals_lle', ''),
        'ant_direction_rle': request.form.get('med_gastro_rle', ''),
        'ant_direction_lle': request.form.get('med_gastro_lle', ''),
        'post_lateral_direction_rle': request.form.get('tib_anterior_lle', ''),
        'post_lateral_direction_lle': request.form.get('tib_anterior_rle', ''),
        'left_leg_length': request.form.get('lat_gastro_lle', ''),
        'right_leg_length': request.form.get('lat_gastro_rle', ''),
        'composite_score_rle': request.form.get(''),
        'composite_score_lle': request.form.get(''),
        'assessment': request.form.get('assessment', ''),
        'treatment': request.form.get('treatment', ''),
    }
    session_id = request.form.get('session_id', '')
    if request.method == 'POST':
        res = requests.post('%s/composite/' % API_BASE_URL, data=payload,
                       headers=headers)
        if res.ok:
            return redirect(url_for('trainer'))
        else:
            error = 'Error creating session, code: %s' % res.status_code
    res = requests.get('%s/api/player/' % API_BASE_URL, headers=headers)
    injuries = requests.get('%s/api/injury' % API_BASE_URL, headers=headers).json()
    athlete_profiles = res.json()
    print(athlete_profiles)
    return render_template('createcomposite.html', error=error, data=payload, athletes_profiles=athlete_profiles, injuries=injuries)

@app.route('/updatesession/<player_id>', methods=['GET','POST'])
def update_session(player_id):
    error = ""
    headers = {
        'Authorization': 'Token %s' % session['access_token'],
    }

    player_session = requests.get('%s/session/?search=%s' % (API_BASE_URL, player_id), headers=headers)

    player_session = player_session.json()[-1]
    print(player_session)
    if request.method == ' POST':
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
        session_id = request.form.get('session_id', '')


        res = requests.put('%s/session/%s' % (API_BASE_URL, session_id), data=payload,
                              headers=headers)

        if res.ok:
            return redirect(url_for('trainer'))
        else:
            error = 'Error creating session, code: %s' % res.status_code
            print(error)

    return render_template('asessment.html',data=player_session, error=error)


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
        ## This function below is used to update the assessment and treatment data of the athlete
        player_session = requests.get('%s/session/?search=%s' % (API_BASE_URL,payload['player_profile']))
        index = player_session.json().__len__() - 1
        k = player_session.json()[index]
        k['assessment'] = payload['assessment']
        k['treatment'] = payload['treatment']
        update_req = requests.put('%s/session/?search=%s' % (API_BASE_URL,payload['player_profile'] ), data=payload, headers=headers)

        ## end of get players session
        res = requests.post('%s/session/%s' % API_BASE_URL, data=payload,
                            headers=headers)
        print(res)
        if res.ok:
            return redirect(url_for('trainer'))
        else:
            error = 'Error creating session, code: %s' % res.status_code
    return render_template('session.html', data=payload,
                           athlete_profiles=athlete_profiles, error=error)


@app.route('/dashboard', methods=['GET', 'POST'])
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


@app.route('/upload-session', methods=['GET', 'POST'])
def upload_session():
    if 'username' not in session:
        return redirect(url_for('login'))
    error = ''
    headers = {
        'Authorization': 'Token %s' % session['access_token']
    }
    res = requests.get('%s/api/player/' % API_BASE_URL, headers=headers)
    athlete_profiles = res.json()
    if request.method == 'POST':
        # check if the post request has the file change
        if 'data-lle' not in request.files:
            error = 'Left leg data file missing'
            return render_template('upload_session.html', error=error)
        if 'data-rle' not in request.files:
            error = 'Right leg data file missing'
            return render_template('upload_session.html', error=error)

        lle_file = request.files['data-lle']
        rle_file = request.files['data-rle']

        if lle_file.filename == '' or rle_file.filename == '':
            error = 'No file selected'
            return render_template('upload_session.html', error=error)
        if ('csv' not in lle_file.filename) or (
                'csv' not in rle_file.filename):
            error = 'Only CSV Files '
            return render_template('upload_session.html', error=error)
        lle_filename = secure_filename(lle_file.filename)
        rle_filename = secure_filename(rle_file.filename)
        lle_file.save(os.path.join('uploads', lle_filename))
        rle_file.save(os.path.join('uploads', rle_filename))

        s = reader.read_csv(os.path.join('uploads', lle_filename))
        lle_payload = reader.neuro_sum(s)
        s = reader.read_csv(os.path.join('uploads', rle_filename))
        rle_payload = reader.neuro_sum(s)
        payload = {
            'player_profile': request.form.get('athlete_profile', ''),
            'peroneals_rle': json.dumps(rle_payload['peroneals_rle']),
            'peroneals_lle': json.dumps(lle_payload['peroneals_lle']),
            'med_gastro_rle': json.dumps(rle_payload['med_gastro_rle']),
            'med_gastro_lle': json.dumps(lle_payload['med_gastro_lle']),
            'tib_anterior_lle': json.dumps(lle_payload['tib_anterior_lle']),
            'tib_anterior_rle': json.dumps(rle_payload['tib_anterior_rle']),
            'lat_gastro_lle': json.dumps(lle_payload['lat_gastro_lle']),
            'lat_gastro_rle': json.dumps(rle_payload['lat_gastro_rle']),
        }

        res = requests.post('%s/session/' % API_BASE_URL, data=payload,
                            headers=headers)
        s = payload
        if res.ok:
            return redirect(url_for('trainer'))
    return render_template('upload_session.html', profiles=athlete_profiles)


if __name__ == '__main__':
    app.run(port='8080',debug=True)
