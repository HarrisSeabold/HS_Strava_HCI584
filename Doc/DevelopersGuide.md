# Developer's Guide: HS_Trava Web App

## Overview

HS_Trava is a web application that allows users to visualize their personal running and cycling data obtained from Strava. 
The application provides powerful visualization tools to track progress and performance over time. 
This developer's guide aims to provide an in-depth understanding of the project's structure, code flow, known issues, and potential areas for 
future development.

## Condensed Planning Specs

The current implementation covers the following functionality:
- User authentication with Strava API using OAuth token.
- Data retrieval from Strava's API for activities like running and biking.
- Data analysis to calculate cumulative metrics based on user-selected options.
- Visualization of metrics in a bar chart using Matplotlib.
- Web interface for user interaction and chart creation.

## Install, Deployment, and Admin Issues

Before starting development, ensure you have Python installed (version 3.7 or higher). You also need to install the required packages using pip:

> pip install Flask requests matplotlib

The app can be deployed locally by running the main application file:

`App.py`

Please note that this guide assumes the developer has already read the user's guide and understands how to run the web app locally.

## User Interaction and Code Flow

### User Interaction Flow:

1. The user lands on the homepage and can navigate to the dashboard or login page.
2. On the dashboard, the user selects the time frame, activity type, metric, and sum data options from dropdowns.
3. The user clicks the "Create Visualization" button to generate a chart.
4. The chart is displayed on the dashboard showing the selected metric's progression over time.
5. The user can repeat the process by selecting different options or time frames.

### Code Flow:

1. The main application file is `App.py`.
2. When the user visits the homepage (`/`), the `index()` function in `App.py` renders the `landing.html` template.
3. The user can click on the "dashboard" link to visit the dashboard (`/indexpage`).
4. The `indexpage()` function in `App.py` renders the `index.html` template with an empty chart (`img_tag=""`).
5. When the user selects options and clicks the "Create Visualization" button, the `make_chart()` function in `App.py` is triggered.
6. The selected options are retrieved from the form data.
7. The `data_analysis()` function performs data retrieval and analysis based on the selected options.
8. The Matplotlib library is used to create a bar chart, and the chart is converted to a base64 image.
9. The chart is then displayed on the dashboard (`index.html`) using the `img_tag` variable.

## Known Issues

### Minor:

- No error handling for invalid input or failed API requests. Implement better error handling to enhance user experience.

### Major:

- The Strava access token is currently hardcoded, which is not secure. Implement a more robust token management system.

## Future Work

- Implement user account creation and login system to enhance security and provide personalized experiences.
- Allow users to select and compare multiple metrics in the chart for better data analysis.
- Add interactive features like hovering over data points on the chart to display detailed information.
- Optimize data retrieval and processing algorithms to handle larger datasets efficiently.
- Implement a caching mechanism to reduce API calls and improve performance.
