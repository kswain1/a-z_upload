import requests 


#getting data from athletes api
r = requests.get("https://a-zapi.herokuapp.com/api/profile/2")
print(r.text)

r = requests.get("https://a-zapi.herokuapp.com/api/profile")
print(r.status_code, "if data was a success via python code")

#create login form
login = {"username":"kehlin@xplosionlive.com",
			"password":"Awesome1"}
b = requests.post("https://a-zapi.herokuapp.com/login/",data=login)
print(b.text)
token = b.json()['token']
token = "Token " + token


#create player form
header_two = dict(Authorization =token)
player_name = "Zack Cross"
team_name = "University of Miami"
user_age = 18
payload_player = {'player_name':player_name, 'team_name':team_name,'user_age':user_age}
d = requests.post("https://a-zapi.herokuapp.com/player", data=payload_player, headers=header_two)
print(d.status_code)



#Create Session Form
header = dict(Authorization="Token d3fd16e25de98308c111af5013faf465bce4e494")
payload_2 = {'player_profile': 4, 'peroneals_rle':None,'peroneals_lle':None,'med_gasto_rle':None,
             'med_gastro_lle':None, 'tib_anterior_lle':None,'tib_anterior_rle':None, 'lat_gastro_lle':None,
              'lat_gastro_rle':None, 'assessment':None, 'treatment':None }

c = requests.post("https://a-zapi.herokuapp.com/session/", data=payload_2, headers=header)
print(c.status_code)
print (c.content)


 # "user_age": 12,
 # "tib_anterior_lle": "sdfksdfs",
 # "tib_anterior_rle": "asdfsadfsa",
 # "peroneals_rle": "adfdsaf",
 # "peroneals_lle": "sfsfsdfs",
 # "med_gastro_rle": "fasdfds",
 # "med_gastro_lle": "fsfsf",
 # "lat_gastro_rle": "sadfsdf",
 # "lat_gastro_lle": "fsafdsaf",
 # "created_on": "2018-09-21T21:38:00.340890Z",
 # "assessment": "asfdsfs",
 # "treatment": "sfsafsfsd"