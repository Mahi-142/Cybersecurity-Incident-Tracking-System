from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mahii@1402",
    database="CyberSecurityDB"
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_incident', methods=['POST'])
def add_incident():

    title = request.form['title']
    description = request.form['description']
    severity = request.form['severity']

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO Incidents
        (title,description,severity,status,reported_by,assigned_to)
        VALUES(%s,%s,%s,'Open',3,2)
    """, (title, description, severity))

    db.commit()

    return redirect('/incidents')


@app.route('/incidents')
def incidents():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Incidents
        ORDER BY incident_id DESC
    """)

    incidents = cursor.fetchall()

    return render_template(
        'incidents.html',
        incidents=incidents
    )


@app.route('/resolve/<int:id>')
def resolve_incident(id):

    cursor = db.cursor()

    cursor.execute("""
        UPDATE Incidents
        SET status='Resolved'
        WHERE incident_id=%s
    """, (id,))

    db.commit()

    return redirect('/incidents')


@app.route('/delete/<int:id>')
def delete_incident(id):

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM Incidents
        WHERE incident_id=%s
    """, (id,))

    db.commit()

    return redirect('/incidents')


if __name__ == "__main__":
    app.run(debug=True)