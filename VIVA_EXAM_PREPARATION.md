# 🎓 Study Room Booking System - Complete Viva Exam Guide

This document is your definitive study guide for explaining your project comprehensively during your viva exam. It covers the problem statement, technology choices, the exact code architecture, data flow, and potential exam questions.

---

## 1. Problem Statement: Why Build This?

### **The Problem**
In many educational institutions, booking study rooms is heavily manual, involving paper logbooks or scattered spreadsheets. This causes massive inefficiencies:
* **Double Booking:** Two different groups reserve the exact same room at the same time.
* **Information Scarcity:** Students don't know the exact capacity of the room or if it has necessary facilities (like a Projector or Smart TV) before they arrive.
* **Over-fetching of Data (API Issue):** Traditional REST APIs are inefficient for this. If a mobile app needs a room's location and its facilities, a REST API usually forces the app to download *everything* (making 2 or 3 separate HTTP requests) causing slow load times and wasted bandwidth.

### **The Solution**
We developed a centralized, automated **Study Room Booking Backend System** that features:
* A concrete business-logic algorithm that strictly prevents time-conflicts and double-bookings.
* Relational database design allowing users to instantly filter rooms by capacity and view available facilities.
* A **GraphQL API**, solving the REST over-fetching issue by allowing the client side to request *exactly* what data they need in one single request.

---

## 2. Technology Choices & Best Practices

### **Why Python & Flask? (Instead of Django/FastAPI)**
* **Simplicity & Control:** Flask is a micro-framework. It is exceptionally lightweight and does not enforce a rigid structure. For a project focused wholly on demonstrating GraphQL routing and Database Architecture, Flask gets straight to the point without bringing in unneeded background complexity.

### **Why GraphQL Instead of REST APIs?**
This is a critical distinction your examiner will care about. Let's compare them:
* **The REST Issue:** In a REST API, you hit multiple endpoints (`/rooms` and then `/facilities/1`). If your frontend only needed the `roomNumber`, REST forces your server to return *all* data (location, capacity, created_at, etc.). This is called **Over-fetching**. If you need data from a different table, you have to hit a *second* endpoint, which is **Under-fetching**.
* **The GraphQL Solution:** GraphQL has only **ONE** single endpoint (`/graphql`). The frontend sends a JSON-like Query dictating exactly what it wants (e.g., "Give me the room number and facilities of Room 1"). The server responds with *exactly* that data, nothing more. It saves multiple trips to the server and massive amounts of bandwidth.

---

## 3. The Architecture & Request Flow Explained

During the viva, explain how a request moves from the user's browser down to the database using this flowchart:

```text
Client (Web Browser / GraphiQL)
   ↓
Query / Mutation (The JSON Request)
   ↓
GraphQL Server (Flask App)
   ↓
Schema (Validates the shape of the data)
   ↓
Resolver (The Python Logic)
   ↓
Database / ORM (SQLAlchemy -> SQLite)
   ↓
Response (Formatted JSON Data back to Client)
```

**Step-by-Step Flow Explanation:**
1. **Client / Query:** The user opens the web browser and types a `mutation` payload asking to book "Room 1" from 10 AM to 12 PM.
2. **GraphQL Server:** The Flask server (`app.py`) receives the HTTP POST request at the `/graphql` URL.
3. **Schema:** Graphene steps in. It checks the payload against `schema.py` to ensure `studentId`, `roomId`, and `startTime` actually exist and are the correct data types (Integers/Strings).
4. **Resolver:** This is the brain! The resolver (`mutate` inside `BookRoom`) executes Python code. It checks the database for time conflicts.
5. **Database:** Since no conflicts are found, SQLAlchemy (`models.py`) converts the Python object into an `INSERT INTO` SQL command and saves it in the local `studyrooms.db` file.
6. **Response:** Graphene formats the newly created database ID into a clean JSON object and shoots it right back to the browser.

---

## 4. File Structure & Code Explanation

