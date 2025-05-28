from nameko.rpc import rpc
import dependencies
from auth import hash_password, verify_password, generate_access_token, decode_token

class EmployeeService:

    name = 'employee_service'

    database = dependencies.Database()

    @rpc
    def get_all_employees(self):
        employees = self.database.get_all_employees()
        return employees

    @rpc
    def get_employee_by_id(self, id):
        employee = self.database.get_employee_by_id(id)
        return employee

    @rpc
    def get_employee_by_token(self, token):
        try:
            payload = decode_token(token)
            employee_data = {
                "id": payload.get("id"),
                "name": payload.get("name"),
                "email": payload.get("email"),
                "role": payload.get("role")
            }
            return employee_data
        except Exception:
            return None

    @rpc
    def get_employee_by_email(self, email):
        employee = self.database.get_employee_by_email(email)
        return employee

    @rpc
    def register_employee(self, name, email, password):
        hashed = hash_password(password)
        return self.database.register_employee(name, email, hashed)

    @rpc
    def login_employee(self, email, password):
        employee = self.get_employee_by_email(email)
        if not employee:
            return None, "Email not registered"

        if not verify_password(password, employee['password'].encode('utf-8')):
            return None, "Incorrect password"

        token = generate_access_token(employee["id"], employee["name"], employee["email"], employee["role"])

        success = self.database.save_access_token(employee["id"], token)
        if not success:
            return None, "Failed to save access token"

        employee_data = {
            "id": employee["id"],
            "name": employee["name"],
            "email": employee["email"],
            "role": employee["role"],
            "salary_per_shift": employee["salary_per_shift"],
            "access_token": token
        }

        return employee_data, None

    @rpc
    def authorize_and_logout(self, token):
        try:
            payload = decode_token(token)
            employee_id = payload.get('id')
            if not employee_id:
                return False, "Invalid token payload"

            success, error = self.logout_employee(employee_id, token)
            if not success:
                return False, error

            return True, None
        except Exception as e:
            return False, "Invalid or expired token"

    @rpc
    def logout_employee(self, employee_id, token):
        employee = self.get_employee_by_id(employee_id)
        if not employee or employee.get("access_token") != token:
            return False, "Invalid token"

        success = self.database.delete_access_token(employee_id)
        if not success:
            return False, "Invalid token"

        return True, None

    @rpc
    def create_schedule(self, employee_id, date, shift_type):
        return self.database.create_schedule(employee_id, date, shift_type)

    @rpc
    def create_batch_schedule(self, employee_ids, date, shift_type):
        return self.database.create_batch_schedule(employee_ids, date, shift_type)

    @rpc
    def update_schedule(self, schedule_id, note=None, attendance=None):
        return self.database.update_schedule(schedule_id, note, attendance)

    @rpc
    def get_schedule_by_date_shift(self, date, shift_type):
        return self.database.get_schedule_by_date_shift(date, shift_type)