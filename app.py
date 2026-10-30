
from flask import Flask, render_template, request

app = Flask(__name__)

categories = {
    "corporate": {
        "name": "Corporate Events",
        "image": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=1200",
        "description": "We create professional corporate experiences, from business conferences and product launches to networking events and company celebrations.",
        "services": [
            "Budget Management",
            "Sponsorship Coordination",
            "Food and Beverage Management",
            "Event Décor and Production",
            "Venue Selection and Management",
            "Guest and Registration Management"
        ]
    },

    "non-profit": {
        "name": "Non-Profit Events",
        "image": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=1200",
        "description": "We help non-profit organisations create meaningful events that bring people together, raise awareness and support important causes.",
        "services": [
            "Fundraising Event Planning",
            "Budget Management",
            "Sponsorship Coordination",
            "Food and Beverage Management",
            "Event Décor and Production",
            "Volunteer and Guest Coordination"
        ]
    },

    "social": {
        "name": "Social Events",
        "image": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1200",
        "description": "From birthdays and private parties to special celebrations, we make every social gathering memorable and enjoyable.",
        "services": [
            "Theme and Concept Planning",
            "Budget Management",
            "Food and Beverage Management",
            "Event Décor and Production",
            "Entertainment Coordination",
            "Venue and Guest Management"
        ]
    },

    "wedding": {
        "name": "Wedding Events",
        "image": "https://images.unsplash.com/photo-1519741497674-611481863552?w=1200",
        "description": "We bring wedding dreams to life with thoughtful planning, beautiful décor and seamless coordination of every special moment.",
        "services": [
            "Wedding Budget Management",
            "Venue Selection",
            "Food and Beverage Management",
            "Wedding Décor and Production",
            "Photography and Entertainment Coordination",
            "Guest and Vendor Management"
        ]
    }
}


@app.route("/")
def home():
    return render_template("index.html", categories=categories)


@app.route("/events")
def events():
    selected = request.args.get("category", "corporate")

    if selected not in categories:
        selected = "corporate"

    return render_template(
        "events.html",
        categories=categories,
        selected=selected,
        event=categories[selected]
    )


if __name__ == "__main__":
    app.run(debug=True)






