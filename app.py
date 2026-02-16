from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = "study.db"
PRICE_PER_HOUR = 1000


# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS study (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            hours REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ================= ROUTES =================

@app.route("/")
def index():
    conn = get_db()
    data = conn.execute("SELECT * FROM study ORDER BY id DESC").fetchall()
    conn.close()

    total_hours = sum(row["hours"] for row in data)
    total_fees = total_hours * PRICE_PER_HOUR

    return render_template("index.html",
                           data=data,
                           total_hours=total_hours,
                           total_fees=total_fees)


@app.route("/add", methods=["POST"])
def add_entry():
    date = request.form["date"]
    hours = request.form["hours"]

    try:
        hours = float(hours)
    except:
        return redirect(url_for("index"))

    conn = get_db()
    conn.execute("INSERT INTO study (date, hours) VALUES (?, ?)", (date, hours))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update_entry():
    record_id = request.form["id"]
    date = request.form["date"]
    hours = request.form["hours"]

    try:
        hours = float(hours)
    except:
        return redirect(url_for("index"))

    conn = get_db()
    conn.execute("UPDATE study SET date=?, hours=? WHERE id=?",
                 (date, hours, record_id))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete_entry():
    record_id = request.form["id"]

    conn = get_db()
    conn.execute("DELETE FROM study WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# ================= MAIN =================

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
