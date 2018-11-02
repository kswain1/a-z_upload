from flask import (
    Flask, render_template, redirect, url_for, request, session, g,
    flash)
import requests
import os
from werkzeug.utils import secure_filename
from parser import HomerTechniqueCSVReader as reader
import json
import pandas as pd

UPLOAD_FOLDER = '~/'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xlsx'])
API_BASE_URL = 'https://a-zapi.herokuapp.com'
#API_BASE_URL = 'http://localhost:8000'


app = Flask(__name__)
app.secret_key = 'precious'


@app.route('/', methods=['GET', 'POST'])
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
        'team': request.form.get('team', ''),
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
    s = requests.get('%s/session/?search=%s' % (API_BASE_URL, player_id))
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
        error = 'Error creating session, code: %s' % s.status_code
        return error
    player = requests.get('%s/player/%s' % (API_BASE_URL, player_id))
    return render_template('dashboard.html', data=session, player=player.json(), error=error)


@app.route('/summary/<player_id>', methods=['GET', ])
def summary(player_id):
    s = requests.get('%s/session/?search=%s' % (API_BASE_URL, player_id))
    composite = requests.get('%s/composite/?search=%s' %(API_BASE_URL, player_id)).json()
    #TODO create better logic for figuring whether or not to choose right or left leg. In this exp
    composite = composite[0]['composite_score_rle']
    error = ''
    if s.ok:
        #changed session data into a different format
        #session = s.json()[0]
        session = s.json()[-1]
        print(session)
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
        error = 'Error connecting to database session, code: %s' % s.status_code
        return render_template('report.html', error=error)

    player = requests.get('%s/player/%s' % (API_BASE_URL, player_id))
    injury = requests.get('%s/injury/' % (API_BASE_URL)).json()

    #predicts when muscle is injuried
    muscle_groups = {'peroneals_rle':False,'peroneals_lle':False,'med_gastro_lle':False,'med_gastro_rle':False,
                     'tib_anterior_lle':False,'tib_anterior_rle':False,'lat_gastro_lle':False,'lat_gastro_rle':False}

    ##TODO remove hardcoding and have this section udpate the id based on the name the injury
    # for i in range(injury):
    #     if muscle_groups[i] in injury[i]['name']

    muscle_types = {'peroneals_rle':0,'peroneals_lle':1,'lat_gastro_rle':2, 'lat_gastro_lle':3,
                    'med_gastro_rle':4,'med_gastro_lle':5,'tib_anterior_rle':6,'tib_anterior_lle':7}

    injured_muscles_list = []
    injured_muscle = {'name':'','url':''}

    for session_data in session:
        for muscle in muscle_groups:
            if session_data == muscle and session[muscle][0] >= 50:
                muscle_groups[muscle] = True
                index = muscle_types[muscle]
                muscle_name = injury[index]['name']
                muscle_url = injury[index]['url']
                injured_muscle['name'] = muscle_name
                injured_muscle['url'] = muscle_url
                injured_muscles_list.append(injured_muscle)
    #Tags the muscles that are injured (in the future create left leg and right leg muscle to reduce the amount iteration




    return render_template('report.html', data=session, player=player.json(), composite=composite, injured_muscles=injured_muscles_list)


@app.route('/composite/<player_id>', methods=['GET', 'POST'])
def composite(player_id):
    s = requests.get('%s/composite/?search=%s' % (API_BASE_URL, player_id))
    composite = s.json()[-1]
    injury = requests.get('%s/injury/%s' % (API_BASE_URL, composite['risk_area'])).json()

    return render_template('composite.html', player=player_id, composite=composite, injury=injury)


@app.route('/createcomposite', methods=['GET', 'POST'])
def createcomposite():
    error = ""
    if 'username' not in session:
        return redirect(url_for('login'))
    headers = {
        'Authorization': 'Token %s' % session['access_token'],
    }

    payload = {
        'player_profile': request.form.get('athlete_profile', ''),
        'risk_area': request.form.get('injuries', ),
        'post_medial_direction_rle': request.form.get('post_medial_direction_rle', ''),
        'post_medial_direction_lle': request.form.get('post_medial_direction_lle', ''),
        'ant_direction_rle': request.form.get('ant_direction_rle', ''),
        'ant_direction_lle': request.form.get('ant_direction_lle', ''),
        'post_lateral_direction_rle': request.form.get('post_lateral_direction_rle', ''),
        'post_lateral_direction_lle': request.form.get('post_lateral_direction_lle', ''),
        'left_leg_length': request.form.get('left_leg_length', ''),
        'right_leg_length': request.form.get('right_leg_length', ''),
        'composite_score_rle': request.form.get('composite_score_rle', ''),
        'composite_score_lle': request.form.get('composite_score_lle', ''),
        'assessment': request.form.get('assessment', ''),
        'treatment': request.form.get('treatment', ''),
    }
    s = requests.get('%s/composite/' % API_BASE_URL)
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
    return render_template('createcomposite.html', error=error, data=payload, athletes_profiles=athlete_profiles,
                           injuries=injuries)

#TODO app.route playercomposite
#TODO app.route('updatecomposite<player_id)>',methods=['GET'])


