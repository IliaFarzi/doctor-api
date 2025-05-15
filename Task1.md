# Task 1: Create Doctor Profile

## Title:
Create an Doctor Profile API in the system.

## Description:
Create an API endpoint to manage doctor profiles, allowing users to create, retrieve, update, and delete doctor data.

## Acceptance Criteria:
- The API must accept the following data:
  - name (string): The full name of the doctor.
  - specialty (string): The doctor's specialty (e.g., "Cardiology", "Dentistry").
  - available_slots (array of objects): A list of available time slots for each date.
     - Each object contains:
        - date (string, format: YYYY-MM-DD): The date for which the slots are available.
        - day (string): The day of the week (e.g., "Monday", "Wednesday").
        - slots (array of strings): Available time slots in HH:MM-HH:MM format.


## API Details:

- **Method**: `POST`, `GET`
- **Endpoint**: `/api/v1/doctors/`

### Request Body:
```json
  {
    "name": "Dr. John Smith",
    "specialty": "Cardiology",
    "available_slots": [
        {
            "date": "2025-02-15",
            "day": "Monday",
            "slots": ["09:00-11:00", "14:00-16:00"]
        },
        {
            "date": "2025-02-17",
            "day": "Wednesday",
            "slots": ["10:00-12:00"]
        }
    ]
}
```

### Response:
- Success:
```json
{
    "success": true,
    "message": "Doctor profile created successfully.",
    "doctor_id": 1
}
```

- Error:
```json
{
    "success": false,
    "message": "Invalid user ID or missing data."
}
```


## Database Structure for Doctors API

The database is designed to store and manage doctor profiles and related data. Below is a detailed explanation of the structure for each table involved in the Doctors API.

---

### 1. **Collection: `doctors`**
This table stores information about doctors, including their expertise, availability, and hourly rate.

#### **Schema**
```json
{
  "_id": ObjectId("..."),           // Automatically generated unique doctor ID
  "user_id": ObjectId("..."),       // Reference to the user document (foreign key equivalent)
  "name": "Dr. Jane Doe",           // Full name of the doctor
  "specialty": "Cardiology",        // Doctor's specialty
  "available_slots": {
    "2025-05-01": ["09:00", "10:00", "11:00"],
    "2025-05-02": ["14:00", "15:00"]
  },
  "created_at": ISODate("2025-05-01T08:00:00Z"),   // Creation timestamp
  "updated_at": ISODate("2025-05-01T08:00:00Z")    // Last update timestamp
}

```


### Technical Notes

- Optional part: Use JWT (that get in Login api) in Header of your request for authorization according to [this video](https://www.youtube.com/watch?v=0A_GCXBCNUQ&pp=0gcJCdgAo7VqN5tD).
- Use FastAPI to implement the API.
- Store the doctor details in an Mongodb database (use pymongo to connect).
- A Postman Collection containing API tests should be provided for testing purposes.
- Swagger UI configured with this endpoint for interactive testing and documentation.

### Deliverables:
- A .py file on Telegram.
- An image of response in postman.