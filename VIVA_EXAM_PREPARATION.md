# 🎓 Study Room Booking System - Viva Exam Preparation Guide

This document is your complete study guide to explain all parts of the project during your viva exam. It is structured exactly how you should think about and explain the project conceptually.

---

## 1. Project Overview
**What is this project?**
It is a Backend API for a Study Room Booking System. Using this API, students can:
* See available study rooms and their facilities.
* Filter rooms based on how many people they can fit (capacity).
* Book a room for a specific time slot while avoiding time conflicts.
* Cancel a booking.
* Submit a review for the room after their booking is complete.

---

## 2. Core Technologies Used (And WHY)

Examiners love asking *why* you chose a specific technology. Here is your answer:

* **Python & Flask:** Flask is a lightweight web framework. Rather than bringing in a heavy framework like Django, Flask is perfect for building a simple, fast API.
* **SQLite:** It is a file-based, serverless database. It is incredibly fast to set up, requires no background database server to run, and keeps the whole project portable and easy to test.
* **SQLAlchemy (ORM):** An Object-Relational Mapper. Instead of writing raw SQL commands (like `SELECT * FROM students`), SQLAlchemy lets us write Python classes to represent our database tables. This makes our code much safer against SQL Injection attacks.
* **GraphQL (via Graphene):** Instead of making a traditional REST API (with multiple endpoints like `/rooms` and `/bookings`), we used GraphQL.
  * **Why GraphQL?** It solves the issue of *over-fetching* and *under-fetching* data. The frontend application can hit a **single endpoint** (`/graphql`) and request exactly the exact fields it needs.

---

## 3. Database Architecture (The Logic inside `models.py`)

Our relational database consists of 5 tables. Think of them logically:

1. **Student (`Student`):** Holds user information (Name, Email).
2. **Room (`Room`):** Holds physical room properties (Room Number, Capacity, Location).
3. **Facility (`Facility`):** Holds items available in a room (Projector, Smart TV). 
   * *Relational Logic:* A Room can have *many* Facilities (One-to-Many).
4. **Booking (`Booking`):** This is the bridge. It links a Student (Foreign Key) to a Room (Foreign Key), and stores a `start_time`, `end_time`, and a `status` (like 'booked' or 'cancelled').
5. **Review (`Review`):** Links a rating and comment to a specific past Booking.

---

## 4. GraphQL Concepts (The Logic inside `schema.py`)

In GraphQL, there are exactly two main operations we need to understand: Queries and Mutations.

### A. Queries (Reading Data)
Queries are used like `GET` requests in REST. They only *read* information from the database. 
* *Example:* `rooms(capacityGreaterThan: 4)`.
* *Logic (`resolve_rooms` function):* The resolver function catches the query. It looks at the database, applies an `if` logic filter (e.g., `Room.capacity > 4`), retrieves the matching rows from SQLite, and hands them back to the user.

### B. Mutations (Modifying Data)
Mutations are used like `POST`, `PUT`, or `DELETE` requests in REST. They create, update, or remove data.
* *Example:* `bookRoom`, `cancelBooking`, `addReview`.

---

## 5. Core Business Logic Explained 

The main brain of the app is inside the `bookRoom` mutation in `schema.py`. 

### How do we prevent time conflicts (Double Booking)?
When a student tries to book a room, the system does **not** blindly save it. It performs a specific algorithm checking for overlaps:

1. The API receives a new proposed `start_time` and `end_time` alongside a `roomId`.
2. It asks the database: *"Are there any active bookings for this room where the existing start time is BEFORE the newly requested end time, AND the existing end time is AFTER the newly requested start time?"*
3. **Code snippet of the algorithm:**
   ```python
   conflicts = db_session.query(BookingModel).filter(
       BookingModel.room_id == input.roomId,
       BookingModel.status == 'booked',
       BookingModel.start_time < new_end,
       BookingModel.end_time > new_start
   ).count()
   ```
4. If `conflicts > 0` (meaning there's an overlap), the system throws a Python `Exception` rejecting the booking. If `conflicts == 0`, it saves the data successfully.

---

## 6. The Request Flow (From Browser to Database)

If the examiner asks: *"Walk me through exactly what happens when I click 'Book Room' on the frontend"*, this is the answer:

1. **The Request:** The user submits a GraphQL Mutation from GraphiQL in their browser.
2. **The Server (`app.py`):** The Flask server receives the request at the `/graphql` route.
3. **The Schema (`schema.py`):** The server routes the payload to Graphene. Graphene identifies it as a `BookRoom` mutation.
4. **Validation:** The Python resolver parses the Date Strings into actual Python `datetime` objects and runs the Time Conflict algorithm.
5. **The Database (`database.py` & `models.py`):** If valid, SQLAlchemy translates the Python `BookingModel` object into an `INSERT INTO` SQL command and commits it to the SQLite `studyrooms.db` file.
6. **The Response:** The newly created booking ID is sent back to the browser in JSON format.

---

## 7. Common Viva Questions & Short Answers

**Q1: What is a GraphQL Resolver?**
> A resolver is a function that acts as the data fetcher for a specific field in the schema. In our app, resolvers translate the GraphQL request into a SQLAlchemy database query.

**Q2: What is an ORM and why did you use SQLAlchemy?**
> ORM stands for Object-Relational Mapping. It allows developers to interact with a database using native object-oriented code (like Python Classes) instead of raw SQL strings. It helps prevent SQL injection vulnerabilities and makes the code cleaner.

**Q3: How would you scale this project for a massive real-world university?**
> I would migrate the database from SQLite to PostgreSQL handling millions of concurrent transactions. I would also add User Authentication (like JWT tokens) so users actually have to log in to book rooms, avoiding fake requests.
