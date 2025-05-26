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