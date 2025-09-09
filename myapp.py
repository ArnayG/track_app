from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import Config

from models import db, School

# Import all query/plotting functions from queries.py
from queries import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/query1")
    def query1():
        results = query_example()
        return render_template("query1.html", results=results)

    @app.route("/top_schools_by_enrollment")
    def top_schools_by_enrollment_route():
        results = top_schools_by_enrollment()
        return render_template("top_schools_by_enrollment.html", results=results)

    @app.route("/most_common_nicknames")
    def most_common_nicknames_route():
        results = most_common_nicknames()
        return render_template("most_common_nicknames.html", results=results)

    @app.route("/school_with_most_athletes")
    def school_with_most_athletes_route():
        results = school_with_most_athletes()
        return render_template("school_with_most_athletes.html", results=results)

    @app.route("/avg_result_by_event")
    def avg_result_by_event_route():
        results = avg_result_by_event()
        return render_template("avg_result_by_event.html", results=results)

    @app.route("/athlete_gender_distribution")
    def athlete_gender_distribution_route():
        results = athlete_gender_distribution()
        return render_template("athlete_gender_distribution.html", results=results)

    # --- Plotting Routes ---

    @app.route("/plot/enrollment")
    def plot_enrollment():
        school_id = request.args.get("school_id", None)
        if school_id is None:
            # Default: pick the first school for demonstration
            school = School.query.first()
            school_id = school.school_id if school else None

        plot_data = plot_enrollment_by_school(school_id) if school_id else None
        return render_template("plot_enrollment.html", plot_data=plot_data)

    @app.route("/plot/nicknames")
    def plot_nicknames():
        plot_data = plot_top_nicknames()
        return render_template("plot_nicknames.html", plot_data=plot_data)

    @app.route("/plot/gender")
    def plot_gender():
        plot_data = plot_athlete_gender_pie()
        return render_template("plot_gender.html", plot_data=plot_data)

    @app.route("/plot/house_values")
    def plot_house_values():
        plot_data = plot_avg_house_value_by_zip()
        return render_template("plot_house_values.html", plot_data=plot_data)

    @app.route("/plot/school_type")
    def plot_school_type():
        plot_data = plot_school_type_distribution()
        return render_template("plot_school_type.html", plot_data=plot_data)

    @app.route("/plot/top_events")
    def plot_top_events():
        plot_data = plot_top_events_by_participation()
        return render_template("plot_top_events.html", plot_data=plot_data)
if __name__ == "__main__":
    app.run(debug=True)
