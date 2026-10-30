import sqlite3
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


categories = {
    "corporate": {
        "name": "Corporate Events",
        "image": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=1200",
        "description": "We specialise in creating professional corporate experiences that bring businesses, teams and clients together. From conferences to product launches, we make every business event successful.",
        "services": [
            {
                "name": "Conference and Seminar Planning",
                "description": "We organise business conferences, seminars and professional meetings, including schedules, speakers and venue arrangements."
            },
            {
                "name": "Budget Management",
                "description": "We plan and manage event expenses carefully to ensure quality experiences within your budget."
            },
            {
                "name": "Sponsorship Coordination",
                "description": "We help identify sponsorship opportunities and coordinate with business partners."
            },
            {
                "name": "Food and Beverage Management",
                "description": "We arrange catering, refreshments and dining experiences for guests and delegates."
            },
            {
                "name": "Event Décor and Production",
                "description": "We manage stage design, lighting, sound systems, branding and event decorations."
            },
            {
                "name": "Guest and Registration Management",
                "description": "We coordinate guest invitations, registrations, welcome desks and event assistance."
            }
        ]
    },

    "non-profit": {
        "name": "Non-Profit Events",
        "image": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=1200",
        "description": "We help charities and non-profit organisations create meaningful events that inspire communities, raise awareness and support important causes.",
        "services": [
            {
                "name": "Fundraising Event Planning",
                "description": "We organise fundraising dinners, charity galas, donation drives and benefit events."
            },
            {
                "name": "Campaign and Awareness Events",
                "description": "We create events that communicate important causes and encourage public participation."
            },
            {
                "name": "Donor and Sponsor Coordination",
                "description": "We coordinate with donors, sponsors and supporting organisations to build strong partnerships."
            },
            {
                "name": "Budget Management",
                "description": "We plan cost-effective events and help organisations make the best use of available funds."
            },
            {
                "name": "Volunteer Management",
                "description": "We organise volunteer schedules, responsibilities and on-site coordination."
            },
            {
                "name": "Event Décor and Catering",
                "description": "We arrange suitable event décor, refreshments and catering for participants."
            }
        ]
    },

    "social": {
        "name": "Social Events",
        "image": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1200",
        "description": "We turn personal celebrations into memorable experiences. From birthdays and anniversaries to private parties, we take care of every detail.",
        "services": [
            {
                "name": "Theme and Concept Development",
                "description": "We create personalised event themes and concepts that match your style and celebration."
            },
            {
                "name": "Venue Selection",
                "description": "We help find the right venue according to your guest list, preferences and budget."
            },
            {
                "name": "Food and Beverage Management",
                "description": "We arrange customised menus, catering services and refreshments for your guests."
            },
            {
                "name": "Décor and Styling",
                "description": "We manage flowers, lighting, table settings, backdrops and decorative details."
            },
            {
                "name": "Entertainment Coordination",
                "description": "We coordinate DJs, music, performers, games and other entertainment activities."
            },
            {
                "name": "Guest Experience Management",
                "description": "We organise invitations, guest arrangements and on-site assistance to make everyone feel welcome."
            }
        ]
    },

    "wedding": {
        "name": "Wedding Events",
        "image": "https://images.unsplash.com/photo-1519741497674-611481863552?w=1200",
        "description": "We bring wedding dreams to life through beautiful planning, thoughtful details and seamless coordination. We make your special day memorable from beginning to end.",
        "services": [
            {
                "name": "Wedding Planning and Coordination",
                "description": "We manage the wedding timeline, ceremonies and arrangements to ensure everything runs smoothly."
            },
            {
                "name": "Venue Selection",
                "description": "We help couples select beautiful venues that match their wedding style and guest requirements."
            },
            {
                "name": "Wedding Décor and Floral Design",
                "description": "We arrange mandap or stage décor, flowers, lighting, table settings and personalised decorations."
            },
            {
                "name": "Catering and Hospitality",
                "description": "We coordinate menus, food services and guest hospitality throughout the celebrations."
            },
            {
                "name": "Photography and Entertainment",
                "description": "We coordinate photographers, videographers, DJs, musicians and wedding entertainment."
            },
            {
                "name": "Guest and Vendor Management",
                "description": "We coordinate guest arrangements, transport, accommodation and wedding suppliers."
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






