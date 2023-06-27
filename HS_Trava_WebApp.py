from flask import Flask, render_template, request
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])

def process():
    clientid = request.form.get('strava_id')
    clientrefresh = request.form.get('strava_refresh')
    clientsecret = request.form.get('strava_secret')

    auth_url = "https://www.strava.com/oauth/token"
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    payload = {
        'client_id': clientid,
        'client_secret': clientsecret,
        'refresh_token': clientrefresh,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))

    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(activites_url, headers=header, params=param).json()

    print(my_dataset[0]["name"])
    print(my_dataset[0]["map"]["summary_polyline"])

    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(port=5000)