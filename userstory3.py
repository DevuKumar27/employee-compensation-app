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
    return render_template('index3.html')

@app.route('/simulate_increment')
def simulate_increment():
    increment = float(request.args.get('increment', 0))
    custom_by = request.args.get('custom_by')  # either 'location' or 'employee'
    custom_data = request.args.get('custom_data')  # expected as comma-separated string like "NY:10,CA:5" or "John:12,Jane:7"

    custom_map = {}
    if custom_data:
        pairs = custom_data.split(',')
        for pair in pairs:
            key, value = pair.split(':')
            custom_map[key.strip()] = float(value.strip())

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute('''
        SELECT "Name", "Role", "Location", "CurrentComp"
        FROM employee_data
        WHERE "Active" = 'Y'
    ''')

    employees = cur.fetchall()
    updated = []

    for emp in employees:
        name = emp['Name']
        loc = emp['Location']
        current = float(emp['CurrentComp'])

        if custom_by == 'location' and loc in custom_map:
            applied_increment = custom_map[loc]
        elif custom_by == 'employee' and name in custom_map:
            applied_increment = custom_map[name]
        else:
            applied_increment = increment

        new_comp = round(current * (1 + applied_increment / 100), 2)

        updated.append({
            'Name': name,
            'Role': emp['Role'],
            'Location': loc,
            'CurrentComp': current,
            'NewComp': new_comp
        })

    cur.close()
    conn.close()

    return jsonify(updated)

if __name__ == '__main__':
    app.run(debug=True)
