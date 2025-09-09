from models import *  
from sqlalchemy import func
import matplotlib
matplotlib.use('Agg')  # Use the Anti-Grain Geometry backend (renders to images only)
import matplotlib.pyplot as plt

import io
import base64

def query_example():
    """
    Returns a list of all schools from the database.
    Each row is a School object.
    """
    schools = School.query.all()  # fetch all records
    return schools

def top_schools_by_enrollment():
    # For latest available year, otherwise filter by specific year
    subquery = (SchoolEnrollment.query
                .with_entities(SchoolEnrollment.year)
                .order_by(SchoolEnrollment.year.desc())
                .limit(1)
                .subquery())
    results = (School.query
        .join(SchoolEnrollment)
        .filter(SchoolEnrollment.year == subquery.c.year)
        .order_by(SchoolEnrollment.enrollment.desc())
        .limit(5)
        .all())
    return results

def most_common_nicknames():
    results = (db.session.query(Nickname.nickname, func.count(School.school_id))
        .join(School)
        .group_by(Nickname.nickname)
        .order_by(func.count(School.school_id).desc())
        .limit(10)
        .all())
    return results

def school_with_most_athletes():
    results = (db.session.query(School, func.count(Athlete.athlete_id).label("athlete_count"))
               .join(Athlete, School.school_id == Athlete.school_id)
               .group_by(School.school_id)
               .order_by(func.count(Athlete.athlete_id).desc())
               .limit(1)
               .all())
    return results

def avg_result_by_event():
    results = (db.session.query(AthleteResult.event, func.avg(AthleteResult.result2))
               .group_by(AthleteResult.event)
               .order_by(func.avg(AthleteResult.result2))
               .all())
    return results

def athlete_gender_distribution():
    results = (db.session.query(Athlete.gender, func.count(Athlete.athlete_id))
               .group_by(Athlete.gender)
               .all())
    return results

def plot_enrollment_by_school(school_id):
    # Query enrollment history for a school
    enrollments = (SchoolEnrollment.query
                   .filter_by(school_id=school_id)
                   .order_by(SchoolEnrollment.year)
                   .all())
    years = [int(e.year) for e in enrollments]
    vals = [e.enrollment for e in enrollments]

    plt.figure()
    plt.plot(years, vals, marker='o')
    plt.title("Enrollment Over Years")
    plt.xlabel("Year")
    plt.ylabel("Enrollment")
    plt.tight_layout()

    # Convert plot to PNG in memory and Base64 encode
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_top_nicknames(n=10):
    # Get most common nicknames
    data = (db.session.query(School.nickname, func.count(School.school_id))
            .group_by(School.nickname)
            .order_by(func.count(School.school_id).desc())
            .limit(n)
            .all())
    names = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure(figsize=(8,6))
    plt.bar(names, counts, color='skyblue')
    plt.title(f"Top {n} School Nicknames")
    plt.xlabel("Nickname")
    plt.ylabel("Number of Schools")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_athlete_gender_pie():
    data = (db.session.query(Athlete.gender, func.count(Athlete.athlete_id))
            .group_by(Athlete.gender)
            .all())
    labels = [row[0] or "Unknown" for row in data]
    sizes = [row[1] for row in data]

    plt.figure(figsize=(5,5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Athlete Gender Distribution")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_avg_house_value_by_zip(top_n=10):
    # Join to get zip, get latest year per zip, and avg_value
    subq = db.session.query(
        HouseValues.zip,
        func.max(HouseValues.year).label('max_year')
    ).group_by(HouseValues.zip).subquery()

    result = (db.session.query(
        HouseValues.zip,
        HouseValues.avg_value
    )
    .join(subq, (HouseValues.zip == subq.c.zip) & (HouseValues.year == subq.c.max_year))
    .order_by(HouseValues.avg_value.desc())
    .limit(top_n)
    .all())
    zips = [str(z[0]) for z in result]
    values = [z[1] for z in result]

    plt.figure(figsize=(8,5))
    plt.bar(zips, values, color='#4756ff')
    plt.xlabel("ZIP Code")
    plt.ylabel("Average House Value ($)")
    plt.title(f"Top {top_n} ZIP Codes by Avg. House Value")
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_school_type_distribution():
    from models import School, SchoolType
    type_counts = db.session.query(
        School.school_type, func.count(School.school_id)
    ).group_by(School.school_type).all()
    labels = [t[0] or "Unknown" for t in type_counts]
    sizes = [t[1] for t in type_counts]
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=120)
    plt.title("School Type Distribution")
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_top_events_by_participation(top_n=10):
    from models import AthleteResult
    event_data = db.session.query(
        AthleteResult.event, func.count(AthleteResult.athlete_id)
    ).group_by(AthleteResult.event)\
     .order_by(func.count(AthleteResult.athlete_id).desc()).limit(top_n).all()
    events = [e[0] for e in event_data]
    counts = [e[1] for e in event_data]
    plt.figure(figsize=(9,6))
    plt.barh(events[::-1], counts[::-1], color='#304bfc')
    plt.ylabel("Event")
    plt.xlabel("Number of Results")
    plt.title(f"Top {top_n} Events by Athlete Participation")
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')
