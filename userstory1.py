from flask import Flask, request, render_template, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",  # replace with your actual DB name
        user="postgres",
        password="postgres",
        port="5432"
    )

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/get_roles')
def get_roles():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT "Role" FROM employee_data;')
    roles = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(roles)

@app.route('/get_locations')
def get_locations():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT "Location" FROM employee_data;')
    locations = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(locations)

@app.route('/get_employees', methods=['GET'])
def get_employees():
    role = request.args.get('role')
    location = request.args.get('location')
    include_inactive = request.args.get('include_inactive') == 'true'

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = '''
        SELECT "Name", "Role", "Location", "CurrentComp"
        FROM employee_data
        WHERE (%s = '' OR "Role" = %s)
          AND (%s = '' OR "Location" = %s)
          AND (%s = TRUE OR "Active" = 'Y');
    '''

    cur.execute(query, (role, role, location, location, include_inactive))
    employees = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(employees)

@app.route('/get_avg_by_location')
def get_avg_by_location():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    role = request.args.get("role")  # from frontend
    query = '''
        SELECT "Location", AVG("Average Industry Compensation"::FLOAT) AS avg_comp
        FROM average_industry_compensation
        WHERE (%s = '' OR "Role" = %s)
        GROUP BY "Location";
    '''
    cur.execute(query, (role, role))
    result = cur.fetchall()

    print("DEBUG: Fetched avg compensation by location:", result)

    cur.close()
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
