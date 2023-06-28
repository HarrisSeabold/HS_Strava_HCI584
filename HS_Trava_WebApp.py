from flask import Flask, render_template, request
import requests
import urllib3
import os
import matplotlib.pyplot as plt
import io
import base64
from werkzeug.utils import secure_filename

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


@app.route('/demodata_process', methods=['POST'])

def demodata_process():
    uploaded_file = request.files['fileupload']
    
    if uploaded_file.filename != '':
        # Save the uploaded file with a secure filename
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join('uploads', filename))

        with open(uploaded_file.filename, 'r') as file:
            file_content = file.read()
            
            # Perform your analysis on the file content
            # You can process the text, extract information, perform calculations, etc.
            
            line_count = file_content.count('\n') + 1
            
            x = ['Line Count']
            y = [line_count]
            plt.bar(x, y)
            
            # Convert the plot to an image
            image = io.BytesIO()
            plt.savefig(image, format='png')
            image.seek(0)
            plot_url = base64.b64encode(image.getvalue()).decode()
        
        # Delete the uploaded file
        os.remove(uploaded_file.filename)
        
        return render_template('demodata_results.html', plot_url=plot_url)
    else:
        return 'No file selected!'


if __name__ == '__main__':
    app.run(port=5000)