@app.route('/playersessions/<player_id>', methods=['GET'])
def player_sessions(player_id):
    error = ""
    headers = {
        'Authorization': 'Token %s' % session['access_token'],
    }

    sessions = requests.get('%s/session/?search=%s' % (API_BASE_URL, player_id), headers=headers)
    sessions = sessions.json()
    return render_template("playersessions.html", sessions=sessions)


@app.route('/update_composite/<player_id>', methods=['GET','POST'])
def update_composite(player_id):
    error= ""
    headers = {
        'Authorization': 'Token %s' % session['access_token']
    }
    player_composite = request.get('%s/createcomposite/?player_profile')

@app.route('/updatesession/<player_id>', methods=['GET', 'POST'])
def update_session(player_id):
    error = ""
    headers = {
        'Authorization': 'Token %s' % session['access_token'],
    }

    player_session = requests.get('%s/session/?search=%s' % (API_BASE_URL, player_id), headers=headers)
    player_session = player_session.json()[-1]

    player = requests.get('%s/player/%s' % (API_BASE_URL, player_session['player_profile']))
    print(player_session)
    if request.method == 'POST':
        payload = {
            'player_profile': player_id,
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

        res = requests.put('%s/session/%s/' % (API_BASE_URL, session_id), data=payload,
                           headers=headers)

        if res.ok:
            return redirect(url_for('trainer'))
        else:
            error = 'Error creating session, code: %s' % res.status_code
            print(error)

    return render_template('asessment.html', data=player_session, player=player.json(), error=error)


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
        player_session = requests.get('%s/session/?search=%s' % (API_BASE_URL, payload['player_profile']))
        index = player_session.json().__len__() - 1
        k = player_session.json()[index]
        k['assessment'] = payload['assessment']
        k['treatment'] = payload['treatment']
        update_req = requests.put('%s/session/?search=%s' % (API_BASE_URL, payload['player_profile']), data=payload,
                                  headers=headers)

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

    res = requests.get('%s/api/player/' % API_BASE_URL, headers=headers,)
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
            'assessment': request.form.get('assessment',''),
            'treatment':request.form.get('treatment', '')

        }

        res = requests.post('%s/session/' % API_BASE_URL, data=payload,
                            headers=headers,)
        s = payload
        if res.ok:
            return redirect(url_for('trainer'))
        else:
            error = "error uploading to the backend"
            return render_template('upload_session.html', error=error)

    data = {'assessment': '',
            'treatment': ''}

    return render_template('upload_session.html', profiles=athlete_profiles, data=data)

@app.route('/upload-composite', methods=['GET', 'POST'])
def upload_composite():
    if 'username' not in session:
        return redirect(url_for('login'))
    error = ''
    headers = {
        'Authorization': 'Token %s' % session['access_token']
    }
    data = {'assessment': '',
            'treatment': ''}
    res = requests.get('%s/api/player/' % API_BASE_URL, headers=headers)
    athlete_profiles = res.json()
    if request.method == 'POST':
        # if request.files.__len__() >= 1:
        #     composite_file = request.files[0]
        # else: #if no files are selected the error is handled here
        #     error = 'No File selected'
        #     return render_template('upload_composite.html', error=error)
        composite_file = request.files['file']
        if composite_file.filename == '':
            error = 'No file selected'
            return render_template('upload_composite.html', error=error, data=data, profiles=athlete_profiles)
        if 'csv' not in composite_file.filename:
            error = 'I only accept CSV files, Try Again ;)'
            return render_template('upload_composite.html', error=error, data=data, profiles=athlete_profiles)

        composite_filename = secure_filename(composite_file.filename)
        composite_file.save(os.path.join('uploads', composite_filename))

        #parser data goes here
        composite_data = pd.read_csv(os.path.join('uploads',composite_filename))


        payload = {
            'player_profile': request.form.get('athlete_profile', ''),
            'risk_area': "1",
            'left_leg_length': float(composite_data['left_leg_length']),
            'right_leg_length': float(composite_data['right_leg_length']),
            'post_medial_direction_rle': float(composite_data['post_medial_direction_rle']),
            'post_medial_direction_lle': float(composite_data['post_medial_direction_lle']),
            'ant_direction_rle': float(composite_data['ant_direction_rle']),
            'ant_direction_lle': float(composite_data['ant_direction_lle']),
            'post_lateral_direction_lle': float(composite_data['post_lateral_direction_lle']),
            'post_lateral_direction_rle': float(composite_data['post_lateral_direction_rle']),
            'composite_score_lle': float(composite_data['composite_score_lle']),
            'composite_score_rle': float(composite_data['composite_score_rle']),
            'assessment': request.form.get('assessment',''),
            'treatment': request.form.get('treatment','')
        }
        res = requests.post('%s/composite/' % API_BASE_URL, data=payload, headers=headers)

        if res.ok:
            return redirect('trainer')
        else:
            print(res.text)
            error = 'Error sending data to the database'


    return render_template('upload_composite.html', profiles=athlete_profiles, data=data, error=error)



@app.route('/playerprofile', methods=['GET', 'POST'])
def playerprofile():
    return render_template('user.html')


if __name__ == '__main__':
    app.run(port='8080', debug=True)
