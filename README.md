# Endpoints

> **⚠️ Disclaimer:** All endpoints documented here are currently under development. Their structure, parameters, or responses may be subject to change without prior notice.

### 1. Register employee

**URL**: `/employee/register`

**Method**: `POST`

**Description**: Register new employee

**Request Body**:

```json
{
  "name": "Richard Kamitono",
  "email": "r@gmail.com",
  "password": "blablabla"
}
```

**Response**:

- Status: `201 - Created`
- Body:

```json
{
  "message": "User registered successfully",
  "data": {
    "id": "1",
    "name": "Richard Kamitono",
    "email": "r@gmail.com",
    "role": "unassigned",
    "salary_per_shift": -1
  }
}
```

---

### 2. Login employee

**URL**: `/employee/login`

**Method**: `POST`

**Description**: Login Employee.

**Request Body**:

```json
{
  "email": "r@gmail.com",
  "password": "blablabla"
}
```

**Response**:

- Status: `200 - Ok`
- Body:

```json
{
    "message": "User logged in successfully",
    "data": {
        "id": "1",
        "name": "Richard Kamitono",
        "email": "r@gmail.com",
        "role": "unassigned",
        "salary_per_shift": -1,
        "accessToken": <Token>
    }
}
```

---

### 3. Logout employee

**URL**: `/employee/logout`

**Method**: `POST`

**Description**: Logout Employee.

**Request Header**:

```json
{
  "authorization": "Bearer <token>"
}
```

**Success Response**:

- **Status**: `200 OK`  
  **Body**:
  ```json
  {
    "message": "User logged out successfully",
    "data": true
  }
  ```


**Error Responses**:

- **Status**: `401 Unauthorized`  
  **Body**:
  ```json
  {
    "error": "Invalid or expired token"
  }
  ```

---

### 4. Get employee by ID

**URL**: `/employee/:id`

**Method**: `GET`

**Description**: Retrieve details of a single employee.

**Request Header**:

```json
{
  "authorization": "Bearer <token>"
}
```

**Response**:

- Status: `200 - Ok`
- Body:

```json
{
  "message": "Employee retrieved successfully",
  "data": {
    "id": 1,
    "name": "Richard Kamitono",
    "email": "r@gmail.com",
    "role": "unassigned",
    "salary_per_shift": -1
  }
}
```

---

### 5. Get All Employees (Filtered by Role and Search by Name)

**URL**: `/employee`

**Method**: `GET`

**Description**: Retrieve all employees with optional filters by role and search by name.

**Query Parameters**:

| Name   | Type     | Required | Description                            |
|--------|----------|----------|----------------------------------------|
| role   | string   | optional | Filter by role                         |
| search | string   | optional | Search by name (case-insensitive match)|

**Example**:  
`GET /employee?role=Cashier&search=richard`

**Request Header**:

```json
{
  "authorization": "Bearer <token>"
}
```

**Response**:

- Status: `200 - OK`
- Body:

```json
{
  "message": "Employees retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Richard Kamitono",
      "email": "r@gmail.com",
      "role": "Cashier",
      "salary_per_shift": 150000
    }
  ]
}
```

---

### 6. Get Authenticated Employee

**URL**: `/employee/me` 

**Method**: `GET`  

**Description**: Retrieves details of the currently authenticated employee using the access token.

**Request Header**:

```json
{
  "authorization": "Bearer <token>"
}
```

**Response**:

- **Status**: `200 OK`  
  **Body**:
  ```json
  {
    "message": "Employee retrieved successfully",
    "data": {
      "id": 1,
      "name": "Richard Kamitono",
      "email": "r@gmail.com",
      "role": "unassigned",
      "salary_per_shift": -1
    }
  }
  ```

---

### 7. Edit Employee Profile (by Employee)

**URL**: `/employee/:id`

**Method**: `PUT`

**Description**: Allows an employee to update their own profile. Only `name`, `email`, and `password` can be updated.

**Authorization**: Requires access token with `employee` role.

**Request Header**:

```json
{
  "authorization": "Bearer <employee_token>"
}
```

**Request Body**:

```json
{
  "name": "Richard Kamitono",
  "email": "richard@gmail.com",
  "password": "new_secure_password"
}
```

**Response**:

- Status: `200 - OK`
- Body:

