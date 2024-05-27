from flask import Flask, render_template, request, url_for, flash, redirect, abort, jsonify
import sqlite3
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc0160ac70329e84efb49c44a07c778da3fb104319c78c7b'
app.config['JSON_AS_ASCII'] = False
def get_db_connection():
    conn = sqlite3.connect('./data/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_event(event_id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?',
                        (event_id,)).fetchone()
    conn.close()
    if event is None:
        abort(404)
    return event

def get_leads():
    conn = get_db_connection()
    leads = conn.execute('SELECT * FROM leads').fetchall()
    conn.close()
    if leads is None:
        abort(404)
    return leads

@app.route('/')
def index():      
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY events.id_day, events.time').fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    leads = get_leads()
    if request.method == 'POST':
        day = request.form['dayssum']
        time = request.form['time']
        lead = request.form['lead']
        theme = request.form['theme']
        actors = request.form['actors']
        enable = request.form['enable']
        date = request.form['date']

        if not day:
            flash('Day is required!')
        elif not time:
            flash('time is required!')
        elif not lead:
            flash('lead is required!')
        elif not theme:
            flash('theme is required!')                                                       
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO events (id_day, time, lead, theme, actors, enable, date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (day, time, lead, theme, actors, enable, date))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html', leads=leads)

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    event = get_event(id)
    leads = get_leads()

    if request.method == 'POST':
        day = request.form['dayssum']
        time = request.form['time']
        lead = request.form['lead']
        theme = request.form['theme']
        actors = request.form['actors']
        enable = request.form['enable']
        date = request.form['date']

        if not day:
            flash('Day is required!')
        elif not time:
            flash('time is required!')
        elif not lead:
            flash('lead is required!')
        elif not theme:
            flash('theme is required!')   

        else:
            conn = get_db_connection()
            conn.execute('UPDATE events SET id_day = ?, time = ?, lead = ?, theme = ?, actors = ?, enable = ?, date = ?'
                         ' WHERE id = ?',
                         (day, time, lead, theme, actors, enable, date, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', event=event, leads=leads)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    event = get_event(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(event['theme']))
    return redirect(url_for('index'))

@app.route('/leads/', methods=('GET', 'POST'))
def leads():
    conn = get_db_connection()
    leads = conn.execute('SELECT * FROM leads ORDER BY leads.id').fetchall()
    conn.close()

    if request.method == 'POST':
        lead_name = request.form['new_name']
        if not lead_name:
            flash('Name is required!')                                                     
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO leads (name) VALUES (?)',
                            (lead_name,))
            conn.commit()
            conn.close()
            return redirect(url_for('leads'))  

    return render_template('leads.html', leads=leads)

@app.route('/lead_delete/<int:id>/', methods=('GET', 'POST'))
def lead_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM leads WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('leads'))

@app.route('/lead_edit/<int:id>/', methods=('GET', 'POST'))
def lead_edit(id):
    print(request.form['name'])  
    name_lead = request.form['name']
    if not name_lead:
        flash('Name is required!')
    else:
        conn = get_db_connection()
        conn.execute('UPDATE leads SET name = ? WHERE id = ?', (name_lead, id,))
        conn.commit()
        conn.close()
        return redirect(url_for('leads'))

@app.route("/api/result")
def result_json():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events WHERE events.enable = 1 ORDER BY events.time').fetchall()
    conn.close()
    rowarray_list = []
    for row in events:
        t = ({'day':row[1], 'time':row[2], 'lead':row[4], 'theme':row[5], 'actors':row[6], 'date':row[8]})   
        rowarray_list.append(t)      
    response = jsonify(rowarray_list)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True) 
