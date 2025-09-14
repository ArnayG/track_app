from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Make sure these exist somewhere above:
SCHOOLS = [
    {"id": 1, "name": "Park Tudor"},
    {"id": 2, "name": "Carmel High School"},
    {"id": 3, "name": "North Central High School"},
    {"id": 4, "name": "Brebeuf"},
    {"id": 5, "name": "Franklin Central"},
    {"id": 6, "name": "Lawrence Central"},
]

ATHLETES = [
    # Park Tudor (1)
    {"id": 100, "name": "Anna Liu", "gender": "female", "school_id": 1},
    {"id": 101, "name": "Ben Smith", "gender": "male", "school_id": 1},
    {"id": 102, "name": "Chris Young", "gender": "male", "school_id": 1},
    {"id": 103, "name": "Daisy Chen", "gender": "female", "school_id": 1},
    {"id": 104, "name": "Eva Kumar", "gender": "female", "school_id": 1},
    {"id": 105, "name": "Finn Kelly", "gender": "male", "school_id": 1},
    {"id": 106, "name": "Grace Lee", "gender": "female", "school_id": 1},

    # Carmel High School (2)
    {"id": 110, "name": "Henry Ford", "gender": "male", "school_id": 2},
    {"id": 111, "name": "Ivy Tran", "gender": "female", "school_id": 2},
    {"id": 112, "name": "Jack Wang", "gender": "male", "school_id": 2},
    {"id": 113, "name": "Katie O'Brien", "gender": "female", "school_id": 2},
    {"id": 114, "name": "Liam Patel", "gender": "male", "school_id": 2},
    {"id": 115, "name": "Maya Das", "gender": "female", "school_id": 2},
    {"id": 116, "name": "Noah Brown", "gender": "male", "school_id": 2},

    # North Central High School (3)
    {"id": 120, "name": "Olivia Hall", "gender": "female", "school_id": 3},
    {"id": 121, "name": "Paul Kim", "gender": "male", "school_id": 3},
    {"id": 122, "name": "Quinn Li", "gender": "female", "school_id": 3},
    {"id": 123, "name": "Rachel Green", "gender": "female", "school_id": 3},
    {"id": 124, "name": "Sam Parker", "gender": "male", "school_id": 3},
    {"id": 125, "name": "Tina White", "gender": "female", "school_id": 3},
    {"id": 126, "name": "Uriel Johnson", "gender": "male", "school_id": 3},

    # Brebeuf (4)
    {"id": 130, "name": "Vera Zhou", "gender": "female", "school_id": 4},
    {"id": 131, "name": "Will Evans", "gender": "male", "school_id": 4},
    {"id": 132, "name": "Xena Miller", "gender": "female", "school_id": 4},
    {"id": 133, "name": "Yifan Sun", "gender": "male", "school_id": 4},
    {"id": 134, "name": "Zane Harris", "gender": "male", "school_id": 4},
    {"id": 135, "name": "Abby Jacobs", "gender": "female", "school_id": 4},
    {"id": 136, "name": "Brian Cruz", "gender": "male", "school_id": 4},

    # Franklin Central (5)
    {"id": 140, "name": "Cara Zhang", "gender": "female", "school_id": 5},
    {"id": 141, "name": "David Lopez", "gender": "male", "school_id": 5},
    {"id": 142, "name": "Ella Moore", "gender": "female", "school_id": 5},
    {"id": 143, "name": "Felix Turner", "gender": "male", "school_id": 5},
    {"id": 144, "name": "Gina Thomas", "gender": "female", "school_id": 5},
    {"id": 145, "name": "Howard Brown", "gender": "male", "school_id": 5},
    {"id": 146, "name": "Irene Wu", "gender": "female", "school_id": 5},

    # Lawrence Central (6)
    {"id": 150, "name": "Jason Lee", "gender": "male", "school_id": 6},
    {"id": 151, "name": "Kayla Grant", "gender": "female", "school_id": 6},
    {"id": 152, "name": "Lucas Brown", "gender": "male", "school_id": 6},
    {"id": 153, "name": "Maddie Song", "gender": "female", "school_id": 6},
    {"id": 154, "name": "Nick Porter", "gender": "male", "school_id": 6},
    {"id": 155, "name": "Olga Guzman", "gender": "female", "school_id": 6},
    {"id": 156, "name": "Peter Drew", "gender": "male", "school_id": 6},
]

SCHOOL_BY_ID = {s["id"]: s["name"] for s in SCHOOLS}


@app.route("/", methods=["GET"])
def index():
    return render_template("search.html")

@app.route("/api/search", methods=["GET"])
def api_search():
    q = request.args.get("q", "", type=str).strip().lower()
    all_flag = request.args.get("all") == "1"

    rows = [
        {
            "id": a["id"],
            "name": a["name"],
            "gender": a["gender"],
            "school": SCHOOL_BY_ID.get(a["school_id"], ""),
        }
        for a in ATHLETES
    ]

    if all_flag or not q:
        rows.sort(key=lambda r: r["name"])      # <<< Sort by athlete name
        return jsonify(rows[:100])

    filtered = [r for r in rows if q in r["name"].lower() or q in r["school"].lower()]
    filtered.sort(key=lambda r: r["name"])      # <<< Sort by athlete name
    return jsonify(filtered[:100])


@app.route("/athlete/<int:athlete_id>", methods=["GET"])
def athlete_profile(athlete_id):
    # Find athlete and their school
    athlete = next((a for a in ATHLETES if a["id"] == athlete_id), None)
    if not athlete:
        return "Athlete not found", 404
    school = SCHOOL_BY_ID.get(athlete["school_id"], "Unknown School")
    return render_template(
        "athlete.html",
        name=athlete["name"],
        gender=athlete["gender"],
        school=school,
    )

if __name__ == "__main__":
    app.run(debug=True)
