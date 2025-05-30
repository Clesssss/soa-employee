from nameko.extensions import DependencyProvider
import mysql.connector

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

    def get_schedule_by_date_shift(self, date, shift_type):
        cursor = self.connection.cursor(dictionary=True)
        sql = """
            SELECT s.id, s.employee_id, e.name, e.role, s.shift_type, s.date
            FROM schedule s
            JOIN employee e ON s.employee_id = e.id
            WHERE s.date = %s AND s.shift_type = %s
        """
        cursor.execute(sql, (date, shift_type))
        result = cursor.fetchall()
        cursor.close()

        for row in result:
            row['date'] = row['date'].isoformat()

        return result
#    def __del__(self):
#        self.connection.close()


class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=10,
                pool_reset_session=True,
                host='localhost',
                database='employee',
                user='root',
                password=''
            )
        except mysql.connector.Error as e:
            print ("Error while connecting to MySQL using Connection pool:", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
