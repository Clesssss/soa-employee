import json
import logging
from nameko.rpc import RpcProxy
from nameko.web.handlers import http

class GatewayService:
    name = 'gateway'

    employee_rpc = RpcProxy('employee_service')

    @http('GET', '/employee')
    def get_all_employees(self, request):
        employees = self.employee_rpc.get_all_employees()
        return json.dumps({'message': 'Employees retreived successfully', 'data': employees})

    @http('GET', '/employee/<int:id>')
    def get_employee_by_id(self, request, id):
        employee = self.employee_rpc.get_employee_by_id(id)
        if employee:
            return json.dumps({'message': 'Employee retreived successfully', 'data': employee})
        return 404, json.dumps({'error': 'Employee not found'})

    @http('GET', '/employee/me')
    def get_employee_me(self, request):
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return 401, json.dumps({'error': 'Unauthorized'})

        token = auth_header.split(" ")[1]

        try:
            employee = self.employee_rpc.get_employee_by_token(token)
            if not employee:
                return 401, json.dumps({'error': 'Invalid token'})

            return 200, json.dumps({
                "message": "Employee retrieved successfully",
                "data": employee
            })
        except Exception:
            return 401, json.dumps({'error': 'Invalid or expired token'})

    @http('POST', '/employee')
    def register_employee(self, request):
        try:
            data = json.loads(request.get_data(as_text=True))
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')

            if name is None or email is None or password is None:
                return 400, json.dumps({'error': 'Missing attributes'})

            existing_email = self.employee_rpc.get_employee_by_email(email)
            if existing_email:
                return 409, json.dumps({'error': 'Email already used'})

            new_employee = self.employee_rpc.register_employee(name, email, password)
            return 201, json.dumps({'message': 'Employee registered successfully', 'data': new_employee})
        except Exception as e:
            return 500, json.dumps({'error': str(e)})

    @http('POST', '/employee/login')
    def login_employee(self, request):
        try:
            data = json.loads(request.get_data(as_text=True))
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return 400, json.dumps({"error": "Missing email or password"})

            employee_data, error = self.employee_rpc.login_employee(email, password)
            if error:
                return 401, json.dumps({"error": error})

            return 200, json.dumps({
                "message": "User logged in successfully",
                "data": employee_data
            })

        except Exception as e:
            return 500, json.dumps({"error": str(e)})

    @http('POST', '/employee/logout')
    def logout_employee(self, request):
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return 401, json.dumps({'error': 'Unauthorized'})

        token = auth_header.split(" ")[1]

        success, error = self.employee_rpc.authorize_and_logout(token)
        if not success:
            return 401, json.dumps({'error': error})

        return 200, json.dumps({'message': 'User logged out successfully', 'data': True})

    @http('POST', '/employee/schedule')
    def create_schedule(self, request):
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return 401, json.dumps({'error': 'Unauthorized'})
        try:
            data = json.loads(request.get_data(as_text=True))
            employee_id = data.get('employee_id')
            date = data.get('date')
            shift_type = data.get('shift_type')
            if not all([employee_id, date, shift_type]):
                return 400, json.dumps({'error': 'Missing attributes'})
            result = self.employee_rpc.create_schedule(employee_id, date, shift_type)
            return 201, json.dumps({'message': 'Schedule entry created successfully', 'data': result})
        except Exception as e:
            return 500, json.dumps({'error': str(e)})

    @http('POST', '/employee/schedule/batch')
    def create_batch_schedule(self, request):
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return 401, json.dumps({'error': 'Unauthorized'})
        try:
            data = json.loads(request.get_data(as_text=True))
            employee_ids = data.get('employee_ids')
            date = data.get('date')
            shift_type = data.get('shift_type')
            if not all([employee_ids, date, shift_type]):
                return 400, json.dumps({'error': 'Missing attributes'})
            result = self.employee_rpc.create_batch_schedule(employee_ids, date, shift_type)
            return 201, json.dumps({'message': 'Batch schedule created successfully', 'data': result})
        except Exception as e:
            return 500, json.dumps({'error': str(e)})

    @http('PUT', '/employee/schedule/<int:id>')
    def update_schedule(self, request, id):
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return 401, json.dumps({'error': 'Unauthorized'})
        try:
            data = json.loads(request.get_data(as_text=True))
            note = data.get('note')  # Optional
            attendance = data.get('attendance')  # Optional

            if note is None and attendance is None:
                return 400, json.dumps({'error': 'At least one of "note" or "attendance" must be provided'})

            result = self.employee_rpc.update_schedule(id, note, attendance)
            return 200, json.dumps({'message': 'Schedule updated successfully', 'data': result})
        except Exception as e:
            return 500, json.dumps({'error': str(e)})

    @http('GET', '/employee/schedule')
    def get_schedule_by_date_shift(self, request):
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return 401, json.dumps({'error': 'Unauthorized'})
        date = request.args.get('date')
        shift_type = request.args.get('shift_type')
        if not date or not shift_type:
            return 400, json.dumps({'error': 'Missing query parameters'})
        try:
            result = self.employee_rpc.get_schedule_by_date_shift(date, shift_type)
            return 200, json.dumps({'message': 'Schedule retrieved successfully', 'data': result})
        except Exception as e:
            return 500, json.dumps({'error': str(e)})

