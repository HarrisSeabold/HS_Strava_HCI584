from flask import Flask, render_template, request, session
import requests
import urllib3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Strava API credentials
id = 109422
secret = '1a1a3857c3f11f0da887e4bc5064162ecf575246'
refresh = '918b3db21b495d1aaddeb81147d444d8718a5c23'

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'SECRET_SAUCE'

@app.route('/')
def index():
    """Route for the landing page."""
    return render_template('landing.html')

@app.route('/indexpage')
def indexpage():
    """Route for the main dashboard page."""
    return render_template('index.html', img_tag="")

def data_analysis(timeframe="last_month", data_type="run", metric="distance", sum_activities = 0):
    """
    Analyzes Strava data based on selected parameters.

    Parameters:
        timeframe (str): The time frame to filter activities.
        data_type (str): The type of activity (run or bike).
        metric (str): The metric to calculate (kudos, distance, time, average speed, max speed).
        sum_activities (int): Whether to sum the selected metric cumulatively or not (0 or 1).

    Returns:
        activity_data_list (list): List of dictionaries containing activity data for visualization.
    """

    # Strava API URLs
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

    # Filter activities based on the selected data type
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
 
    # Reverse the activity list for chart formatting
    filtered_activities = filtered_activities[::-1]

    # Calculate the total of the selected metric
    cumulative_sum_list = []
    cumulative_sum = 0
    activity_data_list = []

    for activity in filtered_activities:
        # Create a dictionary to store activity data
        activity_data = {}  

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

        # Store the selected metric in the session for later use
        session['metric'] = metric 

        # Don't sum speed metrics
        if sum_activities == 0 or metric == "average speed" or metric == "max speed":
            cumulative_sum_list.append(activity_metric)
        else:
            cumulative_sum += activity_metric
            cumulative_sum_list.append(cumulative_sum)

        # Add activity data to the dictionary
        activity_data['name'] = activity['name']
        activity_data['date'] = datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')

        # Store the last cumulative sum        
        activity_data['cumulative_sum'] = cumulative_sum_list[-1] 

        # Append the activity data dictionary to the list
        activity_data_list.append(activity_data)

    # Reverse the activity_data_list back to its original order
    activity_data_list = activity_data_list[::-1]

    return activity_data_list

@app.route('/make_chart', methods=['POST'])
def make_chart():
    """
    Generates and renders a chart based on user input.

    Returns:
        Rendered template with the generated chart.
    """

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
    fig, ax = plt.subplots(figsize=(15, 4))
    plt.bar(dates, metrics)
    plt.xlabel('Date')
    plt.ylabel('Metrics')  # this should be the correct unit for the current metric ...
    plt.title(session['metric'] + ' Over Time')
    plt.xticks(rotation=-90)
    plt.tight_layout()
    
    # convert figure into a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    data = buffer.getvalue()

    image_buffer = base64.b64encode(data).decode('utf-8')
    img_tag = f'<img src="data:image/png;base64,{image_buffer}"/>'

    # inline the image tag
    return render_template('index.html', img_tag=img_tag)

if __name__ == '__main__':
    app.run(port=5000)