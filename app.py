from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Tahrani3@mn'
app.config['MYSQL_DB'] = 'FOOTBALL'

mysql = MySQL(app)

@app.route('/')
def index():
    return "Welcome to the Football Database App!"

@app.route('/teams')
def teams():
    cur = mysql.connection.cursor()
    cur.execute("SELECT TEAM_NAME, Found_date, type, OWNER_ID, MGR_ID FROM TEAM")
    teams_data = cur.fetchall()
    cur.close()
    return render_template('teams.html', teams=teams_data)

@app.route('/add_team', methods=['POST'])
def add_team():
    team_name = request.form['team_name']
    established = request.form['established']
    team_type = request.form['type']
    owner_id = request.form['owner_id']
    mgr_id = request.form['mgr_id']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO TEAM (TEAM_NAME, Found_date, type, OWNER_ID, MGR_ID) VALUES (%s, %s, %s, %s, %s)",
                (team_name, established, team_type, owner_id, mgr_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('teams'))

@app.route('/edit_team/<team_name>', methods=['GET'])
def edit_team(team_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT TEAM_NAME, Found_date, type, OWNER_ID, MGR_ID FROM TEAM WHERE TEAM_NAME = %s", [team_name])
    team_data = cur.fetchone()
    cur.close()
    return render_template('edit_team.html', team=team_data)

@app.route('/update_team', methods=['POST'])
def update_team():
    original_name = request.form['original_name']
    team_name = request.form['team_name']
    established = request.form['established']
    team_type = request.form['type']
    owner_id = request.form['owner_id']
    mgr_id = request.form['mgr_id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE TEAM SET TEAM_NAME = %s, Found_date = %s, type = %s, OWNER_ID = %s, MGR_ID = %s WHERE TEAM_NAME = %s", 
                (team_name, established, team_type, owner_id, mgr_id, original_name))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('teams'))

@app.route('/delete_team/<team_name>', methods=['GET'])
def delete_team(team_name):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM TEAM WHERE TEAM_NAME = %s", [team_name])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('teams'))

@app.route('/search_teams', methods=['GET'])
def search_teams():
    search_field = request.args.get('search_field')
    search_term = request.args.get('search_term')
    cur = mysql.connection.cursor()
    query = "SELECT * FROM TEAM WHERE {} LIKE %s".format(search_field)
    cur.execute(query, ['%' + search_term + '%'])
    teams_data = cur.fetchall()
    cur.close()
    return render_template('teams.html', teams=teams_data)

if __name__ == '__main__':
    app.run(debug=True)
