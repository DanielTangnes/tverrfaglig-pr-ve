import threading
from flask import Flask, jsonify
import pandas as pd


app = Flask(__name__)
def run_flask():
    app.run()


def run_api(connect_DB):
    global connect_db
    connect_db = connect_DB
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()


@app.route('/api/test', methods=['GET'])
def api_test():
    con = connect_db
    cur = con.cursor()
    cur.execute('SELECT * FROM vare')
    names = [x[0] for x in cur.description]
    rows = cur.fetchall()
    con.close()
    df = pd.DataFrame(rows, columns=names)
    return jsonify(df.to_dict(orient='records'))