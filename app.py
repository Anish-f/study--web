from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

PRICE_PER_HOUR = 1000

def init_db():
    conn = sqlite3.connect("study.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS study (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            hours REAL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("study.db")
    c = conn.cursor()

    if request.method == "POST":
        date = request.form["date"]
        hours = float(request.form["hours"])
        c.execute("INSERT INTO study (date, hours) VALUES (?, ?)", (date, hours))
        conn.commit()

    c.execute("SELECT * FROM study ORDER BY id DESC")
    data = c.fetchall()

    total_hours = sum([row[2] for row in data])
    total_fees = total_hours * PRICE_PER_HOUR

    conn.close()

    return render_template("index.html",
                           data=data,
                           total_hours=total_hours,
                           total_fees=total_fees)

if __name__ == "__main__":
    init_db()
    app.run()
