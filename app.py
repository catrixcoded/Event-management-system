
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to database
def connect_db():
    return sqlite3.connect("events.db")


# Create database tables
def create_table():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            venue TEXT,
            price TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            event_name TEXT
        )
    """)

    cur.execute("SELECT COUNT(*) FROM events")

    if cur.fetchone()[0] == 0:
        sample_events = [
            ("Music Festival", "2026-12-15", "Delhi", "500"),
            ("Tech Workshop", "2026-12-20", "Gurugram", "300"),
            ("College Fest", "2027-01-10", "Sonipat", "200")
        ]

        cur.executemany(
            "INSERT INTO events (name, date, venue, price) VALUES (?, ?, ?, ?)",
            sample_events
        )

    con.commit()
    con.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Events page
@app.route("/events")
def events():
    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM events")
    all_events = cur.fetchall()

    con.close()

    return render_template("events.html", events=all_events)


# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        event_name = request.form["event_name"]

        con = connect_db()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO registrations (name, email, event_name) VALUES (?, ?, ?)",
            (name, email, event_name)
        )

        con.commit()
        con.close()

        return """
        <h1>Registration Successful!</h1>
        <p>Thank you for registering for the event.</p>
        <a href='/'>Go to Home Page</a>
        """

    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT name FROM events")
    event_list = cur.fetchall()
    con.close()

    return render_template("register.html", events=event_list)


# Admin dashboard
@app.route("/admin")
def admin():
    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM registrations")
    registrations = cur.fetchall()

    con.close()

    return render_template(
        "admin.html",
        registrations=registrations
    )


# Add a new event
@app.route("/add_event", methods=["POST"])
def add_event():
    name = request.form["name"]
    date = request.form["date"]
    venue = request.form["venue"]
    price = request.form["price"]

    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO events (name, date, venue, price) VALUES (?, ?, ?, ?)",
        (name, date, venue, price)
    )

    con.commit()
    con.close()

    return redirect(url_for("events"))


# Run website
create_table()

if __name__ == "__main__":
    app.run(debug=True)
