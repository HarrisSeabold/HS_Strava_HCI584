from flask import Flask, render_template, request
import requests
import urllib3
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

id = 109422
secret = '1a1a3857c3f11f0da887e4bc5064162ecf575246'
refresh = '918b3db21b495d1aaddeb81147d444d8718a5c23'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_chart', methods=['POST'])
def make_chart():
    
    auth_url = "https://www.strava.com/oauth/token"
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    
    payload = {
        'client_id': id,
        'client_secret': secret,
        'refresh_token': refresh,
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

    index1 = int(request.form.get('index1'))
    activity1 = my_dataset[index1]
    index2 = int(request.form.get('index2'))
    activity2 = my_dataset[index2]
    metric = request.form.get('metric')

    name1 = activity1.get('name', 'N/A')
    metric1 = activity1.get(metric, 'N/A')

    name2 = activity2.get('name', 'N/A')
    metric2 = activity2.get(metric, 'N/A')


    metric_label = metric

    activities = [name1, name2]
    metrics = [metric1, metric2]

    plt.bar(activities, metrics)
    plt.xlabel('Activity')
    plt.ylabel(metric_label)
    plt.title('Comparison of Metrics')
    plt.show()

    return f"Activity 1: {name1}, {metric}: {metric1} | Activity 2: {name2}, {metric}: {metric2}"

if __name__ == '__main__':
    app.run(port=5000)