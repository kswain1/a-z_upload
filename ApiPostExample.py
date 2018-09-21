import requests 


#getting data from athletes api
r = requests.get("https://a-zapi.herokuapp.com/api/profile/2")
print(r.text)

r = requests.get("https://a-zapi.herokuapp.com/api/profile")
print(r.status_code, "if data was a success via python code")


login = {"username":"kehlin@xplosionlive.com",
			"password":"Awesome1"}
b = requests.post("https://a-zapi.herokuapp.com/login/",data=login)
print(b.text)

headers = dict(Authorization="token d3fd16e25de98308c111af5013faf465bce4e494")

 c = requests.post("https://a-zapi.herokuapp.com/medsession/", data=payload, headers=header)

 "user_age": 12,
 "tib_anterior_lle": "sdfksdfs",
 "tib_anterior_rle": "asdfsadfsa",
 "peroneals_rle": "adfdsaf",
 "peroneals_lle": "sfsfsdfs",
 "med_gastro_rle": "fasdfds",
 "med_gastro_lle": "fsfsf",
 "lat_gastro_rle": "sadfsdf",
 "lat_gastro_lle": "fsafdsaf",
 "created_on": "2018-09-21T21:38:00.340890Z",
 "assessment": "asfdsfs",
 "treatment": "sfsafsfsd"