from flask import Flask, request, render_template, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port="5432"
    )

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/group_by_experience', methods=['GET'])
def group_by_experience():
    group_by = request.args.get('group_by')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    base_query = '''
        SELECT
            CASE
                WHEN minyears IS NULL THEN 'Unknown'
                WHEN minyears < 1 THEN '0-1'
                WHEN minyears < 2 THEN '1-2'
                WHEN minyears < 3 THEN '2-3'
                WHEN minyears < 5 THEN '3-5'
                WHEN minyears < 10 THEN '5-10'
                ELSE '10+'
            END AS experience_range
    '''

    if group_by in ['Role', 'Location']:
        base_query += f', "{group_by}"'

    base_query += ''', COUNT(*) AS count FROM filtered_employee_data GROUP BY experience_range'''

    if group_by in ['Role', 'Location']:
        base_query += f', "{group_by}"'

    base_query += ' ORDER BY experience_range;'

    cur.execute(base_query)
    results = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)