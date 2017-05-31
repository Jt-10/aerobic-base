from . import app, db
from .database import Activity, Athlete

##############################################################
# Tools for Strava Oauth2 authentication and API interaction #
##############################################################
from stravalib import Client
from flask import request
import datetime
from env.config import oauth_credentials

###########################
# Tools for visualization #
###########################
import matplotlib.pyplot as plt
from flask import make_response
from io import BytesIO


client = Client() # stravalib object--documentation available at http://pythonhosted.org/stravalib/

@app.route('/')
# Consider using uuid4 to generate random string for optional state parameter that can be saved
# to prevent xsrf attacks
# Use stravalib module to create an instance of the Client model and generate authorization url
def homepage():
    """Generate and display authorization URL."""

    authorization_url = client.authorization_url(client_id=oauth_credentials["CLIENT_ID"],
                                                 redirect_uri=oauth_credentials["REDIRECT_URI"]
                                                 )

    return "<center>" \
           "<p>Welcome to <b>AerobicBase!</b><br/><br/>" \
           "Visualizing your improvement in aerobic conditioning over time<br/>" \
           "using the public activities from your Strava account.<br/><br/>" \
           "<b>*** Under Construction ***</b><br/><br/>" \
           "<a href={}><img src='static/img/btn_strava_connectwith_light.png'></a><br/><br/>" \
           "<a><img src='static/img/api_logo_pwrdBy_strava_stack_gray.png'></a></p>" \
           "</center>".format(authorization_url)


@app.route("/redirect")
def access_token_and_database():
    """Check user authorization, get temporary authorization code, exchange code for token,
    and manage database."""

    # If user authorizes, "code" will be included in query string
    # If user denies, error message "access_denied" will be included in query string

    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    code = request.args.get("code")
    access_token = client.exchange_code_for_token(client_id=oauth_credentials["CLIENT_ID"],
                                                  client_secret=oauth_credentials["CLIENT_SECRET"],
                                                  code=code)
    authenticated_athlete = Client(access_token=access_token)

    # Get authenticated athlete firstname (http://strava.github.io/api/v3/athlete/).
    name = authenticated_athlete.get_athlete().firstname

    # Check whether authenticated_athlete already exists in database. If true, delete activities.
    # If false, add athlete.
    athlete_in_database = Athlete.query.filter_by(access_token=access_token).first()
    if athlete_in_database:
        activities_to_delete = Activity.query.filter_by(athlete_id=athlete_in_database.id)
        for activity in activities_to_delete:
            db.session.delete(activity)
        db.session.commit()
    else:
        athlete_in_database = Athlete(access_token=access_token,
                                      name=name,
                                      activities=[])
        db.session.add(athlete_in_database)
        db.session.commit()

    ######################################################################
    # Get authenticated athlete list of activities and store to database #
    ######################################################################

    # Define variable for the last year of activities
    one_year_ago = datetime.datetime.utcnow() - datetime.timedelta(days=365)

    activities = authenticated_athlete.get_activities(after=one_year_ago)
    for activity in activities:
        if activity.has_heartrate and activity.average_speed.num > 0:
            value = (activity.average_speed / activity.average_heartrate)
            # Stravalib is returning Activity classes that work with units, requiring ".num" for some
            entry = Activity(distance = activity.distance.num,
                             moving_time = activity.moving_time,
                             total_elevation_gain = activity.total_elevation_gain.num,
                             type = activity.type,
                             start_date = activity.start_date, # Column = 4
                             start_date_local = activity.start_date_local,
                             average_speed = activity.average_speed.num,
                             average_heartrate = activity.average_heartrate,
                             aerobic_value = value.num, # Column = 8
                             athlete_id=athlete_in_database.id)
            db.session.add(entry)
        db.session.commit()

    message = "<center>" \
              "<p>Hello, {}. Thank you for authorizing with Strava.<br/><br/>"\
              "<a href=http://localhost:8080/visualization.png>" \
              "Ready to analyze your activities?</a><br/><br/>" \
              "<a><img src='static/img/api_logo_pwrdBy_strava_stack_gray.png'></a></p>" \
              "</center>".format(name)

    return message


@app.route("/visualization.png")
def display_visualization():
    """Display a visualization of the activities stored to the database."""
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    dates = Activity.query.with_entities(Activity.start_date).all()
    aerobic_values = Activity.query.with_entities(Activity.aerobic_value).all()

    try:
        fig = Figure()
        ax=fig.add_subplot(111)
        ax.plot_date(dates, aerobic_values, "-")
        ax.xaxis.set_major_formatter(DateFormatter('%m-%d-%Y'))
        fig.autofmt_xdate()
        ax.xlabel("Date")
        ax.ylabel("Aerobic Value = AvgSpeed/AvgHR")
        canvas = FigureCanvas(fig)
        png_output = BytesIO()
        canvas.print_png(png_output)
        response = make_response(png_output.getvalue())
        response.headers["Content-Type"] = "image/png"
        return response

    except:
        return "{} {}".format(dates, aerobic_values)

@app.route("/logout")
def logout():
    pass