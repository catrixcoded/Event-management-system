import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "eventease-development-key")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ChangeThisPassword123!")



categories = {
    "corporate": {
        "name": "Corporate Events",
        "description": "Professional events designed to connect people, build relationships and create business opportunities.",
        "image": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=1200",
        "services": [
            {
                "name": "Conference and Seminar Planning",
                "description": "Planning and organising professional conferences, seminars and business meetings."
            },
            {
                "name": "Budget Management",
                "description": "Managing event expenses and ensuring efficient use of resources."
            },
            {
                "name": "Sponsorship Coordination",
                "description": "Connecting with sponsors and managing sponsorship arrangements."
            },
            {
                "name": "Food and Beverage Management",
                "description": "Arranging refreshments, catering and dining experiences for guests."
            },
            {
                "name": "Event Décor and Production",
                "description": "Creating professional event settings with suitable décor, lighting and sound."
            },
            {
                "name": "Guest and Registration Management",
                "description": "Handling guest invitations, registrations and event check-ins."
            }
        ]
    },

    "social": {
        "name": "Social Events",
        "description": "Special celebrations that bring friends, families and communities together.",
        "image": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=1200",
        "services": [
            {
                "name": "Theme and Concept Development",
                "description": "Creating unique themes and concepts based on the occasion."
            },
            {
                "name": "Venue Selection",
                "description": "Finding suitable venues that match the event requirements."
            },
            {
                "name": "Food and Beverage Management",
                "description": "Organising catering and refreshments for guests."
            },
            {
                "name": "Décor and Styling",
                "description": "Designing attractive event spaces with creative decorations."
            },
            {
                "name": "Entertainment Coordination",
                "description": "Arranging music, performances and entertainment activities."
            },
            {
                "name": "Guest Experience Management",
                "description": "Making sure guests enjoy a comfortable and memorable experience."
            }
        ]
    },

    "wedding": {
        "name": "Wedding Events",
        "description": "Beautifully planned wedding celebrations that turn special moments into lasting memories.",
        "image": "https://images.unsplash.com/photo-1519741497674-611481863552?w=1200",
        "services": [
            {
                "name": "Wedding Planning and Coordination",
                "description": "Managing wedding preparations and coordinating the celebrations."
            },
            {
                "name": "Venue Selection",
                "description": "Finding the perfect location for the wedding ceremony and reception."
            },
            {
                "name": "Wedding Décor and Floral Design",
                "description": "Creating elegant decorations and floral arrangements."
            },
            {
                "name": "Catering and Hospitality",
                "description": "Arranging food, beverages and hospitality services."
            },
            {
                "name": "Photography and Entertainment",
                "description": "Coordinating photography, music and entertainment."
            },
            {
                "name": "Guest and Vendor Management",
                "description": "Coordinating guests and working with wedding service providers."
            }
        ]
    },

    "exhibitions": {
        "name": "Exhibitions",
        "description": "Immersive and creative experiences that bring art, culture, ideas and innovation to life.",
        "image": "https://images.unsplash.com/photo-1577083552431-6e5fd01aa342?w=1200",
        "services": [
            {
                "name": "Exhibition Planning",
                "description": "Planning exhibition concepts, schedules and visitor experiences."
            },
            {
                "name": "Art and Display Arrangements",
                "description": "Organising artwork, installations and exhibition displays."
            },
            {
                "name": "Venue and Space Management",
                "description": "Selecting and arranging spaces for exhibitions and installations."
            },
            {
                "name": "Lighting and Visual Design",
                "description": "Creating engaging displays through lighting and visual effects."
            },
            {
                "name": "Visitor Management",
                "description": "Managing visitor registrations, entry and movement throughout the exhibition."
            },
            {
                "name": "Promotion and Coordination",
                "description": "Promoting exhibitions and coordinating artists, exhibitors and partners."
            }
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


def create_contact_table():
    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_date TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_contact_table()


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    event_type = request.form.get("event_type", "").strip()
    event_date = request.form.get("event_date", "").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, phone, event_type, event_date, message]):
        return "Please fill in all the fields.", 400

    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO enquiries
        (name, email, phone, event_type, event_date, message)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, phone, event_type, event_date, message))

    connection.commit()
    connection.close()

    return redirect(url_for("home") + "?submitted=1#contact")

if __name__ == "__main__":
    app.run(debug=True)






