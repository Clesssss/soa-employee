from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import pooling
import time

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def get_all_employees(self, role=None, search=None):
        cursor = self.connection.cursor(dictionary=True)
        result = []

        sql = "SELECT * FROM employee WHERE 1=1"
        params = []

        if role:
            sql += " AND role = %s"
            params.append(role)

        if search:
            sql += " AND LOWER(name) LIKE %s"
            params.append(f"%{search.lower()}%")

        cursor.execute(sql, params)

        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'role': row['role'],
                'salary_per_shift': row['salary_per_shift']
            })

        cursor.close()
        return result

    def get_employee_by_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT id, name, email, role, salary_per_shift, access_token FROM employee WHERE id = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_employee_by_email(self, email):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM employee WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result


    def register_employee(self, name, email, password_hashed):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("INSERT INTO employee (name, email, password) VALUES (%s, %s, %s)", (name, email, password_hashed))
        self.connection.commit()
        employee_id = cursor.lastrowid
        cursor.close()
        return self.get_employee_by_id(employee_id)

    def update_employee(self, id, update_data):
        if not update_data:
            raise ValueError("No update data provided")

        print(update_data)
        cursor = self.connection.cursor(dictionary=True)

        fields = []
        values = []

        for key, value in update_data.items():
            fields.append(f"{key} = %s")
            values.append(value)

        values.append(id)
        print(fields)

        sql = f"UPDATE employee SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(sql, tuple(values))
        self.connection.commit()

        cursor.execute("SELECT id, name, email, role, salary_per_shift FROM employee WHERE id = %s", (id,))
        updated_employee = cursor.fetchone()
        cursor.close()

        return updated_employee


    def save_access_token(self, employee_id: int, token: str) -> bool:
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE employee SET access_token = %s WHERE id = %s"
            cursor.execute(sql, (token, employee_id))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error saving access token: {e}")
            return False

    def delete_access_token(self, employee_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE employee SET access_token = NULL WHERE id = %s"
            cursor.execute(sql, (employee_id,))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error deleting access token: {e}")
            return False


    def create_schedule(self, employee_id, date, shift_type):
        cursor = self.connection.cursor(dictionary=True)
        sql = """
            INSERT INTO schedule (employee_id, date, shift_type)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (employee_id, date, shift_type))
        self.connection.commit()
        schedule_id = cursor.lastrowid
        cursor.close()
        return {
            "id": schedule_id,
            "employee_id": employee_id,
            "date": date,
            "shift_type": shift_type
        }

    def create_batch_schedule(self, employee_ids, date, shift_type):
        cursor = self.connection.cursor(dictionary=True)
        data = []
        for emp_id in employee_ids:
            cursor.execute(
                "INSERT INTO schedule (employee_id, date, shift_type) VALUES (%s, %s, %s)",
                (emp_id, date, shift_type)
            )
            data.append({
                "employee_id": emp_id,
                "date": date,
                "shift_type": shift_type
            })
        self.connection.commit()
        cursor.close()
        return data

    def update_schedule(self, schedule_id, note=None, attendance=None):
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM schedule WHERE id = %s", (schedule_id,))
        existing = cursor.fetchone()
        if not existing:
            cursor.close()
            raise ValueError(f"Schedule with id {schedule_id} not found")

        sql = """
               UPDATE schedule
               SET note = COALESCE(%s, note),
                   attendance = COALESCE(%s, attendance)
               WHERE id = %s
           """
        cursor.execute(sql, (note, attendance, schedule_id))
        self.connection.commit()

        cursor.execute("SELECT * FROM schedule WHERE id = %s", (schedule_id,))
        updated_row = cursor.fetchone()
        updated_row['date'] = updated_row['date'].isoformat()

        cursor.close()
        return updated_row

    def get_schedule(self, date=None, from_date=None, month=None, shift=None,
                     role=None, attendance=None, search=None, employee_id=None, limit=None):
        cursor = self.connection.cursor(dictionary=True)

        sql = """
            SELECT s.id, s.employee_id, e.name, e.role, s.shift_type, s.date, s.attendance
            FROM schedule s
            JOIN employee e ON s.employee_id = e.id
            WHERE 1=1
        """
        params = []

        # Handle date filters with priority: date > month > from_date
        if date:
            sql += " AND s.date = %s"
            params.append(date)
        elif month:
            # Filter by month in 'YYYY-MM' format using LIKE, e.g. '2025-06%'
            sql += " AND s.date LIKE %s"
            params.append(f"{month}%")
        elif from_date:
            sql += " AND s.date >= %s"
            params.append(from_date)
        # else no date filter, fetch all

        if shift:
            sql += " AND s.shift_type = %s"
            params.append(shift)

        if role:
            sql += " AND e.role = %s"
            params.append(role)

        if attendance is not None:
            sql += " AND s.attendance = %s"
            params.append(int(attendance))  # Convert boolean to 0 or 1

        # If employee_id is provided, ignore search
        if employee_id:
            sql += " AND s.employee_id = %s"
            params.append(employee_id)
        elif search:
            sql += " AND LOWER(e.name) LIKE %s"
            params.append(f"%{search.lower()}%")

        sql += " ORDER BY s.date ASC"

        if limit:
            sql += " LIMIT %s"
            params.append(limit)

        cursor.execute(sql, params)
        result = cursor.fetchall()
        cursor.close()

        # Convert date to ISO format string
        for row in result:
            if isinstance(row['date'], (str, bytes)):
                # Already string, do nothing or ensure proper format
                row['date'] = row['date']
            else:
                row['date'] = row['date'].isoformat()

            # Optional: convert attendance int (0/1) to boolean for clarity
            row['attendance'] = bool(row['attendance'])

        return result

    def __del__(self):
        self.connection.close()


class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        # Try to connect multiple times with delays
        retries = 5
        for attempt in range(retries):
            try:
                self.connection_pool = pooling.MySQLConnectionPool(
                    pool_name="database_pool",
                    pool_size=10,
                    pool_reset_session=True,
                    host='employee-mysql',
                    database='employee',
                    user='root',
                    password=''
                )
                print("MySQL connection pool created successfully")
                break
            except mysql.connector.Error as e:
                print(f"Attempt {attempt + 1} - MySQL connection failed: {e}")
                time.sleep(3)  # wait 3 seconds before retry
        else:
            # After retries exhausted
            print("Failed to connect to MySQL after several attempts.")
            self.connection_pool = None

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
