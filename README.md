# Endpoints
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
    "salary_per_shift": -1,
    "createdAt": "2021-02-01T10:08:23.000Z",
    "updatedAt": "2021-02-01T10:08:23.000Z"
  }
}
```

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
        "createdAt": "2024-12-04T12:35:54.602Z",
        "updatedAt": "2024-12-04T12:35:54.602Z",
        "accessToken": <Token>
    }
}
```

### 3. Logout User

**URL**: `/employee/logout`

**Method**: `DELETE`

**Description**: Logout Employee.

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
  "message": "User logged out successfully",
  "data": true
}
```

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
    "salary_per_shift": -1,
    "created_at": "2025-05-21T08:00:00Z",
    "updated_at": "2025-05-21T08:00:00Z"
  }
}
```

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
  "data": {
    "id": 1,
    "name": "Richard Kamitono",
    "email": "r@gmail.com",
    "role": "unassigned",
    "salary_per_shift": -1,
    "created_at": "2025-05-21T08:00:00Z",
    "updated_at": "2025-05-21T08:00:00Z"
  }
}
```


