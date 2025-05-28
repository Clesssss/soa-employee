# Endpoints

> **⚠️ Disclaimer:** All endpoints documented here are currently under development. Their structure, parameters, or responses may be subject to change without prior notice.

### 1. Register user

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

### 2. Login User

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

### 3. Logout User

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

### 4. Get employees

**URL**: `/employee`

**Parameters**: 

| Name         | Type       | Required | Description                                                                |
| ------------ | ---------- | -------- | -------------------------------------------------------------------------- |
| `role`       | `string`   | optional | (Cashier, Waiter, Chef, Delivery, Manager, Unassigned)                                                 |
| `work_date`  | `date`     | optional | (default = today)                                      |
| `attendance` | `boolean`  | optional | (default = 1)                                   |
| `shift_type` | `string`   | optional | (`day` or `night`)                                    |

**Example**: GET /employee?role=cashier&shift_type=day

> This returns all employees with:
>  - role = cashier
>  - shift_type = day
>  - attendance = true (by default)
>  - work_date = today's date (by default)


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
  "data": [
  {
    "id": 1,
    "name": "Richard Kamitono",
    "email": "r@gmail.com",
    "role": "unassigned",
    "salary_per_shift": -1
  },
  {
    "id": 1,
    "name": "Richard Kamitono",
    "email": "r@gmail.com",
    "role": "unassigned",
    "salary_per_shift": -1
  }
  ]
}
```

---

### 5. Get Authenticated Employee

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

### 6. Entry Schedule

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

### 7. Batch Entry Schedule

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

### 8. Edit Schedule

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

### 9. Fetch Schedule by Date & Shift

**URL**: `employee/schedule`

**Method**: `GET`

**Parameters**:

| Name    | Type     | Required | Description               |
| ------- | -------- | -------- | ------------------------- |
| `date`  | `string` | yes      | Schedule date (YYYY-MM-DD)|
| `shift` | `string` | yes      | `day` or `night`          |

**Example**:  
`GET /employee/schedule?date=2025-05-28&shift=day`

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
    "message": "Schedule retrieved successfully",
    "data": [
        {
            "id": 5,
            "employee_id": 2,
            "name": "Richard Kamitono",
            "role": "unassigned",
            "shift_type": "day",
            "date": "2025-05-28"
        },
        {
            "id": 6,
            "employee_id": 3,
            "name": "Richard Kamitono",
            "role": "unassigned",
            "shift_type": "day",
            "date": "2025-05-28"
        },
        {
            "id": 1,
            "employee_id": 4,
            "name": "Richard Kamitono",
            "role": "unassigned",
            "shift_type": "day",
            "date": "2025-05-28"
        }
    ]
}
```
