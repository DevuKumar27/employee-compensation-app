from flask import Flask, request, render_template, jsonify, Response
import psycopg2
import psycopg2.extras
import io
import csv

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
    return render_template('index4.html')

@app.route('/get_roles_and_locations')
def get_roles_and_locations():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT DISTINCT "Role" FROM employee_data;')
    roles = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT DISTINCT "Location" FROM employee_data;')
    locations = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    return jsonify({'roles': roles, 'locations': locations})

@app.route('/get_filtered_employees', methods=['GET'])
def get_filtered_employees():
    role = request.args.get('role', '')
    location = request.args.get('location', '')
    include_inactive = request.args.get('include_inactive') == 'true'
    global_increment = float(request.args.get('global_increment', 0))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Note: I'm assuming "Experience" refers to a column in your table.
    # If it's `ManYears` or `MinYears` from our previous discussion,
    # adjust the column name accordingly here and in the CSV output.
    query = '''
        SELECT
            "Name",
            "Role",
            "Location",
            "Years of Experience", -- Assuming this is your original VARCHAR column
            "CurrentComp",
            "Active" as "Status"
        FROM filtered_employee_data
        WHERE (%s = '' OR "Role" = %s)
          AND (%s = '' OR "Location" = %s)
          AND (%s = TRUE OR "Active" = 'Y');
    '''
    # The first %s for `include_inactive` should be a boolean check, not a string
    cur.execute(query, (role, role, location, location, include_inactive))
    employees = cur.fetchall()

    processed_employees = []
    for emp in employees:
        current_comp = float(emp.get('CurrentComp', 0)) # Ensure it's float
        new_comp = round(current_comp * (1 + global_increment / 100), 2)
        
        # Prepare data for rendering in HTML table
        processed_employees.append({
            'Name': emp.get('Name'),
            'Role': emp.get('Role'),
            'Location': emp.get('Location'),
            'Experience': emp.get('Years of Experience'), # Use the column name directly
            'CurrentComp': emp.get('CurrentComp'),
            'NewComp': new_comp,
            'Status': emp.get('Status')
        })
    
    cur.close()
    conn.close()
    return jsonify(processed_employees)


@app.route('/download_csv', methods=['GET'])
def download_csv():
    role = request.args.get('role', '')
    location = request.args.get('location', '')
    include_inactive = request.args.get('include_inactive') == 'true'
    global_increment = float(request.args.get('global_increment', 0))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = '''
        SELECT
            "Name",
            "Role",
            "Location",
            "Years of Experience", -- Use the exact column name from your DB for Experience
            "CurrentComp",
            "Active" as "Status"
        FROM filtered_employee_data
        WHERE (%s = '' OR "Role" = %s)
          AND (%s = '' OR "Location" = %s)
          AND (%s = TRUE OR "Active" = 'Y');
    '''
    cur.execute(query, (role, role, location, location, include_inactive))
    employees = cur.fetchall()
    cur.close()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    # CSV Header
    header = ["Name", "Role", "Location", "Experience", "Current Compensation", "New Compensation", "Status"]
    writer.writerow(header)

    for emp in employees:
        current_comp = float(emp.get('CurrentComp', 0))
        new_comp = round(current_comp * (1 + global_increment / 100), 2)
        
        row = [
            emp.get('Name'),
            emp.get('Role'),
            emp.get('Location'),
            emp.get('Years of Experience'), # Ensure this matches your DB column
            emp.get('CurrentComp'),
            new_comp,
            emp.get('Status')
        ]
        writer.writerow(row)

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=employee_data.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)