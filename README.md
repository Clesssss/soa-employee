# Endpoints

> **⚠️ Note:** All of the endpoints listed in this documentation have been tested locally and are currently working. If you encounter any issues accessing them or have questions, please contact the repository owner. Please note that the request formats, authorization methods, or responses may change as development progresses, so always refer back to this documentation or subscribe to the repository for the latest updates.


### 1. Register employee

**URL**: `/employee`

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

**Description**: Log in an employee.

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
        "access_token": <Token>
    }
}
```

---

### 3. Logout employee

**URL**: `/employee/logout`

**Method**: `POST`

**Description**: Log out the currently authenticated employee.

**Request Header**:

```json
{
  "Authorization": "Bearer <token>"
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

**Description**: Retrieve a single employee's details

**Request Header**:

```json
{
  "Authorization": "Bearer <token>"
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

**Description**: Retrieve all employees, optionally filtered by role and name search.

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
  "Authorization": "Bearer <token>"
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

**Description**: Retrieves the currently authenticated employee's details using access token.

**Request Header**:

```json
{
  "Authorization": "Bearer <token>"
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

**Description**: Employee can update their own profile (`name`, `email`, `password`)

**Authorization**: Requires access token with the same id as the one being edit.

**Request Header**:

```json
{
  "Authorization": "Bearer <employee_token>"
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

### 8. Edit Employee Profile (by Manager)

**URL**: `/employee/:id`

**Method**: `PUT`

**Description**: Manager can update employee’s profil (`name`, `role`, `salary_per_shift`).

**Authorization**: Requires access token with `manager` role.

**Request Header**:

```json
{
  "Authorization": "Bearer <manager_token>"
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

**Description**: Create a schedule for a single employee.

**Request Header**:

```json
{
  "Authorization": "Bearer <token>"
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

**Description**: Create schedules for multiple employees on the same `date` and `shift`.

**Request Header**:

```json
{
  "Authorization": "Bearer <token>"
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

**Description**: Update a schedule entry. Only `note` and `attendance` can be modified.

**Request Header**:

```json
{
  "Authorization": "Bearer <token>"
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

**Description**: Retrieve scheduled employees with support for date, role, shift, attendance, and other filters. If no parameters are provided, all schedules will be returned.

**Query Parameters**:

| Name          | Type    | Required | Description                                 |
| ------------- | ------- | -------- | ------------------------------------------- |
| `date`        | string  | ❌ No     | Exact date in `YYYY-MM-DD`.                 |
| `from_date`   | string  | ❌ No     | Fetch all schedules from this date forward. |
| `month`       | string  | ❌ No     | Filter by specific month, format `YYYY-MM`. |
| `shift`       | string  | ❌ No     | `day` or `night`.                           |
| `role`        | string  | ❌ No     | Employee role.                              |
| `attendance`  | boolean | ❌ No     | `true` or `false`.                          |
| `search`      | string  | ❌ No     | Partial name search.                        |
| `employee_id` | integer | ❌ No     | Specific employee only.                     |
| `limit`       | integer | ❌ No     | Maximum number of records returned.         |

***Parameter Conflict Rules***   
To avoid ambiguous filters, the following rules apply:

You may use only one of the following parameters at a time:

- `date`
- `month`
- `from_date`

If more than one is provided, the priority is:
1. date
2. month
3. from_date

`shift`, `role`, `attendance`, `employee_id`, and `search` can be used alongside any date filter.
If `limit` is used with `date`, it will only limit records on that exact date, not future days.
If `employee_id` is used with `search`, the `employee_id` will take precedence (i.e. it will ignore `search`).

---

***Example Prioritization***

| Query                         | Behavior                                  |
|-------------------------------|-------------------------------------------|
| `date`, `month`, `from_date`  | Only `date` is used                       |
| `month`, `from_date`           | Only `month` is used                      |
| `from_date`, `shift`, `limit=3`| Fetch 3 upcoming shifts from `from_date` |
| `employee_id=1`, `search=richard` | Only employee with ID 1 is searched (ignores `search`) |

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

