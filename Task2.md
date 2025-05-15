# Task 2: Authentication & Appointment Scheduling

## Title:
Implement User Authentication (Sign Up / Sign In) and Appointment Maintenance Scheduling API endpoints.

## Description:
Extend the doctor appointment system by adding user authentication (JWT-based Sign Up and Sign In) and endpoints to create, retrieve, update, and cancel patient appointments with doctors.

---

## Part A: User Authentication

### Acceptance Criteria:
- **Sign Up**: Users can register with email and password.
  - Email must be unique and valid.
  - Password must be at least 8 characters.
- **Sign In**: Registered users can log in with email and password.
  - On success, return a JWT access token.
  - On failure, return 401 Unauthorized.

### API Details:

| Method | Endpoint               | Description               |
| ------ | ---------------------- | ------------------------- |
| POST   | `/api/v1/auth/signup`  | Register a new user       |
| POST   | `/api/v1/auth/signin`  | Authenticate and get JWT  |

#### Request Body (Sign Up):
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
#### Response (Sign Up Success):
```json
{
  "success": true,
  "message": "User registered successfully.",
  "user_id": "<new_user_id>"
}
```

#### Request Body (Sign In):
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
#### Response (Sign In Success):
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

---

## Part B: Appointment Scheduling Endpoints

### Acceptance Criteria:
- **Create Appointment**: Authenticated users can book an appointment with a doctor by specifying doctor_id, date, and time slot.
- **Get Appointments**: Users can list their upcoming appointments.
- **Update Appointment**: Users can reschedule (change date/time) before the appointment date.
- **Cancel Appointment**: Users can cancel an appointment.

### API Details:

| Method | Endpoint                          | Description                        | Auth Required |
| ------ | --------------------------------- | ---------------------------------- | ------------- |
| POST   | `/api/v1/appointments/`           | Book a new appointment             | Yes           |
| GET    | `/api/v1/appointments/`           | List user's appointments           | Yes           |
| PUT    | `/api/v1/appointments/{appt_id}`  | Reschedule an existing appointment | Yes           |
| DELETE | `/api/v1/appointments/{appt_id}`  | Cancel an appointment              | Yes           |

#### Request Body (Create):
```json
{
  "doctor_id": "607f1f77bcf86cd799439011",
  "date": "2025-05-10",
  "time_slot": "09:00-09:30"
}
```
#### Response (Create Success):
```json
{
  "success": true,
  "message": "Appointment booked successfully.",
  "appointment_id": "<new_appt_id>"
}
```

---

## Database Structure

### 1. `users` Collection
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "hashed_password": "<bcrypt_hash>",
  "created_at": ISODate
}
```

### 2. `appointments` Collection
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,         // Patient reference
  "doctor_id": ObjectId,       // Doctor reference
  "date": "2025-05-10",
  "time_slot": "09:00-09:30",
  "status": "booked",         // [booked, cancelled, completed]
  "created_at": ISODate,
  "updated_at": ISODate
}
```

---

## Technical Notes:
- Use **FastAPI**, **pymongo**, **python-jose** for JWT, **bcrypt** for password hashing.
- Protect appointment endpoints with JWT Bearer token.
- Validate slot availability against `doctors.available_slots`.
- Return 409 Conflict if slot already booked.
- Swagger UI automatically generated at `/docs`.

## Deliverables:
1. `auth.py`, `appointments.py`, updated `main.py` files (to be uploaded via Telegram).
2. Screenshot of endpoint test on swagger for:
   - Sign Up, Sign In
   - CRUD operations on appointments