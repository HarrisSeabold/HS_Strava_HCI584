from flask import Flask, render_template, request #, session
import requests
import urllib3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

id = 109422
secret = '1a1a3857c3f11f0da887e4bc5064162ecf575246'
refresh = '918b3db21b495d1aaddeb81147d444d8718a5c23'

app = Flask(__name__)

# app.secret_key = 'SECRET_SAUCE'

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/indexpage')
def indexpage():\
    return render_template('index.html')

def data_analysis(timeframe="last_month", data_type="run", metric="distance", sum_activities = 0):
    
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

    if data_type == "run":
        filtered_activities = [activity for activity in my_dataset if activity['type'] == 'Run']
    elif data_type == "bike":
        filtered_activities = [activity for activity in my_dataset if activity['type'] == 'Ride']
    else:
        filtered_activities = [activity for activity in my_dataset if activity['type'] == 'Run']
        pass

    # Filter activities based on the selected timeframe
    if timeframe == "last_year":
        start_date = datetime.now() - timedelta(days=365)
    elif timeframe == "ytd":
        start_date = datetime(datetime.now().year, 1, 1)
    elif timeframe == "last_month":
        start_date = datetime.now() - timedelta(days=30)
    elif timeframe == "last_week":
        start_date = datetime.now() - timedelta(days=7)        
    else:
        # Default to last month
        start_date = datetime.now() - timedelta(days=30)

    if timeframe == "last_5":
        filtered_activities = [filtered_activities[0],filtered_activities[1],filtered_activities[2],filtered_activities[3],filtered_activities[4]]
    else:
        filtered_activities = [activity for activity in my_dataset if datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ') > start_date]

    filtered_activities = filtered_activities[::-1]

    # Calculate the total of the selected metric in the reverse direction
    cumulative_sum_list = []
    cumulative_sum = 0
    activity_data_list = []

    for activity in filtered_activities:
        activity_data = {}  # Create a dictionary to store activity data

        if metric == "kudos":
            activity_metric = activity['kudos_count']
        elif metric == "distance":
            activity_metric = activity['distance']
        elif metric == "time":
            activity_metric = activity['moving_time']
        elif metric == "average speed":
            activity_metric = activity['average_speed']
        elif metric == "max speed":
            activity_metric = activity['max_speed']
        else:
            # Default to kudos
            activity_metric = activity['kudos_count']

        # Don't sum speed metrics
        if sum_activities == 0 or metric == "average speed" or metric == "max speed":
            cumulative_sum_list.append(activity_metric)
        else:
            cumulative_sum += activity_metric
            cumulative_sum_list.append(cumulative_sum)

        # Add activity data to the dictionary
        activity_data['name'] = activity['name']
        activity_data['date'] = datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')        
        activity_data['cumulative_sum'] = cumulative_sum_list[-1]  # Store the last cumulative sum
        # Append the activity data dictionary to the list
        activity_data_list.append(activity_data)

    # Reverse the activity_data_list back to its original order
    activity_data_list = activity_data_list[::-1]

    return activity_data_list

@app.route('/make_chart', methods=['POST'])
def make_chart():
    data = request.form
    metric = data.get('metric', 'distance')
    data_type = data.get('activity_type', 'run')
    timeframe = data.get('timeframe', 'last_month')
    sum_activities = int(data.get('activity_sum', 0))

    data = data_analysis(timeframe, data_type, metric, sum_activities)
    data = data[::-1]

    metrics = [activity['cumulative_sum'] for activity in data]
    dates = [activity['date'] for activity in data]

    # Create the chart using Matplotlib
    plt.bar(dates, metrics)
    plt.xlabel('Date')
    plt.ylabel('Metrics')
    plt.title('Metrics Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the chart in a separate window
    plt.show()

    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)