```json
{
  "message": "Profile updated successfully",
  "data": {
    "id": 1,
    "name": "Richard Kamitono",
    "email": "richard@gmail.com"
  }
}
```

---

### 8. Edit Employee Profile (by Manager/Admin)

**URL**: `/employee/:id`

**Method**: `PUT`

**Description**: Allows a manager or admin to update an employee’s profile. Editable fields include `name`, `role` and `salary_per_shift`.

**Authorization**: Requires access token with `manager` role.

**Request Header**:

```json
{
  "authorization": "Bearer <admin_token>"
}
```

**Request Body**:

```json
{
  "name": "Richard Kamitono",
  "role": "Cashier",
  "salary_per_shift": 150000
}
```

**Response**:

- Status: `200 - OK`
- Body:

```json
{
  "message": "Employee updated successfully",
  "data": {
    "id": 1,
    "name": "Richard Kamitono",
    "role": "Cashier",
    "salary_per_shift": 150000
  }
}
```

### 9. Entry Schedule

**URL**: `/employee/schedule`

**Method**: `POST`

**Description**: Create a single employee schedule entry.

**Request Header**:

```json
{
  "authorization": "Bearer <token>"
}
```

**Request Body**:

```json
{
  "employee_id": 4,
  "date": "2025-05-28",
  "shift_type": "day"
}
```

**Response**:

- Status: `201 - Created`
- Body:

```json
{
  "message": "Schedule entry created successfully",
  "data": {
    "id": 0,
    "employee_id": 4,
    "date": "2025-05-28",
    "shift_type": "day"
  }    
}
```

---

### 10. Batch Entry Schedule

**URL**: `/employee/schedule/batch`

**Method**: `POST`

**Description**: Create multiple schedule entries for the same date and shift.

**Request Header**:

```json
{
  "authorization": "Bearer <token>"
}
```

**Request Body**:

{
  "employee_ids": [2, 3],
  "date": "2025-05-28",
  "shift_type": "day"
}

**Response**:

- Status: `201 - Created`
- Body:

```json
{
    "message": "Batch schedule created successfully",
    "data": [
        {
            "employee_id": 2,
            "date": "2025-05-28",
            "shift_type": "day"
        },
        {
            "employee_id": 3,
            "date": "2025-05-28",
            "shift_type": "day"
        }
    ]
}
```

---

### 11. Edit Schedule

**URL**: `employee/schedule/:id`

**Method**: `PUT`

**Description**: Update an existing schedule entry by ID.

**Note**: Only the note and attendance fields can be updated. If you need to change the employee_id, date, or shift_type, please delete the existing row and create a new one to maintain schedule uniqueness.

**Request Header**:

```json
{
  "authorization": "Bearer <token>"
}
```

**Request Body**:

```json
{
  "note": "test",
  "attendance": 0
}
```

**Response**:

- Status: `200 - Ok`
- Body:

```json
{
    "message": "Schedule updated successfully",
    "data": {
        "id": 5,
        "employee_id": 2,
        "date": "2025-05-28",
        "shift_type": "day",
        "note": "test",
        "attendance": 0
    }
}
```

---

### 12. Get Employees by Schedule (Filtered by Role, Attendance, and Search by Name)

**URL**: `/employee/schedule`

**Method**: `GET`

**Description**: Retrieve employees scheduled on a specific date and shift. Filterable by role, attendance (optional), and searchable by name.

**Query Parameters**:

| Name        | Type     | Required | Description                                      |
|-------------|----------|----------|--------------------------------------------------|
| date        | string   | yes      | Schedule date in format `YYYY-MM-DD`            |
| shift       | string   | yes      | Shift type: `day` or `night`                    |
| role        | string   | optional | Filter by role                                  |
| attendance  | boolean  | optional | Filter by attendance status                     |
| search      | string   | optional | Search by employee name (case-insensitive match)|

**Example**:  
`GET /employee/schedule/employees?date=2025-05-28&shift=day&role=Cashier&attendance=true&search=richard`

**Request Header**:

```json
{
  "authorization": "Bearer <token>"
}
```

**Response**:

- Status: `200 - OK`
- Body:

```json
{
  "message": "Employees on schedule retrieved successfully",
  "data": [
    {
      "id": 5,
      "employee_id": 1,
      "name": "Richard Kamitono",
      "role": "Cashier",
      "shift_type": "day",
      "date": "2025-05-28",
      "attendance": 1
    }
  ]
}
```

