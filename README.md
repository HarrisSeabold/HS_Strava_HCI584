# User's Guide for Setting Up and Using the HS_Trava Web App

## Introduction
HS_Trava is a web application that allows you to visualize your fitness activities data from Strava in a customizable chart. This guide will walk you through the steps to set up the web app and how to use it to create your own fitness activity chart.

#### Requirements:

_Python 3.x, Flask, Requests, Matplotlib_

_A Strava Account with logged activities_

## Setting up the WebApp

Make sure you have Python 3.x installed on your computer. If you don't have it, download and install it from the official Python website (https://www.python.org/).

Install Flask, Requests, and Matplotlib packages. Open your terminal or command prompt and run the following commands:

> pip install Flask

> pip install requests

> pip install matplotlib

## Preparing the Strava API

In order for HS_Trava to work with your personal data, you will need some key pieces of information from Strava's API:

_Client ID_

_Client Secret_

_Refresh Token_

Follow this tutorial to get each piece of this information from Strava: [https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde]

Then place this information into lines 9, 10, and 11 of App.py


![client info](https://github.com/HarrisSeabold/HS_Trava_HCI584/blob/main/Doc/Client%20Info.PNG))

## Using the App

Run the App.py file and open a web browser

Go to http://127.0.0.1:5000/ to access the landing page of the HS_Trava web app.

### Landing Page
The landing page welcomes you to the HS_Trava web app and showcases its main features. On this page, you'll find the following sections:

![landing page](https://github.com/HarrisSeabold/HS_Trava_HCI584/blob/main/Doc/Landing%20Page.PNG)

**Title:** The title displays the HS_Trava logo and a brief description of the app's purpose.

**Get Started:** Click the "Get Started" button to navigate to the dashboard page where you can start building visualizations of your fitness activities.

### Dashboard Page

The dashboard page is the main application interface of the HS_Trava web app, where you can generate and visualize your fitness activity chart based on different parameters.

![dashboard](https://github.com/HarrisSeabold/HS_Trava_HCI584/blob/main/Doc/Dashboard.PNG)

#### Data Selection:

In the "Dropdown Selector" section, you can customize the data for your fitness activity chart using the following options:
Time Frame: Choose the time frame for which you want to visualize your activity data. Select from "Last 5 Activities," "Last Week," "Last Month," "Year to Date," or "Last Year."
Activity Type: Select the type of activity data you want to include in the chart. Choose between "Running" or "Biking."
Metric: Choose the metric you want to display in the chart. Available options include "Distance," "Elapsed Time," "Kudos Count," "Average Speed," or "Max Speed."
Sum Data: Check this box if you want the chart to display the cumulative sum of the selected metric over time. Leave it unchecked if you want individual data points to represent each activity's metric value.

#### Creating the Visualization:

After selecting your desired data parameters, click the "Create Visualization" button to generate the chart.
The chart will be based on the data you've chosen and will display the selected metric's values over time.
Displaying the Chart:

The chart will appear just below the data selection section.
It will be displayed in a bar chart format, with the x-axis representing the date of each activity, and the y-axis showing the chosen metric's values.
If you selected the "Sum Data" option, the chart will display the cumulative sum of the metric over time. Otherwise, each data point will represent an individual activity's metric value.

#### Saving the Chart:

The generated chart can be downloaded and printed for your records or reference.
To save the chart as an image, right-click on it and choose the "Save Image As" option.
The chart will be saved as an image file on your computer.

## Conclusion
Congratulations! You've successfully set up and used the HS_Trava web app to visualize and analyze your running and cycling data from Strava. You can continue exploring various time frames, activity types, and metrics to gain more valuable insights into your fitness journey. If you have any questions or need further assistance, feel free to reach out to the app's creator. Happy tracking!
