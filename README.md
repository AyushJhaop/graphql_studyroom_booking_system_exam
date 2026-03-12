# 📚 Study Room Booking System (GraphQL API)

A simple, beginner-friendly Backend API built for an exam/viva demonstrating the core concepts of GraphQL, Python, and relational database design.

## 🛠️ Technology Stack
*   **Backend Framework:** Python & Flask
*   **API Architecture:** GraphQL (via Graphene & Flask-GraphQL)
*   **ORM (Object Relational Mapping):** SQLAlchemy
*   **Database:** **SQLite** (Used for its simplicity, zero configuration, and easy setup. The entire database is stored locally in `studyrooms.db`).

## 🧱 Database Structure (SQLite)
The application utilizes a local SQLite database designed with the following relational models:
- **Student**: Storing user information
- **Room**: Study room details and capacities
- **Facility**: Features available in rooms (e.g., Whiteboards, Smart TVs)
- **Booking**: Links Students to Rooms, including start and end times
- **Review**: Allows students to rate past bookings

## 🚀 How to Run the Project Local
1. Ensure Python 3.x is installed on your machine.
2. Clone this repository and move into the project directory.
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Seed the SQLite Database with initial sample data (This automatically creates tables and sample records):
```bash
python seed_data.py
```
5. Start the backend Flask Server:
```bash
python app.py
```
6. Open your web browser and navigate to `http://127.0.0.1:5000/graphql` to access the interactive GraphiQL interface!

## 🧪 Example GraphQL Testing Queries

You can paste these directly into the GraphiQL interface once the server is running.

**1. Fetch Available Rooms (Filtered using Arguments)**
```graphql
query {
  rooms(capacityGreaterThan: 2) {
    roomNumber
    capacity
    location
  }
}
```

**2. Create a Room Booking (Mutation)**
*(The backend logic will automatically throw an Exception if there is a detected time conflict in the SQLite database).*
```graphql
mutation {
  bookRoom(input: {
    studentId: 1
    roomId: 2
    startTime: "2024-11-20T10:00:00"
    endTime: "2024-11-20T12:00:00"
  }) {
    id
    status
    startTime
    endTime
  }
}
```

**3. Fetch a Student's Booking History**
```graphql
query {
  bookings(studentId: 1) {
    id
    startTime
    endTime
    status
  }
}
```