Here is exactly what every file in `study_room_booking/` does. 

### `app.py` (The Entry Point)
**Function:** It is the main file that starts the web server.
* **Logic:** 
  * It initializes `Flask`.
  * It creates the single `/graphql` route endpoint using `GraphQLView`.
  * It enables the GraphiQL interactive GUI so users can test queries visually in their browser without needing tools like Postman.

### `database.py` (The Connection Builder)
**Function:** It serves as the bridge between Python and our SQLite database file.
* **Logic:**
  * Uses `create_engine` to connect to `studyrooms.db`.
  * Configures `scoped_session` ensuring that every API request gets a clean, thread-safe connection to the database.

### `models.py` (The Database Architecture)
**Function:** Uses Object-Relational Mapping (ORM) via SQLAlchemy to define our SQL tables structure using Python classes rather than raw SQL strings.
* **Logic / Tables:** 
  * `Student`, `Room`, `Booking`, `Facility`, and `Review`.
  * **Relational Logic:** Defines Foreign Keys (e.g., `booking.room_id`). It utilizes `relationship()` mapping so that querying a Booking automatically knows who the Student is and what the Room is.

### `schema.py` (The Core Engine)
**Function:** This is the most important file in the project. It explicitly tells GraphQL how to interpret Queries (Reading) and Mutations (Writing) and maps them to the database.
* **Logic:**
  * Maps our SQLAlchemy classes into GraphQL Node Types using `SQLAlchemyObjectType`.
  * **Resolvers (`resolve_rooms`, `resolve_bookings`):** These are python functions that run `SELECT` queries on the database when the frontend asks for data.
  * **Mutations (`BookRoom`):** Executes complex business logic. Before creating a Booking in the database, it queries SQLite to check if `existing_start_time < new_end_time` AND `existing_end_time > new_start_time`. If this evaluates to True, it blocks the booking to prevent a conflict. 

### `seed_data.py`
**Function:** A utility script to quickly populate our empty database with initial data so we don't have an empty app on startup. It automatically pushes fake Students, Rooms, and Facilities to SQLite.

---

## 5. Potential Viva Exam Questions & Answers

**Q1: What exactly is an ORM (SQLAlchemy) and why did you use it instead of writing raw SQL code?**
> "An ORM translates Python code (Classes) into SQL tables automatically. I used it because it keeps the codebase clean, makes database migrations much easier in the future, and acts as a massive security shield against SQL Injection vulnerabilities—a major problem if we used raw SQL queries."

**Q2: Let’s say I write a GraphQL Query on the frontend for `rooms`. What happens on the backend?**
> "When the query hits the server, Graphene routes it to the matching `Resolver` function inside `schema.py` (in this case, `resolve_rooms`). That python function runs an SQLAlchemy `.query().all()` operation over the Room database model, formats the resulting rows into JSON, and hands it straight back."

**Q3: How exactly do you prevent Double-Booking? Walk me through the mathematical logic.**
> "Inside the `BookRoom` mutation, before I execute the database `add()` command, I run a clash check query. It checks if the `roomId` matches, and if the existing booking's start time is physically *before* the new booking's end time, while its end time is physically *after* the new start time. If this query returns `> 0` results, it throws an Exception rejecting the request."

**Q4: Why SQLite instead of PostgreSQL or MySQL?**
> "SQLite is a brilliant choice for this specific scope because it is file-based and serverless. The entire database lives locally inside a single file (`studyrooms.db`). This means anyone testing the application doesn't have to install and configure a heavy background database server; the code just runs instantly anywhere."

**Q5: What is the main difference between a Query and a Mutation in GraphQL?**
> "A `Query` strictly acts as a `GET` request to fetch and read data without altering it. A `Mutation`, on the other hand, acts like `POST`, `PUT`, or `DELETE`, and is specifically designed to create or modify data in the database (like booking a room or adding a review). They use separate resolver methodologies."
