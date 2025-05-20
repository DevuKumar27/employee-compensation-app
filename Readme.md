**📊 Employee Compensation Forecasting Application**

This is a full-stack web application that allows HR and management users
to:

✅ Filter and view employee compensation\
✅ Compare against industry averages\
✅ Simulate increments globally or by role/location/employee\
✅ Export data to CSV for reporting

**🔧 Tools & Technologies Used**

  -----------------------------------------------------------------------
  **Category**             **Technology**
  ------------------------ ----------------------------------------------
  **Backend**              Python (Flask), psycopg2

  **Frontend**             HTML, JavaScript, Chart.js

  **Database**             PostgreSQL

  **Data Viz**             Chart.js (Bar Charts)

  **Data Format**          CSV for export

  **Dev Tools**            DBeaver, VS Code
  -----------------------------------------------------------------------

**⚙️ Setup Instructions**

**1. Clone the Repository**

git clone https://github.com/yourusername/employee-compensation-app.git

cd employee-compensation-app

**2. Set Up PostgreSQL Database**

Create a PostgreSQL database (e.g., postgres) and execute the table
creation scripts:

\-- Run the SQL in setup.sql or from documentation (employee_data,
average_industry_compensation, etc.)

Load your data into these tables using DBeaver or SQL scripts.

**3. Install Python Dependencies**

pip install flask psycopg2

**4. Run the Application**

python app.py

The app will be available at: http://localhost:5000/

**📚 User Stories & Features**

**✅ User Story 1: Filter and Display Employees by Role**

-   Filter by **Role** and/or **Location**

-   Toggle **Active/Inactive** employees

-   View:

    -   Employee Name, Role, Location, Current Compensation

-   See a **Bar Chart** of average industry compensation by location

**✅ User Story 2: Group Employees by Experience**

-   Group employees into predefined experience ranges (e.g., 0--1, 1--2,
    3--5)

-   Optional breakdown by **Role** or **Location**

-   Data shown via **stacked bar chart**

**✅ User Story 3: Simulate Compensation Increments**

-   Apply a **global % increment** to all employees

-   Optionally apply **custom % increments**:

    -   Per Location (e.g., \"Pune:8, Jaipur:5\")

    -   Per Employee (e.g., \"Aditi:10, Pooja:7\")

-   View updated compensation vs current

**✅ User Story 4: Download Filtered Employee Data**

-   Download a **CSV** of filtered data (based on role/location/status)

-   Includes applied increment values

-   CSV fields:

    -   Name, Role, Location, Experience, Compensation (after
        increment), Status

**📁 Folder Structure**

csharp

CopyEdit

├── userstudy1.py \# Main backend app

├── userstudy2.py

├── userstudy3.py

├── userstudy4.py

├── templates/

│ ├── index.html \# Dashboard with buttons

│ ├── index1.html \# User Story 1

│ ├── index2.html \# User Story 2

│ ├── index3.html \# User Story 3

│ └── index4.html \# User Story 4

├── static/ \# Optional CSS/JS

└── README.md

**📬 Contact**

For questions or collaboration:\
**Devu Kumar M S** -- \[devukumarms.2325@gmail.com\]\
www.linkedin.com/in/devukumarms
