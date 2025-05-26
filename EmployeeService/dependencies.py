from nameko.extensions import DependencyProvider
import mysql.connector

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def get_all_employees(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM employee"
        cursor.execute(sql)
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
